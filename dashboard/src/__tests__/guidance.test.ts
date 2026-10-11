import { describe, expect, it } from 'vitest';
import { bestWindow, needsAction, statusCounts, WORK_REST } from '../guidance';
import { NOW, trainee } from './fixtures';

const istHour = (h: number) => Date.UTC(2026, 9, 12, h, 0) - 5.5 * 3600 * 1000; // 12 Oct, h:00 IST

describe('TB MED 507 work/rest table', () => {
  it('matches the published values', () => {
    expect(WORK_REST.YELLOW.hard).toEqual({ work: '30 min work / 30 min rest', waterLph: 0.95 });
    expect(WORK_REST.BLACK.easy).toEqual({ work: '50 min work / 10 min rest', waterLph: 0.95 });
    expect(WORK_REST.WHITE.moderate.work).toBe('No limit');
    expect(WORK_REST.RED.hard).toEqual({ work: '20 min work / 40 min rest', waterLph: 0.95 });
    expect(WORK_REST.GREEN.easy).toEqual({ work: 'No limit', waterLph: 0.5 });
  });
});

describe('statusCounts', () => {
  it('counts states and lost signals', () => {
    const c = statusCounts([
      trainee({ trainee_id: 'a', state: 'RED' }), trainee({ trainee_id: 'b', state: 'AMBER' }),
      trainee({ trainee_id: 'c', state: 'GREEN' }), trainee({ trainee_id: 'd', state: 'GREEN', stale: true }),
      trainee({ trainee_id: 'e', state: null, session_id: null, stale: true }),
    ]);
    expect(c).toEqual({ RED: 1, AMBER: 1, RECOVERING: 0, GREEN: 2, CALIBRATING: 0, signalLost: 1 });
  });
});

describe('needsAction', () => {
  const list = [
    trainee({ trainee_id: 'S4', name: 'Ishaan', state: 'RECOVERING' }),
    trainee({ trainee_id: 'T1', name: 'Varad', state: 'GREEN', minutes_to_red: 6 }),
    trainee({ trainee_id: 'S1', name: 'Arjun', state: 'AMBER' }),
    trainee({ trainee_id: 'S2', name: 'Meera', state: 'GREEN', stale: true, last_seen: NOW - 120000 }),
    trainee({ trainee_id: 'S3', name: 'Kabir', state: 'RED', stale: true, last_seen: NOW - 60000 }),
    trainee({ trainee_id: 'X', name: 'Nobody', state: null, session_id: null, stale: true }),
  ];

  it('orders by urgency, one line per trainee', () => {
    expect(needsAction(list, 40, NOW).map((a) => a.text)).toEqual([
      'Stop Kabir now — rest in shade, cool with water.',
      'Check on Meera — no data for 2 min.',
      'Slow Arjun down and give water.',
      'Varad: ~6 min to RED at this effort (model projection).',
      'Keep Ishaan resting until cleared.',
    ]);
  });

  it('uses the indoors variant when PM2.5 is above 60', () => {
    expect(needsAction(list, 72, NOW)[0].text).toBe('Stop Kabir now — rest indoors, cool with water.');
  });
});

describe('bestWindow', () => {
  it('finds the longest GREEN-or-cooler daytime run', () => {
    const flags = ['GREEN', 'GREEN', 'GREEN', 'YELLOW', 'GREEN', 'GREEN', 'GREEN', 'GREEN'] as const;
    const fc = flags.map((flag, i) => ({ t: istHour(3 + i), wbgt_c: 28, flag }));
    const w = bestWindow(fc)!;
    expect(w.label).toBe('07:00–11:00');
    expect(w.start).toBe(istHour(7));
    expect(w.end).toBe(istHour(11));
  });

  it('returns null when no daytime hour is GREEN or cooler', () => {
    expect(bestWindow([8, 9, 10].map((h) => ({ t: istHour(h), wbgt_c: 30, flag: 'YELLOW' as const })))).toBeNull();
  });
});
