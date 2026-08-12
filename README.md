# API Monitoring System

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
<<<<<<< HEAD
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
=======
![React](https://img.shields.io/badge/React-TypeScript-61DAFB)
>>>>>>> master
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)
![Tests](https://img.shields.io/badge/Tests-Pytest-green)

## Sobre o projeto

<<<<<<< HEAD
Sistema de monitoramento de APIs desenvolvido em Python. Monitora endpoints em intervalos regulares, mede latência, classifica o status das respostas (OK / LENTO / ERRO) e dispara alertas, com um dashboard interativo em Streamlit para visualização em tempo real.

## Funcionalidades

- Monitoramento contínuo de endpoints
- Medição de tempo de resposta
- Detecção de lentidão e falhas (por status HTTP e por timeout)
- Alertas inteligentes baseados em histórico e alertas críticos
- Logs estruturados (`logging`, níveis INFO/WARNING/ERROR)
- Dashboard interativo com status, gráfico e histórico de logs
- Testes automatizados com Pytest
=======
Sistema de monitoramento de APIs com dashboard web profissional. A API FastAPI verifica endpoints, mede latência e classifica status (ONLINE / SLOW / ERROR / TIMEOUT); um dashboard em React + TypeScript exibe tudo em tempo real. O monitoramento roda automaticamente em produção via Vercel Cron — nada precisa ser executado manualmente.

Deploy: https://api-monitoring-system-gray.vercel.app

## Preview

Dashboard escuro estilo observabilidade (cards de métricas, tabela de status, gráficos de latência/disponibilidade e painel de alertas). Adicione um screenshot em `docs/dashboard.png` e referencie aqui quando disponível.

## Dashboard

Acessando a URL raiz do deploy, o dashboard React abre diretamente — não é necessário rodar Streamlit, Python ou qualquer comando manual. Ele consulta a API a cada 30s (auto-refresh) e também possui um botão "Atualizar agora".

## Funcionalidades

- Monitoramento automático das APIs via Vercel Cron (sem processo contínuo em produção)
- Classificação ONLINE / SLOW / ERROR / TIMEOUT com thresholds configuráveis
- Persistência de histórico e alertas (Upstash Redis em produção)
- Dashboard React: métricas gerais, tabela de status, detalhes por API, 3 gráficos (latência, distribuição de status, disponibilidade) e painel de alertas
- Estados de loading / erro / vazio tratados no frontend
- Documentação automática da API (Swagger/ReDoc)
- Testes automatizados (Pytest) para API, monitor e persistência
- Execução local contínua opcional (`python monitor.py`) e dashboard Streamlit legado (`dashboard.py`), lendo `logs.txt`
>>>>>>> master

## Arquitetura

```
<<<<<<< HEAD
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
=======
React (dashboard) ──consome──► FastAPI (/api/monitoring/*)
                                      │
Vercel Cron ──chama──► /api/cron/monitor ──executa──► run_monitoring_cycle()
                                      │
                                persistência (Upstash Redis / JSON local em dev)
```

Frontend e backend são publicados em um único projeto Vercel: rotas estáticas (`frontend/dist`) para o dashboard e funções Python serverless (`api/index.py`) para a API.

## Tecnologias

- Backend: Python, FastAPI, Uvicorn, Requests, Pytest
- Frontend: React, TypeScript, Vite, Recharts
- Persistência: Upstash Redis (REST) em produção
- Deploy: Vercel (static build + funções Python + Cron)

## Estrutura

```
api-monitoring-system/
├── api/index.py               # entrypoint serverless (expõe app.py)
├── app.py                     # API FastAPI (endpoints demo + /api/monitoring/* + cron)
├── monitor.py                 # run_monitoring_cycle() + execução contínua local
├── config.py                  # configuração via variáveis de ambiente
├── repository/
│   └── monitoring_repository.py  # persistência (Upstash Redis / JSON local)
├── dashboard.py                # dashboard Streamlit legado (opcional, local)
├── tests/                      # testes Pytest
├── frontend/                   # dashboard React + TypeScript (Vite)
│   └── src/
│       ├── components/         # Header, MetricCard, StatusBadge, ApiStatusTable,
│       │                       # LatencyChart, AlertsPanel, ApiDetails
│       ├── pages/Dashboard/
│       ├── services/api.ts
│       ├── hooks/useMonitoringData.ts
│       └── types/monitoring.ts
>>>>>>> master
├── requirements.txt
├── .env.example
├── vercel.json
└── README.md
```

<<<<<<< HEAD
## Como executar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a API
python -m uvicorn app:app --reload

# Rodar o monitor (em outro terminal)
python monitor.py

# Rodar o dashboard (em outro terminal)
=======
## Execução local

Backend:

```bash
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Frontend (em outro terminal — em dev, o Vite faz proxy de `/api`, `/health`, `/delay`, `/error` para `http://127.0.0.1:8000`):

```bash
cd frontend
npm install
npm run dev
```

Monitoramento contínuo local (opcional, fora da Vercel):

```bash
python monitor.py
```

Dashboard Streamlit legado (opcional):

```bash
>>>>>>> master
streamlit run dashboard.py
```

## Variáveis de ambiente

<<<<<<< HEAD
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
=======
Copie `.env.example` para `.env` e ajuste:

| Variável                    | Descrição                                                          | Padrão                  |
|------------------------------|---------------------------------------------------------------------|--------------------------|
| MONITOR_URL                  | URL base da API monitorada                                          | http://127.0.0.1:8000   |
| CHECK_INTERVAL                | Intervalo entre verificações na execução contínua local (s)         | 30                       |
| TIMEOUT                       | Timeout das requisições do monitor (s)                               | 5                        |
| SLOW_THRESHOLD                 | Limite para classificar como lento (ms)                              | 1000                     |
| ERROR_THRESHOLD                 | Limite para latência crítica nos logs (ms)                           | 2000                     |
| LOG_FILE                        | Arquivo de log da execução local                                     | logs.txt                |
| CRON_SECRET                     | Segredo para autenticar `/api/cron/monitor`                          | (vazio = sem auth)      |
| UPSTASH_REDIS_REST_URL           | URL REST do Upstash Redis (produção)                                  | (vazio = usa JSON local)|
| UPSTASH_REDIS_REST_TOKEN          | Token REST do Upstash Redis (produção)                                | (vazio = usa JSON local)|

## API

| Método | Rota                          | Descrição                                    |
|--------|--------------------------------|-------------------------------------------------|
| GET    | `/health`                       | Healthcheck                                       |
| GET    | `/delay`                        | Simula resposta lenta (2s)                        |
| GET    | `/error`                        | Simula falha (HTTP 500)                           |
| GET    | `/api/monitoring/summary`        | Resumo geral (totais, latência média, uptime)     |
| GET    | `/api/monitoring/status`         | Status atual de cada API monitorada               |
| GET    | `/api/monitoring/history`        | Histórico de ciclos (`?limit=`)                    |
| GET    | `/api/monitoring/alerts`          | Alertas recentes (`?limit=`)                       |
| GET    | `/api/cron/monitor`               | Executa uma rodada de monitoramento (protegido por `CRON_SECRET`) |

Documentação interativa: `/docs` (Swagger) e `/redoc` (ReDoc).

## Monitoramento automático

`run_monitoring_cycle()` (em `monitor.py`) verifica todas as APIs em `config.MONITORED_APIS`, classifica cada resposta e persiste o resultado via `repository/monitoring_repository.py`. Essa função é chamada tanto pelo endpoint `/api/cron/monitor` (produção) quanto pelo loop local `python monitor.py` — sem duplicar lógica.

## Vercel Cron

`vercel.json` agenda `GET /api/cron/monitor` diariamente (`0 3 * * *`). A Vercel envia automaticamente o header `Authorization: Bearer <CRON_SECRET>` quando a variável `CRON_SECRET` está configurada no projeto; o endpoint valida esse header.

**Importante:** no plano Hobby da Vercel, cron jobs rodam no máximo 1x/dia — expressões mais frequentes (ex.: `*/15 * * * *`) são rejeitadas no deploy. Para verificações mais frequentes, é necessário o plano Pro ou disparar `/api/cron/monitor` por um agendador externo (ex.: GitHub Actions).

## Persistência

Em produção, o histórico é salvo no Upstash Redis via REST API (mesmo serviço por trás da Vercel KV) — compatível com funções serverless, sem depender de filesystem. Configure `UPSTASH_REDIS_REST_URL` e `UPSTASH_REDIS_REST_TOKEN` nas variáveis de ambiente da Vercel.

Sem essas variáveis, o sistema usa um arquivo JSON local (`data/history.json`) — **apenas para desenvolvimento**, já que o filesystem é efêmero em serverless.

## Deploy

```bash
npm install --prefix frontend
npm run build --prefix frontend
pytest
vercel login
vercel          # preview
vercel --prod   # produção
```

Environment Variables a configurar no projeto Vercel: `CRON_SECRET`, `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` (e `MONITOR_URL` apontando para o próprio domínio de produção, se diferente do padrão).
>>>>>>> master

## Testes

```bash
pytest
```

<<<<<<< HEAD
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
=======
Cobre: healthcheck, `/error`, `/api/monitoring/summary` sem dados, autenticação do `/api/cron/monitor`, classificação de status (ONLINE/SLOW/ERROR/TIMEOUT) e a camada de persistência.

Frontend:

```bash
npm run build --prefix frontend
npm run lint --prefix frontend
```

## Limitações

- `monitor.py` no modo `while True` é para uso local apenas — não roda como função serverless. Em produção, o ciclo é disparado pelo Vercel Cron.
- Cron no plano Hobby é limitado a 1x/dia (ver seção acima).
- O dashboard Streamlit (`dashboard.py`) é um utilitário local legado, lendo `logs.txt`; não é hospedado na Vercel.
- Sem `UPSTASH_REDIS_REST_URL`/`TOKEN`, a persistência em produção não funciona corretamente (filesystem serverless é efêmero).
>>>>>>> master

## Autor

**Filipe Oliveira Cardoso**
<<<<<<< HEAD
GitHub: https://github.com/Filipcardos/api-monitoring-system
=======
GitHub: https://github.com/Filipcardos
>>>>>>> master
