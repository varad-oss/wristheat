"""Incidents: ids, opening, facts, metrics and reports (spec §6, §9)."""
from __future__ import annotations

from wristheat.engine import EngineState
from wristheat.envctx import Env
from wristheat.repo import ttl_for


def incident_id_for(session_id: str, now_ms: int) -> str:
    return f"inc-{session_id[:8]}-{now_ms}"


def red_rule(psi: float, ct: float, flag: str) -> str:
    if psi >= 7.0:
        return "psi>=7"
    if ct >= 39.0:
        return "core>=39"
    return "psi>=6 & flag"


def open_incident(trainee: dict, session_id: str, st: EngineState, env: Env | None, now_ms: int,
                  flag: str = "NONE", incident_id: str | None = None) -> dict:
    last = st.history[-1] if st.history else {}
    psi = st.psi or 0.0
    trigger = {"psi": round(psi, 1), "core_est_c": round(st.ct, 2), "hr": round(last.get("hr", st.hr_now or 0)),
               "wbgt_c": env.wbgt_c if env else None, "flag": flag, "pm25": env.pm25 if env else None,
               "rule": red_rule(psi, st.ct, flag)}
    iid = incident_id or incident_id_for(session_id, now_ms)
    return {"incident_id": iid, "trainee_id": trainee["trainee_id"], "trainee_name": trainee.get("name", ""),
            "trainee_kind": trainee.get("kind", "real"), "session_id": session_id, "status": "NOTIFIED",
            "opened_at": now_ms, "trigger": trigger,
            "events": [{"t": now_ms, "type": "OPENED", "detail": f"RED entered ({trigger['rule']})"}],
            "ack_pending": False, "ttl": ttl_for("incidents", now_ms)}
