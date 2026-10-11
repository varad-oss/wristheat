import { Link } from 'react-router-dom';
import { elapsed } from '../format';
import type { TraineeRow } from '../types';
import { PsiBar } from './PsiBar';
import { SourceBadge } from './SourceBadge';
import { Sparkline } from './Sparkline';
import { StateChip } from './StateChip';

export const STATE_COLOUR: Record<string, string> = {
  GREEN: '#1f7a4d', AMBER: '#b26a00', RED: '#b42318', RECOVERING: '#1d5fa8', CALIBRATING: '#5d6b66',
};

export function TraineeCard({ t, serverTime, readOnly = false }: { t: TraineeRow; serverTime: number; readOnly?: boolean }) {
  const colour = STATE_COLOUR[t.state ?? ''] ?? '#9aa5a0';
  const ago = t.last_seen ? Math.max(0, Math.round((serverTime - t.last_seen) / 1000)) : null;
  return (
    <article className={`card card-${(t.state ?? 'none').toLowerCase()}`} style={{ borderLeftColor: colour }}>
      <header className="card-head">
        <h3>{readOnly ? t.name : <Link to={`/console/trainee/${t.trainee_id}`}>{t.name}</Link>}</h3>
        <SourceBadge t={t} />
        <StateChip state={t.state} />
      </header>
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
          {t.minutes_to_red !== null && (
            <p className="projection">~{t.minutes_to_red} min to RED at this effort (model projection)</p>
          )}
          {!readOnly && <Sparkline sessionId={t.session_id} colour={colour} stale={t.stale} />}
          {!readOnly && <p className="card-links"><Link to={`/console/sessions/${t.session_id}/report`}>Session report</Link></p>}
          <p className={t.stale ? 'seen lost' : 'seen'}>
            {t.stale ? `Signal lost ${elapsed(ago)}` : `Last reading ${elapsed(ago)} ago`}
          </p>
        </>
      ) : (
        <p className="seen">Not streaming. Start a session on the watch or the simulator.</p>
      )}
    </article>
  );
}
