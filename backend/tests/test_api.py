import json

from fakes import FakeClients
from wristheat.handlers import api
from wristheat.repo import FakeRepo

NOW = 1_791_700_066_000


def session(sid, tid, state, last_seen, source="live", replay_of=None, hr0=74, incident_id=None):
    return {"session_id": sid, "trainee_id": tid, "source": source, "replay_of": replay_of, "device": "SM-R920",
            "started_at": NOW - 600_000, "last_seen": last_seen, "status": "ACTIVE", "state": state,
            "state_since": NOW - 60_000, "hr_now": 150, "incident_id": incident_id, "version": 3,
            "engine": {"hr0": hr0, "ct": 37.9234, "v": 0.01, "psi": 5.93, "minutes_to_red": 6}}


def make_deps():
    repo = FakeRepo()
    repo.put_site({"site_id": "kgp", "name": "IIT Kharagpur campus", "lat": 22.3149, "lon": 87.3105,
                   "env": {"wbgt_c": 31.4, "flag": "RED", "pm25": 72.0, "us_aqi": 158, "updated_at": NOW - 60_000,
                           "temp_c": 31.2, "rh": 71, "wind_ms": 2.1},
                   "coolest_hour": {"local": "06:00", "wbgt_c": 26.9}})
    rows = [("T1", "Varad", "real", "sT1-aaaaaaaa", "AMBER", NOW - 5_000, "live", None),
            ("S1", "Arjun", "simulated", "sS1-aaaaaaaa", "GREEN", NOW - 5_000, "simulated", None),
            ("S3", "Kabir", "simulated", "sS3-aaaaaaaa", "RED", NOW - 45_000, "simulated", None),
            ("R1", "Varad — earlier run", "real", "sR1-aaaaaaaa", "GREEN", NOW - 1_000, "replay", "orig-12345678"),
            ("S2", "Meera", "simulated", None, None, None, None, None),
            ("S0", "Smoke test", "simulated", "sS0-aaaaaaaa", "GREEN", NOW, "simulated", None)]
    for tid, name, kind, sid, state, seen, source, replay_of in rows:
        t = {"trainee_id": tid, "name": name, "kind": kind, "site_id": "kgp", "hidden": tid == "S0"}
        if sid:
            t["current_session_id"] = sid
            repo.sessions[sid] = session(sid, tid, state, seen, source, replay_of)
        repo.put_trainee(t)
    repo.sessions["orig-12345678"] = session("orig-12345678", "T1", "GREEN", NOW - 86_400_000)
    return api.Deps(repo=repo, clients=FakeClients(), context_function="ctx-fn", audio_bucket="audio-bkt")


def call(deps, route, path=None, query=None, body=None, user="supervisor", groups="[supervisors]"):
    event = {"routeKey": route, "pathParameters": path or {}, "queryStringParameters": query,
             "body": json.dumps(body) if body is not None else None,
             "requestContext": {"authorizer": {"jwt": {"claims": {"cognito:username": user, "cognito:groups": groups}}}}}
    return api.route(event, deps, NOW)


def test_roster_shape_and_sorting():
    deps = make_deps()
    status, out = call(deps, "GET /v1/roster")
    assert status == 200
    ids = [t["trainee_id"] for t in out["trainees"]]
    assert ids[:2] == ["S3", "T1"] and "S0" not in ids and ids[-1] == "S2"
    by = {t["trainee_id"]: t for t in out["trainees"]}
    assert by["S3"]["stale"] is True and by["T1"]["stale"] is False
    assert by["R1"]["source"] == "replay" and by["R1"]["replay_of"] == "orig-12345678"
    assert by["R1"]["recorded_at"] == NOW - 600_000 and by["R1"]["recorded_device"] == "SM-R920"
    assert by["S2"]["state"] is None and by["S2"]["session_id"] is None
    t1 = by["T1"]
    assert t1["core_est_c"] == 37.92 and t1["core_band_c"] == 0.6 and t1["psi"] == 5.9 and t1["hr0"] == 74
    assert t1["minutes_to_red"] == 6 and t1["kind"] == "real"
    assert out["site"]["env"]["stale"] is False and out["site"]["env"]["coolest_hour"]["local"] == "06:00"
    assert out["server_time"] == NOW


def test_series_since_minute():
    deps = make_deps()
    sid = "sT1-aaaaaaaa"
    for m in range(100, 105):
        deps.repo.minutes.setdefault(sid, {})[m] = {"session_id": sid, "minute": m, "hr": 150.0, "n": 60,
                                                    "core_est_c": 37.5, "core_var": 0.01, "psi": 5.0,
                                                    "level": "AMBER", "state": "AMBER", "wbgt_c": 31.0,
                                                    "flag": "YELLOW", "pm25": 40.0}
    status, out = call(deps, "GET /v1/sessions/{session_id}/series", {"session_id": sid}, {"since_minute": "102"})
    assert status == 200 and [p["minute"] for p in out["points"]] == [102, 103, 104]
    status, out = call(deps, "GET /v1/sessions/{session_id}/series", {"session_id": sid})
    assert len(out["points"]) == 5


