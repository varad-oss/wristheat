#!/usr/bin/env python3
"""Re-streams a recorded real session as trainee R1 with a REPLAY badge (spec §12).

    python simulator/replay.py --fixture fixtures/<file>.json --as R1 [--api URL --token TOKEN] [--speed 1.0]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import make_payload, post_batch, resolve_api_and_token  # noqa: E402


def shift_samples(samples, end_ms: int, speed: float = 1.0) -> list[tuple[int, int]]:
    """Moves samples so the last one lands at end_ms; spacing is divided by speed."""
    if not samples:
        return []
    last = samples[-1][0]
    return [(int(round(end_ms - (last - t) / speed)), b) for t, b in samples]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--as", dest="as_tid", default="R1")
    ap.add_argument("--api")
    ap.add_argument("--token")
    ap.add_argument("--speed", type=float, default=1.0)
    args = ap.parse_args(argv)
    api, token = resolve_api_and_token(args.api, args.token)
    fx = json.loads(pathlib.Path(args.fixture).read_text())
    samples = [(int(t), int(b)) for t, b in fx["samples"]]
    original = fx["meta"]["session_id"]
    sid = f"replay-{uuid.uuid4().hex[:12]}"
    span = (samples[-1][0] - samples[0][0]) / args.speed
    end_ms = int(time.time() * 1000 + span)
    shifted = shift_samples(samples, end_ms, args.speed)
    print(f"{args.as_tid} [REPLAY of {original}] session={sid} samples={len(shifted)} ~{span / 60000:.1f} min")
    i = 0
    while i < len(shifted):
        now = int(time.time() * 1000)
        batch = []
        while i < len(shifted) and shifted[i][0] <= now and len(batch) < 600:
            batch.append(shifted[i])
            i += 1
        if batch:
            r = post_batch(api, token, make_payload(args.as_tid, sid, "replay", batch, replay_of=original))
            print(f"{time.strftime('%H:%M:%S')} {r['state']:<11} hr={r['hr_now']} psi={r['psi']} alert={r['alert']}")
        time.sleep(5)
    print("replay finished")


if __name__ == "__main__":
    main()
