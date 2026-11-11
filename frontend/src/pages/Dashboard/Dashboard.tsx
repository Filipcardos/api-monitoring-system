import { useCallback, useEffect, useRef, useState } from "react";
import type { ApiStatus, HistoryEntry } from "../../types/monitoring";
import "./Dashboard.css";

const labels: Record<ApiStatus, string> = { ONLINE: "Normal", SLOW: "Lento", ERROR: "Falha", TIMEOUT: "Sem resposta" };
const time = (s: string) => new Date(s).toLocaleString("pt-BR", {day:"2-digit", month:"2-digit", hour:"2-digit", minute:"2-digit", second:"2-digit"});
async function read<T>(path: string, signal: AbortSignal): Promise<T> {
  const res = await fetch("/api/monitoring/" + path, {signal});
  if (!res.ok || !res.headers.get("content-type")?.includes("application/json")) throw Error("Resposta indisponível");
  return res.json();
}

interface Incident { api: string; url: string; type: ApiStatus; started_at: string; resolved_at: string | null; duration_seconds: number }

export function Dashboard() {
  const [incidents,setIncidents] = useState<Incident[]>([]);
  const [storage,setStorage] = useState("");
  const [storageError,setStorageError] = useState<string | null>(null);
  const [service,setService] = useState("");
  const [tab,setTab] = useState("Serviços");
  const [sample,setSample] = useState<HistoryEntry | null>(null);
  const [history,setHistory] = useState<HistoryEntry[]>([]);
  const [busy,setBusy] = useState(true);
  const [failed,setFailed] = useState(false);
  const [archiveFailed,setArchiveFailed] = useState(false);
  const pending = useRef<AbortController | null>(null);
  const refresh = useCallback(async () => {
    if (pending.current) return;
    const controller = new AbortController();
    pending.current = controller;
    setBusy(true);
    const signal = AbortSignal.any([controller.signal, AbortSignal.timeout(25000)]);
    await Promise.all([
      read<HistoryEntry & {storage: string; storage_error: string | null}>("live",signal).then(data => {
        if (!controller.signal.aborted) {setSample(data); setStorage(data.storage); setStorageError(data.storage_error); setFailed(false);}
      }).catch(() => {if (!controller.signal.aborted) setFailed(true);}),
      Promise.all([read<{history: HistoryEntry[]}>("history?limit=200",signal), read<{incidents: Incident[]}>("incidents",signal)])
        .then(([h,i]) => { if (!controller.signal.aborted) {setIncidents(i.incidents); setHistory(h.history); setArchiveFailed(false);} })
        .catch(() => {if (!controller.signal.aborted) setArchiveFailed(true);})
    ]);
    if (pending.current === controller) {pending.current=null; setBusy(false);}
  },[]);
  useEffect(() => {
    void refresh();
    const id = window.setInterval(() => {if (!document.hidden) void refresh();},30000);
    return () => {clearInterval(id); pending.current?.abort(); pending.current=null;};
  },[refresh]);
  const services = sample?.results ?? [];
  const errors = services.filter(r => r.status === "ERROR" || r.status === "TIMEOUT").length;
  const slow = services.filter(r => r.status === "SLOW").length;
  return <main>
    <header><span className="brand"><svg aria-hidden="true" width="30" height="22" viewBox="0 0 30 22"><path d="M1 12h7l4-9 5 17 4-8h8" fill="none" stroke="currentColor" strokeWidth="2.5"/></svg> Monitor de APIs</span><a href="/docs">Documentação ↗</a></header>
    <section className="hero"><div><span className="eyebrow">PAINEL DE OPERAÇÃO</span><h1>Monitoramento</h1><p>Endpoints de demonstração com respostas normal, lenta e de erro.</p></div><button disabled={busy} onClick={refresh}>{busy ? "Verificando…" : "↻  Verificar agora"}</button></section>
    <section className="metrics" aria-label="Última leitura">{[["Endpoints",sample ? services.length : "—"],["Normais",sample ? services.length-errors-slow : "—"],["Lentos",sample ? slow : "—"],["Com falha",sample ? errors : "—"]].map(([name,value])=><div key={name}><small>{name}</small><strong>{value}</strong></div>)}</section>
    <nav aria-label="Visualização">{["Serviços","Histórico","Incidentes"].map(n=><button key={n} aria-pressed={tab===n} onClick={()=>setTab(n)}>{n}</button>)}</nav>
    {storage && storage !== "upstash-redis" && <p role="alert">Histórico temporário nesta instância. Configure o Upstash Redis para conservar os registros na Vercel.</p>}
    {storageError && <p role="alert">{storageError}</p>}
    {failed && <p role="alert">Não foi possível concluir a verificação.{sample && " Exibindo a última leitura disponível."}</p>}
    {tab==="Serviços" ? <section><div className="sectionline"><h2>Última leitura</h2><small>{sample ? time(sample.checked_at) : "Aguardando leitura"}</small></div>
    {services.map(r=><details key={r.name}><summary><b>{r.name}</b><span className={"state "+r.status}><i/>{labels[r.status]}</span><code>{r.latency_ms===null ? "—" : Math.round(r.latency_ms)+" ms"}</code></summary><div className="detail"><code>{r.url}</code><span>HTTP {r.status_code ?? "sem resposta"}</span>{r.error && <span>{r.error}</span>}</div></details>)}
    {!sample && <p>{busy ? "Consultando os endpoints…" : "Nenhuma leitura disponível."}</p>}</section> :
    <section><div className="sectionline"><h2>{tab==="Histórico" ? "Histórico de verificações" : "Incidentes observados"}</h2></div>
    {archiveFailed && <p role="alert">Histórico indisponível no momento.</p>}
    <p>Últimas 200 coletas. Incidentes e duração refletem as observações desta janela; a recuperação é confirmada na próxima coleta.</p>
    <label>Serviço <select value={service} onChange={event => setService(event.target.value)}><option value="">Todos</option>{Array.from(new Set(history.flatMap(h => h.results.map(r => r.name)))).map(name => <option key={name}>{name}</option>)}</select></label>
    {tab==="Histórico" ? history.filter(h => !service || h.results.some(r => r.name === service)).map((h,i)=><details key={h.checked_at+i}><summary><b>{time(h.checked_at)}</b><span>{h.results.length} endpoints</span></summary><div className="detail">{h.results.filter(r => !service || r.name === service).map(r=><span key={r.name}>{r.name} · {labels[r.status]} · {r.latency_ms ?? "—"} ms</span>)}</div></details>) :
    incidents.filter(item => !service || item.api === service).map(item => <div className="incident" key={item.url+item.started_at}><b>{item.api} · {labels[item.type]}</b><span>{item.resolved_at ? "Recuperado" : "Em andamento"}</span><small>Início observado {time(item.started_at)}</small><small>{item.resolved_at ? "Recuperação "+time(item.resolved_at) : "Aguardando recuperação"} · {Math.floor(item.duration_seconds/60)} min {item.duration_seconds%60} s</small></div>)}
    {!archiveFailed && !(tab==="Histórico" ? history : incidents).length && <p>{busy ? "Consultando registros…" : "Nenhum registro disponível. As leituras são salvas a cada 5 minutos enquanto o painel estiver aberto."}</p>}</section>}
    <footer>Verificação automática a cada 30 s enquanto o painel estiver visível.</footer>
  </main>;
}
