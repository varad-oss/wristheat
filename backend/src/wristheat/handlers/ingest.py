"""Ingest Lambda: POST /v1/ingest and POST /v1/sessions/{session_id}/end (spec §5.1)."""
from __future__ import annotations

import base64
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Callable

from wristheat import engine, incidents, strain
from wristheat.clients import Clients, error_code
from wristheat.contract import RequestError, build_response, validate_request
from wristheat.envctx import Env
from wristheat.obs import logger, metric, tracer
from wristheat.repo import OPEN_STATUSES, Repo, VersionConflict, ttl_for

MAX_ATTEMPTS = 4
EVENT_LOG_CAP = 20
STATE_AFTER = {"CALIBRATED": "GREEN", "AMBER_ENTERED": "AMBER", "RED_ENTERED": "RED",
               "RECOVERING_ENTERED": "RECOVERING", "RECOVERY_CONFIRMED": "GREEN"}
JSON_HEADERS = {"content-type": "application/json; charset=utf-8"}


@dataclass
class Deps:
    repo: Repo
    clients: Clients
    state_machine_arn: str
    site_env_loader: Callable[[str, int], Env | None]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _err(status: int, code: str, message: str) -> tuple[int, dict]:
    return status, {"error": code, "message": message}


def _authorized(headers: dict, deps: Deps) -> bool:
    given = (headers or {}).get("x-device-token", "")
    return bool(given) and hmac.compare_digest(given.encode(), deps.clients.get_device_token().encode())


def _send_success(deps: Deps, token: str, output: dict) -> None:
    try:
        deps.clients.sfn.send_task_success(taskToken=token, output=json.dumps(output))
    except Exception as e:  # noqa: BLE001
        if error_code(e) in ("TaskTimedOut", "InvalidToken", "TaskDoesNotExist"):
            logger.warning("task token rejected", extra={"code": error_code(e)})
        else:
            raise


def process_ingest(body: dict, headers: dict, deps: Deps, now_ms: int) -> tuple[int, dict]:
    started = time.perf_counter()
    if not _authorized(headers, deps):
        return _err(401, "unauthorized", "Missing or invalid device token.")
    try:
        meta, accepted, dropped = validate_request(body, now_ms)
    except RequestError as e:
        return _err(e.status, e.code, e.message)
    tid, sid = meta["trainee_id"], meta["session_id"]
    trainee = deps.repo.get_trainee(tid)
    if trainee is None:
        return _err(404, "unknown_trainee", f"Trainee {tid} does not exist.")
    allowed = ("simulated",) if trainee.get("kind") == "simulated" else ("live", "replay")
    if meta["source"] not in allowed:
        return _err(400, "source_mismatch", f"Trainee {tid} may only send {', '.join(allowed)}.")
    site_id = trainee.get("site_id") or os.environ.get("SITE_ID", "kgp")
    env = deps.site_env_loader(site_id, now_ms)
    flag = strain.effective_flag(env, now_ms)

    for attempt in range(MAX_ATTEMPTS):
        session = deps.repo.get_session(sid)
        created = session is None
        if created:
            st0 = engine.new_state(now_ms, trainee.get("rest_hr_override"))
            session = {"session_id": sid, "trainee_id": tid, "source": meta["source"], "device": meta["device"],
                       "replay_of": meta["replay_of"], "started_at": now_ms, "last_seen": now_ms,
                       "status": "ACTIVE", "engine": st0.to_dict(), "state": st0.state,
                       "state_since": st0.state_since, "pending_alert": "NONE", "incident_id": None,
                       "hr_now": None, "version": 0, "ttl": ttl_for("sessions", now_ms)}
        elif session["trainee_id"] != tid:
            return _err(400, "bad_request", "session_id belongs to another trainee.")

        st = engine.EngineState.from_dict(session["engine"])
        amber_hr = trainee.get("amber_hr")
        res = engine.apply_samples(st, accepted, env, now_ms, amber_hr=int(amber_hr) if amber_hr is not None else None)
        st = res.state

        incident_id = session.get("incident_id")
        new_incident = None
        if incident_id:
            current = deps.repo.get_incident(incident_id)
            if current is None or current.get("status") not in OPEN_STATUSES:
                incident_id = None
        for _, event in res.events:
            if event == "RED_ENTERED" and incident_id is None:
                new_incident = incidents.open_incident(trainee, sid, st, env, now_ms, flag=flag)
                incident_id = new_incident["incident_id"]

        log = list(session.get("recent_events") or [])
        log += [{"t": (m + 1) * 60_000, "event": ev, "state": STATE_AFTER.get(ev, st.state)} for m, ev in res.events]
        response = build_response(tid, sid, len(accepted), dropped, st, env, incident_id, now_ms)
        st.pending_alert = "NONE"  # the one-shot alert is consumed by this response
        session.update(engine=st.to_dict(), state=st.state, state_since=st.state_since, pending_alert="NONE",
                       incident_id=incident_id, hr_now=st.hr_now, last_seen=now_ms,
                       recent_events=log[-EVENT_LOG_CAP:],
                       ttl=ttl_for("sessions", now_ms))
        try:
            if created:
                deps.repo.create_session({**session, "version": 0})
            else:
                deps.repo.save_session(session, session["version"])
            break
        except VersionConflict:
            logger.info("session version conflict; retrying", extra={"session_id": sid, "attempt": attempt})
    else:
        return _err(503, "conflict", "Too many concurrent updates; retry.")

    if created:
        deps.repo.set_current_session(tid, sid)
    if accepted:
        deps.repo.put_readings(sid, accepted, now_ms)
    if res.minutes:
        deps.repo.put_minutes(sid, res.minutes, now_ms)
    _after_events(deps, res.events, session, new_incident, now_ms)

    metric("SamplesIngested", len(accepted))
    metric("IngestLatencyMs", (time.perf_counter() - started) * 1000, unit="Milliseconds")
    for _, event in res.events:
        metric("StateTransitions", 1, to=event)
    return 200, response


