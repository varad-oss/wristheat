"""Offline end-to-end: the S3 escalation scenario through the real ingest pipeline (FakeRepo)."""
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "backend" / "src"))
sys.path.insert(0, str(HERE.parents[1] / "backend" / "tests"))
import common  # noqa: E402
import simulate  # noqa: E402
from fakes import FakeClients  # noqa: E402
from wristheat.envctx import Env  # noqa: E402
from wristheat.handlers import ingest  # noqa: E402
from wristheat.repo import FakeRepo  # noqa: E402

TOKEN = "tok"
START = 1_791_700_000_000


def run(flag="YELLOW", backfill_min=18, surge_after=30, live_min=20, recover_min=15):
    repo = FakeRepo()
    repo.trainees["S3"] = {"trainee_id": "S3", "name": "Kabir", "kind": "simulated", "site_id": "kgp",
                           "rest_hr_override": 76}
    deps = ingest.Deps(repo, FakeClients(TOKEN), "arn:sm",
                       lambda s, now: Env(wbgt_c=31.0, flag=flag, pm25=51.0, us_aqi=158, updated_at=now))
    rng, sid, timeline = random.Random(7), "sim-S3-abcdef123456", []

    def post(samples, now):
        status, r = ingest.process_ingest(common.make_payload("S3", sid, "simulated", samples),
                                          {"x-device-token": TOKEN}, deps, now)
        assert status == 200, r
        if r["alert"] != "NONE":
            timeline.append(((now - START) / 60000, r["alert"]))

    for chunk in simulate.backfill_batches("atrisk", START, backfill_min, surge_after, rng):
        post(chunk, START)
    t = START
    for profile, minutes in (("atrisk", live_min), ("easy96", recover_min)):
        for _ in range(minutes * 12):
            samples = [(t + k * 1000, simulate.profile_hr(profile, (t + k * 1000 - START) / 1000, surge_after, rng))
                       for k in range(1, 6)]
            t += 5000
            post(samples, t)
    return timeline, deps


def test_s3_reaches_red_then_recovers_under_yellow_flag():
    timeline, deps = run()
    alerts = [a for _, a in timeline]
    assert "RED" in alerts and alerts.index("RED") < alerts.index("RECOVERED")
    assert len(deps.clients.sfn.ops("start_execution")) == 1
    print("\nS3 timeline (min since live start):", [(round(m, 1), a) for m, a in timeline])
