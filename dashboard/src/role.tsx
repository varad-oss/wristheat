import { fetchAuthSession } from 'aws-amplify/auth';
import { useEffect, useState } from 'react';

export type Role = 'supervisor' | 'wearer' | 'unknown';

/** Reads the Cognito groups from the ID token: supervisors see the group, wearers see their own page. */
export function useRole(): Role | null {
  const [role, setRole] = useState<Role | null>(null);
  useEffect(() => {
    const groupsOf = (s: Awaited<ReturnType<typeof fetchAuthSession>>) =>
      (s.tokens?.idToken?.payload['cognito:groups'] as string[] | undefined) ?? [];
    (async () => {
      let groups = groupsOf(await fetchAuthSession());
      // A token issued before the user was added to a group has no groups claim; refresh it once.
      if (groups.length === 0) groups = groupsOf(await fetchAuthSession({ forceRefresh: true }));
      setRole(groups.includes('supervisors') ? 'supervisor' : groups.includes('wearers') ? 'wearer' : 'unknown');
    })().catch(() => setRole('unknown'));
  }, []);
  return role;
}
