# API Monitoring System

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)
![Tests](https://img.shields.io/badge/Tests-Pytest-green)

## Sobre o projeto

Sistema de monitoramento de APIs desenvolvido em Python. Monitora endpoints em intervalos regulares, mede latência, classifica o status das respostas (OK / LENTO / ERRO) e dispara alertas, com um dashboard interativo em Streamlit para visualização em tempo real.

## Funcionalidades

- Monitoramento contínuo de endpoints
- Medição de tempo de resposta
- Detecção de lentidão e falhas (por status HTTP e por timeout)
- Alertas inteligentes baseados em histórico e alertas críticos
- Logs estruturados (`logging`, níveis INFO/WARNING/ERROR)
- Dashboard interativo com status, gráfico e histórico de logs
- Testes automatizados com Pytest

## Arquitetura

```
Monitor (worker contínuo) ──► logs.txt ──► Dashboard (Streamlit)
API FastAPI (endpoints monitorados) ──► deploy serverless (Vercel)
```

## Tecnologias

- Python
- FastAPI + Uvicorn
- Requests
- Streamlit
- Pytest

## Estrutura do projeto

```
api-monitoring-system/
├── api/
│   └── index.py        # entrypoint serverless para a Vercel
├── tests/
│   ├── test_app.py
│   └── test_monitor.py
├── app.py               # API FastAPI
├── monitor.py           # worker de monitoramento contínuo
├── dashboard.py          # dashboard Streamlit
├── config.py             # configuração via variáveis de ambiente
├── requirements.txt
├── .env.example
├── vercel.json
└── README.md
```

## Como executar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a API
python -m uvicorn app:app --reload

# Rodar o monitor (em outro terminal)
python monitor.py

# Rodar o dashboard (em outro terminal)
streamlit run dashboard.py
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste se necessário:

| Variável         | Descrição                                  | Padrão                  |
|------------------|---------------------------------------------|--------------------------|
| MONITOR_URL      | URL base da API monitorada                   | http://127.0.0.1:8000   |
| CHECK_INTERVAL   | Intervalo entre verificações (s)             | 5                        |
| TIMEOUT          | Timeout das requisições do monitor (s)        | 5                        |
| SLOW_THRESHOLD   | Limite para classificar como lento (ms)       | 1000                     |
| ERROR_THRESHOLD  | Limite para alerta crítico de lentidão (ms)   | 2000                     |
| LOG_FILE         | Caminho do arquivo de log                     | logs.txt                |

## API

| Método | Rota      | Descrição                       |
|--------|-----------|-----------------------------------|
| GET    | `/`       | Status geral da API               |
| GET    | `/health` | Healthcheck                        |
| GET    | `/delay`  | Simula resposta lenta (2s)         |
| GET    | `/error`  | Simula falha (HTTP 500)            |

## Documentação Swagger

Com a API em execução:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Monitoramento

`monitor.py` verifica os endpoints em `config.py` a cada `CHECK_INTERVAL` segundos, classifica cada resposta (OK/LENTO/ERRO), detecta desvios de padrão comparando com a média das últimas 5 medições e registra tudo via `logging` em `logs.txt` e no console.

## Dashboard

`dashboard.py` lê `logs.txt` e exibe status geral do sistema, tempo médio de resposta, gráfico de performance e o histórico recente de logs.

## Testes

```bash
pytest
```

Cobre o healthcheck, os endpoints principais e a lógica de classificação de status do monitor.

## Deploy na Vercel

A API (`app.py`, exposta via `api/index.py`) está pronta para deploy serverless:

```bash
vercel login
vercel dev      # teste local
vercel          # preview
vercel --prod   # produção
```

## Limitações da arquitetura serverless

- `monitor.py` é um processo contínuo (loop infinito) e **não roda como função serverless** — deve ser executado localmente ou em um worker separado (ex.: VM, container, cron job).
- O dashboard Streamlit também não é compatível com o modelo serverless da Vercel; deve ser executado localmente ou hospedado separadamente (ex.: Streamlit Community Cloud).
- Apenas a API FastAPI é hospedada na Vercel.

## Exemplos de requisições

```bash
curl https://sua-api.vercel.app/health
curl https://sua-api.vercel.app/delay
curl https://sua-api.vercel.app/error
```

## Objetivos de aprendizado

Projeto de portfólio para praticar desenvolvimento de APIs com FastAPI, monitoramento/observabilidade básica, testes automatizados e deploy serverless.

## Autor

**Filipe Oliveira Cardoso**
GitHub: https://github.com/Filipcardos/api-monitoring-system
