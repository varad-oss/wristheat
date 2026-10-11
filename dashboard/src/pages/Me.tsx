import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ackIncident, ApiError, getMe } from '../api';
import { PsiBar } from '../components/PsiBar';
import { StateChip } from '../components/StateChip';
import { TodayPanel } from '../components/TodayPanel';
import { STATE_COLOUR } from '../components/TraineeCard';
import { dateTime, elapsed, hhmm, num } from '../format';
import type { IncidentSummary, MeView } from '../types';
import { useRoster } from '../useRoster';

const EVENT: Record<string, string> = {
  CALIBRATED: 'Calibrated', AMBER_ENTERED: 'AMBER', RED_ENTERED: 'RED',
  RECOVERING_ENTERED: 'Recovering', RECOVERY_CONFIRMED: 'Recovery confirmed',
};

function RedAlert({ inc }: { inc: IncidentSummary }) {
  const [state, setState] = useState<'idle' | 'pending' | 'done' | 'error'>(inc.acked_at ? 'done' : 'idle');
  const [msg, setMsg] = useState('');
  const onAck = async () => {
    setState('pending');
    try {
      await ackIncident(inc.incident_id, 'wearer stopped');
      setState('done');
    } catch (e) {
      if (e instanceof ApiError && e.status === 409) { setState('done'); return; }
      setState('error');
      setMsg(e instanceof Error ? e.message : 'network error');
    }
  };
  return (
    <section className="me-alert" role="alert">
      <p className="me-alert-title">Stop now. You reached RED heat strain.</p>
      <p>{inc.advice.en}</p>
      <p className="num">Strain index {num(inc.trigger.psi)}, est. core {num(inc.trigger.core_est_c, 2)} °C, HR {inc.trigger.hr} bpm, at {hhmm(inc.opened_at)}.</p>
      {state === 'done' ? (
        <p className="me-alert-ok" role="status">Got it. Your emergency contact will not be emailed. This alert closes when your data confirms recovery.</p>
      ) : (
        <>
          <button className="btn btn-ack" onClick={onAck} disabled={state === 'pending'}>
            {state === 'pending' ? 'Sending…' : "I've stopped and I'm cooling down"}
          </button>
          <p className="me-alert-note">
            {inc.escalated_at ? `Your emergency contact was emailed at ${hhmm(inc.escalated_at)}.`
              : 'If you do not respond within 90 seconds, your emergency contact is emailed.'}
          </p>
          {state === 'error' && <p className="me-alert-note">Couldn't send: {msg}. Try again.</p>}
        </>
      )}
    </section>
  );
}

/** A solo wearer's own page: right now, today's heat plan, past runs. No supervisor involved. */
export function Me() {
  const { roster: data, error } = useRoster<MeView>(4000, getMe);
  if (!data) {
    const unlinked = error && /not linked|no_wearer_profile/.test(error);
    return <main id="main" className="page"><p role="status">{unlinked
      ? 'This sign-in is not linked to a wearer. Ask the organiser to link your watch to your account.'
      : error ? `Couldn't load your page: ${error}` : 'Loading your data…'}</p></main>;
  }
  const t = data.live;
  const ago = t.last_seen ? Math.max(0, Math.round((data.server_time - t.last_seen) / 1000)) : null;
  const colour = STATE_COLOUR[t.state ?? ''] ?? '#9aa5a0';
  return (
    <main id="main" className="page me">
      <h1 className="me-title">{data.trainee.name}, training on your own</h1>
      {data.open_incidents.map((inc) => <RedAlert key={inc.incident_id} inc={inc} />)}

      <section className="panel me-now" role="region" aria-label="Right now" style={{ borderLeftColor: colour }}>
        <div className="me-now-head">
          <h2>Right now</h2>
          <StateChip state={t.state} />
        </div>
        {t.session_id ? (
          <>
            <div className="card-vitals">
              <div className="hr"><span className="num big">{t.hr_now ?? '–'}</span><span className="unit">bpm</span></div>
              <div className="core">
                <span className="num mid">{t.core_est_c === null ? 'Calibrating' : `${t.core_est_c.toFixed(2)} ± 0.6 °C`}</span>
                <span className="caption">Est. core, estimated trend</span>
              </div>
            </div>
            <PsiBar psi={t.psi} />
            {t.minutes_to_red !== null && <p className="projection">~{t.minutes_to_red} min to RED at this effort (model projection)</p>}
            <p className={t.stale ? 'seen lost' : 'seen'}>{t.stale ? `No data from your watch for ${elapsed(ago)}` : `Last reading ${elapsed(ago)} ago`}</p>
          </>
        ) : <p className="muted">Start a session on your watch. Sit still for 2 minutes while it measures your resting heart rate.</p>}
      </section>

      <TodayPanel site={data.site} serverTime={data.server_time} />

      <div className="me-cols">
        <section className="panel" role="region" aria-label="Your runs">
          <h2>Your runs</h2>
          {data.sessions.length === 0 ? <p className="muted">Your runs will appear here.</p> : (
            <ul className="me-runs">
              {data.sessions.map((s) => (
                <li key={s.session_id}>
                  <Link to={`/me/runs/${s.session_id}`}>{dateTime(s.started_at)}</Link>
                  <span className="muted">{s.source === 'replay' ? 'replay' : s.status === 'ENDED' ? 'ended' : 'in progress'}</span>
                  <StateChip state={s.state} />
                </li>
              ))}
            </ul>
          )}
        </section>
        <section className="panel" role="region" aria-label="Today's changes">
          <h2>This session</h2>
          {data.activity.length === 0 ? <p className="muted">State changes will appear here.</p> : (
            <ol className="me-feed">
              {data.activity.map((a) => <li key={`${a.t}-${a.event}`}><time className="num">{hhmm(a.t)}</time> {EVENT[a.event] ?? a.event}</li>)}
            </ol>
          )}
        </section>
      </div>
    </main>
  );
}
