import re

import pytest

from fakes import ClientError, FakeClients
from wristheat import engine, incidents, obs
from wristheat.envctx import Env

NOW = 1_791_700_000_000


def test_incident_id_format():
    assert incidents.incident_id_for("3f6c1e9a-0b7d-4a51", NOW) == f"inc-3f6c1e9a-{NOW}"


@pytest.mark.parametrize("psi,ct,flag,rule", [
    (7.2, 38.4, "NONE", "psi>=7"),
    (5.0, 39.1, "NONE", "core>=39"),
    (6.3, 38.3, "RED", "psi>=6 & flag"),
])
def test_open_incident_rule_names(psi, ct, flag, rule):
    st = engine.new_state(NOW, 76)
    st.psi, st.ct, st.history = psi, ct, [{"minute": 1, "level": "RED", "hr": 170.4, "psi": psi, "ct": ct}]
    env = Env(wbgt_c=31.4, flag=flag, pm25=72.0, us_aqi=158, updated_at=NOW)
    inc = incidents.open_incident({"trainee_id": "S3", "name": "Kabir", "kind": "simulated"}, "sess-12345678",
                                  st, env, NOW, flag=flag)
    assert inc["trigger"]["rule"] == rule
    assert inc["trigger"]["hr"] == 170 and inc["trigger"]["wbgt_c"] == 31.4
    assert inc["status"] == "NOTIFIED" and inc["events"][0]["type"] == "OPENED"


def test_polly_texts_verbatim():
    t = incidents.polly_texts("Kabir", 7.2, 31.4, False)
    assert t["en"] == ("Heat alert. Kabir needs to stop now. Strain index 7.2. Open-field W B G T 31.4 degrees. "
                       "Move them to shade and cool them with water.")
    assert t["hi"] == "गर्मी की चेतावनी। Kabir को अभी रुकना होगा। उन्हें छाँव में ले जाएँ और पानी से ठंडा करें।"
    t = incidents.polly_texts("Kabir", 7.2, None, True)
    assert "indoors" in t["en"] and "W B G T" not in t["en"] and "अंदर" in t["hi"]


def _incident(**over):
    inc = {"incident_id": "inc-1", "trainee_id": "S3", "trainee_name": "Kabir", "trainee_kind": "simulated",
           "session_id": "s", "status": "ACKNOWLEDGED", "opened_at": NOW, "acked_at": NOW + 40_000,
           "acked_by": "supervisor", "recovered_at": NOW + 300_000,
           "trigger": {"psi": 7.1, "core_est_c": 38.6, "hr": 176, "wbgt_c": 31.4, "flag": "YELLOW", "pm25": 51.0,
                       "rule": "psi>=7"},
           "events": [{"t": NOW, "type": "OPENED", "detail": ""}, {"t": NOW + 40_000, "type": "ACKNOWLEDGED", "detail": ""}]}
    inc.update(over)
    return inc


def test_metrics():
    minutes = [{"minute": NOW // 60000 + i, "state": "RED" if i < 5 else "RECOVERING", "psi": 7.0 + i / 10,
                "core_est_c": 38.5 + i / 100} for i in range(8)]
    m = incidents.compute_metrics(_incident(), minutes)
    assert m["time_to_ack_s"] == 40 and m["time_to_recovery_s"] == 300 and m["minutes_in_red"] == 5
    assert m["peak_psi"] == 7.7 and m["peak_core_c"] == 38.57 and m["escalated"] is False
    m = incidents.compute_metrics(_incident(acked_at=None, recovered_at=None), [])
    assert m["time_to_ack_s"] is None and m["time_to_recovery_s"] is None and m["minutes_in_red"] == 0


def _facts(**over):
    inc = _incident(**over)
    metrics = incidents.compute_metrics(inc, [])
    return incidents.report_facts(inc, metrics, {"name": "IIT Kharagpur campus",
                                                 "coolest_hour": {"local": "06:00", "wbgt_c": 26.9}})


def test_template_report_word_limit_and_suffix():
    for over in ({}, {"acked_at": None}, {"recovered_at": None, "outcome": "not_confirmed"}):
        text = incidents.template_report(_facts(**over))
        assert len(text.split()) <= 120
        assert text.endswith("Estimated values; not a medical assessment.")
        assert "Kabir" in text and "06:00" in text
        assert re.search(r"\d\d:\d\d", text)


def test_bedrock_success_uses_model():
    clients = FakeClients()
    text, source = incidents.bedrock_report(clients, "apac.amazon.nova-lite-v1:0", _facts())
    assert source == "bedrock" and text.endswith("Estimated values; not a medical assessment.")
    call = clients.bedrock.ops("converse")[0]
    assert call["modelId"] == "apac.amazon.nova-lite-v1:0"
    assert call["inferenceConfig"] == {"maxTokens": 400, "temperature": 0.2}
    assert call["system"][0]["text"].startswith("You write short factual incident summaries")


def test_bedrock_failure_falls_back():
    clients = FakeClients(bedrock={"converse": ClientError("AccessDeniedException")})
    obs.RECORDED.clear()
    text, source = incidents.bedrock_report(clients, "apac.amazon.nova-lite-v1:0", _facts())
    assert source == "template" and text.endswith("Estimated values; not a medical assessment.")
    assert "BedrockFallbacks" in [m[0] for m in obs.RECORDED]


def test_bedrock_empty_model_uses_template():
    text, source = incidents.bedrock_report(FakeClients(), "", _facts())
    assert source == "template"
