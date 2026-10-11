import json

import jsonschema
import pytest

from conftest import CONTRACTS_DIR
from wristheat import engine
from wristheat.advice import advice_for
from wristheat.contract import RequestError, build_response, validate_request
from wristheat.envctx import Env

NOW = 1_791_700_000_000
RESP_SCHEMA = json.loads((CONTRACTS_DIR / "ingest_response.schema.json").read_text(encoding="utf-8"))


def body(**over):
    b = {"schema": 1, "trainee_id": "T1", "session_id": "3f6c1e9a-0b7d-4a51", "source": "live",
         "device": "SM-R920", "samples": [{"t": NOW - 1000, "bpm": 90}]}
    b.update(over)
    return b


def test_advice_red_indoors():
    assert advice_for("RED", 72.4, "NONE")["en"] == "Stop now. Rest indoors — outdoor air is poor (PM2.5 72 µg/m³)."
    assert advice_for("RED", 72.4, "NONE")["hi"] == "अभी रुकें। अंदर आराम करें — बाहर की हवा खराब है (PM2.5 72 µg/m³)।"


def test_advice_recovered_overrides():
    assert advice_for("GREEN", 10, "RECOVERED")["en"] == "Recovery confirmed. Resume only at an easier pace."


@pytest.mark.parametrize("state,pm25,en", [
    ("CALIBRATING", None, "Sit still — measuring your resting heart rate."),
    ("GREEN", None, "Strain low. Keep drinking water."),
    ("AMBER", 80, "Strain rising. Slow down and drink water."),
    ("RED", 60, "Stop now. Rest in shade and cool down with water."),
    ("RECOVERING", None, "Recovering. Stay in shade until cleared."),
    ("RECOVERING", 61, "Recovering. Stay indoors until cleared."),
])
def test_advice_table(state, pm25, en):
    assert advice_for(state, pm25, "NONE")["en"] == en


def test_validate_drops_out_of_range_and_future():
    samples = [{"t": NOW - 5000, "bpm": 25}, {"t": NOW - 4000, "bpm": 240}, {"t": NOW + 61_000, "bpm": 90},
               {"t": NOW - 7 * 3600_000, "bpm": 90}, {"t": NOW - 1000, "bpm": 91}]
    meta, accepted, dropped = validate_request(body(samples=samples), NOW)
    assert dropped == 4
    assert accepted == [(NOW - 1000, 91)]
    assert meta["trainee_id"] == "T1" and meta["source"] == "live"


@pytest.mark.parametrize("bad", [
    {k: v for k, v in body().items() if k != "samples"},
    body(samples=[{"t": NOW - i, "bpm": 90} for i in range(601)]),
    body(source="replay"),
    body(schema=2),
    body(session_id="short"),
    body(source="other"),
    body(samples=[{"t": NOW, "bpm": "90"}]),
    body(extra=1),
])
def test_validate_rejects_bad_schema(bad):
    with pytest.raises(RequestError) as e:
        validate_request(bad, NOW)
    assert e.value.status == 400 and e.value.code == "bad_request"


def test_replay_with_replay_of_ok():
    meta, _, _ = validate_request(body(source="replay", replay_of="orig-session-1",
                                       samples=[{"t": NOW - 8 * 3600_000, "bpm": 90}]), NOW)
    assert meta["replay_of"] == "orig-session-1"


def _resp(st, env, alert=None, incident=None):
    if alert:
        st.pending_alert = alert
    r = build_response("T1", "sess-12345678", 5, 0, st, env, incident, NOW)
    jsonschema.validate(r, RESP_SCHEMA)
    return r


def test_response_matches_schema():
    env = Env(wbgt_c=31.4, flag="RED", pm25=72.0, us_aqi=158, updated_at=NOW - 60_000, temp_c=31.2, rh=70, wind_ms=2)
    cal = engine.new_state(NOW - 30_000, None)
    cal = engine.apply_samples(cal, [(NOW - 30_000, 80)], env, NOW).state
    r = _resp(cal, env)
    assert r["state"] == "CALIBRATING" and r["hr0"] is None and r["core_est_c"] is None and r["psi"] is None
    assert r["core_band_c"] == 0.6 and 0 < r["calibration_remaining_s"] <= 120

    st = engine.new_state(NOW - 600_000, 75)
    st = engine.apply_samples(st, [(NOW - 600_000 + k * 1000, 160) for k in range(540)], env, NOW).state
    st.state = "AMBER"
    r = _resp(st, env, alert="AMBER", incident=None)
    assert r["alert"] == "AMBER" and r["advice"]["en"].startswith("Strain rising")
    assert isinstance(r["psi"], float) and r["core_est_c"] == round(r["core_est_c"], 2)
    assert set(r["env"]) == {"wbgt_c", "flag", "pm25", "us_aqi", "updated_at", "stale"}

    r = _resp(st, None)
    assert r["env"] is None
