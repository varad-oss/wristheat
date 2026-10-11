import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../api';
import { SessionReport } from '../pages/SessionReport';
import type { SessionSummary } from '../types';
import { NOW } from './fixtures';

vi.mock('../api', () => ({ getSessionSummary: vi.fn() }));

const summary = (over: Partial<SessionSummary> = {}): SessionSummary => ({
  session: { session_id: 'sim-S3-abc', source: 'simulated', device: 'simulator', replay_of: null, started_at: NOW - 1800000,
    last_seen: NOW, status: 'ACTIVE', state: 'GREEN' },
  trainee: { trainee_id: 'S3', name: 'Kabir', kind: 'simulated', age: 21 },
  started_at: NOW - 1800000, last_seen: NOW, duration_min: 30, hr0: 76,
  minutes_by_state: { GREEN: 12, AMBER: 9, RED: 4, RECOVERING: 5, CALIBRATING: 0, gap: 0 },
  peak_psi: 8.1, peak_core_c: 38.55, peak_hr: 181, flag_minutes: { YELLOW: 30 },
  env_at_start: { wbgt_c: 30.8, flag: 'YELLOW' },
  incidents: [{ incident_id: 'inc-1', status: 'CLOSED', opened_at: NOW - 900000, closed_at: NOW - 600000, outcome: 'recovered',
    trigger: { psi: 7.7, core_est_c: 38.45, hr: 177, wbgt_c: 30.8, flag: 'YELLOW', pm25: 49, rule: 'psi>=7' },
    metrics: { time_to_ack_s: 107, time_to_recovery_s: 299, minutes_in_red: 4, peak_psi: 8.1, peak_core_c: 38.55, escalated: true },
    acked_at: NOW - 793000, acked_by: 'supervisor', recovered_at: NOW - 601000, report_source: 'template' }],
  ...over,
});

const renderAt = () => render(
  <MemoryRouter initialEntries={['/sessions/sim-S3-abc/report']}>
    <Routes><Route path="/sessions/:id/report" element={<SessionReport />} /></Routes>
  </MemoryRouter>);

beforeEach(() => vi.mocked(api.getSessionSummary).mockResolvedValue(summary()));

describe('Session report', () => {
  it('shows the trainee with the SIMULATED badge', async () => {
    renderAt();
    expect(await screen.findByRole('heading', { name: /Kabir/ })).toBeInTheDocument();
    expect(screen.getByText('SIMULATED')).toBeInTheDocument();
  });

  it('shows time in each state with minutes', async () => {
    renderAt();
    const bar = await screen.findByRole('img', { name: /Time in state/ });
    expect(bar).toHaveAccessibleName('Time in state: GREEN 12 min, AMBER 9 min, RED 4 min, RECOVERING 5 min');
  });

  it('lists incidents with response times', async () => {
    renderAt();
    expect(await screen.findByText('Acknowledged after 1 min 47 s')).toBeInTheDocument();
    expect(screen.getByText('Recovery confirmed after 4 min 59 s')).toBeInTheDocument();
    expect(screen.getByText(/Escalated to backup contact/)).toBeInTheDocument();
  });

  it('handles a session with no completed minutes', async () => {
    vi.mocked(api.getSessionSummary).mockResolvedValue(summary({ duration_min: 0, peak_psi: null, peak_core_c: null, peak_hr: null,
      minutes_by_state: { GREEN: 0, AMBER: 0, RED: 0, RECOVERING: 0, CALIBRATING: 0, gap: 0 }, incidents: [], env_at_start: null }));
    renderAt();
    expect(await screen.findByText('No completed minutes yet')).toBeInTheDocument();
  });

  it('prints', async () => {
    const print = vi.spyOn(window, 'print').mockImplementation(() => undefined);
    renderAt();
    fireEvent.click(await screen.findByRole('button', { name: 'Print / save PDF' }));
    expect(print).toHaveBeenCalledTimes(1);
  });
});
