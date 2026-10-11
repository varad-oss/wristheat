import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getSessionSummary } from '../api';
import { SourceBadge } from '../components/SourceBadge';
import { dateTime, duration, hhmm, num } from '../format';
import type { SessionSummary, State } from '../types';

const SHOWN: State[] = ['GREEN', 'AMBER', 'RED', 'RECOVERING', 'CALIBRATING'];
const OUTCOME: Record<string, string> = {
  recovered: 'Acknowledged, then recovery confirmed by the data',
  recovered_unacknowledged: 'Recovery confirmed by the data without an acknowledgement',
  not_confirmed: 'Recovery not confirmed within the wait window',
};

/** Duty-of-care record for one session; prints cleanly to A4. */
export function SessionReport() {
  const { id = '' } = useParams();
  const [s, setS] = useState<SessionSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    getSessionSummary(id).then(setS).catch((e) => setError(e instanceof Error ? e.message : 'load failed'));
  }, [id]);

  if (!s) return <main className="page"><p role="status">{error ? `Couldn't load this report: ${error}` : 'Loading report…'}</p></main>;
  return <ReportView s={s} />;
}

export function ReportView({ s }: { s: SessionSummary }) {
  const states = SHOWN.filter((k) => s.minutes_by_state[k] > 0);
  const total = Math.max(1, s.duration_min);
  const label = `Time in state: ${states.map((k) => `${k} ${s.minutes_by_state[k]} min`).join(', ')}`;
  const tb = { kind: s.trainee.kind, source: s.session.source, recorded_at: null, recorded_device: null };

  return (
    <main className="page report-page">
      <p className="no-print"><Link to="/">Group view</Link></p>
      <header className="report-head">
        <div>
          <h1 className="inc-title">{s.trainee.name} <SourceBadge t={tb} /></h1>
          <p className="inc-sub">
            Session report, {dateTime(s.started_at)} to {hhmm(s.last_seen)} IST ({s.duration_min} min recorded).
            {s.hr0 ? ` Resting heart rate ${s.hr0} bpm.` : ''}
            {s.env_at_start?.wbgt_c != null ? ` Heat at start: WBGT ${num(s.env_at_start.wbgt_c)} °C, ${s.env_at_start.flag} flag.` : ''}
          </p>
        </div>
        <button className="btn no-print" onClick={() => window.print()}>Print / save PDF</button>
      </header>

      {s.duration_min === 0 ? <p>No completed minutes yet</p> : (
        <>
          <section className="report-block">
            <h2>Time in state</h2>
            <div className="statebar" role="img" aria-label={label}>
              {states.map((k) => (
                <span key={k} className={`statebar-seg chip-${k.toLowerCase()}`} style={{ flexGrow: s.minutes_by_state[k] / total }}>
                  {k} {s.minutes_by_state[k]} min
                </span>
              ))}
            </div>
            {s.minutes_by_state.gap > 0 && <p className="muted">{s.minutes_by_state.gap} min without enough readings.</p>}
          </section>
          <dl className="tiles">
            <div><dt>Peak strain index</dt><dd className="num">{num(s.peak_psi)}</dd></div>
            <div><dt>Peak est. core</dt><dd className="num">{s.peak_core_c ? `${num(s.peak_core_c, 2)} °C` : '–'}</dd></div>
            <div><dt>Peak heart rate</dt><dd className="num">{s.peak_hr ?? '–'} bpm</dd></div>
            <div><dt>Incidents</dt><dd className="num">{s.incidents.length}</dd></div>
          </dl>
        </>
      )}

      <section className="report-block">
        <h2>Incidents and responses</h2>
        {s.incidents.length === 0 ? <p className="muted">No incidents in this session.</p> : (
          <ul className="report-incidents">
            {s.incidents.map((i) => (
              <li key={i.incident_id}>
                <p><strong>RED at {hhmm(i.opened_at)}</strong> ({i.trigger.rule}): strain index {num(i.trigger.psi)},
                  est. core {num(i.trigger.core_est_c, 2)} °C, HR {i.trigger.hr} bpm.</p>
                {i.metrics?.escalated && <p>Escalated to backup contact (no acknowledgement within the window).</p>}
                {i.metrics?.time_to_ack_s != null && <p>{`Acknowledged after ${duration(i.metrics.time_to_ack_s)}`}</p>}
                {i.metrics?.time_to_recovery_s != null && <p>{`Recovery confirmed after ${duration(i.metrics.time_to_recovery_s)}`}</p>}
                <p className="muted">{i.outcome ? OUTCOME[i.outcome] ?? i.outcome : 'Incident still open'}.{' '}
                  <Link className="no-print" to={`/incidents/${i.incident_id}`}>Open incident</Link></p>
              </li>
            ))}
          </ul>
        )}
      </section>
      <p className="source">Estimated values from a research prototype (ECTemp core-temperature trend, ± 0.6 °C). Not a medical record.</p>
    </main>
  );
}
