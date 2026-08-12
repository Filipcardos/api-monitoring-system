"""
Lógica de monitoramento.

`run_monitoring_cycle()` executa UMA rodada de verificação de todas as
APIs monitoradas e persiste o resultado. É a função usada tanto pelo
endpoint de cron (`/api/cron/monitor`) quanto pela execução contínua local
(`python monitor.py`).
"""
import logging
import time

import requests

from config import (
    CHECK_INTERVAL,
    ERROR_THRESHOLD,
    LOG_FILE,
    MONITORED_APIS,
    TIMEOUT,
)
from repository import monitoring_repository as repo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("monitor")

_historico_latencia: dict[str, list] = {}


def classificar(status_code, tempo, slow_threshold):
    if status_code is None:
        return "TIMEOUT"
    if status_code >= 500:
        return "ERROR"
    if tempo > slow_threshold:
        return "SLOW"
    return "ONLINE"


def _comportamento_anormal(nome, tempo):
    historico = _historico_latencia.setdefault(nome, [])
    historico.append(tempo)
    historico[:] = historico[-5:]
    if len(historico) >= 5:
        media = sum(historico) / len(historico)
        if tempo > media * 1.5:
            return True
    return False


def verificar_api(api: dict) -> dict:
    nome, url = api["name"], api["url"]
    try:
        inicio = time.time()
        response = requests.get(url, timeout=TIMEOUT)
        tempo = round((time.time() - inicio) * 1000, 2)
        status = classificar(response.status_code, tempo, api["slow_threshold"])
        status_code = response.status_code
        erro = None
    except requests.Timeout:
        tempo, status, status_code, erro = None, "TIMEOUT", None, "Tempo limite excedido"
    except requests.RequestException as exc:
        tempo, status, status_code, erro = None, "ERROR", None, str(exc)

    anormal = _comportamento_anormal(nome, tempo) if tempo is not None else False
    critico = tempo is not None and tempo > ERROR_THRESHOLD

    resultado = {
        "name": nome,
        "url": url,
        "status": status,
        "status_code": status_code,
        "latency_ms": tempo,
        "error": erro,
        "anomaly_detected": anormal,
    }

    log_msg = f"{status} | {nome} ({url}) | HTTP: {status_code} | {tempo}ms"
    if status in ("ERROR", "TIMEOUT"):
        logger.error(log_msg)
    elif status == "SLOW" or critico:
        logger.warning(log_msg)
    else:
        logger.info(log_msg)

    return resultado


def run_monitoring_cycle() -> dict:
    """Executa uma rodada de verificação de todas as APIs monitoradas e persiste o resultado."""
    logger.info("Iniciando ciclo de monitoramento...")
    resultados = [verificar_api(api) for api in MONITORED_APIS]
    entry = repo.save_cycle(resultados)
    logger.info("Ciclo concluído: %d API(s) verificadas.", len(resultados))
    return entry


def monitorar_continuamente():
    """Execução local contínua (NÃO utilizar em ambiente serverless)."""
    while True:
        run_monitoring_cycle()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitorar_continuamente()
