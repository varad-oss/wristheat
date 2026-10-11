// Shapes of the supervisor API (spec §5.2).
export type State = 'CALIBRATING' | 'GREEN' | 'AMBER' | 'RED' | 'RECOVERING';
export type Flag = 'NONE' | 'WHITE' | 'GREEN' | 'YELLOW' | 'RED' | 'BLACK';

export interface SiteEnv {
  wbgt_c: number | null; flag: Flag; temp_c: number | null; rh: number | null; wind_ms: number | null;
  pm25: number | null; us_aqi: number | null; updated_at: number; stale: boolean;
  coolest_hour: { local: string; wbgt_c: number } | null;
}

export interface Site {
  site_id: string; name: string; lat: number; lon: number; env: SiteEnv | null;
  forecast: { t: number; wbgt_c: number | null; flag: Flag }[];
}

export interface TraineeRow {
  trainee_id: string; name: string; kind: 'real' | 'simulated'; source: 'live' | 'simulated' | 'replay' | null;
  session_id: string | null; state: State | null; state_since: number | null; hr_now: number | null;
  hr0: number | null; core_est_c: number | null; core_band_c: number; psi: number | null;
  minutes_to_red: number | null; last_seen: number | null; stale: boolean; incident_id: string | null;
  replay_of: string | null; recorded_at: number | null; recorded_device: string | null;
}

export interface Trigger {
  psi: number; core_est_c: number; hr: number; wbgt_c: number | null; flag: Flag; pm25: number | null; rule: string;
}

export interface IncidentSummary {
  incident_id: string; trainee_id: string; trainee_name: string; trainee_kind: 'real' | 'simulated';
  session_id: string; status: 'NOTIFIED' | 'ESCALATED' | 'ACKNOWLEDGED' | 'CLOSED'; opened_at: number;
  closed_at: number | null; outcome: string | null; trigger: Trigger; escalated_at: number | null;
  acked_at: number | null; acked_by: string | null; advice: { en: string; hi: string };
}

export interface ActivityItem {
  t: number; trainee_id: string; name: string; kind: 'real' | 'simulated'; source: TraineeRow['source'];
  event: string; state: State;
}

export interface Roster {
  site: Site | null; trainees: TraineeRow[]; open_incidents: IncidentSummary[]; server_time: number;
  activity?: ActivityItem[];
}

export interface MinutePoint {
  minute: number; hr: number | null; n: number; core_est_c: number; core_var: number; psi: number | null;
  level: string | null; state: State; wbgt_c: number | null; flag: Flag;
}

export interface Series { session_id: string; points: MinutePoint[] }

export interface IncidentEvent { t: number; type: string; detail: string }

export interface Incident extends Omit<IncidentSummary, 'advice'> {
  events: IncidentEvent[];
  metrics?: { time_to_ack_s: number | null; time_to_recovery_s: number | null; minutes_in_red: number;
              peak_psi: number | null; peak_core_c: number | null; escalated: boolean };
  report?: { text: string; source: 'bedrock' | 'template'; model: string | null; generated_at: number };
  audio: { en?: string; hi?: string };
  console_url: string | null;
  summary: IncidentSummary;
  recovered_at?: number | null;
}

export interface SessionSummary {
  session: { session_id: string; source: TraineeRow['source']; device: string | null; replay_of: string | null;
             started_at: number; last_seen: number; status: string; state: State | null };
  trainee: { trainee_id: string; name: string; kind: 'real' | 'simulated'; age: number | null };
  started_at: number; last_seen: number; duration_min: number; hr0: number | null;
  minutes_by_state: Record<State | 'gap', number>;
  peak_psi: number | null; peak_core_c: number | null; peak_hr: number | null;
  flag_minutes: Record<string, number>;
  env_at_start: { wbgt_c: number | null; flag: Flag } | null;
  incidents: (Pick<Incident, 'incident_id' | 'status' | 'opened_at' | 'closed_at' | 'outcome' | 'trigger' | 'metrics' |
    'acked_at' | 'acked_by'> & { recovered_at: number | null; report_source: 'bedrock' | 'template' | null })[];
}

export interface MeView {
  trainee: { trainee_id: string; name: string; kind: 'real' | 'simulated'; mode: 'solo' | 'group'; age: number | null; amber_hr?: number | null };
  live: TraineeRow;
  site: Site | null;
  open_incidents: IncidentSummary[];
  activity: { t: number; event: string; state: State }[];
  sessions: { session_id: string; started_at: number; last_seen: number; status: string; state: State | null; source: TraineeRow['source'] }[];
  server_time: number;
}
