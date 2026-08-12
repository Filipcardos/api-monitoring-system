import "./ApiStatusTable.css";
import type { ApiCheckResult } from "../../types/monitoring";
import { StatusBadge } from "../StatusBadge/StatusBadge";

interface ApiStatusTableProps {
  apis: ApiCheckResult[];
  onSelect: (api: ApiCheckResult) => void;
}

export function ApiStatusTable({ apis, onSelect }: ApiStatusTableProps) {
  if (apis.length === 0) {
    return <p className="empty-state">Nenhuma métrica disponível.</p>;
  }

  return (
    <div className="api-table" role="table" aria-label="Status das APIs monitoradas">
      <div className="api-table__row api-table__row--head" role="row">
        <span role="columnheader">Nome</span>
        <span role="columnheader">URL</span>
        <span role="columnheader">Status</span>
        <span role="columnheader">HTTP</span>
        <span role="columnheader">Latência</span>
      </div>
      {apis.map((api) => (
        <button
          key={api.name}
          className="api-table__row api-table__row--body"
          role="row"
          onClick={() => onSelect(api)}
        >
          <span role="cell" className="api-table__name">
            {api.name}
          </span>
          <span role="cell" className="api-table__url">
            {api.url}
          </span>
          <span role="cell">
            <StatusBadge status={api.status} />
          </span>
          <span role="cell" className="api-table__mono">
            {api.status_code ?? "—"}
          </span>
          <span role="cell" className="api-table__mono">
            {api.latency_ms !== null ? `${api.latency_ms}ms` : "—"}
          </span>
        </button>
      ))}
    </div>
  );
}