def _after_events(deps: Deps, events: list, session: dict, new_incident: dict | None, now_ms: int) -> None:
    if new_incident:
        deps.repo.put_incident(new_incident)
        metric("IncidentsOpened", 1)
        if deps.state_machine_arn:
            out = deps.clients.sfn.start_execution(
                stateMachineArn=deps.state_machine_arn, name=new_incident["incident_id"],
                input=json.dumps({"incident_id": new_incident["incident_id"]}))
            deps.repo.update_incident(new_incident["incident_id"], execution_arn=out.get("executionArn"))
    if any(e == "RECOVERY_CONFIRMED" for _, e in events) and session.get("incident_id"):
        iid = session["incident_id"]
        inc = deps.repo.get_incident(iid)
        if inc and inc.get("status") in OPEN_STATUSES and not inc.get("recovered_at"):
            deps.repo.update_incident(iid, recovered_at=now_ms)
            deps.repo.append_incident_event(iid, {"t": now_ms, "type": "RECOVERY_CONFIRMED",
                                                  "detail": "Recovery confirmed from the data"})
            # Re-read: the workflow may have stored its token after our first read.
            token = (deps.repo.get_incident(iid) or {}).get("recovery_token")
            if token:
                _send_success(deps, token, {"recovered_at": now_ms})


def process_end(session_id: str, headers: dict, deps: Deps, now_ms: int) -> tuple[int, dict]:
    if not _authorized(headers, deps):
        return _err(401, "unauthorized", "Missing or invalid device token.")
    if deps.repo.get_session(session_id) is None:
        return _err(404, "unknown_session", f"Session {session_id} does not exist.")
    deps.repo.end_session(session_id, now_ms)
    return 200, {"ended": True}


# --- Lambda wiring -------------------------------------------------------------------------------------

_DEPS: Deps | None = None


def load_site_env(repo: Repo) -> Callable[[str, int], Env | None]:
    cache: dict[str, tuple[float, Env | None]] = {}

    def loader(site_id: str, now_ms: int) -> Env | None:
        hit = cache.get(site_id)
        if hit and time.monotonic() - hit[0] < 60:
            return hit[1]
        site = repo.get_site(site_id)
        env = Env.from_dict(site.get("env")) if site else None
        cache[site_id] = (time.monotonic(), env)
        return env
    return loader


def _deps() -> Deps:
    global _DEPS
    if _DEPS is None:
        from wristheat.repo import DynamoRepo
        repo = DynamoRepo({k: os.environ.get(f"TABLE_{k.upper()}", "") for k in
                           ("sites", "trainees", "sessions", "readings", "minutes", "incidents")})
        _DEPS = Deps(repo=repo, clients=Clients(), state_machine_arn=os.environ.get("STATE_MACHINE_ARN", ""),
                     site_env_loader=load_site_env(repo))
    return _DEPS


def respond(status: int, payload: dict) -> dict:
    return {"statusCode": status, "headers": JSON_HEADERS, "body": json.dumps(payload, ensure_ascii=False)}


def parse_body(event: dict):
    raw = event.get("body") or ""
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    return json.loads(raw) if raw else {}


@logger.inject_lambda_context(clear_state=True)
@tracer.capture_lambda_handler
def handler(event, context):
    route = event.get("routeKey", "")
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    try:
        if route == "POST /v1/ingest":
            try:
                body = parse_body(event)
            except (ValueError, UnicodeDecodeError):
                return respond(400, {"error": "bad_request", "message": "Body is not valid JSON."})
            return respond(*process_ingest(body, headers, _deps(), _now_ms()))
        if route == "POST /v1/sessions/{session_id}/end":
            sid = (event.get("pathParameters") or {}).get("session_id", "")
            return respond(*process_end(sid, headers, _deps(), _now_ms()))
        return respond(404, {"error": "not_found", "message": route})
    except Exception:
        logger.exception("ingest failed")
        return respond(500, {"error": "internal", "message": "Internal error."})
