#!/usr/bin/env python3
"""Streams labelled SIMULATED trainees S1–S4 at 1 Hz, one batch every 5 s (spec §12).

    python simulator/simulate.py [--api URL --token TOKEN] [--backfill-minutes 20] [--surge-after 120]
                                 [--only S3] [--profile atrisk|steady138|steady124|easy96] [--seed 7]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
import time
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import make_payload, post_batch, resolve_api_and_token  # noqa: E402

STATE_FILE = pathlib.Path(__file__).resolve().parent / ".state.json"
CONTINUE_MS = 10 * 60_000
DEFAULT_PROFILES = {"S1": "steady138", "S2": "steady124", "S3": "atrisk", "S4": "easy96"}
TARGET_SD = {"steady138": (138, 2.0), "steady124": (124, 2.0), "easy96": (96, 1.5), "atrisk": (150, 2.0)}
SURGE_TO, SURGE_S = 182, 6 * 60


def profile_hr(profile: str, t_s: float, surge_after_s: float | None, rng: random.Random) -> int:
    """Heart rate for a simulated trainee at t_s seconds since the simulation started."""
    target, sd = TARGET_SD[profile]
    if profile == "atrisk" and surge_after_s is not None and t_s > surge_after_s:
        target += (SURGE_TO - target) * min(1.0, (t_s - surge_after_s) / SURGE_S)
    noise = max(-10.0, min(10.0, rng.gauss(0, sd)))
    return int(round(target + noise))


def _load_state(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def session_for(tid: str, now_ms: int, path: pathlib.Path = STATE_FILE) -> str:
    """Continues the trainee's session if it was written in the last 10 min, else starts a new one."""
    entry = _load_state(path).get(tid)
    if entry and now_ms - entry["last_write_ms"] <= CONTINUE_MS:
        return entry["session_id"]
    return f"sim-{tid}-{uuid.uuid4().hex[:12]}"


def remember(tid: str, sid: str, now_ms: int, path: pathlib.Path = STATE_FILE) -> None:
    state = _load_state(path)
    state[tid] = {"session_id": sid, "last_write_ms": now_ms}
    path.write_text(json.dumps(state, indent=2))


def backfill_batches(profile: str, start_ms: int, minutes: int, surge_after_s, rng, batch: int = 300):
    """Past samples from start_ms - minutes to start_ms (exclusive), in batches of 300."""
    samples = []
    for k in range(minutes * 60, 0, -1):
        t = start_ms - k * 1000
        samples.append((t, profile_hr(profile, -k, surge_after_s, rng)))
    for i in range(0, len(samples), batch):
        yield samples[i:i + batch]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api")
    ap.add_argument("--token")
    ap.add_argument("--backfill-minutes", type=int, default=0)
    ap.add_argument("--surge-after", type=float, default=None, help="seconds after start before S3 surges")
    ap.add_argument("--only", help="simulate one trainee, e.g. S3")
    ap.add_argument("--profile", choices=list(TARGET_SD), help="override the --only trainee's profile")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--duration", type=float, default=None, help="stop after N seconds (default: run forever)")
    args = ap.parse_args(argv)
    api, token = resolve_api_and_token(args.api, args.token)
    rng = random.Random(args.seed)
    profiles = dict(DEFAULT_PROFILES)
    if args.only:
        profiles = {args.only: args.profile or DEFAULT_PROFILES.get(args.only, "steady124")}
    start_ms = int(time.time() * 1000)
    sessions = {tid: session_for(tid, start_ms) for tid in profiles}
    last_t = {tid: start_ms - 1000 for tid in profiles}

    for tid, profile in profiles.items():
        print(f"{tid} [SIMULATED] profile={profile} session={sessions[tid]}")
        if args.backfill_minutes:
            for chunk in backfill_batches(profile, start_ms, args.backfill_minutes, args.surge_after, rng):
                r = post_batch(api, token, make_payload(tid, sessions[tid], "simulated", chunk))
                print(f"  backfill {tid}: {r['state']} hr={r['hr_now']} psi={r['psi']} alert={r['alert']}")
        remember(tid, sessions[tid], int(time.time() * 1000))

    try:
        while args.duration is None or time.time() * 1000 - start_ms < args.duration * 1000:
            time.sleep(5)
            now = int(time.time() * 1000)
            for tid, profile in profiles.items():
                ts = list(range(last_t[tid] + 1000, now + 1, 1000))
                if not ts:
                    continue
                samples = [(t, profile_hr(profile, (t - start_ms) / 1000, args.surge_after, rng)) for t in ts]
                last_t[tid] = ts[-1]
                try:
                    r = post_batch(api, token, make_payload(tid, sessions[tid], "simulated", samples))
                    flag = f" ALERT={r['alert']}" if r["alert"] != "NONE" else ""
                    print(f"{time.strftime('%H:%M:%S')} {tid} {r['state']:<11} hr={r['hr_now']} "
                          f"psi={r['psi']} core={r['core_est_c']} mtr={r['minutes_to_red']}{flag}")
                    remember(tid, sessions[tid], now)
                except Exception as e:  # noqa: BLE001 — keep streaming through transient errors
                    print(f"{tid} post failed: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        print("stopped")


if __name__ == "__main__":
    main()
