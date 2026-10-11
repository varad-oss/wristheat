/** Physiological Strain Index 0–10 with the published band edges at 5 and 7. */
export function PsiBar({ psi }: { psi: number | null }) {
  const pct = psi === null ? 0 : Math.max(0, Math.min(10, psi)) * 10;
  const band = psi === null ? 'none' : psi >= 7 ? 'high' : psi >= 5 ? 'moderate' : 'low';
  return (
    <div className="psi">
      <div className="psi-head">
        <span>Strain index</span>
        <strong className="num">{psi === null ? '–' : psi.toFixed(1)}</strong>
        <span className="psi-band">{psi === null ? '' : band}</span>
      </div>
      <div className="psi-track" role="meter" aria-label="Strain index" aria-valuemin={0} aria-valuemax={10}
           aria-valuenow={psi ?? undefined}>
        <div className={`psi-fill psi-${band}`} style={{ width: `${pct}%` }} />
        <span className="psi-tick" style={{ left: '50%' }} />
        <span className="psi-tick" style={{ left: '70%' }} />
      </div>
    </div>
  );
}
