import "./AlertsPanel.css";
import type { Alert } from "../../types/monitoring";

interface AlertsPanelProps {
  alerts: Alert[];
}

const ICON: Record<string, string> = {
  ERROR: "🔴",
  TIMEOUT: "🔴",
  SLOW: "🟡",
  ONLINE: "🟢",
};

function formatTime(iso: string): string {
  const date = new Date(iso.endsWith("Z") ? iso : `${iso}Z`);
  return date.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

export function AlertsPanel({ alerts }: AlertsPanelProps) {
  return (
    <div className="alerts-panel">
      <h3 className="alerts-panel__title">Alertas</h3>
      {alerts.length === 0 ? (
        <p className="empty-state">Nenhum alerta recente.</p>
      ) : (
        <ul className="alerts-panel__list">
          {alerts.map((alert, idx) => (
            <li key={`${alert.api}-${alert.timestamp}-${idx}`} className="alerts-panel__item">
              <span aria-hidden="true">{ICON[alert.type] ?? "🔵"}</span>
              <div>
                <p className="alerts-panel__message">{alert.message}</p>
                <span className="alerts-panel__meta">
                  {alert.api} · {formatTime(alert.timestamp)}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
