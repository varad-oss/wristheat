import { render, screen, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { Live } from '../pages/Live';
import type { Roster } from '../types';
import { NOW, roster, trainee } from './fixtures';

vi.mock('../api', () => ({ getSeries: vi.fn().mockResolvedValue({ session_id: 'x', points: [] }), refreshContext: vi.fn() }));

const hour = (h: number) => Date.UTC(2026, 9, 12, h, 0) - 5.5 * 3600 * 1000;

function yellowRoster(): Roster {
  const r = roster([
    trainee({ trainee_id: 'S3', name: 'Kabir', kind: 'simulated', source: 'simulated', state: 'RED' }),
    trainee({ trainee_id: 'S1', name: 'Arjun', kind: 'simulated', source: 'simulated', state: 'GREEN' }),
    trainee({ trainee_id: 'T1', name: 'Varad', state: 'GREEN' }),
  ]);
  r.site!.env!.flag = 'YELLOW';
  r.site!.env!.wbgt_c = 30.4;
  r.site!.env!.pm25 = 40;
  r.site!.forecast = [5, 6, 7, 8, 9].map((h) => ({ t: hour(h), wbgt_c: 28.5, flag: 'GREEN' as const }));
  r.activity = [
    { t: NOW - 60000, trainee_id: 'S3', name: 'Kabir', kind: 'simulated', source: 'simulated', event: 'RED_ENTERED', state: 'RED' },
    { t: NOW - 600000, trainee_id: 'T1', name: 'Varad', kind: 'real', source: 'live', event: 'CALIBRATED', state: 'GREEN' },
  ];
  return r;
}

const renderLive = (r: Roster) => render(<MemoryRouter><Live roster={r} error={null} /></MemoryRouter>);

describe('Command view', () => {
  it('shows group status counts as words', () => {
    renderLive(yellowRoster());
    const bar = screen.getByRole('region', { name: 'Group status' });
    expect(within(bar).getByText('1')).toBeInTheDocument();
    expect(bar).toHaveTextContent(/1\s*RED/);
    expect(bar).toHaveTextContent(/2\s*GREEN/);
  });

  it('lists the RED trainee first under Needs action now', () => {
    renderLive(yellowRoster());
    const list = screen.getByRole('region', { name: 'Needs action now' });
    expect(within(list).getAllByRole('listitem')[0]).toHaveTextContent('Stop Kabir now — rest in shade, cool with water.');
  });

  it('says no action is needed when nobody needs it', () => {
    renderLive(roster([trainee({ state: 'GREEN' })]));
    expect(screen.getByText('No action needed right now.')).toBeInTheDocument();
  });

  it('shows the activity feed with badges', () => {
    renderLive(yellowRoster());
    const feed = screen.getByRole('region', { name: 'Activity' });
    const first = within(feed).getAllByRole('listitem')[0];
    expect(first).toHaveTextContent('Kabir → RED');
    expect(within(first).getByText('SIMULATED')).toBeInTheDocument();
  });
});

describe('Today panel', () => {
  it('shows the TB MED 507 rules for the current flag with the source', () => {
    renderLive(yellowRoster());
    const today = screen.getByRole('region', { name: 'Today' });
    const hard = within(today).getByRole('row', { name: /Hard/ });
    expect(hard).toHaveTextContent('30 min work / 30 min rest');
    expect(hard).toHaveTextContent('0.95 L/h');
    expect(today).toHaveTextContent('US Army TB MED 507');
    expect(today).toHaveTextContent('Best window: 05:00–10:00');
  });

  it('handles a missing forecast', () => {
    const r = yellowRoster();
    r.site!.forecast = [];
    renderLive(r);
    expect(screen.getByText('Heat forecast not available yet')).toBeInTheDocument();
  });
});
