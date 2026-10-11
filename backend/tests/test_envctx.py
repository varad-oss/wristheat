import json
import re
from datetime import datetime, timezone

import pytest

from conftest import REPO
from wristheat import envctx
from wristheat.strain import FLAG_ORDER

FIX = REPO / "backend" / "tests" / "fixtures"


@pytest.mark.parametrize("hh,expected", [(0, 0.0870), (6, 0.8658), (12, -0.1751)])
def test_cossza_golden(hh, expected):
    when = datetime(2026, 10, 11, hh, 30, tzinfo=timezone.utc)
    assert envctx.cossza(22.3149, 87.3105, when) == pytest.approx(expected, abs=0.002)


def test_wbgt_golden_sun():
    assert envctx.wbgt_liljegren_c(31, 70, 1005, 2.0, 700, 490, 0.8) == pytest.approx(31.99, abs=0.05)


def test_wbgt_golden_night():
    assert envctx.wbgt_liljegren_c(31, 70, 1005, 2.0, 0, 0, -0.1) == pytest.approx(27.65, abs=0.05)


def test_wbgt_none_on_missing_input():
    assert envctx.wbgt_liljegren_c(None, 70, 1005, 2.0, 0, 0, -0.1) is None


def test_build_env_from_fixture():
    fc = json.loads((FIX / "openmeteo_forecast.json").read_text())
    air = json.loads((FIX / "openmeteo_air.json").read_text())
    now = 1_791_700_000_000
    env, forecast, coolest = envctx.build_env(fc, air, 22.3149, 87.3105, now)
    assert env.flag in FLAG_ORDER and env.wbgt_c is not None
    assert env.pm25 == air["current"]["pm2_5"] and env.us_aqi == air["current"]["us_aqi"]
    assert env.temp_c == fc["current"]["temperature_2m"] and env.updated_at == now
    assert len(forecast) == 24
    assert all(p["flag"] in FLAG_ORDER for p in forecast)
    assert re.match(r"^\d\d:00$", coolest["local"])
    hour = int(coolest["local"][:2])
    assert 5 <= hour <= 19


def test_build_env_tolerates_missing_air():
    fc = json.loads((FIX / "openmeteo_forecast.json").read_text())
    env, _, _ = envctx.build_env(fc, None, 22.3149, 87.3105, 1)
    assert env.pm25 is None and env.us_aqi is None and env.wbgt_c is not None
