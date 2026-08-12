"""Configuração centralizada via variáveis de ambiente."""
import os

MONITOR_URL = os.getenv("MONITOR_URL", "http://127.0.0.1:8000")
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "5"))
TIMEOUT = float(os.getenv("TIMEOUT", "5"))
SLOW_THRESHOLD = float(os.getenv("SLOW_THRESHOLD", "1000"))   # ms
ERROR_THRESHOLD = float(os.getenv("ERROR_THRESHOLD", "2000"))  # ms
LOG_FILE = os.getenv("LOG_FILE", "logs.txt")

MONITORED_PATHS = ["/", "/health", "/delay", "/error"]
