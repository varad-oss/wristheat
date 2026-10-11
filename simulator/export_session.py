#!/usr/bin/env python3
"""Exports a recorded session's readings to fixtures/ for replay (spec §12).

    python simulator/export_session.py --session SID [--outputs infra/outputs.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "backend" / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, stack_outputs  # noqa: E402


def main(argv=None):
    from wristheat.repo import DynamoRepo
    import boto3
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--session", required=True)
    ap.add_argument("--outputs")
    args = ap.parse_args(argv)
    out = stack_outputs(args.outputs)
    repo = DynamoRepo({"sessions": out["TableSessions"], "readings": out["TableReadings"]},
                      resource=boto3.resource("dynamodb", region_name="ap-south-1"))
    s = repo.get_session(args.session)
    if not s:
        sys.exit(f"unknown session {args.session}")
    samples = repo.get_readings(args.session)
    stamp = time.strftime("%Y%m%d-%H%M", time.localtime(s["started_at"] / 1000))
    path = ROOT / "fixtures" / f"{stamp}-{s['trainee_id']}-{args.session[:8]}.json"
    path.parent.mkdir(exist_ok=True)
    meta = {k: s.get(k) for k in ("session_id", "trainee_id", "device", "started_at", "source")}
    path.write_text(json.dumps({"meta": meta, "samples": [[t, b] for t, b in samples]}))
    print(f"wrote {path} ({len(samples)} samples)")


if __name__ == "__main__":
    main()
