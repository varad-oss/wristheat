// Dev-only visual preview with fixture data (no Cognito, no API). Not part of the production build.
import { createRoot } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import { roster, trainee, NOW } from './__tests__/fixtures';
import { AlertBanner } from './components/AlertBanner';
import { Footer } from './components/Footer';
import { Live } from './pages/Live';
import './styles.css';

const r = roster([
  trainee({ trainee_id: 'T1', name: 'Varad', state: 'AMBER', hr_now: 158, core_est_c: 37.92, psi: 5.9, minutes_to_red: 6 }),
  trainee({ trainee_id: 'S1', name: 'Arjun', kind: 'simulated', source: 'simulated', state: 'GREEN', hr_now: 138, core_est_c: 37.71, psi: 4.4 }),
  trainee({ trainee_id: 'S3', name: 'Kabir', kind: 'simulated', source: 'simulated', state: 'RED', hr_now: 179, core_est_c: 38.64, psi: 7.4 }),
  trainee({ trainee_id: 'S4', name: 'Ishaan', kind: 'simulated', source: 'simulated', state: 'RECOVERING', hr_now: 97, core_est_c: 38.1, psi: 3.6, stale: true, last_seen: NOW - 45000 }),
  trainee({ trainee_id: 'R1', name: 'Varad — earlier run', source: 'replay', replay_of: 'x', recorded_at: NOW - 3 * 3600000, recorded_device: 'SM-R920', state: 'GREEN', hr_now: 112, core_est_c: 37.3, psi: 2.2 }),
  trainee({ trainee_id: 'S2', name: 'Meera', kind: 'simulated', source: null, session_id: null, state: null, hr_now: null }),
], [{
  incident_id: 'inc-sim-S3-a-1', trainee_id: 'S3', trainee_name: 'Kabir', trainee_kind: 'simulated', session_id: 'x',
  status: 'ESCALATED', opened_at: NOW - 120000, closed_at: null, outcome: null, escalated_at: NOW - 30000, acked_at: null, acked_by: null,
  trigger: { psi: 7.2, core_est_c: 38.62, hr: 176, wbgt_c: 31.4, flag: 'YELLOW', pm25: 51, rule: 'psi>=7' },
  advice: { en: 'Stop now. Rest in shade and cool down with water.', hi: 'अभी रुकें। छाँव में आराम करें और पानी से शरीर ठंडा करें।' },
}]);

r.site!.env!.flag = 'YELLOW'; r.site!.env!.wbgt_c = 30.4; r.site!.env!.pm25 = 49;
r.site!.forecast = Array.from({ length: 24 }, (_, i) => {
  const t = NOW - (NOW % 3600000) + i * 3600000;
  const h = (new Date(t).getUTCHours() + 5.5) % 24;
  const flag = h >= 19 || h < 6 ? 'NONE' : h < 8 ? 'GREEN' : h < 10 ? 'YELLOW' : h < 16 ? 'RED' : 'YELLOW';
  return { t, wbgt_c: 26 + (flag === 'RED' ? 5 : flag === 'YELLOW' ? 4 : 2), flag: flag as 'NONE' };
});
r.activity = [
  { t: NOW - 90000, trainee_id: 'S3', name: 'Kabir', kind: 'simulated', source: 'simulated', event: 'RED_ENTERED', state: 'RED' },
  { t: NOW - 400000, trainee_id: 'T1', name: 'Varad', kind: 'real', source: 'live', event: 'AMBER_ENTERED', state: 'AMBER' },
  { t: NOW - 900000, trainee_id: 'S4', name: 'Ishaan', kind: 'simulated', source: 'simulated', event: 'RECOVERING_ENTERED', state: 'RECOVERING' },
];

createRoot(document.getElementById('root')!).render(
  <MemoryRouter>
    <header className="top"><span className="brand">WristHeat</span></header>
    <AlertBanner incidents={r.open_incidents} />
    <Live roster={r} error={null} />
    <Footer />
  </MemoryRouter>,
);
