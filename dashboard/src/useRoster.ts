import { useEffect, useState } from 'react';
import { getRoster } from './api';
import type { Roster } from './types';

/** Loads at once, then polls every few seconds while the tab is visible (roster by default). */
export function useRoster<T = Roster>(intervalMs = 3000, load: () => Promise<T> = getRoster as unknown as () => Promise<T>) {
  const [roster, setRoster] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    let alive = true;
    let timer: number | undefined;
    let first = true;
    const tick = async () => {
      if (first || document.visibilityState === 'visible') {
        first = false;
        try {
          const r = await load();
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
  }, [intervalMs, load]);
  return { roster, error };
}
