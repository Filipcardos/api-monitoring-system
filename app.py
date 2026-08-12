import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="API Monitoring System",
    description="API de exemplo utilizada para simular cenários monitorados "
                 "(resposta normal, lenta e com erro).",
    version="1.1.0",
)


@app.get("/", tags=["Status"], summary="Status geral da API")
def home():
    return {"status": "API online"}


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
