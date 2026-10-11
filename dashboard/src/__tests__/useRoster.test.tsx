import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useRoster } from '../useRoster';
import { roster } from './fixtures';

function Probe({ load }: { load: () => Promise<ReturnType<typeof roster>> }) {
  const { roster: r } = useRoster(3000, load);
  return <p>{r ? 'loaded' : 'loading'}</p>;
}

describe('useRoster', () => {
  afterEach(() => vi.restoreAllMocks());

  it('loads once on mount even when the tab starts hidden', async () => {
    vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('hidden');
    const load = vi.fn().mockResolvedValue(roster([]));
    render(<Probe load={load} />);
    expect(await screen.findByText('loaded')).toBeInTheDocument();
    expect(load).toHaveBeenCalledTimes(1);
  });
});
