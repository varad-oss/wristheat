"""Supervisor API (Cognito JWT): roster, series, incidents, acknowledgement, context refresh (spec §5.2)."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass

from wristheat import strain
from wristheat.advice import advice_for
from wristheat.clients import Clients, error_code
from wristheat.envctx import Env
from wristheat.handlers.ingest import parse_body, respond
from wristheat.obs import logger, tracer
from wristheat.repo import OPEN_STATUSES, ConditionFailed, Repo

STALE_SESSION_MS = 30_000
STATE_ORDER = {"RED": 0, "AMBER": 1, "RECOVERING": 2, "GREEN": 3, "CALIBRATING": 4, None: 5}
ACKABLE = ("NOTIFIED", "ESCALATED")
PRIVATE_FIELDS = ("ack_token", "recovery_token", "ttl")
CONSOLE = "https://ap-south-1.console.aws.amazon.com/states/home?region=ap-south-1#/v2/executions/details/"
PRESIGN_S = 900


@dataclass
class Deps:
    repo: Repo
    clients: Clients
    context_function: str
    audio_bucket: str


def _err(status: int, code: str, message: str) -> tuple[int, dict]:
    return status, {"error": code, "message": message}


# --- roster --------------------------------------------------------------------------------------------

def _site_payload(site: dict | None, now_ms: int) -> dict | None:
    if not site:
        return None
    env = site.get("env")
    env_out = None
    if env:
        env_out = {k: env.get(k) for k in ("wbgt_c", "flag", "temp_c", "rh", "wind_ms", "pm25", "us_aqi", "updated_at")}
        env_out["stale"] = strain.is_stale(Env.from_dict(env), now_ms)
        env_out["coolest_hour"] = site.get("coolest_hour") or None
    return {"site_id": site["site_id"], "name": site.get("name"), "lat": site.get("lat"), "lon": site.get("lon"),
            "env": env_out, "forecast": site.get("forecast", [])}


def _trainee_row(repo: Repo, t: dict, now_ms: int, open_by_session: dict) -> dict:
    row = {"trainee_id": t["trainee_id"], "name": t.get("name"), "kind": t.get("kind", "real"), "source": None,
           "session_id": None, "state": None, "state_since": None, "hr_now": None, "hr0": None,
           "core_est_c": None, "core_band_c": 0.6, "psi": None, "minutes_to_red": None, "last_seen": None,
           "stale": True, "incident_id": None, "replay_of": None, "recorded_at": None, "recorded_device": None}
    sid = t.get("current_session_id")
    s = repo.get_session(sid) if sid else None
    if not s:
        return row
    eng = s.get("engine") or {}
    calibrated = s.get("state") not in (None, "CALIBRATING") and eng.get("hr0") is not None
    row.update(source=s.get("source"), session_id=sid, state=s.get("state"), state_since=s.get("state_since"),
               hr_now=s.get("hr_now"), last_seen=s.get("last_seen"),
               stale=now_ms - int(s.get("last_seen") or 0) > STALE_SESSION_MS,
               hr0=eng.get("hr0") if calibrated else None,
               core_est_c=round(eng["ct"], 2) if calibrated and eng.get("ct") is not None else None,
               psi=round(eng["psi"], 1) if calibrated and eng.get("psi") is not None else None,
               minutes_to_red=eng.get("minutes_to_red"), incident_id=open_by_session.get(sid),
               replay_of=s.get("replay_of"))
    if s.get("status") == "ENDED":
        row["stale"] = True
    if row["replay_of"]:
        orig = repo.get_session(row["replay_of"])
        if orig:
            row.update(recorded_at=orig.get("started_at"), recorded_device=orig.get("device"))
    return row


def _summary(inc: dict, site_env: dict | None) -> dict:
    escalated = next((e["t"] for e in inc.get("events", []) if e.get("type") == "ESCALATED"), None)
    pm25 = (inc.get("trigger") or {}).get("pm25")
    if pm25 is None and site_env:
        pm25 = site_env.get("pm25")
    return {"incident_id": inc["incident_id"], "trainee_id": inc.get("trainee_id"),
            "trainee_name": inc.get("trainee_name"), "trainee_kind": inc.get("trainee_kind"),
            "session_id": inc.get("session_id"), "status": inc.get("status"), "opened_at": inc.get("opened_at"),
            "closed_at": inc.get("closed_at"), "outcome": inc.get("outcome"), "trigger": inc.get("trigger"),
            "escalated_at": escalated, "acked_at": inc.get("acked_at"), "acked_by": inc.get("acked_by"),
            "advice": advice_for("RED", pm25, "NONE")}


def roster(deps: Deps, now_ms: int) -> tuple[int, dict]:
    site_id = os.environ.get("SITE_ID", "kgp")
    site = deps.repo.get_site(site_id)
    incidents = deps.repo.list_incidents()
    open_inc = sorted((i for i in incidents if i.get("status") in OPEN_STATUSES),
                      key=lambda i: i.get("opened_at", 0), reverse=True)
    open_by_session = {i.get("session_id"): i["incident_id"] for i in open_inc}
    rows = [_trainee_row(deps.repo, t, now_ms, open_by_session)
            for t in deps.repo.list_trainees() if not t.get("hidden")]
    rows.sort(key=lambda r: (STATE_ORDER.get(r["state"], 5), r["trainee_id"]))
    return 200, {"site": _site_payload(site, now_ms), "trainees": rows,
                 "open_incidents": [_summary(i, (site or {}).get("env")) for i in open_inc],
                 "server_time": now_ms}


# --- series and incidents --------------------------------------------------------------------------------

def series(deps: Deps, session_id: str, since: str | None) -> tuple[int, dict]:
    try:
        since_minute = int(since) if since not in (None, "") else None
    except ValueError:
        return _err(400, "bad_request", "since_minute must be an integer")
    keys = ("minute", "hr", "n", "core_est_c", "core_var", "psi", "level", "state", "wbgt_c", "flag")
    points = [{k: m.get(k) for k in keys} for m in deps.repo.get_minutes(session_id, since_minute)]
    return 200, {"session_id": session_id, "points": points}


def list_incidents(deps: Deps, status: str | None) -> tuple[int, dict]:
    items = deps.repo.list_incidents()
    if (status or "open") == "open":
        items = [i for i in items if i.get("status") in OPEN_STATUSES]
    items.sort(key=lambda i: i.get("opened_at", 0), reverse=True)
    site = deps.repo.get_site(os.environ.get("SITE_ID", "kgp")) or {}
    return 200, {"incidents": [_summary(i, site.get("env")) for i in items[:50]]}


def get_incident(deps: Deps, iid: str) -> tuple[int, dict]:
    inc = deps.repo.get_incident(iid)
    if inc is None:
        return _err(404, "unknown_incident", f"Incident {iid} does not exist.")
    out = {k: v for k, v in inc.items() if k not in PRIVATE_FIELDS}
    audio = {}
    for lang, key in (inc.get("audio") or {}).items():
        audio[lang] = deps.clients.s3.generate_presigned_url(
            ClientMethod="get_object", Params={"Bucket": deps.audio_bucket, "Key": key}, ExpiresIn=PRESIGN_S)
    out["audio"] = audio
    out["console_url"] = CONSOLE + inc["execution_arn"] if inc.get("execution_arn") else None
    site = deps.repo.get_site(os.environ.get("SITE_ID", "kgp")) or {}
    out["summary"] = _summary(inc, site.get("env"))
    return 200, out


def _send_success(clients: Clients, token: str, output: dict) -> None:
    try:
        clients.sfn.send_task_success(taskToken=token, output=json.dumps(output))
    except Exception as e:  # noqa: BLE001
        if error_code(e) in ("TaskTimedOut", "InvalidToken", "TaskDoesNotExist"):
            logger.warning("ack token rejected", extra={"code": error_code(e)})
        else:
            raise


def ack_incident(repo: Repo, clients: Clients, incident_id: str, username: str, note: str,
                 now_ms: int) -> tuple[int, dict]:
    inc = repo.get_incident(incident_id)
    if inc is None:
        return _err(404, "unknown_incident", f"Incident {incident_id} does not exist.")
    if inc.get("status") not in ACKABLE:
        return _err(409, "already_acknowledged", "Already acknowledged")
    token = inc.get("ack_token")
    try:
        repo.update_incident(incident_id, status_in=ACKABLE, status="ACKNOWLEDGED", acked_at=now_ms,
                             acked_by=username, ack_note=note, ack_pending=token is None)
    except ConditionFailed:
        return _err(409, "already_acknowledged", "Already acknowledged")
    repo.append_incident_event(incident_id, {"t": now_ms, "type": "ACKNOWLEDGED",
                                             "detail": f"by {username}" + (f": {note}" if note else "")})
    if token is None:
        # The workflow may have stored its token between our read and write; re-read to avoid a stuck wait.
        token = (repo.get_incident(incident_id) or {}).get("ack_token")
    if token:
        _send_success(clients, token, {"acked_by": username})
    return 200, {"status": "ACKNOWLEDGED"}


def refresh_context(deps: Deps) -> tuple[int, dict]:
    out = deps.clients.lam.invoke(FunctionName=deps.context_function, InvocationType="RequestResponse",
                                  Payload=b"{}")
    payload = json.loads(out["Payload"].read().decode("utf-8") or "{}")
    if out.get("FunctionError"):
        return _err(502, "context_failed", str(payload)[:200])
    return 200, {"env": payload.get("env")}


# --- routing -------------------------------------------------------------------------------------------------

def route(event: dict, deps: Deps, now_ms: int) -> tuple[int, dict]:
    key = event.get("routeKey", "")
    path = event.get("pathParameters") or {}
    query = event.get("queryStringParameters") or {}
    claims = (((event.get("requestContext") or {}).get("authorizer") or {}).get("jwt") or {}).get("claims") or {}
    if key == "GET /v1/roster":
        return roster(deps, now_ms)
    if key == "GET /v1/sessions/{session_id}/series":
        return series(deps, path.get("session_id", ""), query.get("since_minute"))
    if key == "GET /v1/incidents":
        return list_incidents(deps, query.get("status"))
    if key == "GET /v1/incidents/{incident_id}":
        return get_incident(deps, path.get("incident_id", ""))
    if key == "POST /v1/incidents/{incident_id}/ack":
        try:
            body = parse_body(event) or {}
        except ValueError:
            return _err(400, "bad_request", "Body is not valid JSON.")
        user = claims.get("cognito:username") or claims.get("username") or "supervisor"
        return ack_incident(deps.repo, deps.clients, path.get("incident_id", ""), user,
                            str(body.get("note", ""))[:200], now_ms)
    if key == "POST /v1/context/refresh":
        return refresh_context(deps)
    return _err(404, "not_found", key)


_DEPS: Deps | None = None


def _deps() -> Deps:
    global _DEPS
    if _DEPS is None:
        from wristheat.repo import DynamoRepo
        repo = DynamoRepo({k: os.environ.get(f"TABLE_{k.upper()}", "") for k in
                           ("sites", "trainees", "sessions", "readings", "minutes", "incidents")})
        _DEPS = Deps(repo=repo, clients=Clients(), context_function=os.environ.get("CONTEXT_FUNCTION_NAME", ""),
                     audio_bucket=os.environ.get("AUDIO_BUCKET", ""))
    return _DEPS


@logger.inject_lambda_context(clear_state=True)
@tracer.capture_lambda_handler
def handler(event, context):
    try:
        return respond(*route(event, _deps(), int(time.time() * 1000)))
    except Exception:
        logger.exception("api failed")
        return respond(500, {"error": "internal", "message": "Internal error."})
