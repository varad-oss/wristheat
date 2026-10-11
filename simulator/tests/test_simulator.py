import json
import pathlib
import random
import sys

import jsonschema
import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import common  # noqa: E402
import replay  # noqa: E402
import simulate  # noqa: E402

REQ_SCHEMA = json.loads((HERE.parents[1] / "contracts" / "ingest_request.schema.json").read_text(encoding="utf-8"))
TARGETS = {"steady138": 138, "steady124": 124, "atrisk": 150, "easy96": 96}


@pytest.mark.parametrize("profile", list(TARGETS))
def test_profile_ranges(profile):
    rng = random.Random(7)
    draws = [simulate.profile_hr(profile, t, None, rng) for t in range(1000)]
    assert all(abs(d - TARGETS[profile]) <= 12 for d in draws)
    assert abs(sum(draws) / len(draws) - TARGETS[profile]) < 1.5


def test_atrisk_surge_reaches_180():
    rng = random.Random(7)
    surge = 120
    at = surge + 6 * 60
    draws = [simulate.profile_hr("atrisk", at + k, surge, rng) for k in range(60)]
    assert sum(draws) / 60 >= 178
    before = [simulate.profile_hr("atrisk", surge - 10, surge, rng) for _ in range(60)]
    assert abs(sum(before) / 60 - 150) < 2


def test_replay_shifts_timestamps():
    samples = [(1_791_000_000_000 + k * 1000, 90 + k % 5) for k in range(120)]
    now = 1_791_700_000_000
    shifted = replay.shift_samples(samples, now)
    assert shifted[-1][0] == now
    assert [b[0] - a[0] for a, b in zip(shifted, shifted[1:])] == [1000] * 119
    assert [s[1] for s in shifted] == [s[1] for s in samples]
    payload = common.make_payload("R1", "replay-12345678", "replay", shifted[:5], replay_of="orig-12345678")
    assert payload["source"] == "replay" and payload["replay_of"] == "orig-12345678"
    jsonschema.validate(payload, REQ_SCHEMA)


def test_replay_speed_compresses_spacing():
    samples = [(1_791_000_000_000 + k * 1000, 90) for k in range(10)]
    shifted = replay.shift_samples(samples, 2_000_000_000_000, speed=2.0)
    assert shifted[-1][0] == 2_000_000_000_000 and shifted[1][0] - shifted[0][0] == 500


def test_payload_matches_contract():
    p = common.make_payload("S3", "sim-S3-1234abcd", "simulated", [(1_791_700_000_000, 150), (1_791_700_001_000, 151)])
    jsonschema.validate(p, REQ_SCHEMA)
    assert "replay_of" not in p


def test_session_continuation(tmp_path):
    state = tmp_path / "state.json"
    now = 1_791_700_000_000
    sid = simulate.session_for("S3", now, state)
    simulate.remember("S3", sid, now, state)
    assert simulate.session_for("S3", now + 9 * 60_000, state) == sid
    assert simulate.session_for("S3", now + 11 * 60_000, state) != sid


def test_backfill_batches():
    rng = random.Random(1)
    batches = list(simulate.backfill_batches("easy96", 1_791_700_000_000, minutes=10, surge_after_s=None, rng=rng))
    assert [len(b) for b in batches] == [300, 300]
    assert batches[-1][-1][0] < 1_791_700_000_000
