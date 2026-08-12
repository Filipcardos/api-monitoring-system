import "./StatusBadge.css";

type Status = "ONLINE" | "SLOW" | "ERROR" | "TIMEOUT" | "UNKNOWN";

interface StatusBadgeProps {
  status: Status;
  label?: string;
}

const DOT: Record<Status, string> = {
  ONLINE: "🟢",
  SLOW: "🟡",
  ERROR: "🔴",
  TIMEOUT: "🔴",
  UNKNOWN: "⚪",
};

export function StatusBadge({ status, label }: StatusBadgeProps) {
  return (
    <span className={`status-badge status-badge--${status.toLowerCase()}`}>
      <span aria-hidden="true">{DOT[status]}</span>
      {label ?? status}
    </span>
  );
}
