import "./MetricCard.css";

interface MetricCardProps {
  label: string;
  value: string;
  tone?: "default" | "online" | "slow" | "error" | "info";
}

export function MetricCard({ label, value, tone = "default" }: MetricCardProps) {
  return (
    <div className={`metric-card metric-card--${tone}`}>
      <span className="metric-card__label">{label}</span>
      <span className="metric-card__value">{value}</span>
    </div>
  );
}
