import { fetchAuthSession } from 'aws-amplify/auth';
import { getConfig } from './config';
import type { Incident, IncidentSummary, Roster, Series, SessionSummary, SiteEnv } from './types';

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

async function call<T>(path: string, init: RequestInit = {}): Promise<T> {
  const session = await fetchAuthSession();
  const token = session.tokens?.idToken?.toString();
  const res = await fetch(`${getConfig().apiUrl.replace(/\/$/, '')}${path}`, {
    ...init,
    headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
  });
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
