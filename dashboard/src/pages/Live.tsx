import { SiteStrip } from '../components/SiteStrip';
import { TraineeCard } from '../components/TraineeCard';
import { stateRank } from '../format';
import type { Roster } from '../types';

export function Live({ roster, error }: { roster: Roster | null; error: string | null }) {
  if (!roster) {
    return <main className="page"><p role="status">{error ? `Couldn't load the roster: ${error}` : 'Loading roster…'}</p></main>;
  }
  const trainees = [...roster.trainees].sort((a, b) => stateRank(a.state) - stateRank(b.state)
    || a.trainee_id.localeCompare(b.trainee_id));
  return (
    <main className="page">
      <SiteStrip site={roster.site} />
      {error && <p className="warn" role="alert">Connection problem: {error}. Showing the last data received.</p>}
      <section className="grid" aria-label="Trainees">
        {trainees.map((t) => <TraineeCard key={t.trainee_id} t={t} serverTime={roster.server_time} />)}
        {trainees.length === 0 && <p>No trainees yet. Run scripts/seed.py to add them.</p>}
      </section>
    </main>
  );
}
