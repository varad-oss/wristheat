import type { State } from '../types';

/** State in words and colour; colour is never the only signal. */
export function StateChip({ state }: { state: State | null }) {
  if (!state) return <span className="chip chip-none">No session</span>;
  return <span className={`chip chip-${state.toLowerCase()}`}>{state}</span>;
}