def add_incident(deps, iid="inc-sS3-aaaa-1", status="NOTIFIED", **extra):
    deps.repo.put_incident({"incident_id": iid, "trainee_id": "S3", "trainee_name": "Kabir", "session_id": "sS3-aaaaaaaa",
                            "status": status, "opened_at": NOW - 100_000, "trigger": {"psi": 7.1, "rule": "psi>=7"},
                            "events": [{"t": NOW - 100_000, "type": "OPENED", "detail": ""}], "ack_pending": False,
                            "execution_arn": "arn:aws:states:ap-south-1:1:execution:wristheat-escalation:" + iid,
                            **extra})
    return iid


def test_incident_get_has_presigned_audio_and_console_url():
    deps = make_deps()
    iid = add_incident(deps, audio={"en": f"audio/x/en.mp3", "hi": f"audio/x/hi.mp3"}, ack_token="secret-token")
    status, out = call(deps, "GET /v1/incidents/{incident_id}", {"incident_id": iid})
    assert status == 200
    assert out["console_url"].startswith(
        "https://ap-south-1.console.aws.amazon.com/states/home?region=ap-south-1#/v2/executions/details/")
    assert out["audio"]["en"].startswith("https://") and out["audio"]["hi"].startswith("https://")
    assert "ack_token" not in out and "recovery_token" not in out
    assert call(deps, "GET /v1/incidents/{incident_id}", {"incident_id": "nope"})[0] == 404


def test_incident_list_open_and_all():
    deps = make_deps()
    add_incident(deps, "inc-a", "NOTIFIED")
    add_incident(deps, "inc-b", "CLOSED")
    assert [i["incident_id"] for i in call(deps, "GET /v1/incidents", query={"status": "open"})[1]["incidents"]] == ["inc-a"]
    assert len(call(deps, "GET /v1/incidents", query={"status": "all"})[1]["incidents"]) == 2
    _, roster = call(deps, "GET /v1/roster")
    assert [i["incident_id"] for i in roster["open_incidents"]] == ["inc-a"]
    assert roster["open_incidents"][0]["advice"]["en"].startswith("Stop now.")


def test_ack_with_token_sends_success():
    deps = make_deps()
    iid = add_incident(deps, ack_token="tok-ack")
    status, out = call(deps, "POST /v1/incidents/{incident_id}/ack", {"incident_id": iid}, body={"note": "cooling"})
    assert status == 200 and out == {"status": "ACKNOWLEDGED"}
    assert [c["taskToken"] for c in deps.clients.sfn.ops("send_task_success")] == ["tok-ack"]
    inc = deps.repo.get_incident(iid)
    assert inc["acked_by"] == "supervisor" and inc["acked_at"] == NOW and inc["status"] == "ACKNOWLEDGED"
    assert inc["events"][-1]["type"] == "ACKNOWLEDGED"


def test_ack_before_token_sets_pending():
    deps = make_deps()
    iid = add_incident(deps)
    status, _ = call(deps, "POST /v1/incidents/{incident_id}/ack", {"incident_id": iid}, body={})
    assert status == 200
    assert deps.repo.get_incident(iid)["ack_pending"] is True
    assert deps.clients.sfn.ops("send_task_success") == []


def test_ack_twice_returns_409_and_signals_once():
    deps = make_deps()
    iid = add_incident(deps, "inc-e", "ESCALATED", ack_token="tok-ack")
    assert call(deps, "POST /v1/incidents/{incident_id}/ack", {"incident_id": iid}, body={})[0] == 200
    status, out = call(deps, "POST /v1/incidents/{incident_id}/ack", {"incident_id": iid}, body={})
    assert status == 409 and out["error"] == "already_acknowledged"
    assert len(deps.clients.sfn.ops("send_task_success")) == 1


def test_context_refresh_invokes_context_lambda():
    deps = make_deps()
    deps.clients.lam.returns["invoke"] = lambda **kw: {"Payload": _Payload(b'{"env": {"wbgt_c": 30.1}}')}
    status, out = call(deps, "POST /v1/context/refresh")
    assert status == 200 and out == {"env": {"wbgt_c": 30.1}}
    assert deps.clients.lam.ops("invoke")[0]["FunctionName"] == "ctx-fn"


class _Payload:
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data


