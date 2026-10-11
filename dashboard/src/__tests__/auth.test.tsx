import { renderHook, waitFor } from '@testing-library/react';
import { fetchAuthSession } from 'aws-amplify/auth';
import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('aws-amplify/auth', () => ({ fetchAuthSession: vi.fn() }));
vi.mock('../config', () => ({ getConfig: () => ({ apiUrl: 'https://api.test' }) }));

import { getRoster } from '../api';
import { useRole } from '../role';

const session = (groups: string[] | undefined, raw = 'tok') => ({
  tokens: { idToken: { payload: groups ? { 'cognito:groups': groups } : {}, toString: () => raw } },
});

beforeEach(() => {
  vi.mocked(fetchAuthSession).mockReset();
  vi.unstubAllGlobals();
});

describe('useRole', () => {
  it('refreshes a token issued before the user joined a group', async () => {
    vi.mocked(fetchAuthSession).mockImplementation(async (o?: { forceRefresh?: boolean }) =>
      (o?.forceRefresh ? session(['supervisors']) : session(undefined)) as never);
    const { result } = renderHook(() => useRole());
    await waitFor(() => expect(result.current).toBe('supervisor'));
    expect(fetchAuthSession).toHaveBeenCalledWith({ forceRefresh: true });
  });
});

describe('api call', () => {
  it('retries once with a refreshed token after a 403', async () => {
    vi.mocked(fetchAuthSession).mockImplementation(async (o?: { forceRefresh?: boolean }) =>
      session(['supervisors'], o?.forceRefresh ? 'fresh' : 'stale') as never);
    const fetchMock = vi.fn(async (_url: string, init: RequestInit) => {
      const auth = (init.headers as Record<string, string>).authorization;
      return auth === 'Bearer fresh'
        ? new Response(JSON.stringify({ trainees: [] }), { status: 200 })
        : new Response(JSON.stringify({ error: 'forbidden', message: 'no' }), { status: 403 });
    });
    vi.stubGlobal('fetch', fetchMock);
    await expect(getRoster()).resolves.toEqual({ trainees: [] });
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
