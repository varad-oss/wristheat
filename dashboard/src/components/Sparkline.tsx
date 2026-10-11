import { useEffect, useState } from 'react';
import { getSeries } from '../api';
import type { MinutePoint } from '../types';

/** 30-minute estimated-core sparkline, refreshed every 30 s. */
export function Sparkline({ sessionId, colour, stale = false }: { sessionId: string | null; colour: string; stale?: boolean }) {
  const [points, setPoints] = useState<MinutePoint[]>([]);
  useEffect(() => {
    if (!sessionId) return;
    let alive = true;
    const load = () => getSeries(sessionId, Math.floor(Date.now() / 60000) - 30)
      .then((s) => alive && setPoints(s.points)).catch(() => undefined);
    load();
    const id = window.setInterval(load, 30000);
    return () => { alive = false; window.clearInterval(id); };
  }, [sessionId]);
  const vals = points.filter((p) => p.hr !== null).map((p) => p.core_est_c);
  if (vals.length < 2) {
    return <div className="spark spark-empty">{stale ? 'No readings in the last 30 min' : 'Core trend appears after 2 min'}</div>;
  }
  const lo = Math.min(36.8, ...vals), hi = Math.max(38.6, ...vals);
  const w = 200, h = 36;
  const d = vals.map((v, i) => `${i ? 'L' : 'M'}${(i / (vals.length - 1)) * w},${h - ((v - lo) / (hi - lo)) * h}`).join(' ');
  return (
    <svg className="spark" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" role="img"
         aria-label={`Estimated core over the last ${vals.length} minutes`}>
      <path d={d} fill="none" stroke={colour} strokeWidth="2" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}
