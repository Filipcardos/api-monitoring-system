import "./ApiDetails.css";
import type { ApiCheckResult, HistoryEntry } from "../../types/monitoring";
import { StatusBadge } from "../StatusBadge/StatusBadge";

interface ApiDetailsProps {
  api: ApiCheckResult;
  history: HistoryEntry[];
  onClose: () => void;
}

function computeStats(name: string, history: HistoryEntry[]) {
  const points = history
    .flatMap((entry) => entry.results.filter((r) => r.name === name).map((r) => ({ ...r, checked_at: entry.checked_at })))
    .filter((r) => r.latency_ms !== null);

  const latencies = points.map((p) => p.latency_ms as number);
  const avgLatency = latencies.length
    ? Math.round(latencies.reduce((a, b) => a + b, 0) / latencies.length)
    : null;

  const total = history.flatMap((e) => e.results.filter((r) => r.name === name)).length;
  const online = history
    .flatMap((e) => e.results.filter((r) => r.name === name))
    .filter((r) => r.status === "ONLINE").length;
  const uptime = total > 0 ? Math.round((online / total) * 100) : null;

  const errors = history
    .flatMap((e) => e.results.filter((r) => r.name === name && (r.status === "ERROR" || r.status === "TIMEOUT")))
    .slice(0, 5);

  return { avgLatency, uptime, errors };
}

export function ApiDetails({ api, history, onClose }: ApiDetailsProps) {
  const { avgLatency, uptime, errors } = computeStats(api.name, history);

  return (
    <div className="api-details__overlay" onClick={onClose}>
      <div
        className="api-details"
        role="dialog"
        aria-modal="true"
        aria-label={`Detalhes de ${api.name}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="api-details__header">
          <h2>{api.name}</h2>
          <button className="api-details__close" onClick={onClose} aria-label="Fechar detalhes">
            ✕
          </button>
        </div>

        <p className="api-details__url">{api.url}</p>

        <div className="api-details__grid">
          <div>
            <span className="api-details__label">Status atual</span>
            <StatusBadge status={api.status} />
          </div>
          <div>
            <span className="api-details__label">HTTP</span>
            <span>{api.status_code ?? "—"}</span>
          </div>
          <div>
            <span className="api-details__label">Latência atual</span>
            <span>{api.latency_ms !== null ? `${api.latency_ms}ms` : "—"}</span>
          </div>
          <div>
            <span className="api-details__label">Latência média</span>
            <span>{avgLatency !== null ? `${avgLatency}ms` : "—"}</span>
          </div>
          <div>
            <span className="api-details__label">Uptime</span>
            <span>{uptime !== null ? `${uptime}%` : "—"}</span>
          </div>
        </div>

        {api.error && <p className="api-details__error">Erro atual: {api.error}</p>}

        <h3 className="api-details__subtitle">Erros recentes</h3>
        {errors.length === 0 ? (
          <p className="empty-state">Nenhum erro recente.</p>
        ) : (
          <ul className="api-details__errors">
            {errors.map((e, idx) => (
              <li key={idx}>
                {e.error ?? `HTTP ${e.status_code}`}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
