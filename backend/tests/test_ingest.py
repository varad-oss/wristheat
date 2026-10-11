import json

import jsonschema
import pytest

from conftest import CONTRACTS_DIR
from fakes import ClientError, FakeClients
from test_engine import D_BASE, T0, minutes_to_samples
from wristheat.envctx import Env
from wristheat.handlers import ingest
from wristheat.repo import FakeRepo

TOKEN = "tok-0123456789abcdef0123456789abcd"
SID = "3f6c1e9a-0b7d-4a51-9a52-0c3c0d2f8e11"
RESP_SCHEMA = json.loads((CONTRACTS_DIR / "ingest_response.schema.json").read_text(encoding="utf-8"))


def make_deps(flag="RED", clients=None, repo=None):
    repo = repo or FakeRepo()
    repo.trainees["T1"] = {"trainee_id": "T1", "name": "Varad", "kind": "real", "age": 21, "site_id": "kgp"}
    repo.trainees["S3"] = {"trainee_id": "S3", "name": "Kabir", "kind": "simulated", "age": 21,
                           "site_id": "kgp", "rest_hr_override": 76}

    def env_loader(site_id, now_ms):
        return Env(wbgt_c=31.5, flag=flag, pm25=30.0, us_aqi=90, updated_at=now_ms)

    return ingest.Deps(repo=repo, clients=clients or FakeClients(TOKEN), state_machine_arn="arn:sm",
                       site_env_loader=env_loader)


def body(samples, tid="T1", source="live", sid=SID):
    return {"schema": 1, "trainee_id": tid, "session_id": sid, "source": source, "device": "SM-R920",
            "samples": [{"t": t, "bpm": b} for t, b in samples]}


def post(deps, b, now, token=TOKEN):
    return ingest.process_ingest(b, {"x-device-token": token}, deps, now)


def drive(deps, minute_hrs, batch=5):
    samples = minutes_to_samples(minute_hrs)
    responses = []
    for i in range(0, len(samples), batch):
        chunk = samples[i:i + batch]
        status, resp = post(deps, body(chunk), chunk[-1][0])
        assert status == 200, resp
        responses.append(resp)
    return responses


def test_unauthorized():
    status, resp = post(make_deps(), body([(T0, 80)]), T0, token="nope")
    assert status == 401 and resp["error"] == "unauthorized"


def test_unknown_trainee_404():
    status, resp = post(make_deps(), body([(T0, 80)], tid="ZZ"), T0)
    assert status == 404 and resp["error"] == "unknown_trainee"


def test_simulated_trainee_cannot_send_live():
    status, resp = post(make_deps(), body([(T0, 80)], tid="S3", source="live"), T0)
    assert status == 400 and resp["error"] == "source_mismatch"


def test_bad_request_400():
    status, resp = post(make_deps(), {"schema": 1}, T0)
    assert status == 400 and resp["error"] == "bad_request"


def test_first_batch_creates_session_and_sets_current():
    deps = make_deps()
    status, resp = post(deps, body([(T0 + k * 1000, 80) for k in range(5)]), T0 + 5000)
    assert status == 200
    jsonschema.validate(resp, RESP_SCHEMA)
    assert resp["state"] == "CALIBRATING" and resp["accepted"] == 5
    assert deps.repo.sessions[SID]["trainee_id"] == "T1"
    assert deps.repo.trainees["T1"]["current_session_id"] == SID
    assert len(deps.repo.readings[SID]) == 5


def test_red_entered_opens_incident_and_starts_execution():
    deps = make_deps("RED")
    responses = drive(deps, D_BASE[:14])
    starts = deps.clients.sfn.ops("start_execution")
    assert len(starts) == 1
    incident_id = starts[0]["name"]
    assert incident_id.startswith("inc-3f6c1e9a-")
    assert json.loads(starts[0]["input"])["incident_id"] == incident_id
    alerts = [r["alert"] for r in responses]
    i = alerts.index("RED")
    assert alerts[i + 1] == "NONE" and alerts.count("RED") == 1
    assert responses[i]["incident_id"] == incident_id
    inc = deps.repo.incidents[incident_id]
    assert inc["trainee_id"] == "T1" and inc["trigger"]["rule"] in ("psi>=7", "core>=39", "psi>=6 & flag")
    for r in responses:
        jsonschema.validate(r, RESP_SCHEMA)


