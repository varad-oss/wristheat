import { elapsed } from './format';
import type { Flag, TraineeRow } from './types';

// --- US Army TB MED 507 work/rest and water table (acclimatized adults). 1 US quart = 0.95 L. ---------------------
export interface Rule { work: string; waterLph: number }
type Category = 'WHITE' | 'GREEN' | 'YELLOW' | 'RED' | 'BLACK';

const rule = (work: [number, number] | null, waterLph: number): Rule =>
  ({ work: work ? `${work[0]} min work / ${work[1]} min rest` : 'No limit', waterLph });

export const WORK_REST: Record<Category, { easy: Rule; moderate: Rule; hard: Rule }> = {
  WHITE: { easy: rule(null, 0.5), moderate: rule(null, 0.7), hard: rule([40, 20], 0.7) },
  GREEN: { easy: rule(null, 0.5), moderate: rule([50, 10], 0.7), hard: rule([30, 30], 0.95) },
  YELLOW: { easy: rule(null, 0.7), moderate: rule([40, 20], 0.7), hard: rule([30, 30], 0.95) },
  RED: { easy: rule(null, 0.7), moderate: rule([30, 30], 0.7), hard: rule([20, 40], 0.95) },
  BLACK: { easy: rule([50, 10], 0.95), moderate: rule([20, 40], 0.95), hard: rule([10, 50], 0.95) },
};

export const WORK_REST_SOURCE =
  'Work/rest and water: US Army TB MED 507 (acclimatized adults). Published guidance, not individualised.';
export const WATER_LIMITS = 'Hourly fluid intake should not exceed 1.4 L; daily intake should not exceed 11 L.';

// --- Group status -----------------------------------------------------------------------------------------------
export interface StatusCounts { RED: number; AMBER: number; RECOVERING: number; GREEN: number; CALIBRATING: number; signalLost: number }

export function statusCounts(trainees: TraineeRow[]): StatusCounts {
  const c: StatusCounts = { RED: 0, AMBER: 0, RECOVERING: 0, GREEN: 0, CALIBRATING: 0, signalLost: 0 };
  for (const t of trainees) {
    if (t.state) c[t.state] += 1;
    if (t.session_id && t.stale) c.signalLost += 1;
  }
  return c;
}

// --- Needs action now (spec v2 §2.1) ---------------------------------------------------------------------------
export interface Action { trainee: TraineeRow; priority: number; text: string }

export function needsAction(trainees: TraineeRow[], sitePm25: number | null, serverTime: number): Action[] {
  const indoors = sitePm25 !== null && sitePm25 > 60;
  const out: Action[] = [];
  for (const t of trainees) {
    if (!t.session_id) continue;
    const lost = t.stale ? elapsed(t.last_seen ? Math.max(0, Math.round((serverTime - t.last_seen) / 1000)) : null) : null;
    let a: Omit<Action, 'trainee'> | null = null;
    if (t.state === 'RED') a = { priority: 0, text: `Stop ${t.name} now — rest ${indoors ? 'indoors' : 'in shade'}, cool with water.` };
    else if (t.stale) a = { priority: 1, text: `Check on ${t.name} — no data for ${lost}.` };
    else if (t.state === 'AMBER') a = { priority: 2, text: `Slow ${t.name} down and give water.` };
    else if (t.minutes_to_red !== null && t.minutes_to_red <= 10 && t.state !== 'CALIBRATING')
      a = { priority: 3, text: `${t.name}: ~${t.minutes_to_red} min to RED at this effort (model projection).` };
    else if (t.state === 'RECOVERING') a = { priority: 4, text: `Keep ${t.name} resting until cleared.` };
    if (a) out.push({ trainee: t, ...a });
  }
  return out.sort((x, y) => x.priority - y.priority || x.trainee.name.localeCompare(y.trainee.name));
}

// --- Best training window (spec v2 §2.2) -----------------------------------------------------------------------
const COOL: Flag[] = ['NONE', 'WHITE', 'GREEN'];
const HOUR_MS = 3600_000;

function localHour(t: number, tz: string): number {
  return Number(new Intl.DateTimeFormat('en-GB', { hour: '2-digit', hourCycle: 'h23', timeZone: tz }).format(t));
}

function hm(t: number, tz: string): string {
  return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: tz }).format(t);
}

export function bestWindow(forecast: { t: number; wbgt_c: number | null; flag: Flag }[], tz = 'Asia/Kolkata'):
  { start: number; end: number; label: string } | null {
  let best: { start: number; end: number } | null = null;
  let run: { start: number; end: number } | null = null;
  for (const p of forecast) {
    const h = localHour(p.t, tz);
    const ok = h >= 5 && h <= 18 && COOL.includes(p.flag);
    if (ok) {
      run = run && run.end === p.t ? { start: run.start, end: p.t + HOUR_MS } : { start: p.t, end: p.t + HOUR_MS };
      if (!best || run.end - run.start > best.end - best.start) best = { ...run };
    } else {
      run = null;
    }
  }
  return best ? { ...best, label: `${hm(best.start, tz)}–${hm(best.end, tz)}` } : null;
}
