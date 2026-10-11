"""Ingest request validation and response building (spec §5.1). Hand-written; no jsonschema at runtime."""
from __future__ import annotations

import re

from wristheat import engine, strain
from wristheat.advice import advice_for
from wristheat.engine import EngineState
from wristheat.envctx import Env

SESSION_RE = re.compile(r"^[A-Za-z0-9-]{8,64}$")
SOURCES = ("live", "simulated", "replay")
TOP_KEYS = {"schema", "trainee_id", "session_id", "source", "device", "replay_of", "samples"}
MAX_SAMPLES = 600
MIN_T = 1_700_000_000_000
BPM_MIN, BPM_MAX = 30, 230
FUTURE_MS = 60_000
LIVE_MAX_AGE_MS = 6 * 3600_000
CORE_BAND_C = 0.6


class RequestError(Exception):
    def __init__(self, status: int, code: str, message: str = ""):
        super().__init__(message or code)
        self.status, self.code, self.message = status, code, message or code


def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _bad(msg: str) -> RequestError:
    return RequestError(400, "bad_request", msg)


def validate_request(body: dict, now_ms: int) -> tuple[dict, list[tuple[int, int]], int]:
    if not isinstance(body, dict):
        raise _bad("body must be a JSON object")
    missing = {"schema", "trainee_id", "session_id", "source", "device", "samples"} - body.keys()
    if missing:
        raise _bad(f"missing fields: {sorted(missing)}")
    if body.keys() - TOP_KEYS:
        raise _bad(f"unknown fields: {sorted(body.keys() - TOP_KEYS)}")
    if body["schema"] != 1 or not _is_int(body["schema"]):
        raise _bad("schema must be 1")
    tid = body["trainee_id"]
    if not isinstance(tid, str) or not 1 <= len(tid) <= 32:
        raise _bad("trainee_id must be 1–32 chars")
    sid = body["session_id"]
    if not isinstance(sid, str) or not SESSION_RE.match(sid):
        raise _bad("session_id must match [A-Za-z0-9-]{8,64}")
    source = body["source"]
    if source not in SOURCES:
        raise _bad("source must be live, simulated or replay")
    device = body["device"]
    if not isinstance(device, str) or len(device) > 40:
        raise _bad("device must be ≤ 40 chars")
    replay_of = body.get("replay_of")
    if replay_of is not None and (not isinstance(replay_of, str) or len(replay_of) > 64):
        raise _bad("replay_of must be a string ≤ 64 chars")
    if source == "replay" and not replay_of:
        raise _bad("replay_of is required when source is replay")
    samples = body["samples"]
    if not isinstance(samples, list) or len(samples) > MAX_SAMPLES:
        raise _bad(f"samples must be a list of at most {MAX_SAMPLES}")

    accepted: list[tuple[int, int]] = []
    dropped = 0
    for s in samples:
        if not isinstance(s, dict) or set(s) != {"t", "bpm"} or not _is_int(s["t"]) or not _is_int(s["bpm"]):
            raise _bad("each sample must be {t: int, bpm: int}")
        t, bpm = s["t"], s["bpm"]
        if t < MIN_T:
            raise _bad("sample t must be epoch milliseconds")
        too_old = source == "live" and t < now_ms - LIVE_MAX_AGE_MS
        if not BPM_MIN <= bpm <= BPM_MAX or t > now_ms + FUTURE_MS or too_old:
            dropped += 1
            continue
        accepted.append((t, bpm))
    accepted.sort()
    meta = {"schema": 1, "trainee_id": tid, "session_id": sid, "source": source, "device": device,
            "replay_of": replay_of}
    return meta, accepted, dropped


def env_payload(env: Env | None, now_ms: int) -> dict | None:
    if env is None:
        return None
    return {"wbgt_c": env.wbgt_c, "flag": env.flag, "pm25": env.pm25,
            "us_aqi": int(env.us_aqi) if env.us_aqi is not None else None,
            "updated_at": int(env.updated_at), "stale": strain.is_stale(env, now_ms)}


def build_response(trainee_id: str, session_id: str, accepted: int, dropped: int, st: EngineState,
                   env: Env | None, incident_id: str | None, now_ms: int) -> dict:
    calibrated = st.hr0 is not None and st.state != "CALIBRATING"
    alert = st.pending_alert
    return {
        "schema": 1,
        "trainee_id": trainee_id,
        "session_id": session_id,
        "accepted": accepted,
        "dropped": dropped,
        "state": st.state,
        "state_since": int(st.state_since),
        "calibration_remaining_s": engine.calibration_remaining_s(st, now_ms),
        "hr_now": st.hr_now,
        "hr0": st.hr0 if calibrated else None,
        "core_est_c": round(st.ct, 2) if calibrated else None,
        "core_band_c": CORE_BAND_C,
        "psi": round(st.psi, 1) if (calibrated and st.psi is not None) else None,
        "minutes_to_red": st.minutes_to_red,
        "env": env_payload(env, now_ms),
        "advice": advice_for(st.state, env.pm25 if env else None, alert),
        "alert": alert,
        "incident_id": incident_id,
        "server_time": now_ms,
    }
