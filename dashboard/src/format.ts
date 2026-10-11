import type { State } from './types';

const IST = 'Asia/Kolkata';

export function hhmm(ms: number | null | undefined): string {
  if (!ms) return '–';
  return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: IST }).format(ms);
}

export function hhmmss(ms: number | null | undefined): string {
  if (!ms) return '–';
  return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: IST })
    .format(ms);
}

export function dateTime(ms: number | null | undefined): string {
  if (!ms) return '–';
  return new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
    timeZone: IST }).format(ms);
}

export function num(v: number | null | undefined, digits = 1): string {
  return v === null || v === undefined ? '–' : v.toFixed(digits);
}

export function duration(s: number | null | undefined): string {
  if (s === null || s === undefined) return '–';
  if (s < 60) return `${s} s`;
  return `${Math.floor(s / 60)} min ${s % 60} s`;
}

export const STATE_RANK: Record<string, number> = { RED: 0, AMBER: 1, RECOVERING: 2, GREEN: 3, CALIBRATING: 4 };

export function stateRank(s: State | null): number {
  return s ? STATE_RANK[s] ?? 5 : 5;
}

export const STATE_LABEL: Record<State, string> = {
  RED: 'RED', AMBER: 'AMBER', GREEN: 'GREEN', RECOVERING: 'RECOVERING', CALIBRATING: 'CALIBRATING',
};

/** Elapsed time for "Signal lost …": seconds under 2 min, then minutes, then hours and minutes. */
export function elapsed(s: number | null): string {
  if (s === null) return '–';
  if (s < 120) return `${s} s`;
  const min = Math.round(s / 60);
  if (min < 90) return `${min} min`;
  return `${Math.floor(min / 60)} h ${min % 60} min`;
}
