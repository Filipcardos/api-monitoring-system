
st.subheader("📡 Status geral")

if any("ERRO" in log for log in logs[-10:]):
    st.error("❌ Sistema com falhas recentes")
else:
    st.success("✅ Sistema estável")

import streamlit as st

st.title("📊 Smart API Monitor")

with open("logs.txt", "r", encoding="utf-8", errors="ignore") as file:
    logs = file.readlines()

st.subheader("📄 Logs do sistema")

for log in reversed(logs[-20:]):
    if "ERRO" in log:
        st.error(log)
    elif "LENTO" in log:
        st.warning(log)
    else:
        st.success(log)
