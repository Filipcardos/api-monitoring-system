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
import time
from pathlib import Path
from typing import Any, Optional

import requests

HISTORY_LIMIT = 200
ALERTS_LIMIT = 100

UPSTASH_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

_LOCAL_FILE = Path(__file__).resolve().parent.parent / "data" / "history.json"

_USE_UPSTASH = bool(UPSTASH_URL and UPSTASH_TOKEN)


# ----------------------------------------------------------------------
# Backend: Upstash Redis REST
# ----------------------------------------------------------------------
def _upstash_command(*args: Any) -> Any:
    url = f"{UPSTASH_URL}/{'/'.join(str(a) for a in args)}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"}, timeout=5)
    resp.raise_for_status()
    return resp.json().get("result")


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


def save_cycle(results: list) -> dict:
    """Persiste o resultado de um ciclo de monitoramento e retorna a entrada salva."""
    entry = {"checked_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "results": results}

    alerts = [
        {
            "type": r["status"],
            "message": f"{r['name']} está com status {r['status']}",
            "api": r["name"],
            "timestamp": entry["checked_at"],
        }
        for r in results
        if r["status"] != "ONLINE"
    ]

    if _USE_UPSTASH:
        _upstash_save_cycle(entry)
        _upstash_save_alerts(alerts)
    else:
        _local_save_cycle(entry)
        _local_save_alerts(alerts)

    return entry


def get_latest() -> Optional[dict]:
    return _upstash_get_latest() if _USE_UPSTASH else _local_get_latest()


def get_history(limit: int = 50) -> list:
    return _upstash_get_history(limit) if _USE_UPSTASH else _local_get_history(limit)


def get_alerts(limit: int = 20) -> list:
    return _upstash_get_alerts(limit) if _USE_UPSTASH else _local_get_alerts(limit)
