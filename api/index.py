import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no path para importar app.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import app  # noqa: E402

# Vercel (runtime Python) reconhece a variável `app` como handler ASGI
