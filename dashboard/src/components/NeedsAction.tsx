import { Link } from 'react-router-dom';
import type { Action } from '../guidance';
import { SourceBadge } from './SourceBadge';

const TONE = ['red', 'lost', 'amber', 'watch', 'recovering'];

/** Who needs the supervisor right now, most urgent first. */
export function NeedsAction({ actions }: { actions: Action[] }) {
  return (
    <section className="panel actions" role="region" aria-label="Needs action now">
      <h2>Needs action now</h2>
      {actions.length === 0 ? (
        <p className="muted">No action needed right now.</p>
      ) : (
        <ul>
          {actions.map((a) => (
            <li key={a.trainee.trainee_id} className={`action action-${TONE[a.priority]}`}>
              <Link to={`/trainee/${a.trainee.trainee_id}`}>{a.text}</Link>
              <SourceBadge t={a.trainee} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
