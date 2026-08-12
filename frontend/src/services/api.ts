import type {
  MonitoringAlertsResponse,
  MonitoringHistoryResponse,
  MonitoringStatusResponse,
  MonitoringSummary,
} from "../types/monitoring";

// Mesmo domínio em produção (Vercel). Em dev, o Vite faz proxy para a API local.
const BASE_URL = "";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Falha ao consultar ${path} (HTTP ${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getSummary: () => fetchJson<MonitoringSummary>("/api/monitoring/summary"),
  getStatus: () => fetchJson<MonitoringStatusResponse>("/api/monitoring/status"),
  getHistory: (limit = 50) =>
    fetchJson<MonitoringHistoryResponse>(`/api/monitoring/history?limit=${limit}`),
  getAlerts: (limit = 20) =>
    fetchJson<MonitoringAlertsResponse>(`/api/monitoring/alerts?limit=${limit}`),
};
