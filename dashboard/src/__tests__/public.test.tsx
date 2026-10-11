import { render, screen } from '@testing-library/react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../api';
import { SiteRoutes } from '../App';
import { roster, trainee } from './fixtures';

vi.mock('../api', () => ({ getPublicRoster: vi.fn(), getSeries: vi.fn(), refreshContext: vi.fn() }));

function Probe() {
  return <p>console at {useLocation().pathname}</p>;
}

const at = (path: string) => render(<MemoryRouter initialEntries={[path]}><SiteRoutes consoleElement={<Probe />} /></MemoryRouter>);

beforeEach(() => {
  const r = roster([trainee({ trainee_id: 'S3', name: 'Kabir', kind: 'simulated', source: 'simulated', state: 'RED' })]);
  vi.mocked(api.getPublicRoster).mockResolvedValue({ ...r, public: true });
});

describe('Landing page', () => {
  it('shows the global scale with sources, both ways to use it, and the entry points', () => {
    at('/');
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /489,000 people die from heat/ })).toBeInTheDocument();
    for (const who of ['Outdoor and manual workers', 'School children', 'Recruitment and military training',
      'Pilgrims, runners and crowds', 'India, summer 2024']) {
      expect(screen.getByRole('heading', { name: who })).toBeInTheDocument();
    }
    expect(screen.getByRole('link', { name: 'ILO, 2024' })).toHaveAttribute('href', expect.stringContaining('ilo.org'));
    for (const h of ['On your own', 'With a group', 'Plan around the heat, before anyone starts']) {
      expect(screen.getByRole('heading', { name: h })).toBeInTheDocument();
    }
    expect(screen.getAllByRole('link', { name: 'See the live demo' })[0]).toHaveAttribute('href', '/demo');
    expect(screen.getAllByRole('link', { name: 'Sign in' })[0]).toHaveAttribute('href', '/console');
    expect(document.body.textContent).not.toMatch(/—/);
  });
});

describe('Public demo', () => {
  it('shows only simulated trainees, labelled, with no supervisor actions', async () => {
    at('/demo');
    expect(await screen.findByText('Kabir')).toBeInTheDocument();
    expect(screen.getByText('Public demo. All trainees here are SIMULATED. Real wearers are visible only to signed-in supervisors.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Acknowledge/ })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Refresh heat data' })).not.toBeInTheDocument();
    expect(screen.queryByRole('link', { name: 'Session report' })).not.toBeInTheDocument();
  });
});

describe('Console routes', () => {
  it('redirects old console paths under /console', () => {
    at('/incidents');
    expect(screen.getByText('console at /console/incidents')).toBeInTheDocument();
  });

  it('serves the console under /console', () => {
    at('/console/trainee/T1');
    expect(screen.getByText('console at /console/trainee/T1')).toBeInTheDocument();
  });
});
