import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./LatencyChart.css";
import type { HistoryEntry } from "../../types/monitoring";

const STATUS_COLORS: Record<string, string> = {
  ONLINE: "#34d399",
  SLOW: "#fbbf24",
  ERROR: "#f87171",
  TIMEOUT: "#f87171",
};

interface ChartsProps {
  history: HistoryEntry[];
}

function buildLatencySeries(history: HistoryEntry[]) {
  return [...history]
    .reverse()
    .map((entry) => {
      const values = entry.results
        .map((r) => r.latency_ms)
        .filter((v): v is number => v !== null);
      const avg = values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
      return {
        time: new Date(entry.checked_at.endsWith("Z") ? entry.checked_at : `${entry.checked_at}Z`)
          .toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
        latency: avg !== null ? Math.round(avg) : null,
      };
    });
}

function buildStatusDistribution(history: HistoryEntry[]) {
  const counts: Record<string, number> = { ONLINE: 0, SLOW: 0, ERROR: 0, TIMEOUT: 0 };
  history.forEach((entry) =>
    entry.results.forEach((r) => {
      counts[r.status] = (counts[r.status] ?? 0) + 1;
    })
  );
  return Object.entries(counts)
    .filter(([, value]) => value > 0)
    .map(([status, value]) => ({ status, value }));
}

function buildAvailabilityHistory(history: HistoryEntry[]) {
  return [...history]
    .reverse()
    .map((entry) => {
      const total = entry.results.length || 1;
      const online = entry.results.filter((r) => r.status === "ONLINE").length;
      return {
        time: new Date(entry.checked_at.endsWith("Z") ? entry.checked_at : `${entry.checked_at}Z`)
          .toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
        availability: Math.round((online / total) * 100),
      };
    });
}

function EmptyChart() {
  return <p className="chart-empty">Dados históricos ainda não disponíveis.</p>;
}

export function LatencyOverTimeChart({ history }: ChartsProps) {
  const data = buildLatencySeries(history);
  const hasData = data.some((d) => d.latency !== null);

  return (
    <div className="chart-card">
      <h3 className="chart-card__title">Latência ao longo do tempo</h3>
      {hasData ? (
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={data}>
            <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
            <XAxis dataKey="time" stroke="var(--text-muted)" fontSize={11} />
            <YAxis stroke="var(--text-muted)" fontSize={11} unit="ms" />
            <Tooltip
              contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)" }}
            />
            <Line type="monotone" dataKey="latency" stroke="#60a5fa" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <EmptyChart />
      )}
    </div>
  );
}

export function StatusDistributionChart({ history }: ChartsProps) {
  const data = buildStatusDistribution(history);

  return (
    <div className="chart-card">
      <h3 className="chart-card__title">Distribuição de status</h3>
      {data.length ? (
        <ResponsiveContainer width="100%" height={220}>
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="status" innerRadius={45} outerRadius={75}>
              {data.map((entry) => (
                <Cell key={entry.status} fill={STATUS_COLORS[entry.status] ?? "#8b93a7"} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)" }}
            />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <EmptyChart />
      )}
    </div>
  );
}

export function AvailabilityHistoryChart({ history }: ChartsProps) {
  const data = buildAvailabilityHistory(history);

  return (
    <div className="chart-card">
      <h3 className="chart-card__title">Histórico de disponibilidade</h3>
      {data.length ? (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={data}>
            <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
            <XAxis dataKey="time" stroke="var(--text-muted)" fontSize={11} />
            <YAxis stroke="var(--text-muted)" fontSize={11} unit="%" domain={[0, 100]} />
            <Tooltip
              contentStyle={{ background: "var(--bg-elevated)", border: "1px solid var(--border)" }}
            />
            <Bar dataKey="availability" fill="#34d399" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <EmptyChart />
      )}
    </div>
  );
}
