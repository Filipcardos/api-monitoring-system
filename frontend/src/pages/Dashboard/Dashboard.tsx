import { useState } from "react";
import "./Dashboard.css";
import { Header } from "../../components/Header/Header";
import { MetricCard } from "../../components/MetricCard/MetricCard";
import { ApiStatusTable } from "../../components/ApiStatusTable/ApiStatusTable";
import {
  AvailabilityHistoryChart,
  LatencyOverTimeChart,
  StatusDistributionChart,
} from "../../components/LatencyChart/LatencyChart";
import { AlertsPanel } from "../../components/AlertsPanel/AlertsPanel";
import { ApiDetails } from "../../components/ApiDetails/ApiDetails";
import { useMonitoringData } from "../../hooks/useMonitoringData";
import type { ApiCheckResult } from "../../types/monitoring";

function overallStatus(apis: ApiCheckResult[]): "ONLINE" | "SLOW" | "ERROR" | "UNKNOWN" {
  if (apis.length === 0) return "UNKNOWN";
  if (apis.some((a) => a.status === "ERROR" || a.status === "TIMEOUT")) return "ERROR";
  if (apis.some((a) => a.status === "SLOW")) return "SLOW";
  return "ONLINE";
}

export function Dashboard() {
  const { summary, apis, history, alerts, loading, error, refresh } = useMonitoringData();
  const [selectedApi, setSelectedApi] = useState<ApiCheckResult | null>(null);

  return (
    <div className="dashboard">
      <Header
        overallStatus={overallStatus(apis)}
        lastUpdated={summary?.last_updated ?? null}
        onRefresh={refresh}
        refreshing={loading}
      />

      <main className="dashboard__content">
        {error && (
          <div className="dashboard__banner dashboard__banner--error" role="alert">
            Serviço de monitoramento temporariamente indisponível.
          </div>
        )}

        {loading && !summary && !error && (
          <p className="dashboard__loading">Carregando métricas...</p>
        )}

        {!loading && !error && summary && !summary.has_data && (
          <div className="dashboard__banner">
            Nenhuma métrica disponível ainda. Aguardando a primeira execução do monitoramento
            (via <code>/api/cron/monitor</code> ou execução local de <code>monitor.py</code>).
          </div>
        )}

        {summary && (
          <section className="dashboard__metrics" aria-label="Métricas gerais">
            <MetricCard label="APIs monitoradas" value={String(summary.total_apis)} />
            <MetricCard label="Online" value={String(summary.online)} tone="online" />
            <MetricCard label="Lentas" value={String(summary.slow)} tone="slow" />
            <MetricCard label="Com erro" value={String(summary.error)} tone="error" />
            <MetricCard
              label="Latência média"
              value={summary.avg_latency_ms !== null ? `${summary.avg_latency_ms}ms` : "—"}
              tone="info"
            />
            <MetricCard
              label="Uptime"
              value={summary.uptime_percent !== null ? `${summary.uptime_percent}%` : "—"}
              tone="info"
            />
          </section>
        )}

        <section className="dashboard__section" aria-label="Status das APIs">
          <h2 className="dashboard__section-title">Status das APIs</h2>
          <ApiStatusTable apis={apis} onSelect={setSelectedApi} />
        </section>

        <section className="dashboard__charts" aria-label="Gráficos">
          <LatencyOverTimeChart history={history} />
          <StatusDistributionChart history={history} />
          <AvailabilityHistoryChart history={history} />
        </section>

        <section aria-label="Alertas">
          <AlertsPanel alerts={alerts} />
        </section>
      </main>

      {selectedApi && (
        <ApiDetails api={selectedApi} history={history} onClose={() => setSelectedApi(null)} />
      )}
    </div>
  );
}
