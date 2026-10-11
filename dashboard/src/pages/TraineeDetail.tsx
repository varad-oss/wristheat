import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Area, CartesianGrid, ComposedChart, Line, ReferenceArea, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { getSeries } from '../api';
import { SourceBadge } from '../components/SourceBadge';
import { StateChip } from '../components/StateChip';
import { STATE_COLOUR } from '../components/TraineeCard';
import { hhmm } from '../format';
import type { MinutePoint, Roster } from '../types';

const FLAG_COLOUR: Record<string, string> = { NONE: '#dfe4e1', WHITE: '#f4f6f5', GREEN: '#4f9d6e', YELLOW: '#e0b43a', RED: '#c8433a', BLACK: '#232a2d' };

export function TraineeDetail({ roster }: { roster: Roster | null }) {
  const { id = '' } = useParams();
  const t = roster?.trainees.find((x) => x.trainee_id === id) ?? null;
  const [points, setPoints] = useState<MinutePoint[]>([]);
  useEffect(() => {
    if (!t?.session_id) return;
    let alive = true;
    const load = () => getSeries(t.session_id!).then((s) => alive && setPoints(s.points)).catch(() => undefined);
    load();
    const timer = window.setInterval(load, 15000);
    return () => { alive = false; window.clearInterval(timer); };
  }, [t?.session_id]);

  if (!t) return <main id="main" className="page"><p role="status">{roster ? 'This trainee is not on the roster.' : 'Loading…'}</p></main>;
  const data = points.map((p) => ({
    t: p.minute * 60000, hr: p.hr, core: p.hr === null ? null : p.core_est_c,
    band: p.hr === null ? null : [p.core_est_c - 0.6, p.core_est_c + 0.6], state: p.state, flag: p.flag,
  }));
  const segments: { from: number; to: number; state: string }[] = [];
  for (const d of data) {
    const last = segments[segments.length - 1];
    if (last && last.state === d.state) last.to = d.t + 60000;
    else segments.push({ from: d.t, to: d.t + 60000, state: d.state });
  }
  const incidents = (roster?.open_incidents ?? []).filter((i) => i.session_id === t.session_id);
  return (
    <main id="main" className="page">
      <p><Link to="/console">Group view</Link></p>
      <h1 className="inc-title">{t.name} <SourceBadge t={t} /> <StateChip state={t.state} /></h1>
      <p className="inc-sub">Heart rate (left) and estimated core with its ± 0.6 °C band (right). Background shows the state; the strip shows the heat flag.</p>
      {data.length < 2 ? <p>The chart appears after two closed minutes.</p> : (
        <div className="chart">
          <ResponsiveContainer width="100%" height={380}>
            <ComposedChart data={data} margin={{ top: 8, right: 8, bottom: 8, left: 0 }}>
              <CartesianGrid stroke="#dfe4e1" vertical={false} />
              {segments.map((s, i) => (
                <ReferenceArea key={i} yAxisId="hr" x1={s.from} x2={s.to} fill={STATE_COLOUR[s.state] ?? '#999'} fillOpacity={0.08} />
              ))}
              {incidents.map((i) => <ReferenceLine key={i.incident_id} yAxisId="hr" x={i.opened_at} stroke="#b42318" strokeDasharray="4 3" label={{ value: 'Incident', fill: '#b42318', fontSize: 12 }} />)}
              <XAxis dataKey="t" type="number" scale="time" domain={['dataMin', 'dataMax']} tickFormatter={hhmm} />
              <YAxis yAxisId="hr" domain={[50, 200]} label={{ value: 'bpm', angle: -90, position: 'insideLeft' }} />
              <YAxis yAxisId="core" orientation="right" domain={[36.5, 40]} label={{ value: '°C', angle: 90, position: 'insideRight' }} />
              <Tooltip labelFormatter={(v) => hhmm(Number(v))} />
              <Area yAxisId="core" dataKey="band" stroke="none" fill="#1d5fa8" fillOpacity={0.15} name="Core ± 0.6 °C" />
              <Line yAxisId="core" dataKey="core" stroke="#1d5fa8" dot={false} strokeWidth={2} name="Est. core (°C)" connectNulls={false} />
              <Line yAxisId="hr" dataKey="hr" stroke="#17252A" dot={false} strokeWidth={1.5} name="Heart rate (bpm)" connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
          <div className="flagstrip" aria-label="Heat flag by minute">
            {data.map((d) => <span key={d.t} title={`${hhmm(d.t)} ${d.flag} flag`} style={{ background: FLAG_COLOUR[d.flag] ?? '#ccc' }} />)}
          </div>
        </div>
      )}
    </main>
  );
}
