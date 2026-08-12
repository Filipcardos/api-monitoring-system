export type ApiStatus = "ONLINE" | "SLOW" | "ERROR" | "TIMEOUT";

export interface ApiCheckResult {
  name: string;
  url: string;
  status: ApiStatus;
  status_code: number | null;
  latency_ms: number | null;
  error: string | null;
  anomaly_detected: boolean;
}

export interface MonitoringSummary {
  total_apis: number;
  online: number;
  slow: number;
  error: number;
  avg_latency_ms: number | null;
  uptime_percent: number | null;
  last_updated: string | null;
  has_data: boolean;
}

export interface MonitoringStatusResponse {
  apis: ApiCheckResult[];
}

export interface HistoryEntry {
  checked_at: string;
  results: ApiCheckResult[];
}

export interface MonitoringHistoryResponse {
  history: HistoryEntry[];
}

export interface Alert {
  type: string;
  message: string;
  api: string;
  timestamp: string;
}

export interface MonitoringAlertsResponse {
  alerts: Alert[];
}
