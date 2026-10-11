import { hhmm } from '../format';
import type { ActivityItem } from '../types';
import { SourceBadge } from './SourceBadge';

/** The latest state changes across the group, newest first. */
export function ActivityFeed({ items }: { items: ActivityItem[] }) {
  return (
    <section className="panel feed" role="region" aria-label="Activity">
      <h2>Activity</h2>
      {items.length === 0 ? (
        <p className="muted">State changes will appear here.</p>
      ) : (
        <ol>
          {items.map((a) => (
            <li key={`${a.trainee_id}-${a.t}-${a.event}`}>
              <time className="num">{hhmm(a.t)}</time>
              <span className="feed-text">{`${a.name} → `}<span className={`feed-state s-${a.state.toLowerCase()}`}>{a.state}</span></span>
              <SourceBadge t={{ kind: a.kind, source: a.source, recorded_at: null, recorded_device: null }} />
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
