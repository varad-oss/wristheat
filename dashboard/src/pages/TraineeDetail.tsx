import { Link, useParams } from 'react-router-dom';
import { SourceBadge } from '../components/SourceBadge';
import { StateChip } from '../components/StateChip';
import { VitalsChart } from '../components/VitalsChart';
import type { Roster } from '../types';

export function TraineeDetail({ roster }: { roster: Roster | null }) {
  const { id = '' } = useParams();
  const t = roster?.trainees.find((x) => x.trainee_id === id) ?? null;
  if (!t) return <main id="main" className="page"><p role="status">{roster ? 'This trainee is not on the roster.' : 'Loading…'}</p></main>;
  const incidents = (roster?.open_incidents ?? []).filter((i) => i.session_id === t.session_id);
  return (
    <main id="main" className="page">
      <p><Link to="/console">Group view</Link></p>
      <h1 className="inc-title">{t.name} <SourceBadge t={t} /> <StateChip state={t.state} /></h1>
      <p className="inc-sub">Heart rate (left) and estimated core with its ± 0.6 °C band (right). Background shows the state; the strip shows the heat flag.</p>
      {t.session_id ? <VitalsChart sessionId={t.session_id} incidents={incidents} /> : <p>No session yet.</p>}
    </main>
  );
}
