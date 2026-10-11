import { bestWindow, WATER_LIMITS, WORK_REST, WORK_REST_SOURCE } from '../guidance';
import { hhmm, num } from '../format';
import type { Site } from '../types';

const NIGHT = (h: number) => h < 5 || h >= 19;
const localHour = (t: number) =>
  Number(new Intl.DateTimeFormat('en-GB', { hour: '2-digit', hourCycle: 'h23', timeZone: 'Asia/Kolkata' }).format(t));

/** Before the session: 24-h heat-flag timeline, best window and the published work/rest + water rules. */
export function TodayPanel({ site, serverTime }: { site: Site | null; serverTime: number }) {
  const env = site?.env ?? null;
  const flag = env && !env.stale ? env.flag : 'NONE';
  const forecast = site?.forecast ?? [];
  const best = forecast.length ? bestWindow(forecast) : null;
  const rules = flag === 'NONE' ? null : WORK_REST[flag];

  return (
    <section className="panel today" role="region" aria-label="Today">
      <div className="today-plan">
      <div className="today-head">
        <h2>Plan today's session</h2>
        {forecast.length === 0 ? (
          <p className="muted">Heat forecast not available yet</p>
        ) : (
          <p className="today-window">
            {best ? <>Best window: <strong>{best.label}</strong> (GREEN flag or cooler)</>
              : <>No GREEN-or-cooler daytime hour in the next 24 h. {site?.env?.coolest_hour
                ? `Coolest hour ${site.env.coolest_hour.local}, WBGT ${num(site.env.coolest_hour.wbgt_c)} °C.` : ''}</>}
          </p>
        )}
      </div>

      {forecast.length > 0 && (
        <div className="timeline" role="img" aria-label="Heat flag by hour for the next 24 hours">
          {forecast.map((p) => {
            const h = localHour(p.t);
            const now = serverTime >= p.t && serverTime < p.t + 3600_000;
            const inBest = best && p.t >= best.start && p.t < best.end;
            return (
              <div key={p.t} className={`tl-hour ${NIGHT(h) ? 'is-night' : ''} ${now ? 'is-now' : ''} ${inBest ? 'is-best' : ''}`}
                   title={`${hhmm(p.t)} · ${p.flag === 'NONE' ? 'no flag' : `${p.flag} flag`} · WBGT ${num(p.wbgt_c)} °C`}>
                <span className={`tl-bar flag-${p.flag.toLowerCase()}`} />
                <span className="tl-label num">{h % 3 === 0 || now ? (now ? 'now' : `${String(h).padStart(2, '0')}`) : ''}</span>
              </div>
            );
          })}
        </div>
      )}
      </div>

      <div className="rules">
        <h3>{flag === 'NONE' ? 'No heat flag right now' : `Work and rest under a ${flag} flag`}</h3>
        {rules ? (
          <table>
            <thead><tr><th scope="col">Effort</th><th scope="col">Work / rest each hour</th><th scope="col">Water</th></tr></thead>
            <tbody>
              {(['easy', 'moderate', 'hard'] as const).map((k) => (
                <tr key={k}>
                  <th scope="row">{k[0].toUpperCase() + k.slice(1)}</th>
                  <td>{rules[k].work}</td>
                  <td className="num">{rules[k].waterLph.toFixed(2).replace(/0$/, '')} L/h</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>Below heat category 1: normal precautions.</p>
        )}
        <p className="source">{WORK_REST_SOURCE} {WATER_LIMITS}</p>
      </div>
    </section>
  );
}
