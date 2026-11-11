"""
Camada de persistência do histórico de monitoramento.

Produção (Vercel): usa Upstash Redis via REST API (mesmo serviço por trás
da Vercel KV), configurado com UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN.
Não depende de filesystem, compatível com funções serverless.

Local/dev: se as variáveis do Upstash não estiverem definidas, usa um
arquivo JSON local (data/history.json). Essa opção NÃO deve ser usada em
produção serverless (filesystem é efêmero).

O restante da aplicação depende apenas das funções deste módulo, nunca
da implementação concreta do armazenamento.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import requests
import threading

_LOCAL_LOCK = threading.Lock()

HISTORY_LIMIT = 200
ALERTS_LIMIT = 100

UPSTASH_URL = os.getenv("UPSTASH_REDIS_REST_URL") or os.getenv("KV_REST_API_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN") or os.getenv("KV_REST_API_TOKEN")

_LOCAL_FILE = Path(__file__).resolve().parent.parent / "data" / "history.json"

if os.getenv("VERCEL"):
    _LOCAL_FILE = Path("/tmp/api-monitor/history.json")

_USE_UPSTASH = bool(UPSTASH_URL and UPSTASH_TOKEN)


# ----------------------------------------------------------------------
# Backend: Upstash Redis REST
# ----------------------------------------------------------------------
def _upstash_command(*args: Any) -> Any:
    resp = requests.post(UPSTASH_URL, json=list(args), headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"}, timeout=5)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("error"):
        raise RuntimeError(payload["error"])
    return payload.get("result")


def _upstash_save_cycle(entry: dict) -> None:
    payload = json.dumps(entry)
    _upstash_command("LPUSH", "monitoring:history", payload)
    _upstash_command("LTRIM", "monitoring:history", 0, HISTORY_LIMIT - 1)
    _upstash_command("SET", "monitoring:latest", payload)


def _upstash_save_alerts(alerts: list) -> None:
    for alert in alerts:
        _upstash_command("LPUSH", "monitoring:alerts", json.dumps(alert))
    if alerts:
        _upstash_command("LTRIM", "monitoring:alerts", 0, ALERTS_LIMIT - 1)


def _upstash_get_latest() -> Optional[dict]:
    raw = _upstash_command("GET", "monitoring:latest")
    return json.loads(raw) if raw else None


def _upstash_get_history(limit: int) -> list:
    raw_list = _upstash_command("LRANGE", "monitoring:history", 0, limit - 1) or []
    return [json.loads(item) for item in raw_list]


def _upstash_get_alerts(limit: int) -> list:
    raw_list = _upstash_command("LRANGE", "monitoring:alerts", 0, limit - 1) or []
    return [json.loads(item) for item in raw_list]


# ----------------------------------------------------------------------
# Backend: arquivo JSON local (somente desenvolvimento)
# ----------------------------------------------------------------------
def _local_load() -> dict:
    if not _LOCAL_FILE.exists():
        return {"history": [], "alerts": []}
    try:
        return json.loads(_LOCAL_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"history": [], "alerts": []}


def _local_save(data: dict) -> None:
    _LOCAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    _LOCAL_FILE.write_text(json.dumps(data), encoding="utf-8")


def _local_save_cycle(entry: dict) -> None:
    data = _local_load()
    data["history"].insert(0, entry)
    data["history"] = data["history"][:HISTORY_LIMIT]
    _local_save(data)


def _local_save_alerts(alerts: list) -> None:
    if not alerts:
        return
    data = _local_load()
    data["alerts"] = alerts + data["alerts"]
    data["alerts"] = data["alerts"][:ALERTS_LIMIT]
    _local_save(data)


def _local_get_latest() -> Optional[dict]:
    data = _local_load()
    return data["history"][0] if data["history"] else None


def _local_get_history(limit: int) -> list:
    return _local_load()["history"][:limit]


def _local_get_alerts(limit: int) -> list:
    return _local_load()["alerts"][:limit]


# ----------------------------------------------------------------------
# Interface pública (usada pelo restante da aplicação)
# ----------------------------------------------------------------------
def backend_name() -> str:
    return "upstash-redis" if _USE_UPSTASH else "local-json (dev only)"


def save_cycle(results: list, min_interval: int = 0) -> dict:
    """Save at most one sample per interval, including concurrent Redis callers."""
    now = datetime.now(timezone.utc)
    entry = {"checked_at": now.isoformat(), "results": results}
    if _USE_UPSTASH:
        script = """
        local previous = redis.call('GET', KEYS[1])
        local last_time = tonumber(redis.call('GET', KEYS[3])) or 0
        if previous and tonumber(ARGV[2]) - last_time < tonumber(ARGV[3]) then
            return previous
        end
        redis.call('SET', KEYS[1], ARGV[1])
        redis.call('SET', KEYS[3], ARGV[2])
        redis.call('LPUSH', KEYS[2], ARGV[1])
        redis.call('LTRIM', KEYS[2], 0, tonumber(ARGV[4]) - 1)
        return ARGV[1]
        """
        raw = _upstash_command(
            "EVAL", script, 3, "monitoring:latest", "monitoring:history",
            "monitoring:last_saved_epoch", json.dumps(entry), now.timestamp(),
            min_interval, HISTORY_LIMIT,
        )
        return json.loads(raw)
    with _LOCAL_LOCK:
        data = _local_load()
        if data["history"] and now.timestamp() - data.get("last_saved_epoch", 0) < min_interval:
            return data["history"][0]
        data["history"].insert(0, entry)
        data["history"] = data["history"][:HISTORY_LIMIT]
        data["last_saved_epoch"] = now.timestamp()
        _local_save(data)
    return entry


def get_latest() -> Optional[dict]:
    return _upstash_get_latest() if _USE_UPSTASH else _local_get_latest()


def get_history(limit: int = 50) -> list:
    return _upstash_get_history(limit) if _USE_UPSTASH else _local_get_history(limit)


def get_incidents() -> list:
    """Reconstruct observed incidents from the retained history window."""
    incidents = []
    active = {}
    for entry in reversed(get_history(HISTORY_LIMIT)):
        for result in entry["results"]:
            key = result["url"]
            incident = active.get(key)
            if result["status"] != "ONLINE" and incident is None:
                incident = {
                    "api": result["name"], "url": key, "type": result["status"],
                    "started_at": entry["checked_at"], "resolved_at": None,
                }
                incidents.append(incident)
                active[key] = incident
            elif result["status"] == "ONLINE" and incident is not None:
                incident["resolved_at"] = entry["checked_at"]
                del active[key]
    now = datetime.now(timezone.utc)
    for incident in incidents:
        start = datetime.fromisoformat(incident["started_at"]).replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(incident["resolved_at"]).replace(tzinfo=timezone.utc) if incident["resolved_at"] else now
        incident["duration_seconds"] = max(0, int((end - start).total_seconds()))
    return list(reversed(incidents))


def get_alerts(limit: int = 20) -> list:
    return [{
        "api": item["api"], "type": item["type"],
        "timestamp": item["started_at"],
        "message": "Incidente observado",
    } for item in get_incidents()][:max(1, min(limit, ALERTS_LIMIT))]
