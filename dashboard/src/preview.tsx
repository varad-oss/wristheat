// Dev-only visual preview with fixture data (no Cognito, no API). Not part of the production build.
import { createRoot } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import { roster, trainee, NOW } from './__tests__/fixtures';
import { AlertBanner } from './components/AlertBanner';
import { Footer } from './components/Footer';
import { Live } from './pages/Live';
import { ReportView } from './pages/SessionReport';
import './styles.css';

const r = roster([
  trainee({ trainee_id: 'S2', name: 'Meera', kind: 'simulated', source: 'simulated', state: 'AMBER', hr_now: 158, core_est_c: 37.92, psi: 5.9, minutes_to_red: 6 }),
  trainee({ trainee_id: 'S1', name: 'Arjun', kind: 'simulated', source: 'simulated', state: 'GREEN', hr_now: 138, core_est_c: 37.71, psi: 4.4 }),
  trainee({ trainee_id: 'S3', name: 'Kabir', kind: 'simulated', source: 'simulated', state: 'RED', hr_now: 179, core_est_c: 38.64, psi: 7.4 }),
  trainee({ trainee_id: 'S4', name: 'Ishaan', kind: 'simulated', source: 'simulated', state: 'RECOVERING', hr_now: 97, core_est_c: 38.1, psi: 3.6, stale: true, last_seen: NOW - 45000 }),
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
  { t: NOW - 400000, trainee_id: 'S2', name: 'Meera', kind: 'simulated', source: 'simulated', event: 'AMBER_ENTERED', state: 'AMBER' },
  { t: NOW - 900000, trainee_id: 'S4', name: 'Ishaan', kind: 'simulated', source: 'simulated', event: 'RECOVERING_ENTERED', state: 'RECOVERING' },
];

createRoot(document.getElementById('root')!).render(
  <MemoryRouter>
    <header className="top"><span className="brand">WristHeat</span></header>
    <AlertBanner incidents={r.open_incidents} />
    {location.search.includes('report') ? <ReportView s={{
      session: { session_id: 'sim-S3-abc', source: 'simulated', device: 'simulator', replay_of: null, started_at: NOW - 1800000, last_seen: NOW, status: 'ACTIVE', state: 'GREEN' },
      trainee: { trainee_id: 'S3', name: 'Kabir', kind: 'simulated', age: 21 }, started_at: NOW - 1800000, last_seen: NOW, duration_min: 30, hr0: 76,
      minutes_by_state: { GREEN: 12, AMBER: 9, RED: 4, RECOVERING: 5, CALIBRATING: 0, gap: 0 }, peak_psi: 8.1, peak_core_c: 38.55, peak_hr: 181,
      flag_minutes: { YELLOW: 30 }, env_at_start: { wbgt_c: 30.8, flag: 'YELLOW' },
      incidents: [{ incident_id: 'inc-1', status: 'CLOSED', opened_at: NOW - 900000, closed_at: NOW - 600000, outcome: 'recovered',
        trigger: { psi: 7.7, core_est_c: 38.45, hr: 177, wbgt_c: 30.8, flag: 'YELLOW', pm25: 49, rule: 'psi>=7' },
        metrics: { time_to_ack_s: 107, time_to_recovery_s: 299, minutes_in_red: 4, peak_psi: 8.1, peak_core_c: 38.55, escalated: true },
        acked_at: NOW - 793000, acked_by: 'supervisor', recovered_at: NOW - 601000, report_source: 'template' }],
    }} /> : <Live roster={r} error={null} />}
    <Footer />
  </MemoryRouter>,
);
