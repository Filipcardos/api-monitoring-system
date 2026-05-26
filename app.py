from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API online"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/delay")
def delay():
    time.sleep(2)  # simula lentidão
    return {"status": "resposta lenta"}

@app.get("/error")
def error():
    return {"erro": "falha simulada"}
