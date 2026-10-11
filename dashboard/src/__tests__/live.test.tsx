import { render, screen, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { Footer, ATTRIBUTION } from '../components/Footer';
import { Live } from '../pages/Live';
import { roster, trainee } from './fixtures';

vi.mock('../api', () => ({ getSeries: vi.fn().mockResolvedValue({ session_id: 'x', points: [] }) }));

function renderLive(r = roster([])) {
  return render(<MemoryRouter><Live roster={r} error={null} /></MemoryRouter>);
}

describe('Live group view', () => {
  it('renders SIMULATED badge for kind simulated', () => {
    renderLive(roster([trainee({ trainee_id: 'S1', name: 'Arjun', kind: 'simulated', source: 'simulated' })]));
    expect(screen.getByText('SIMULATED')).toBeInTheDocument();
  });

  it('labels a replay with its recording time and device', () => {
    renderLive(roster([trainee({ trainee_id: 'R1', source: 'replay', replay_of: 'orig', recorded_at: 1791650000000,
      recorded_device: 'SM-R920' })]));
    expect(screen.getByText(/^REPLAY · recorded .* on SM-R920$/)).toBeInTheDocument();
  });

  it('orders RED card first', () => {
    renderLive(roster([
      trainee({ trainee_id: 'S1', name: 'Arjun', state: 'GREEN' }),
      trainee({ trainee_id: 'S3', name: 'Kabir', state: 'RED' }),
      trainee({ trainee_id: 'S2', name: 'Meera', state: 'AMBER' }),
    ]));
    const cards = screen.getAllByRole('article');
    expect(within(cards[0]).getByText('Kabir')).toBeInTheDocument();
    expect(within(cards[1]).getByText('Meera')).toBeInTheDocument();
  });

  it('shows "Signal lost" when stale', () => {
    renderLive(roster([trainee({ stale: true, last_seen: 1791700066000 - 45000 })]));
    expect(screen.getByText(/Signal lost 45 s/)).toBeInTheDocument();
  });

  it('shows "~6 min to RED (model projection)" when minutes_to_red = 6', () => {
    renderLive(roster([trainee({ state: 'AMBER', minutes_to_red: 6 })]));
    expect(screen.getByText(/~6 min to RED.*\(model projection\)/)).toBeInTheDocument();
  });

  it('shows the estimated core with its band and caption', () => {
    renderLive(roster([trainee({ core_est_c: 37.92 })]));
    expect(screen.getByText('37.92 ± 0.6 °C')).toBeInTheDocument();
    expect(screen.getByText(/estimated trend/)).toBeInTheDocument();
  });

  it('shows the site WBGT with its flag in words', () => {
    renderLive();
    expect(screen.getByText('31.4')).toBeInTheDocument();
    expect(screen.getByText(/RED flag/)).toBeInTheDocument();
    expect(screen.getByText(/Open-field WBGT \(sun\), Liljegren method/)).toBeInTheDocument();
  });

  it('footer contains the exact attribution string', () => {
    render(<Footer />);
    expect(screen.getByRole('contentinfo')).toHaveTextContent(ATTRIBUTION);
    expect(ATTRIBUTION).toBe('Weather: Open-Meteo.com (CC BY 4.0) · Air quality: CAMS via Open-Meteo · ' +
      'Core-temperature estimate: ECTemp (USARIEM, US patent 10702165), used in a non-commercial research prototype');
  });
});
