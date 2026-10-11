import json

from conftest import REPO
from wristheat import obs
from wristheat.handlers import context
from wristheat.repo import FakeRepo

FIX = REPO / "backend" / "tests" / "fixtures"
FC = json.loads((FIX / "openmeteo_forecast.json").read_text())
AIR = json.loads((FIX / "openmeteo_air.json").read_text())
SITE = {"site_id": "kgp", "name": "IIT Kharagpur campus", "lat": 22.3149, "lon": 87.3105}


def fetch_ok(url):
    return AIR if "air-quality" in url else FC


def fetch_fail(url):
    raise OSError("network down")


def test_refresh_writes_env_forecast_and_coolest_hour():
    repo = FakeRepo()
    repo.put_site(dict(SITE))
    env = context.refresh_site(repo, "kgp", 1_791_700_000_000, fetch_ok)
    site = repo.get_site("kgp")
    assert site["env"]["wbgt_c"] == env["wbgt_c"] and site["env"]["updated_at"] == 1_791_700_000_000
    assert len(site["forecast"]) == 24 and "local" in site["coolest_hour"]
    assert site["name"] == "IIT Kharagpur campus"


def test_context_failure_keeps_previous_env():
    repo = FakeRepo()
    prev = {"wbgt_c": 30.0, "flag": "YELLOW", "pm25": 40.0, "us_aqi": 100, "updated_at": 5}
    repo.put_site({**SITE, "env": prev})
    obs.RECORDED.clear()
    env = context.refresh_site(repo, "kgp", 1_791_700_000_000, fetch_fail)
    assert repo.get_site("kgp")["env"] == prev
    assert env == prev
    assert "ContextFetchErrors" in [m[0] for m in obs.RECORDED]


def test_unexpected_shape_counts_as_failure():
    repo = FakeRepo()
    repo.put_site(dict(SITE))
    obs.RECORDED.clear()
    context.refresh_site(repo, "kgp", 1, lambda url: {"error": True, "reason": "bad variable"})
    assert "env" not in repo.get_site("kgp")
    assert "ContextFetchErrors" in [m[0] for m in obs.RECORDED]
