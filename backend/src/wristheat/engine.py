"""Risk engine: minute aggregation, calibration and the state machine (spec §7.1, §7.4, §7.5).

Pure Python, no AWS imports. Events carry the epoch minute index (t // 60000).
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field

from wristheat import ectemp, strain
from wristheat.envctx import Env

GAP_N = 10
CALIBRATION_MINUTES = 2
HISTORY_LEN = 4
RANK = {"GREEN": 0, "AMBER": 1, "RED": 2, "RECOVERING": 1}


@dataclass
class EngineState:
    started_at: int
    first_minute: int | None = None
    last_t: int | None = None
    ct: float = ectemp.CT0
    v: float = ectemp.V0
    open_minute: int | None = None
    open_sum: float = 0.0
    open_n: int = 0
    calib_means: list[float] = field(default_factory=list)
    hr0: int | None = None
    rest_hr_override: int | None = None
    state: str = "CALIBRATING"
    state_since: int = 0
    history: list[dict] = field(default_factory=list)
    pending_alert: str = "NONE"
    hr_now: int | None = None
    psi: float | None = None
    minutes_to_red: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "EngineState":
        d = dict(d)
        d["calib_means"] = [float(x) for x in d.get("calib_means", [])]
        d["history"] = [dict(h) for h in d.get("history", [])]
        for k in ("ct", "v", "open_sum"):
            d[k] = float(d[k])
        if d.get("psi") is not None:
            d["psi"] = float(d["psi"])
        for k in ("started_at", "first_minute", "last_t", "open_minute", "open_n", "hr0",
                  "rest_hr_override", "state_since", "hr_now", "minutes_to_red"):
            if d.get(k) is not None:
                d[k] = int(d[k])
        known = cls.__dataclass_fields__
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class MinuteRow:
    minute: int
    hr: float | None
    n: int
    core_est_c: float
    core_var: float
    psi: float | None
    level: str | None
    state: str
    wbgt_c: float | None
    flag: str
    pm25: float | None


@dataclass
class EngineResult:
    state: EngineState
    minutes: list[MinuteRow]
    events: list[tuple[int, str]]


def new_state(started_at_ms: int, rest_hr_override: int | None) -> EngineState:
    st = EngineState(started_at=started_at_ms, state_since=started_at_ms, rest_hr_override=rest_hr_override)
    if rest_hr_override is not None:
        st.hr0 = int(rest_hr_override)
        st.state = "GREEN"
    return st


def calibration_remaining_s(state: EngineState, now_ms: int) -> int:
    if state.hr0 is not None:
        return 0
    if state.first_minute is None:
        return CALIBRATION_MINUTES * 60
    remaining = math.ceil(((state.first_minute + CALIBRATION_MINUTES) * 60_000 - now_ms) / 1000)
    return max(0, min(CALIBRATION_MINUTES * 60, remaining))


def apply_samples(state: EngineState, samples: list[tuple[int, int]], env: Env | None, now_ms: int) -> EngineResult:
    st = EngineState.from_dict(state.to_dict())  # never mutate the caller's copy
    flag = strain.effective_flag(env, now_ms)
    stale = strain.is_stale(env, now_ms)
    rows: list[MinuteRow] = []
    events: list[tuple[int, str]] = []
    new_bpm: list[int] = []

    for t, bpm in sorted(samples):
        if st.last_t is not None and t <= st.last_t:
            continue
        st.last_t = t
        new_bpm.append(bpm)
        m = t // 60_000
        if st.first_minute is None:
            st.first_minute = m
        if st.open_minute is None:
            st.open_minute, st.open_sum, st.open_n = m, 0.0, 0
        elif m > st.open_minute:
            _close_minute(st, flag, env, stale, rows, events)
            st.open_minute, st.open_sum, st.open_n = m, 0.0, 0
        st.open_sum += bpm
        st.open_n += 1

    if new_bpm:
        st.hr_now = round(sum(new_bpm) / len(new_bpm))
    st.minutes_to_red = _minutes_to_red(st, flag)
    return EngineResult(state=st, minutes=rows, events=events)


def _close_minute(st: EngineState, flag: str, env: Env | None, stale: bool,
                  rows: list[MinuteRow], events: list[tuple[int, str]]) -> None:
    m, n = st.open_minute, st.open_n
    wbgt = None if (env is None or stale) else env.wbgt_c
    pm25 = None if (env is None or stale) else env.pm25
    if n < GAP_N:
        rows.append(MinuteRow(m, None, n, st.ct, st.v, None, None, st.state, wbgt, flag, pm25))
        return

    hr = st.open_sum / n
    st.ct, st.v = ectemp.step(st.ct, st.v, hr)

    if st.hr0 is None:
        st.calib_means.append(hr)
        if len(st.calib_means) >= CALIBRATION_MINUTES:
            st.hr0 = int(round(min(100.0, max(45.0, min(st.calib_means)))))
            _transition(st, "GREEN", m, events, "CALIBRATED", alert=None)
        rows.append(MinuteRow(m, hr, n, st.ct, st.v, None, None, st.state, wbgt, flag, pm25))
        return

    p = strain.psi(st.ct, hr, st.hr0)
    level = strain.candidate_level(p, st.ct, flag)
    st.psi = p
    st.history = (st.history + [{"minute": m, "level": level, "hr": hr, "psi": p, "ct": st.ct}])[-HISTORY_LEN:]
    _evaluate(st, m, events)
    rows.append(MinuteRow(m, hr, n, st.ct, st.v, p, level, st.state, wbgt, flag, pm25))


def _evaluate(st: EngineState, m: int, events: list[tuple[int, str]]) -> None:
    last2 = st.history[-2:]
    rank = RANK[st.state]
    # Rule 2: escalate (RED before AMBER) — takes priority over everything else.
    if len(last2) == 2:
        for target in ("RED", "AMBER"):
            if rank < RANK[target] and all(RANK[h["level"]] >= RANK[target] for h in last2):
                _transition(st, target, m, events, f"{target}_ENTERED", alert=target)
                return
    # Rule 3: de-escalate to RECOVERING (no alert).
    if st.state in ("AMBER", "RED") and len(last2) == 2 and all(RANK[h["level"]] < RANK[st.state] for h in last2):
        _transition(st, "RECOVERING", m, events, "RECOVERING_ENTERED", alert=None)
        return
    # Rule 4: confirm recovery from the data.
    if st.state == "RECOVERING" and len(st.history) >= 4:
        last3 = st.history[-3:]
        ok = all(h["level"] == "GREEN" and h["hr"] <= st.hr0 + 30 and h["psi"] < 4.0 for h in last3)
        if ok and st.history[-1]["ct"] <= st.history[-4]["ct"]:
            _transition(st, "GREEN", m, events, "RECOVERY_CONFIRMED", alert="RECOVERED")


def _transition(st: EngineState, new_state_name: str, m: int, events: list, event: str, alert: str | None) -> None:
    st.state = new_state_name
    st.state_since = (m + 1) * 60_000
    events.append((m, event))
    if alert is not None:
        st.pending_alert = alert


def _minutes_to_red(st: EngineState, flag: str) -> int | None:
    if st.hr0 is None or st.state not in ("GREEN", "AMBER", "RECOVERING") or not st.history:
        return None
    recent = st.history[-3:]
    hr_mean = sum(h["hr"] for h in recent) / len(recent)
    if hr_mean < st.hr0 + 20:
        return None
    return strain.project_minutes_to_red(st.ct, st.v, hr_mean, st.hr0, flag)
