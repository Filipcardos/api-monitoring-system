import streamlit as st

st.set_page_config(page_title="Smart API Monitor", layout="wide")

st.title("🚀 Smart API Monitor")

# ✅ LER LOGS
with open("logs.txt", "r", encoding="utf-8", errors="ignore") as file:
    logs = file.readlines()

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
            except:
                pass

    if tempos:
        media = sum(tempos) / len(tempos)
        st.metric("Tempo médio", f"{round(media,2)} ms")

# 📊 GRÁFICO DE TEMPO
st.subheader("📊 Gráfico de Performance")

tempos_grafico = []

for log in ultimos:
    if "Tempo:" in log:
        try:
            tempo = float(log.split("Tempo:")[1].replace("ms", "").strip())
            tempos_grafico.append(tempo)
        except:
            pass

if tempos_grafico:
    st.line_chart(tempos_grafico)

# 📄 LOGS
st.subheader("📄 Logs")

for log in reversed(ultimos[-20:]):
    if "ERRO" in log:
        st.error(log)
    elif "LENTO" in log:
        st.warning(log)
    else:
        st.success(log)
