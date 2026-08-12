"""Configuração centralizada via variáveis de ambiente."""
import os

MONITOR_URL = os.getenv("MONITOR_URL", "http://127.0.0.1:8000")
<<<<<<< HEAD
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "5"))
TIMEOUT = float(os.getenv("TIMEOUT", "5"))
SLOW_THRESHOLD = float(os.getenv("SLOW_THRESHOLD", "1000"))   # ms
ERROR_THRESHOLD = float(os.getenv("ERROR_THRESHOLD", "2000"))  # ms
LOG_FILE = os.getenv("LOG_FILE", "logs.txt")

MONITORED_PATHS = ["/", "/health", "/delay", "/error"]
=======
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "30"))
TIMEOUT = float(os.getenv("TIMEOUT", "5"))
SLOW_THRESHOLD = float(os.getenv("SLOW_THRESHOLD", "1000"))    # ms
ERROR_THRESHOLD = float(os.getenv("ERROR_THRESHOLD", "2000"))  # ms alerta crítico
LOG_FILE = os.getenv("LOG_FILE", "logs.txt")

CRON_SECRET = os.getenv("CRON_SECRET", "")

# APIs monitoradas: os próprios endpoints de demonstração da aplicação.
# "/" agora serve o dashboard (frontend), por isso não é monitorado aqui.
MONITORED_APIS = [
    {"name": "Health", "url": f"{MONITOR_URL}/health", "slow_threshold": SLOW_THRESHOLD},
    {"name": "Delay", "url": f"{MONITOR_URL}/delay", "slow_threshold": SLOW_THRESHOLD},
    {"name": "Error", "url": f"{MONITOR_URL}/error", "slow_threshold": SLOW_THRESHOLD},
]
>>>>>>> master
