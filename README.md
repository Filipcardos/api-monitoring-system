#  API Monitoring System 

Sistema completo de monitoramento de APIs desenvolvido em Python, com análise de performance, detecção de falhas e alertas inteligentes em tempo real.

---

##  Sobre o Projeto

O **API Monitoring System** é uma aplicação que simula um ambiente real de produção, realizando monitoramento contínuo de endpoints, análise de tempo de resposta e detecção de comportamentos anormais.

O projeto foi inspirado em ferramentas utilizadas em produção como:

- Datadog  
- Prometheus  
- New Relic  

---

##  Funcionalidades

 Monitoramento contínuo de APIs  
 Medição de tempo de resposta  
 Detecção de lentidão  
 Alertas automáticos e críticos  
 Detecção de comportamento anormal (baseado em histórico)  
 Simulação de falhas de conexão  
 Geração de logs persistentes  
 Dashboard interativo com Streamlit  

---

##  Inteligência do Sistema

O sistema analisa o comportamento das requisições e identifica padrões anormais:

-  Detecta quando o tempo de resposta foge do padrão  
-  Identifica lentidão automaticamente  
-  Dispara alertas críticos para eventos graves  
-  Usa média dos últimos resultados para análise  

---

##  Cenários simulados

A aplicação simula situações reais de produção:

-  API funcionando normalmente  
-  API com alta latência  
-  API indisponível  
-  Variação de performance ao longo do tempo  

---

##  Dashboard

O projeto inclui um dashboard interativo com:

- Status geral do sistema  
- Logs em tempo real  
- Indicadores de performance  
- Classificação de eventos (OK, LENTO, ERRO)
 <img width="1914" height="949" alt="image" src="https://github.com/user-attachments/assets/8243f129-6b0f-4047-a0cd-9521785e38eb" />

---

##  Tecnologias Utilizadas

- Python  
- FastAPI  
- Requests  
- Streamlit  

---

##  Como Executar o Projeto

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar API
python -m uvicorn app:app --reload

# Rodar monitor
python monitor.py

# Rodar dashboard
python -m streamlit run dashboard.py
```
##  Estrutura do Projeto
api-monitoring-system/
````│
├── app.py
├── monitor.py
├── dashboard.py
├── logs.txt
├── requirements.txt
└── README.md
````

##  Contexto Profissional
Este projeto demonstra habilidades práticas em:

Desenvolvimento Backend
Monitoramento de aplicações
Observabilidade
Diagnóstico de falhas
Automação de processos
Análise de performance

##  Autor
Filipe Oliveira Cardoso 
