import { useEffect, useState } from 'react';
import { getRoster } from './api';
import type { Roster } from './types';

/** Polls GET /v1/roster every 3 s; pauses while the tab is hidden. */
export function useRoster(intervalMs = 3000) {
  const [roster, setRoster] = useState<Roster | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    let alive = true;
    let timer: number | undefined;
    const tick = async () => {
      if (document.visibilityState === 'visible') {
        try {
          const r = await getRoster();
          if (alive) { setRoster(r); setError(null); }
        } catch (e) {
          if (alive) setError(e instanceof Error ? e.message : 'network error');
        }
      }
      if (alive) timer = window.setTimeout(tick, intervalMs);
    };
    const onVisible = () => { if (document.visibilityState === 'visible') { window.clearTimeout(timer); tick(); } };
    tick();
    document.addEventListener('visibilitychange', onVisible);
    return () => { alive = false; window.clearTimeout(timer); document.removeEventListener('visibilitychange', onVisible); };
  }, [intervalMs]);
  return { roster, error };
}
