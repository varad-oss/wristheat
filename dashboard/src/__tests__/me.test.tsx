import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../api';
import { RoleGate } from '../App';
import { Me } from '../pages/Me';
import type { MeView } from '../types';
import { NOW, roster, trainee } from './fixtures';

vi.mock('../api', async () => {
  const actual = await vi.importActual<typeof import('../api')>('../api');
  return { ApiError: actual.ApiError, getMe: vi.fn(), ackIncident: vi.fn(), getIncident: vi.fn().mockResolvedValue({ audio: {} }),
           getSeries: vi.fn().mockResolvedValue({ session_id: 'x', points: [] }), refreshContext: vi.fn() };
});

function me(over: Partial<MeView> = {}): MeView {
  const r = roster([]);
  return {
    trainee: { trainee_id: 'T1', name: 'Varad', kind: 'real', mode: 'solo', age: 21 },
    live: trainee({ state: 'AMBER', hr_now: 162, core_est_c: 37.84, psi: 5.4, minutes_to_red: 9 }),
    site: r.site, open_incidents: [], activity: [{ t: NOW - 60000, event: 'AMBER_ENTERED', state: 'AMBER' }],
    sessions: [{ session_id: 'sess-1', started_at: NOW - 1800000, last_seen: NOW, status: 'ACTIVE', state: 'AMBER', source: 'live' },
               { session_id: 'sess-0', started_at: NOW - 90000000, last_seen: NOW - 88000000, status: 'ENDED', state: 'GREEN', source: 'live' }],
    server_time: NOW, ...over,
  };
}

const red = { incident_id: 'inc-t1', trainee_id: 'T1', trainee_name: 'Varad', trainee_kind: 'real' as const, session_id: 'sess-1',
  status: 'NOTIFIED' as const, opened_at: NOW - 30000, closed_at: null, outcome: null, escalated_at: null, acked_at: null, acked_by: null,
  trigger: { psi: 7.1, core_est_c: 38.5, hr: 178, wbgt_c: 31, flag: 'YELLOW' as const, pm25: 40, rule: 'psi>=7' },
  advice: { en: 'Stop now. Rest in shade and cool down with water.', hi: '' } };

const renderMe = () => render(<MemoryRouter><Me /></MemoryRouter>);

beforeEach(() => { vi.mocked(api.getMe).mockResolvedValue(me()); vi.mocked(api.ackIncident).mockReset(); });

describe('Personal page', () => {
  it('shows my live state in words and numbers', async () => {
    renderMe();
    expect(await screen.findByRole('heading', { name: /Varad/ })).toBeInTheDocument();
    const live = screen.getByRole('region', { name: 'Right now' });
    expect(live).toHaveTextContent('AMBER');
    expect(live).toHaveTextContent('162');
    expect(live).toHaveTextContent('37.84 ± 0.6 °C');
    expect(live).toHaveTextContent(/~9 min to RED/);
  });

  it('asks me to confirm I stopped when I am RED, and explains the emergency contact', async () => {
    vi.mocked(api.getMe).mockResolvedValue(me({ open_incidents: [red] }));
    vi.mocked(api.ackIncident).mockResolvedValue({ status: 'ACKNOWLEDGED' });
    renderMe();
    expect(await screen.findByText('Stop now. You reached RED heat strain.')).toBeInTheDocument();
    expect(screen.getByText(/emergency contact is emailed/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: "I've stopped and I'm cooling down" }));
    expect(await screen.findByText(/Your emergency contact will not be emailed/)).toBeInTheDocument();
    expect(api.ackIncident).toHaveBeenCalledWith('inc-t1', 'wearer stopped');
  });

  it('lists my runs with links to their reports', async () => {
    renderMe();
    const runs = await screen.findByRole('region', { name: 'Your runs' });
    const links = runs.querySelectorAll('a');
    expect(links[0]).toHaveAttribute('href', '/me/runs/sess-1');
    expect(links.length).toBe(2);
  });

  it('explains when the sign-in has no wearer profile', async () => {
    vi.mocked(api.getMe).mockRejectedValue(new api.ApiError(404, 'no_wearer_profile', 'This sign-in is not linked to a wearer.'));
    renderMe();
    expect(await screen.findByText(/not linked to a wearer/)).toBeInTheDocument();
  });
});

function Where() { return <p>at {useLocation().pathname}</p>; }

describe('RoleGate', () => {
  it('sends a wearer from the console to their own page', () => {
    render(<MemoryRouter initialEntries={['/console']}><Routes>
      <Route path="/console/*" element={<RoleGate role="wearer"><p>console</p></RoleGate>} />
      <Route path="/me" element={<Where />} /></Routes></MemoryRouter>);
    expect(screen.getByText('at /me')).toBeInTheDocument();
  });

  it('lets a supervisor into the console', () => {
    render(<MemoryRouter initialEntries={['/console']}><Routes>
      <Route path="/console/*" element={<RoleGate role="supervisor"><p>console</p></RoleGate>} /></Routes></MemoryRouter>);
    expect(screen.getByText('console')).toBeInTheDocument();
  });
});
