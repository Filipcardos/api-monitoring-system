import "./Header.css";
import { StatusBadge } from "../StatusBadge/StatusBadge";

interface HeaderProps {
  overallStatus: "ONLINE" | "SLOW" | "ERROR" | "UNKNOWN";
  lastUpdated: string | null;
  onRefresh: () => void;
  refreshing: boolean;
}

function formatRelativeTime(iso: string | null): string {
  if (!iso) return "—";
  const date = new Date(iso.endsWith("Z") ? iso : `${iso}Z`);
  const diffMs = Date.now() - date.getTime();
  const diffSec = Math.round(diffMs / 1000);
  if (Number.isNaN(diffSec)) return "—";
  if (diffSec < 5) return "agora";
  if (diffSec < 60) return `há ${diffSec}s`;
  const diffMin = Math.round(diffSec / 60);
  if (diffMin < 60) return `há ${diffMin}min`;
  const diffHour = Math.round(diffMin / 60);
  return `há ${diffHour}h`;
}

export function Header({ overallStatus, lastUpdated, onRefresh, refreshing }: HeaderProps) {
  return (
    <header className="header" role="banner">
      <div className="header__brand">
        <div className="header__logo" aria-hidden="true">
          ◈
        </div>
        <div>
          <h1 className="header__title">API Monitoring System</h1>
          <p className="header__subtitle">Observabilidade em tempo real</p>
        </div>
      </div>

      <div className="header__actions">
        <StatusBadge status={overallStatus} label={overallStatusLabel(overallStatus)} />
        <span className="header__updated">
          Atualizado <time>{formatRelativeTime(lastUpdated)}</time>
        </span>
        <button
          className="header__refresh"
          onClick={onRefresh}
          disabled={refreshing}
          aria-label="Atualizar agora"
        >
          <span className={refreshing ? "spin" : ""}>⟳</span> Atualizar agora
        </button>
      </div>
    </header>
  );
}

function overallStatusLabel(status: HeaderProps["overallStatus"]): string {
  switch (status) {
    case "ONLINE":
      return "Sistema estável";
    case "SLOW":
      return "Sistema lento";
    case "ERROR":
      return "Sistema com falhas";
    default:
      return "Sem dados";
  }
}