def test_recovery_sends_task_success_when_token_present():
    deps = make_deps("RED")
    drive(deps, D_BASE[:14])
    incident_id = deps.clients.sfn.ops("start_execution")[0]["name"]
    deps.repo.incidents[incident_id]["recovery_token"] = "rec-token"
    # continue the same session: minutes 15..32
    samples = minutes_to_samples(D_BASE)[14 * 60:]
    for i in range(0, len(samples), 5):
        chunk = samples[i:i + 5]
        post(deps, body(chunk), chunk[-1][0])
    calls = deps.clients.sfn.ops("send_task_success")
    assert [c["taskToken"] for c in calls] == ["rec-token"]
    inc = deps.repo.incidents[incident_id]
    assert inc["recovered_at"] is not None
    assert "RECOVERY_CONFIRMED" in [e["type"] for e in inc["events"]]


def test_recovery_token_errors_are_ignored():
    clients = FakeClients(TOKEN, sfn={"send_task_success": ClientError("TaskTimedOut")})
    deps = make_deps("RED", clients=clients)
    drive(deps, D_BASE[:14])
    incident_id = clients.sfn.ops("start_execution")[0]["name"]
    deps.repo.incidents[incident_id]["recovery_token"] = "rec-token"
    samples = minutes_to_samples(D_BASE)[14 * 60:]
    for i in range(0, len(samples), 5):
        chunk = samples[i:i + 5]
        status, _ = post(deps, body(chunk), chunk[-1][0])
        assert status == 200


def test_ingest_retries_on_version_conflict():
    plain = make_deps()
    drive(plain, D_BASE[:6])
    racy = make_deps()
    racy.repo.fail_next_save_with_conflict = 1
    drive(racy, D_BASE[:6])
    a, b = plain.repo.sessions[SID], racy.repo.sessions[SID]
    assert a["engine"] == b["engine"] and a["state"] == b["state"]


def test_end_session_marks_ended():
    deps = make_deps()
    post(deps, body([(T0, 80)]), T0)
    status, resp = ingest.process_end(SID, {"x-device-token": TOKEN}, deps, T0 + 1000)
    assert status == 200 and resp == {"ended": True}
    assert deps.repo.sessions[SID]["status"] == "ENDED"
    status, _ = ingest.process_end(SID, {"x-device-token": "bad"}, deps, T0 + 1000)
    assert status == 401


def test_end_unknown_session_404():
    status, resp = ingest.process_end("nope-nope-nope", {"x-device-token": TOKEN}, make_deps(), T0)
    assert status == 404 and resp["error"] == "unknown_session"


class Ctx:
    function_name, memory_limit_in_mb = "ingest", 512
    invoked_function_arn, aws_request_id = "arn:aws:lambda:ap-south-1:1:function:ingest", "req-1"


def test_handler_routes_and_utf8(monkeypatch):
    deps = make_deps()
    monkeypatch.setattr(ingest, "_deps", lambda: deps)
    monkeypatch.setattr(ingest, "_now_ms", lambda: T0 + 5000)
    event = {"routeKey": "POST /v1/ingest", "headers": {"x-device-token": TOKEN},
             "body": json.dumps(body([(T0 + k * 1000, 80) for k in range(5)])), "isBase64Encoded": False}
    out = ingest.handler(event, Ctx())
    assert out["statusCode"] == 200
    assert out["headers"]["content-type"] == "application/json; charset=utf-8"
    assert "आराम" in out["body"]  # Hindi arrives unescaped
    event = {"routeKey": "POST /v1/sessions/{session_id}/end", "headers": {"x-device-token": TOKEN},
             "pathParameters": {"session_id": SID}}
    assert ingest.handler(event, Ctx())["statusCode"] == 200
