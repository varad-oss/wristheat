import type { StatusCounts } from '../guidance';

const ORDER: { key: keyof StatusCounts; label: string; cls: string }[] = [
  { key: 'RED', label: 'RED', cls: 'red' },
  { key: 'AMBER', label: 'AMBER', cls: 'amber' },
  { key: 'RECOVERING', label: 'RECOVERING', cls: 'recovering' },
  { key: 'GREEN', label: 'GREEN', cls: 'green' },
  { key: 'CALIBRATING', label: 'CALIBRATING', cls: 'calibrating' },
  { key: 'signalLost', label: 'signal lost', cls: 'lost' },
];

/** Group status at a glance: a count per state, always with the state word. */
export function CommandBar({ counts, total }: { counts: StatusCounts; total: number }) {
  return (
    <section className="cmdbar" role="region" aria-label="Group status">
      <p className="cmdbar-total"><strong className="num">{total}</strong> in the group</p>
      <ul>
        {ORDER.map(({ key, label, cls }) => (
          <li key={key} className={`cmdbar-item cmdbar-${cls} ${counts[key] ? '' : 'is-zero'}`}>
            <strong className="num">{counts[key]}</strong> <span>{label}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
