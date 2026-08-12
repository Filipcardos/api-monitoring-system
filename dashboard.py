import os

import streamlit as st

from config import LOG_FILE

st.set_page_config(page_title="Smart API Monitor", layout="wide")

st.title("🚀 Smart API Monitor")

if not os.path.exists(LOG_FILE):
    st.info("Nenhum log encontrado ainda. Execute `python monitor.py` para começar a monitorar.")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as file:
    logs = file.readlines()

if not logs:
    st.info("Arquivo de logs vazio. Aguardando novas verificações.")
    st.stop()

ultimos = logs[-50:]

col1, col2 = st.columns(2)

# 📡 STATUS DO SISTEMA
with col1:
    st.subheader("📡 Status do Sistema")

    if any("ERRO" in log for log in ultimos):
        st.error("❌ Sistema com falhas")
    elif any("LENTO" in log for log in ultimos):
        st.warning("⚠️ Sistema lento")
    else:
        st.success("✅ Sistema estável")

# ⏱️ PERFORMANCE MÉDIA
with col2:
    st.subheader("⏱️ Performance")

    tempos = []

    for log in ultimos:
        if "Tempo:" in log:
            try:
                tempo = float(log.split("Tempo:")[1].replace("ms", "").strip())
                tempos.append(tempo)
            except ValueError:
                pass

    if tempos:
        media = sum(tempos) / len(tempos)
        st.metric("Tempo médio", f"{round(media, 2)} ms")
    else:
        st.metric("Tempo médio", "sem dados")

# 📊 GRÁFICO DE TEMPO
st.subheader("📊 Gráfico de Performance")

if tempos:
    st.line_chart(tempos)
else:
    st.caption("Sem dados suficientes para gerar o gráfico.")

# 📄 LOGS
st.subheader("📄 Logs")

for log in reversed(ultimos[-20:]):
    if "ERRO" in log:
        st.error(log)
    elif "LENTO" in log:
        st.warning(log)
    else:
        st.success(log)
