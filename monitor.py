import requests
import time

URLS = [
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000/health",
    "http://127.0.0.1:8000/delay",
    "http://127.0.0.1:8000/error"
]

tempos = []

def analisar_tempo(tempo):
    tempos.append(tempo)

    if len(tempos) >= 5:
        media = sum(tempos[-5:]) / 5

        if tempo > media * 1.5:
            print("🧠 ALERTA INTELIGENTE: comportamento fora do padrão detectado!")

def alerta_critico(url, tempo):
    if tempo > 2000:
        print(f"🚨 ALERTA CRÍTICO: {url} está muito lento ({tempo}ms)")

def salvar_log(mensagem):
    with open("logs.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(mensagem + "\n")

def monitorar():
    while True:
        print("\n🔎 Iniciando verificação...\n")

        for url in URLS:
            try:
                inicio = time.time()
                response = requests.get(url)
                tempo = round((time.time() - inicio) * 1000, 2)

                if tempo > 1000:
                    status = "⚠️ LENTO"
                    print("🚨 ALERTA: API lenta detectada!")
                else:
                    status = "✅ OK"

                # CHAMANDO INTELIGÊNCIA
                analisar_tempo(tempo)
                alerta_critico(url, tempo)

                log = f"{status} | {url} | Status: {response.status_code} | Tempo: {tempo}ms"

            except Exception as e:
                log = f"❌ ERRO | {url} | Falha: {str(e)}"

            print(log)
            salvar_log(log)

        time.sleep(5)

if __name__ == "__main__":
    monitorar()