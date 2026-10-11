import { fetchAuthSession } from 'aws-amplify/auth';
import { getConfig } from './config';
import type { Incident, IncidentSummary, MeView, Roster, Series, SessionSummary, SiteEnv } from './types';

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

async function send(path: string, init: RequestInit, forceRefresh: boolean): Promise<Response> {
  const session = await fetchAuthSession(forceRefresh ? { forceRefresh: true } : undefined);
  const token = session.tokens?.idToken?.toString();
  return fetch(`${getConfig().apiUrl.replace(/\/$/, '')}${path}`, {
    ...init,
    headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
  });
}

async function call<T>(path: string, init: RequestInit = {}): Promise<T> {
  let res = await send(path, init, false);
  // A 403 can mean the cached token predates a group change; retry once with a fresh token.
  if (res.status === 403) res = await send(path, init, true);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(res.status, body.error ?? 'error', body.message ?? `HTTP ${res.status}`);
  return body as T;
}

export const getRoster = () => call<Roster>('/v1/roster');
export const getSeries = (sessionId: string, sinceMinute?: number) =>
  call<Series>(`/v1/sessions/${encodeURIComponent(sessionId)}/series${sinceMinute ? `?since_minute=${sinceMinute}` : ''}`);
export const getIncidents = (status: 'open' | 'all') =>
  call<{ incidents: IncidentSummary[] }>(`/v1/incidents?status=${status}`);
export const getIncident = (id: string) => call<Incident>(`/v1/incidents/${encodeURIComponent(id)}`);
export const ackIncident = (id: string, note: string) =>
  call<{ status: string }>(`/v1/incidents/${encodeURIComponent(id)}/ack`, { method: 'POST', body: JSON.stringify({ note }) });
export const refreshContext = () => call<{ env: SiteEnv | null }>('/v1/context/refresh', { method: 'POST' });
export const getSessionSummary = (sessionId: string) =>
  call<SessionSummary>(`/v1/sessions/${encodeURIComponent(sessionId)}/summary`);

/** Public read-only demo roster (simulated trainees only); no sign-in. */
export async function getPublicRoster(): Promise<Roster & { public: true }> {
  const res = await fetch(`${getConfig().apiUrl.replace(/\/$/, '')}/v1/public/roster`);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(res.status, body.error ?? 'error', body.message ?? `HTTP ${res.status}`);
  return body;
}
export const getMe = () => call<MeView>('/v1/me');
