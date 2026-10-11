import json

from fakes import ClientError, FakeClients
from wristheat import escalation
from wristheat.repo import FakeRepo

NOW = 1_791_700_000_000
IID = "inc-sim-S3-a-1791700000000"


def make(**fail):
    repo = FakeRepo()
    repo.put_site({"site_id": "kgp", "name": "IIT Kharagpur campus", "env": {"wbgt_c": 31.4, "pm25": 51.0},
                   "coolest_hour": {"local": "06:00", "wbgt_c": 26.9}})
    repo.put_trainee({"trainee_id": "S3", "name": "Kabir", "kind": "simulated"})
    repo.put_incident({"incident_id": IID, "trainee_id": "S3", "trainee_name": "Kabir", "trainee_kind": "simulated",
                       "session_id": "sim-S3-a", "status": "NOTIFIED", "opened_at": NOW, "ack_pending": False,
                       "trigger": {"psi": 7.2, "core_est_c": 38.6, "hr": 176, "wbgt_c": 31.4, "flag": "YELLOW",
                                   "pm25": 51.0, "rule": "psi>=7"},
                       "events": [{"t": NOW, "type": "OPENED", "detail": ""}]})
    cfg = escalation.Config(supervisor_topic="arn:sup", backup_topic="arn:backup", audio_bucket="audio",
                            dashboard_url="https://d123.cloudfront.net", model_id="apac.amazon.nova-lite-v1:0",
                            site_id="kgp")
    return escalation.Deps(repo, FakeClients(**fail), cfg)


def types(deps):
    return [e["type"] for e in deps.repo.get_incident(IID)["events"]]


def test_notify_synthesises_audio_and_emails():
    deps = make()
    escalation.notify(deps, IID, NOW + 1000)
    inc = deps.repo.get_incident(IID)
    assert inc["audio"] == {"en": f"audio/{IID}/en.mp3", "hi": f"audio/{IID}/hi.mp3"}
    puts = deps.clients.s3.ops("put_object")
    assert [p["Key"] for p in puts] == [f"audio/{IID}/en.mp3", f"audio/{IID}/hi.mp3"]
    voices = [(c["VoiceId"], c["Engine"], c["LanguageCode"]) for c in deps.clients.polly.ops("synthesize_speech")]
    assert voices == [("Kajal", "neural", "en-IN"), ("Kajal", "neural", "hi-IN")]
    msg = deps.clients.sns.ops("publish")[0]
    assert msg["TopicArn"] == "arn:sup" and "SIMULATED" in msg["Subject"]
    assert f"https://d123.cloudfront.net/incidents/{IID}" in msg["Message"] and "Strain index" not in msg["Subject"]
    assert types(deps)[-2:] == ["NOTIFIED", "AUDIO_READY"]


def test_notify_hindi_falls_back_to_aditi():
    deps = make()
    calls = []

    def synth(**kw):
        calls.append(kw)
        if kw["LanguageCode"] == "hi-IN" and kw["Engine"] == "neural":
            raise ClientError("ValidationException")
        from fakes import _Stream
        return {"AudioStream": _Stream(b"ID3")}
    deps.clients.polly.returns["synthesize_speech"] = synth
    escalation.notify(deps, IID, NOW)
    assert (calls[-1]["VoiceId"], calls[-1]["Engine"]) == ("Aditi", "standard")
    assert "hi" in deps.repo.get_incident(IID)["audio"]


def test_notify_survives_polly_outage():
    deps = make(polly={"synthesize_speech": ClientError("ServiceUnavailable")})
    escalation.notify(deps, IID, NOW)
    assert deps.clients.sns.ops("publish") and "NOTIFIED" in types(deps)
    assert "AUDIO_READY" not in types(deps)


def test_register_ack_stores_token():
    deps = make()
    escalation.register(deps, IID, "ack", "tok-1")
    assert deps.repo.get_incident(IID)["ack_token"] == "tok-1"
    assert deps.clients.sfn.ops("send_task_success") == []


def test_register_ack_with_pending_immediately_succeeds():
    deps = make()
    deps.repo.update_incident(IID, ack_pending=True, status="ACKNOWLEDGED")
    escalation.register(deps, IID, "ack", "tok-1")
    assert [c["taskToken"] for c in deps.clients.sfn.ops("send_task_success")] == ["tok-1"]


def test_register_recovery_when_already_recovered_immediately_succeeds():
    deps = make()
    deps.repo.update_incident(IID, recovered_at=NOW + 5000)
    escalation.register(deps, IID, "recovery", "tok-r")
    assert [c["taskToken"] for c in deps.clients.sfn.ops("send_task_success")] == ["tok-r"]
    assert deps.repo.get_incident(IID)["recovery_token"] == "tok-r"


def test_escalate_marks_and_emails_backup():
    deps = make()
    escalation.escalate(deps, IID, NOW + 90_000)
    inc = deps.repo.get_incident(IID)
    assert inc["status"] == "ESCALATED" and types(deps)[-1] == "ESCALATED"
    assert deps.clients.sns.ops("publish")[0]["TopicArn"] == "arn:backup"


def test_close_sets_outcome():
    cases = [({"acked_at": NOW + 40_000, "recovered_at": NOW + 300_000, "status": "ACKNOWLEDGED"}, "recovered"),
             ({"recovered_at": NOW + 300_000}, "recovered_unacknowledged"),
             ({"acked_at": NOW + 40_000, "status": "ACKNOWLEDGED"}, "not_confirmed")]
    for fields, outcome in cases:
        deps = make()
        deps.repo.update_incident(IID, **fields)
        escalation.close(deps, IID, NOW + 400_000)
        inc = deps.repo.get_incident(IID)
        assert inc["status"] == "CLOSED" and inc["outcome"] == outcome and inc["closed_at"] == NOW + 400_000
        assert inc["report"]["source"] == "bedrock" and inc["report"]["text"]
        assert types(deps)[-2:] == ["REPORT_READY", "CLOSED"]
        assert set(inc["metrics"]) == {"time_to_ack_s", "time_to_recovery_s", "minutes_in_red", "peak_psi",
                                       "peak_core_c", "escalated"}
        resolved = deps.clients.sns.ops("publish")[-1]
        assert resolved["TopicArn"] == "arn:sup" and outcome.replace("_", " ") in resolved["Message"]


def test_handlers_wire_events(monkeypatch):
    from wristheat.handlers import esc_close, esc_escalate, esc_notify, esc_register
    deps = make()
    for mod in (esc_notify, esc_register, esc_escalate, esc_close):
        monkeypatch.setattr(mod, "_deps", lambda: deps)
    esc_notify.handler({"incident_id": IID}, None)
    esc_register.handler({"incident_id": IID, "kind": "ack", "token": "t"}, None)
    esc_escalate.handler({"incident_id": IID, "timeout": {"Error": "States.Timeout"}}, None)
    out = esc_close.handler({"incident_id": IID}, None)
    assert json.dumps(out) and deps.repo.get_incident(IID)["status"] == "CLOSED"


def test_sns_subjects_are_ascii_even_with_unicode_names():
    deps = make()
    deps.repo.update_incident(IID, trainee_name="Varad — earlier run")
    escalation.notify(deps, IID, NOW)
    escalation.escalate(deps, IID, NOW + 90_000)
    escalation.close(deps, IID, NOW + 200_000)
    for call in deps.clients.sns.ops("publish"):
        assert call["Subject"].isascii() and "\n" not in call["Subject"] and len(call["Subject"]) <= 100
