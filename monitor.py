import logging
import time

import requests

from config import (
    CHECK_INTERVAL,
    ERROR_THRESHOLD,
    LOG_FILE,
    MONITOR_URL,
    MONITORED_PATHS,
    SLOW_THRESHOLD,
    TIMEOUT,
)

URLS = [f"{MONITOR_URL}{path}" for path in MONITORED_PATHS]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("monitor")

tempos = []


def analisar_tempo(tempo):
    tempos.append(tempo)

    if len(tempos) >= 5:
        media = sum(tempos[-5:]) / 5
        if tempo > media * 1.5:
            logger.warning("ALERTA INTELIGENTE: comportamento fora do padrão detectado!")


def alerta_critico(url, tempo):
    if tempo > ERROR_THRESHOLD:
        logger.error("ALERTA CRÍTICO: %s está muito lento (%sms)", url, tempo)


def classificar(status_code, tempo):
    if status_code >= 500:
        return "ERRO"
    if tempo > SLOW_THRESHOLD:
        return "LENTO"
    return "OK"


def verificar_url(url):
    try:
        inicio = time.time()
        response = requests.get(url, timeout=TIMEOUT)
        tempo = round((time.time() - inicio) * 1000, 2)

        status = classificar(response.status_code, tempo)
        analisar_tempo(tempo)
        alerta_critico(url, tempo)

        mensagem = f"{status} | {url} | Status: {response.status_code} | Tempo: {tempo}ms"

    except requests.RequestException as exc:
        status = "ERRO"
        mensagem = f"ERRO | {url} | Falha: {exc}"

    if status == "ERRO":
        logger.error(mensagem)
    elif status == "LENTO":
        logger.warning(mensagem)
    else:
        logger.info(mensagem)

    return status, mensagem


def monitorar():
    while True:
        logger.info("Iniciando verificação...")
        for url in URLS:
            verificar_url(url)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitorar()
