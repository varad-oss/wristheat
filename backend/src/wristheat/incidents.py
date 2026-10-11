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


# --- Voice alert, metrics and reports (spec §9) ------------------------------------------------------

import json  # noqa: E402
from datetime import datetime, timedelta, timezone  # noqa: E402

from wristheat.obs import logger, metric  # noqa: E402

IST = timezone(timedelta(hours=5, minutes=30))
REPORT_SUFFIX = "Estimated values; not a medical assessment."
SYSTEM_PROMPT = (
    "You write short factual incident summaries for a heat-strain monitoring prototype. Use only the facts in the "
    "JSON you are given. Do not diagnose, do not speculate about medical causes, and do not invent any number. "
    "Write at most 120 words in plain English: what triggered the alert, the response timeline with times, whether "
    "recovery was confirmed by the data, and one practical suggestion for the next session that follows from the "
    "facts (for example the coolest hour). End with: \"Estimated values; not a medical assessment.\""
)


def polly_texts(name: str, psi: float, wbgt: float | None, indoors: bool) -> dict[str, str]:
    place_en, place_hi = ("indoors", "अंदर") if indoors else ("shade", "छाँव में")
    wbgt_part = f" Open-field W B G T {wbgt:.1f} degrees." if wbgt is not None else ""
    en = (f"Heat alert. {name} needs to stop now. Strain index {psi:.1f}.{wbgt_part} "
          f"Move them to {place_en} and cool them with water.")
    hi = f"गर्मी की चेतावनी। {name} को अभी रुकना होगा। उन्हें {place_hi} ले जाएँ और पानी से ठंडा करें।"
    return {"en": en, "hi": hi}


def _secs(a, b):
    return int(round((a - b) / 1000)) if a and b else None


def compute_metrics(incident: dict, minutes: list[dict]) -> dict:
    opened = incident.get("opened_at")
    psis = [m["psi"] for m in minutes if m.get("psi") is not None]
    cores = [m["core_est_c"] for m in minutes if m.get("core_est_c") is not None]
    return {
        "time_to_ack_s": _secs(incident.get("acked_at"), opened),
        "time_to_recovery_s": _secs(incident.get("recovered_at"), opened),
        "minutes_in_red": sum(1 for m in minutes if m.get("state") == "RED"),
        "peak_psi": round(max(psis), 1) if psis else (incident.get("trigger") or {}).get("psi"),
        "peak_core_c": round(max(cores), 2) if cores else (incident.get("trigger") or {}).get("core_est_c"),
        "escalated": any(e.get("type") == "ESCALATED" for e in incident.get("events", [])),
    }


def hhmm(ms: int | None, seconds: bool = False) -> str | None:
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, IST).strftime("%H:%M:%S" if seconds else "%H:%M")


def report_facts(incident: dict, metrics: dict, site: dict) -> dict:
    kind = incident.get("trainee_kind", "real")
    return {
        "trainee": incident.get("trainee_name") or incident.get("trainee_id"),
        "trainee_label": "SIMULATED" if kind == "simulated" else "LIVE",
        "site": site.get("name"),
        "alert_time_ist": hhmm(incident.get("opened_at")),
        "trigger": incident.get("trigger"),
        "timeline_ist": [{"time": hhmm(e["t"], seconds=True), "event": e["type"], "detail": e.get("detail", "")}
                         for e in incident.get("events", [])],
        "acknowledged_by": incident.get("acked_by"),
        "acknowledged_at_ist": hhmm(incident.get("acked_at")),
        "recovery_confirmed_at_ist": hhmm(incident.get("recovered_at")),
        "outcome": incident.get("outcome"),
        "metrics": metrics,
        "coolest_hour_next_24h": site.get("coolest_hour") or None,
        "values_are_estimates": True,
    }


def template_report(facts: dict) -> str:
    t, m = facts.get("trigger") or {}, facts.get("metrics") or {}
    who = f"{facts['trainee']} ({facts['trainee_label']})"
    parts = [f"{who} triggered a RED heat-strain alert at {facts['alert_time_ist']} IST"
             + (f" at {facts['site']}" if facts.get("site") else "") + ":"
             f" strain index {t.get('psi')}, estimated core {t.get('core_est_c')} °C, heart rate {t.get('hr')} bpm"
             + (f", open-field WBGT {t.get('wbgt_c')} °C ({t.get('flag')} flag)" if t.get("wbgt_c") is not None else "")
             + "."]
    if m.get("escalated"):
        esc = next((x["time"][:5] for x in facts.get("timeline_ist", []) if x["event"] == "ESCALATED"), None)
        parts.append(f"No acknowledgement within the window, so it was escalated to the backup contact at {esc}.")
    if facts.get("acknowledged_at_ist"):
        parts.append(f"Acknowledged by {facts.get('acknowledged_by')} at {facts['acknowledged_at_ist']}"
                     f" ({m.get('time_to_ack_s')} s after the alert).")
    else:
        parts.append("No acknowledgement was recorded.")
    if facts.get("recovery_confirmed_at_ist"):
        parts.append(f"Recovery was confirmed by the data at {facts['recovery_confirmed_at_ist']},"
                     f" {round((m.get('time_to_recovery_s') or 0) / 60)} min after the alert;"
                     f" {m.get('minutes_in_red')} min were spent in RED.")
    else:
        parts.append("Recovery was not confirmed by the data within the wait window.")
    ch = facts.get("coolest_hour_next_24h") or {}
    if ch.get("local"):
        parts.append(f"Next session: schedule hard effort near {ch['local']} (forecast WBGT {ch.get('wbgt_c')} °C).")
    parts.append(REPORT_SUFFIX)
    return " ".join(parts)


def bedrock_report(clients, model_id: str, facts: dict) -> tuple[str, str]:
    """(text, source). Falls back to the deterministic template on any error."""
    if model_id:
        try:
            out = clients.bedrock.converse(
                modelId=model_id,
                system=[{"text": SYSTEM_PROMPT}],
                messages=[{"role": "user", "content": [{"text": json.dumps(facts, ensure_ascii=False)}]}],
                inferenceConfig={"maxTokens": 400, "temperature": 0.2},
            )
            text = out["output"]["message"]["content"][0]["text"].strip()
            if text:
                if not text.endswith(REPORT_SUFFIX):
                    text = f"{text} {REPORT_SUFFIX}"
                return text, "bedrock"
        except Exception:  # noqa: BLE001
            logger.exception("bedrock report failed; using template")
    metric("BedrockFallbacks", 1)
    return template_report(facts), "template"