def test_roster_activity_sorted_and_excludes_hidden():
    deps = make_deps()
    deps.repo.sessions["sT1-aaaaaaaa"]["recent_events"] = [{"t": NOW - 300_000, "event": "AMBER_ENTERED", "state": "AMBER"}]
    deps.repo.sessions["sS3-aaaaaaaa"]["recent_events"] = [
        {"t": NOW - 600_000, "event": "AMBER_ENTERED", "state": "AMBER"},
        {"t": NOW - 60_000, "event": "RED_ENTERED", "state": "RED"}]
    deps.repo.sessions["sS0-aaaaaaaa"]["recent_events"] = [{"t": NOW, "event": "CALIBRATED", "state": "GREEN"}]
    _, out = call(deps, "GET /v1/roster")
    act = out["activity"]
    assert [(a["trainee_id"], a["event"]) for a in act] == [("S3", "RED_ENTERED"), ("T1", "AMBER_ENTERED"), ("S3", "AMBER_ENTERED")]
    assert act[0]["name"] == "Kabir" and act[0]["kind"] == "simulated" and act[0]["source"] == "simulated"
    assert act[0]["state"] == "RED" and len(act) <= 20


def _minute(sid, m, state, hr=150.0, psi=5.0, core=37.8, flag="YELLOW"):
    return {"session_id": sid, "minute": m, "hr": hr, "n": 60, "core_est_c": core, "core_var": 0.01, "psi": psi,
            "level": state, "state": state, "wbgt_c": 30.0, "flag": flag, "pm25": 40.0}


def test_summary_counts_minutes_by_state():
    deps = make_deps()
    sid = "sT1-aaaaaaaa"
    rows = [_minute(sid, 100 + i, "GREEN", psi=2.0 + i, core=37.2 + i / 10, hr=120 + i) for i in range(3)]
    rows += [_minute(sid, 103 + i, "AMBER", psi=5.5 + i, core=37.9, hr=160 + i) for i in range(2)]
    rows.append({**_minute(sid, 105, "AMBER"), "hr": None, "psi": None, "level": None, "n": 4})
    deps.repo.minutes[sid] = {r["minute"]: r for r in rows}
    status, out = call(deps, "GET /v1/sessions/{session_id}/summary", {"session_id": sid})
    assert status == 200
    assert out["minutes_by_state"] == {"GREEN": 3, "AMBER": 2, "RED": 0, "RECOVERING": 0, "CALIBRATING": 0, "gap": 1}
    assert out["peak_psi"] == 6.5 and out["peak_core_c"] == 37.9 and out["peak_hr"] == 161
    assert out["trainee"]["name"] == "Varad" and out["trainee"]["kind"] == "real"
    assert out["session"]["source"] == "live" and out["duration_min"] == 6
    assert out["flag_minutes"] == {"YELLOW": 6}


def test_summary_includes_incidents():
    deps = make_deps()
    add_incident(deps, "inc-s3", "CLOSED", outcome="recovered",
                 metrics={"time_to_ack_s": 107, "time_to_recovery_s": 299, "minutes_in_red": 4,
                          "peak_psi": 8.1, "peak_core_c": 38.55, "escalated": True})
    add_incident(deps, "inc-other", "CLOSED", session_id="someone-else")
    _, out = call(deps, "GET /v1/sessions/{session_id}/summary", {"session_id": "sS3-aaaaaaaa"})
    assert [i["incident_id"] for i in out["incidents"]] == ["inc-s3"]
    assert out["incidents"][0]["metrics"]["time_to_ack_s"] == 107 and out["incidents"][0]["outcome"] == "recovered"


def test_summary_empty_session():
    deps = make_deps()
    status, out = call(deps, "GET /v1/sessions/{session_id}/summary", {"session_id": "sS1-aaaaaaaa"})
    assert status == 200 and out["minutes_by_state"]["GREEN"] == 0 and out["duration_min"] == 0
    assert out["peak_psi"] is None and out["peak_core_c"] is None and out["incidents"] == []


def test_summary_unknown_session_404():
    assert call(make_deps(), "GET /v1/sessions/{session_id}/summary", {"session_id": "nope-nope"})[0] == 404


def test_public_roster_only_simulated():
    deps = make_deps()
    add_incident(deps, "inc-s3", "NOTIFIED")
    add_incident(deps, "inc-t1", "NOTIFIED", trainee_id="T1", trainee_name="Varad", trainee_kind="real",
                 session_id="sT1-aaaaaaaa")
    deps.repo.sessions["sT1-aaaaaaaa"]["recent_events"] = [{"t": NOW, "event": "AMBER_ENTERED", "state": "AMBER"}]
    deps.repo.sessions["sS3-aaaaaaaa"]["recent_events"] = [{"t": NOW, "event": "RED_ENTERED", "state": "RED"}]
    status, out = api.route({"routeKey": "GET /v1/public/roster"}, deps, NOW)
    assert status == 200
    ids = {t["trainee_id"] for t in out["trainees"]}
    assert ids == {"S1", "S2", "S3"}
    assert {i["trainee_id"] for i in out["open_incidents"]} == {"S3"}
    assert {a["trainee_id"] for a in out["activity"]} == {"S3"}
    assert all(t["kind"] == "simulated" for t in out["trainees"])
    assert out["public"] is True and out["site"]["env"]["flag"] == "RED"


