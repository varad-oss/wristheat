import pytest

from wristheat import ectemp, strain
from wristheat.envctx import Env


def test_psi_formula():
    assert strain.psi(38.3, 150, 75) == pytest.approx(5 * (1.2 / 2.4) + 5 * (75 / 105), abs=1e-4)


def test_psi_clamped():
    assert strain.psi(36.0, 60, 75) == 0.0
    assert strain.psi(41.0, 200, 75) == 10.0


@pytest.mark.parametrize("wbgt,flag", [
    (25.5, "NONE"), (25.6, "WHITE"), (27.7, "WHITE"), (27.8, "GREEN"), (29.4, "GREEN"),
    (29.5, "YELLOW"), (31.0, "YELLOW"), (31.1, "RED"), (32.1, "RED"), (32.2, "BLACK"),
    (None, "NONE"), (31.04, "YELLOW"),
])
def test_flag_boundaries(wbgt, flag):
    assert strain.flag_for_wbgt(wbgt) == flag


@pytest.mark.parametrize("p,ct,flag,level", [
    (7.0, 38.0, "NONE", "RED"),
    (3.0, 39.0, "NONE", "RED"),
    (6.0, 38.0, "RED", "RED"),
    (6.0, 38.0, "YELLOW", "AMBER"),
    (5.0, 37.5, "NONE", "AMBER"),
    (4.0, 37.5, "YELLOW", "AMBER"),
    (4.0, 37.5, "GREEN", "GREEN"),
    (4.99, 37.5, "NONE", "GREEN"),
])
def test_candidate_levels(p, ct, flag, level):
    assert strain.candidate_level(p, ct, flag) == level


def test_projection_vectors():
    ct, v = ectemp.run([75, 75, 165])[-1]
    assert strain.project_minutes_to_red(ct, v, 165, 75, "RED") == 8
    assert strain.project_minutes_to_red(ct, v, 165, 75, "YELLOW") == 18


def test_projection_none_when_never_red():
    ct, v = ectemp.run([75, 75, 90])[-1]
    assert strain.project_minutes_to_red(ct, v, 90, 75, "NONE") is None


def test_stale_env_treated_as_none():
    now = 1_791_700_000_000
    stale = Env(wbgt_c=31.5, flag="RED", pm25=40.0, us_aqi=100, updated_at=now - 46 * 60_000)
    fresh = Env(wbgt_c=31.5, flag="RED", pm25=40.0, us_aqi=100, updated_at=now - 44 * 60_000)
    assert strain.effective_flag(stale, now) == "NONE"
    assert strain.effective_flag(fresh, now) == "RED"
    assert strain.effective_flag(None, now) == "NONE"
    assert strain.effective_flag(Env(None, "RED", None, None, now), now) == "NONE"
