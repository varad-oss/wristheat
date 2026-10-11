import type { Flag } from '../types';

/** The TB MED 507 heat-category flag as flown at a training ground. */
export function FlagPennant({ flag }: { flag: Flag }) {
  return (
    <svg className={`pennant pennant-${flag.toLowerCase()}`} viewBox="0 0 64 80" aria-hidden="true">
      <rect x="4" y="2" width="4" height="76" rx="1" className="pole" />
      <path d="M8 6 H60 L48 22 L60 38 H8 Z" className="cloth" />
    </svg>
  );
}
