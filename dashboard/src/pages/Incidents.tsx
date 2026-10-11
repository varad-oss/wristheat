import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getIncidents } from '../api';
import { hhmm } from '../format';
import type { IncidentSummary } from '../types';

export function Incidents() {
  const [items, setItems] = useState<IncidentSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    getIncidents('all').then((r) => setItems(r.incidents)).catch((e) => setError(e instanceof Error ? e.message : 'load failed'));
  }, []);
  return (
    <main className="page">
      <h1>Incidents</h1>
      {error && <p role="alert" className="warn">Couldn't load incidents: {error}</p>}
      {!items && !error && <p role="status">Loading incidents…</p>}
      {items && items.length === 0 && <p>No incidents yet. An incident opens when a trainee reaches RED.</p>}
      {items && items.length > 0 && (
        <table className="table">
          <thead><tr><th>Opened</th><th>Trainee</th><th>Status</th><th>Outcome</th></tr></thead>
          <tbody>
            {items.map((i) => (
              <tr key={i.incident_id}>
                <td className="num">{hhmm(i.opened_at)}</td>
                <td><Link to={`/incidents/${i.incident_id}`}>{i.trainee_name}</Link>{i.trainee_kind === 'simulated' && <> <span className="badge badge-sim">SIMULATED</span></>}</td>
                <td>{i.status}</td>
                <td>{i.outcome?.replace(/_/g, ' ') ?? 'open'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
