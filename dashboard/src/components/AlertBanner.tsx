import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { ackIncident, ApiError, getIncident } from '../api';
import { hhmm, num } from '../format';
import { LANG_LABEL, type Lang } from '../i18n';
import type { IncidentSummary } from '../types';

type AckState = { kind: 'idle' } | { kind: 'pending' } | { kind: 'done' } | { kind: 'error'; msg: string };

function IncidentAlert({ inc }: { inc: IncidentSummary }) {
  const [lang, setLang] = useState<Lang>('en');
  const [ack, setAck] = useState<AckState>({ kind: 'idle' });
  const [audio, setAudio] = useState<{ en?: string; hi?: string }>({});
  const tried = useRef(false);
  const enRef = useRef<HTMLAudioElement>(null);
  const hiRef = useRef<HTMLAudioElement>(null);
  const t = inc.trigger;

  useEffect(() => {
    let alive = true;
    getIncident(inc.incident_id).then((full) => alive && setAudio(full.audio ?? {})).catch(() => undefined);
    return () => { alive = false; };
  }, [inc.incident_id, inc.status]);

  useEffect(() => {
    // Try to play once when the alert first appears; browsers may block autoplay, so the buttons stay.
    if (audio.en && !tried.current && enRef.current) {
      tried.current = true;
      enRef.current.play()?.catch(() => undefined);
    }
  }, [audio.en]);

  const acknowledged = inc.status === 'ACKNOWLEDGED' || ack.kind === 'done';
  const onAck = async () => {
    if (ack.kind === 'pending') return;
    setAck({ kind: 'pending' });
    try {
      await ackIncident(inc.incident_id, 'cooling started');
      setAck({ kind: 'done' });
    } catch (e) {
      const msg = e instanceof ApiError && e.status === 409 ? 'Already acknowledged'
        : `Couldn't acknowledge: ${e instanceof Error ? e.message : 'network error'}. Try again.`;
      setAck({ kind: 'error', msg });
    }
  };
  const play = (ref: React.RefObject<HTMLAudioElement>) => ref.current?.play()?.catch(() => undefined);

  return (
    <div className={`alert ${acknowledged ? 'alert-acked' : ''}`} role="alert">
      <div className="alert-main">
        <p className="alert-title">
          <Link to={`/console/incidents/${inc.incident_id}`}>{`${inc.trainee_name}: STOP — heat strain RED`}</Link>
          {inc.trainee_kind === 'simulated' && <span className="badge badge-sim">SIMULATED</span>}
        </p>
        <p className="alert-numbers num">
          PSI {num(t.psi)} · est. core {num(t.core_est_c, 2)} ± 0.6 °C · HR {t.hr} bpm
          {t.wbgt_c !== null ? ` · WBGT ${num(t.wbgt_c)} °C (${t.flag} flag)` : ''}
        </p>
        <div className="alert-advice">
          <div className="seg" role="group" aria-label="Advice language">
            {(['en', 'hi'] as Lang[]).map((l) => (
              <button key={l} className={lang === l ? 'on' : ''} aria-pressed={lang === l} onClick={() => setLang(l)}>
                {LANG_LABEL[l]}
              </button>
            ))}
          </div>
          <p lang={lang}>{inc.advice[lang]}</p>
        </div>
        {inc.escalated_at && <p className="alert-esc">{`Escalated to backup contact at ${hhmm(inc.escalated_at)}`}</p>}
      </div>
      <div className="alert-actions">
        <button className="btn btn-light" onClick={() => play(enRef)} disabled={!audio.en}>▶ Play alert (EN)</button>
        <button className="btn btn-light" onClick={() => play(hiRef)} disabled={!audio.hi}>▶ हिंदी</button>
        {acknowledged ? (
          <p className="alert-ackd" role="status">
            {`Acknowledged${inc.acked_at ? ` at ${hhmm(inc.acked_at)}` : ''}. Waiting for the data to confirm recovery.`}
          </p>
        ) : (
          <button className="btn btn-ack" onClick={onAck} disabled={ack.kind === 'pending'}>
            {ack.kind === 'pending' ? 'Acknowledging…' : 'Acknowledge — cooling started'}
          </button>
        )}
        {ack.kind === 'error' && <p className="alert-err">{ack.msg}</p>}
      </div>
      <audio ref={enRef} src={audio.en} preload="auto" />
      <audio ref={hiRef} src={audio.hi} preload="auto" />
    </div>
  );
}

export function AlertBanner({ incidents }: { incidents: IncidentSummary[] }) {
  if (!incidents.length) return null;
  return (
    <section className="alerts" aria-label="Open incidents">
      {incidents.map((inc) => <IncidentAlert key={inc.incident_id} inc={inc} />)}
    </section>
  );
}
