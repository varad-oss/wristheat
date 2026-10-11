import type { Roster, TraineeRow } from '../types';

export const NOW = 1791700066000;

export function trainee(over: Partial<TraineeRow>): TraineeRow {
  return {
    trainee_id: 'T1', name: 'Varad', kind: 'real', source: 'live', session_id: 'sess-1', state: 'GREEN',
    state_since: NOW - 60000, hr_now: 120, hr0: 74, core_est_c: 37.42, core_band_c: 0.6, psi: 3.1,
    minutes_to_red: null, last_seen: NOW - 2000, stale: false, incident_id: null, replay_of: null,
    recorded_at: null, recorded_device: null, ...over,
  };
}

export function roster(trainees: TraineeRow[], open_incidents: Roster['open_incidents'] = []): Roster {
  return {
    site: {
      site_id: 'kgp', name: 'IIT Kharagpur campus', lat: 22.3149, lon: 87.3105, forecast: [],
      env: { wbgt_c: 31.4, flag: 'RED', temp_c: 31.2, rh: 71, wind_ms: 2.1, pm25: 72, us_aqi: 158,
             updated_at: NOW - 60000, stale: false, coolest_hour: { local: '06:00', wbgt_c: 26.9 } },
    },
    trainees, open_incidents, server_time: NOW,
  };
}