def test_group_roster_excludes_solo_wearers():
    deps = make_deps()
    deps.repo.trainees["T1"]["mode"] = "solo"
    deps.repo.sessions["sT1-aaaaaaaa"]["recent_events"] = [{"t": NOW, "event": "AMBER_ENTERED", "state": "AMBER"}]
    add_incident(deps, "inc-t1", "NOTIFIED", trainee_id="T1", trainee_name="Varad", trainee_kind="real",
                 session_id="sT1-aaaaaaaa")
    _, out = call(deps, "GET /v1/roster")
    assert "T1" not in {t["trainee_id"] for t in out["trainees"]}
    assert "T1" not in {a["trainee_id"] for a in out["activity"]}
    assert "inc-t1" not in {i["incident_id"] for i in out["open_incidents"]}
    assert "S3" in {t["trainee_id"] for t in out["trainees"]}


def wearer_deps():
    deps = make_deps()
    deps.repo.trainees["T1"].update(mode="solo", owner_username="varad")
    add_incident(deps, "inc-t1", "NOTIFIED", trainee_id="T1", trainee_name="Varad", trainee_kind="real",
                 trainee_mode="solo", session_id="sT1-aaaaaaaa")
    add_incident(deps, "inc-s3", "NOTIFIED")
    return deps


def as_wearer(deps, route, path=None, body=None):
    return call(deps, route, path, body=body, user="varad", groups="[wearers]")


def test_wearer_cannot_use_group_routes():
    deps = wearer_deps()
    for route in ("GET /v1/roster", "GET /v1/incidents", "POST /v1/context/refresh"):
        status, out = as_wearer(deps, route)
        assert status == 403 and out["error"] == "forbidden", route


def test_me_returns_own_state_sessions_and_incidents():
    deps = wearer_deps()
    deps.repo.sessions["sT1-old-aaaa"] = session("sT1-old-aaaa", "T1", "GREEN", NOW - 86_400_000)
    status, out = as_wearer(deps, "GET /v1/me")
    assert status == 200
    assert out["trainee"]["trainee_id"] == "T1" and out["trainee"]["mode"] == "solo"
    assert out["live"]["state"] == "AMBER" and out["live"]["core_est_c"] == 37.92
    assert [i["incident_id"] for i in out["open_incidents"]] == ["inc-t1"]
    assert {s["session_id"] for s in out["sessions"]} == {"sT1-aaaaaaaa", "sT1-old-aaaa", "orig-12345678"}
    assert out["sessions"][0]["session_id"] == "sT1-aaaaaaaa"
    assert out["site"]["env"]["flag"] == "RED" and "server_time" in out


def test_me_for_unlinked_user_is_404():
    status, out = call(wearer_deps(), "GET /v1/me", user="nobody", groups="[wearers]")
    assert status == 404 and out["error"] == "no_wearer_profile"


def test_wearer_acks_only_own_incident():
    deps = wearer_deps()
    assert as_wearer(deps, "POST /v1/incidents/{incident_id}/ack", {"incident_id": "inc-s3"}, body={})[0] == 403
    status, out = as_wearer(deps, "POST /v1/incidents/{incident_id}/ack", {"incident_id": "inc-t1"}, body={})
    assert status == 200 and deps.repo.get_incident("inc-t1")["acked_by"] == "varad"


def test_wearer_reads_only_own_session_and_incident():
    deps = wearer_deps()
    assert as_wearer(deps, "GET /v1/sessions/{session_id}/summary", {"session_id": "sT1-aaaaaaaa"})[0] == 200
    assert as_wearer(deps, "GET /v1/sessions/{session_id}/summary", {"session_id": "sS3-aaaaaaaa"})[0] == 403
    assert as_wearer(deps, "GET /v1/sessions/{session_id}/series", {"session_id": "sS3-aaaaaaaa"})[0] == 403
    assert as_wearer(deps, "GET /v1/incidents/{incident_id}", {"incident_id": "inc-t1"})[0] == 200
    assert as_wearer(deps, "GET /v1/incidents/{incident_id}", {"incident_id": "inc-s3"})[0] == 403


def test_groups_claim_as_list_is_accepted():
    deps = make_deps()
    assert call(deps, "GET /v1/roster", groups=["supervisors"])[0] == 200
    assert call(deps, "GET /v1/roster", groups=None)[0] == 403
