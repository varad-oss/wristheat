import pytest

from wristheat import engine
from wristheat.envctx import Env

T0 = 29_861_000 * 60_000  # minute-aligned start


def minutes_to_samples(minute_hrs, start_ms=T0):
    """60 samples at 1 Hz per minute; None → 5 samples (a gap); plus one closing sample."""
    out = []
    for i, hr in enumerate(minute_hrs):
        base = start_ms + i * 60_000
        n = 5 if hr is None else 60
        out += [(base + k * 1000, hr if hr is not None else 80) for k in range(n)]
    out.append((start_ms + len(minute_hrs) * 60_000, 80))
    return out


def env_with(flag):
    return Env(wbgt_c=31.5, flag=flag, pm25=30.0, us_aqi=90, updated_at=T0 + 60 * 60_000)


def feed(minute_hrs, flag, batch=None, override=None):
    st = engine.new_state(T0, override)
    samples = minutes_to_samples(minute_hrs)
    events, results = [], []
    chunks = [samples] if batch is None else [samples[i:i + batch] for i in range(0, len(samples), batch)]
    for chunk in chunks:
        res = engine.apply_samples(st, chunk, env_with(flag), chunk[-1][0])
        st = res.state
        events += res.events
        results.append(res)
    first = T0 // 60_000
    rel = [(m - first + 1, e) for m, e in events]
    return st, rel, results


D_BASE = [75, 75] + [165] * 20 + [100] * 10
VECTORS = {
    "D1": (D_BASE, "RED", [(4, "AMBER_ENTERED"), (12, "RED_ENTERED"), (24, "RECOVERING_ENTERED"), (25, "RECOVERY_CONFIRMED")]),
    "D2": (D_BASE, "YELLOW", [(4, "AMBER_ENTERED"), (22, "RED_ENTERED"), (24, "RECOVERING_ENTERED"), (25, "RECOVERY_CONFIRMED")]),
    "D3": (D_BASE, "NONE", [(6, "AMBER_ENTERED"), (22, "RED_ENTERED"), (24, "RECOVERING_ENTERED"), (25, "RECOVERY_CONFIRMED")]),
    "D4": ([75, 75] + [165] * 14 + [140, 120, 110, 104, 100, 98, 96, 95, 94, 93], "RED",
           [(4, "AMBER_ENTERED"), (12, "RED_ENTERED"), (18, "RECOVERING_ENTERED"), (22, "RECOVERY_CONFIRMED")]),
    "D5": ([75, None, 75] + [165, None, 165, 165] + [165] * 8, "RED", [(6, "AMBER_ENTERED"), (14, "RED_ENTERED")]),
}


@pytest.mark.parametrize("batch", [None, 5], ids=["one_call", "batches_of_5"])
@pytest.mark.parametrize("vid", list(VECTORS))
def test_reference_vectors(vid, batch):
    hrs, flag, expected = VECTORS[vid]
    _, events, _ = feed(hrs, flag, batch)
    assert [e for e in events if e[1] != "CALIBRATED"] == expected
    cal = [m for m, e in events if e == "CALIBRATED"]
    assert cal == [3 if vid == "D5" else 2]


def test_minutes_to_red_after_minute_3():
    for flag, expected in [("RED", 8), ("YELLOW", 18)]:
        st, _, _ = feed([75, 75, 165], flag)
        assert st.minutes_to_red == expected


def test_calibration_clamp():
    st, _, _ = feed([110, 120], "NONE")
    assert st.hr0 == 100
    st, _, _ = feed([40, 42], "NONE")
    assert st.hr0 == 45


def test_override_skips_calibration():
    st = engine.new_state(T0, 80)
    assert st.state == "GREEN" and st.hr0 == 80
    _, events, _ = feed([80, 80, 80], "NONE", override=80)
    assert "CALIBRATED" not in [e for _, e in events]


def test_duplicate_samples_ignored():
    st = engine.new_state(T0, 75)
    batch = [(T0 + k * 1000, 90) for k in range(60)]
    st = engine.apply_samples(st, batch, None, T0 + 60_000).state
    open_n, last_t = st.open_n, st.last_t
    res = engine.apply_samples(st, batch, None, T0 + 61_000)
    assert res.minutes == [] and res.events == []
    assert res.state.open_n == open_n and res.state.last_t == last_t


def test_flush_closes_many_minutes_and_keeps_last_alert():
    st = engine.new_state(T0, None)
    env = env_with("RED")
    st = engine.apply_samples(st, minutes_to_samples([75, 75])[:-1], env, T0 + 120_000).state
    start = T0 + 120_000
    flush = [(start + k * 1000, 165) for k in range(600)]
    res = engine.apply_samples(st, flush, env, flush[-1][0])
    names = [e for _, e in res.events]
    assert "CALIBRATED" in names and "AMBER_ENTERED" in names
    assert res.state.pending_alert == "AMBER"
    more = [(start + 600_000 + k * 1000, 165) for k in range(300)]
    res2 = engine.apply_samples(res.state, more, env, more[-1][0])
    assert "RED_ENTERED" in [e for _, e in res2.events]
    assert res2.state.pending_alert == "RED"


def test_calibration_remaining():
    st = engine.new_state(T0, None)
    st = engine.apply_samples(st, [(T0, 70)], None, T0).state
    assert engine.calibration_remaining_s(st, T0 + 30_000) == 90
    st, _, _ = feed([75, 75], "NONE")
    assert engine.calibration_remaining_s(st, T0 + 999_999) == 0


def test_gap_minute_does_not_update_filter():
    st = engine.new_state(T0, 75)
    st = engine.apply_samples(st, minutes_to_samples([120])[:-1], None, T0).state
    st = engine.apply_samples(st, [(T0 + 60_000, 120)], None, T0).state  # closes minute 1
    ct, v = st.ct, st.v
    gap = [(T0 + 60_000 + k * 1000, 120) for k in range(1, 5)] + [(T0 + 120_000, 120)]
    res = engine.apply_samples(st, gap, None, T0)
    assert res.minutes[-1].hr is None
    assert (res.state.ct, res.state.v) == (ct, v)


def test_state_roundtrip():
    st, _, _ = feed(D_BASE[:6], "RED")
    again = engine.EngineState.from_dict(st.to_dict())
    assert again == st


def test_hr_now_is_mean_of_new_samples():
    st = engine.new_state(T0, 75)
    res = engine.apply_samples(st, [(T0, 100), (T0 + 1000, 103)], None, T0)
    assert res.state.hr_now == 102
