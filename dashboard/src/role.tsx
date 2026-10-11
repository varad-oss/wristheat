import { fetchAuthSession } from 'aws-amplify/auth';
import { useEffect, useState } from 'react';

export type Role = 'supervisor' | 'wearer' | 'unknown';

/** Reads the Cognito groups from the ID token: supervisors see the group, wearers see their own page. */
export function useRole(): Role | null {
  const [role, setRole] = useState<Role | null>(null);
  useEffect(() => {
    fetchAuthSession().then((s) => {
      const groups = (s.tokens?.idToken?.payload['cognito:groups'] as string[] | undefined) ?? [];
      setRole(groups.includes('supervisors') ? 'supervisor' : groups.includes('wearers') ? 'wearer' : 'unknown');
    }).catch(() => setRole('unknown'));
  }, []);
  return role;
}
