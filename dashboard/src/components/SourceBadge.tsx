import { dateTime } from '../format';
import type { TraineeRow } from '../types';

/** LIVE / SIMULATED / REPLAY: every non-live trainee carries its badge everywhere it appears. */
export function SourceBadge({ t }: { t: Pick<TraineeRow, 'kind' | 'source' | 'recorded_at' | 'recorded_device'> }) {
  if (t.kind === 'simulated' || t.source === 'simulated') return <span className="badge badge-sim">SIMULATED</span>;
  if (t.source === 'replay') {
    return (
      <span className="badge badge-replay">
        {`REPLAY · recorded ${dateTime(t.recorded_at)} on ${t.recorded_device ?? 'SM-R920'}`}
      </span>
    );
  }
  if (t.source === 'live') return <span className="badge badge-live">LIVE</span>;
  return null;
}
