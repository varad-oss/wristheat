import { useState } from 'react';
import { refreshContext } from '../api';
import { hhmm, num } from '../format';
import type { Site } from '../types';
import { FlagPennant } from './FlagPennant';

type RefreshState = { kind: 'idle' } | { kind: 'loading' } | { kind: 'done'; at: number } | { kind: 'error'; msg: string };

export function SiteStrip({ site, readOnly = false }: { site: Site | null; readOnly?: boolean }) {
  const [refresh, setRefresh] = useState<RefreshState>({ kind: 'idle' });
  const env = site?.env ?? null;
  const flag = env && !env.stale ? env.flag : 'NONE';

  const onRefresh = async () => {
    setRefresh({ kind: 'loading' });
    try {
      const r = await refreshContext();
      setRefresh({ kind: 'done', at: r.env?.updated_at ?? Date.now() });
    } catch (e) {
      setRefresh({ kind: 'error', msg: e instanceof Error ? e.message : 'Refresh failed' });
    }
  };

  return (
    <section className="site" aria-label="Site heat and air">
      <div className="site-flag">
        <FlagPennant flag={flag} />
        <div>
          <div className="site-wbgt"><span className="num">{num(env?.wbgt_c)}</span><small>°C</small></div>
          <div className="site-flagname">{flag === 'NONE' ? 'No heat flag' : `${flag} flag`}</div>
          <div className="site-method">Open-field WBGT (sun), Liljegren method</div>
        </div>
      </div>
      <dl className="site-facts">
        <div><dt>Air</dt><dd className="num">{num(env?.temp_c)} °C</dd></div>
        <div><dt>Humidity</dt><dd className="num">{num(env?.rh, 0)} %</dd></div>
        <div><dt>Wind</dt><dd className="num">{num(env?.wind_ms)} m/s</dd></div>
        <div><dt>PM2.5</dt><dd className="num">{num(env?.pm25, 0)} µg/m³ <span className="aqi">US AQI {env?.us_aqi ?? '–'}</span></dd></div>
        {env?.coolest_hour?.local && (
          <div><dt>Coolest hour</dt><dd className="num">{env.coolest_hour.local} <span className="aqi">{num(env.coolest_hour.wbgt_c)} °C</span></dd></div>
        )}
      </dl>
      <div className="site-meta">
        <span>{site?.name ?? 'Site not set up'}</span>
        <span>{env ? `Updated ${hhmm(env.updated_at)} · Open-Meteo` : 'No heat data yet'}</span>
        {env?.stale && <span className="warn">Heat data stale: the engine is using heart rate only</span>}
        {!readOnly && (
          <button className="btn btn-quiet" onClick={onRefresh} disabled={refresh.kind === 'loading'}>
            {refresh.kind === 'loading' ? 'Refreshing…' : 'Refresh heat data'}
          </button>
        )}
        {refresh.kind === 'done' && <span role="status">Updated {hhmm(refresh.at)}</span>}
        {refresh.kind === 'error' && <span role="alert" className="warn">Couldn't refresh: {refresh.msg}</span>}
      </div>
    </section>
  );
}
