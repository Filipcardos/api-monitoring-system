import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "../services/api";
import type {
  Alert,
  ApiCheckResult,
  HistoryEntry,
  MonitoringSummary,
} from "../types/monitoring";

const POLL_INTERVAL_MS = 30_000;

interface MonitoringData {
  summary: MonitoringSummary | null;
  apis: ApiCheckResult[];
  history: HistoryEntry[];
  alerts: Alert[];
  loading: boolean;
  error: string | null;
  lastFetchedAt: Date | null;
  refresh: () => void;
}

export function useMonitoringData(): MonitoringData {
  const [summary, setSummary] = useState<MonitoringSummary | null>(null);
  const [apis, setApis] = useState<ApiCheckResult[]>([]);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastFetchedAt, setLastFetchedAt] = useState<Date | null>(null);
  const isFirstLoad = useRef(true);

  const load = useCallback(async () => {
    if (isFirstLoad.current) setLoading(true);
    try {
      const [summaryRes, statusRes, historyRes, alertsRes] = await Promise.all([
        api.getSummary(),
        api.getStatus(),
        api.getHistory(50),
        api.getAlerts(20),
      ]);
      setSummary(summaryRes);
      setApis(statusRes.apis);
      setHistory(historyRes.history);
      setAlerts(alertsRes.alerts);
      setError(null);
      setLastFetchedAt(new Date());
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Serviço de monitoramento temporariamente indisponível."
      );
    } finally {
      setLoading(false);
      isFirstLoad.current = false;
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(load, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [load]);

  return { summary, apis, history, alerts, loading, error, lastFetchedAt, refresh: load };
}
