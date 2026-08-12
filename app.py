import time

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from config import CRON_SECRET
from monitor import run_monitoring_cycle
from repository import monitoring_repository as repo

app = FastAPI(
    title="API Monitoring System",
    description="API de monitoramento com endpoints de demonstração "
                 "(status normal, lento e com erro) e métricas para o dashboard.",
    version="2.0.0",
)


# ------------------------------------------------------------------
# Endpoints de demonstração (monitorados pelo sistema)
# ------------------------------------------------------------------
@app.get("/health", tags=["Status"], summary="Healthcheck")
def health():
    """Endpoint de healthcheck usado por monitores e pela Vercel."""
    return {"status": "ok"}


@app.get("/delay", tags=["Simulação"], summary="Simula resposta lenta")
def delay():
    time.sleep(2)  # simula lentidão
    return {"status": "resposta lenta"}


@app.get("/error", tags=["Simulação"], summary="Simula falha da API")
def error():
    return JSONResponse(status_code=500, content={"erro": "falha simulada"})


# ------------------------------------------------------------------
# Endpoints consumidos pelo dashboard
# ------------------------------------------------------------------
def _current_results() -> list:
    latest = repo.get_latest()
    return latest["results"] if latest else []


def _uptime_percent(history: list) -> float | None:
    total = 0
    online = 0
    for entry in history:
        for r in entry["results"]:
            total += 1
            if r["status"] == "ONLINE":
                online += 1
    if total == 0:
        return None
    return round((online / total) * 100, 2)


@app.get("/api/monitoring/summary", tags=["Monitoring"], summary="Resumo geral do monitoramento")
def monitoring_summary():
    latest = repo.get_latest()
    results = _current_results()
    history = repo.get_history(limit=100)

    total = len(results)
    online = sum(1 for r in results if r["status"] == "ONLINE")
    slow = sum(1 for r in results if r["status"] == "SLOW")
    error = sum(1 for r in results if r["status"] in ("ERROR", "TIMEOUT"))
    latencias = [r["latency_ms"] for r in results if r["latency_ms"] is not None]

    return {
        "total_apis": total,
        "online": online,
        "slow": slow,
        "error": error,
        "avg_latency_ms": round(sum(latencias) / len(latencias), 2) if latencias else None,
        "uptime_percent": _uptime_percent(history),
        "last_updated": latest["checked_at"] if latest else None,
        "has_data": latest is not None,
    }


@app.get("/api/monitoring/status", tags=["Monitoring"], summary="Status atual de cada API")
def monitoring_status():
    return {"apis": _current_results()}


@app.get("/api/monitoring/history", tags=["Monitoring"], summary="Histórico de ciclos de monitoramento")
def monitoring_history(limit: int = 50):
    return {"history": repo.get_history(limit=limit)}


@app.get("/api/monitoring/alerts", tags=["Monitoring"], summary="Alertas recentes")
def monitoring_alerts(limit: int = 20):
    return {"alerts": repo.get_alerts(limit=limit)}


# ------------------------------------------------------------------
# Cron (execução automática via Vercel Cron)
# ------------------------------------------------------------------
@app.get("/api/cron/monitor", tags=["Cron"], summary="Executa uma rodada de monitoramento (uso do Vercel Cron)")
def cron_monitor(authorization: str | None = Header(default=None)):
    if CRON_SECRET:
        if authorization != f"Bearer {CRON_SECRET}":
            raise HTTPException(status_code=401, detail="Unauthorized")

    entry = run_monitoring_cycle()
    return {"status": "ok", "checked_at": entry["checked_at"], "results": entry["results"]}
