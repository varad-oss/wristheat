"""Escalation workflow steps run by the Step Functions Lambdas (spec §9)."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

from wristheat import incidents
from wristheat.advice import advice_for, is_indoors
from wristheat.clients import Clients, error_code
from wristheat.obs import logger
from wristheat.repo import ConditionFailed, Repo

POLLY_TRIES = {"en": [("Kajal", "neural", "en-IN")],
               "hi": [("Kajal", "neural", "hi-IN"), ("Aditi", "standard", "hi-IN")]}


@dataclass
class Config:
    supervisor_topic: str
    backup_topic: str
    audio_bucket: str
    dashboard_url: str
    model_id: str
    site_id: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(os.environ.get("SUPERVISOR_TOPIC_ARN", ""), os.environ.get("BACKUP_TOPIC_ARN", ""),
                   os.environ.get("AUDIO_BUCKET", ""), os.environ.get("DASHBOARD_URL", "(dashboard pending)"),
                   os.environ.get("BEDROCK_MODEL_ID", ""), os.environ.get("SITE_ID", "kgp"))


@dataclass
class Deps:
    repo: Repo
    clients: Clients
    cfg: Config


def _event(deps: Deps, iid: str, now_ms: int, kind: str, detail: str = "") -> None:
    deps.repo.append_incident_event(iid, {"t": now_ms, "type": kind, "detail": detail})


def _link(deps: Deps, iid: str) -> str:
    base = deps.cfg.dashboard_url
    return f"{base}/incidents/{iid}" if base.startswith("http") else base


def _label(inc: dict) -> str:
    return "[SIMULATED] " if inc.get("trainee_kind") == "simulated" else ""


def ascii_subject(subject: str) -> str:
    """SNS subjects must be ASCII without line breaks, at most 100 chars."""
    s = subject.replace("—", "-").replace("–", "-").replace("\n", " ")
    s = s.encode("ascii", "ignore").decode("ascii")
    return " ".join(s.split())[:100] or "WristHeat alert"


def _publish(deps: Deps, topic: str, subject: str, message: str) -> None:
    if not topic:
        logger.warning("no SNS topic configured", extra={"subject": subject})
        return
    deps.clients.sns.publish(TopicArn=topic, Subject=ascii_subject(subject), Message=message)


def _synth(deps: Deps, text: str, lang: str) -> bytes:
    last = None
    for voice, engine, code in POLLY_TRIES[lang]:
        try:
            out = deps.clients.polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice, Engine=engine,
                                                       LanguageCode=code)
            return out["AudioStream"].read()
        except Exception as e:  # noqa: BLE001
            last = e
            logger.warning("polly voice failed", extra={"voice": voice, "engine": engine, "code": error_code(e)})
    raise last  # type: ignore[misc]


def _alert_message(deps: Deps, inc: dict, intro: str) -> str:
    t = inc.get("trigger") or {}
    advice = advice_for("RED", t.get("pm25"), "NONE")["en"]
    lines = [intro, "",
             f"Trainee: {inc.get('trainee_name')} ({'SIMULATED' if inc.get('trainee_kind') == 'simulated' else 'LIVE'})",
             f"Strain index (PSI): {t.get('psi')}   Est. core: {t.get('core_est_c')} ± 0.6 °C   HR: {t.get('hr')} bpm",
             f"Open-field WBGT: {t.get('wbgt_c')} °C ({t.get('flag')} flag)   PM2.5: {t.get('pm25')} µg/m³",
             f"Rule: {t.get('rule')}", "", f"Advice: {advice}", "", f"Open the incident: {_link(deps, inc['incident_id'])}",
             "", "Estimated values from a research prototype; not a medical device."]
    return "\n".join(lines)


def notify(deps: Deps, iid: str, now_ms: int) -> None:
    inc = deps.repo.get_incident(iid)
    t = inc.get("trigger") or {}
    name = inc.get("trainee_name") or inc.get("trainee_id")
    audio = {}
    try:
        texts = incidents.polly_texts(name, float(t.get("psi") or 0), t.get("wbgt_c"), is_indoors(t.get("pm25")))
        for lang in ("en", "hi"):
            key = f"audio/{iid}/{lang}.mp3"
            deps.clients.s3.put_object(Bucket=deps.cfg.audio_bucket, Key=key, Body=_synth(deps, texts[lang], lang),
                                       ContentType="audio/mpeg")
            audio[lang] = key
    except Exception:  # noqa: BLE001 — the email must still go out
        logger.exception("audio synthesis failed")
    _publish(deps, deps.cfg.supervisor_topic, f"{_label(inc)}WristHeat RED: {name} must stop now",
             _alert_message(deps, inc, f"Heat-strain RED alert for {name}."))
    deps.repo.update_incident(iid, audio=audio)
    _event(deps, iid, now_ms, "NOTIFIED", "Supervisor emailed")
    if audio:
        _event(deps, iid, now_ms, "AUDIO_READY", "English and Hindi voice alerts ready")


def _succeed(deps: Deps, token: str, output: dict) -> None:
    try:
        deps.clients.sfn.send_task_success(taskToken=token, output=json.dumps(output))
    except Exception as e:  # noqa: BLE001
        if error_code(e) in ("TaskTimedOut", "InvalidToken", "TaskDoesNotExist"):
            logger.warning("task token rejected", extra={"code": error_code(e)})
        else:
            raise


def register(deps: Deps, iid: str, kind: str, token: str) -> None:
    """Stores the task token; succeeds immediately if the awaited fact already happened."""
    if kind == "ack":
        deps.repo.update_incident(iid, ack_token=token)
        inc = deps.repo.get_incident(iid)
        if inc.get("ack_pending") or inc.get("acked_at"):
            _succeed(deps, token, {"acked": True})
    elif kind == "recovery":
        deps.repo.update_incident(iid, recovery_token=token)
        inc = deps.repo.get_incident(iid)
        if inc.get("recovered_at"):
            _succeed(deps, token, {"recovered": True})
    else:
        raise ValueError(f"unknown kind {kind}")


def escalate(deps: Deps, iid: str, now_ms: int) -> None:
    try:
        deps.repo.update_incident(iid, status_in=("NOTIFIED",), status="ESCALATED", escalated_at=now_ms)
    except ConditionFailed:
        logger.info("incident no longer NOTIFIED; escalating email anyway", extra={"incident_id": iid})
    inc = deps.repo.get_incident(iid)
    name = inc.get("trainee_name")
    _publish(deps, deps.cfg.backup_topic, f"{_label(inc)}ESCALATED WristHeat RED: {name} - supervisor has not responded",
             _alert_message(deps, inc, f"ESCALATION: the supervisor has not acknowledged the RED alert for {name}."))
    _event(deps, iid, now_ms, "ESCALATED", "Backup contact emailed")


def close(deps: Deps, iid: str, now_ms: int) -> dict:
    inc = deps.repo.get_incident(iid)
    if inc.get("recovered_at"):
        outcome = "recovered" if inc.get("acked_at") else "recovered_unacknowledged"
    else:
        outcome = "not_confirmed"
    inc["outcome"] = outcome
    since = (inc.get("opened_at") or now_ms) // 60_000 - 1
    minutes = [m for m in deps.repo.get_minutes(inc["session_id"], since) if m["minute"] * 60_000 <= now_ms]
    metrics = incidents.compute_metrics(inc, minutes)
    site = deps.repo.get_site(deps.cfg.site_id) or {}
    facts = incidents.report_facts(inc, metrics, site)
    text, source = incidents.bedrock_report(deps.clients, deps.cfg.model_id, facts)
    report = {"text": text, "source": source, "model": deps.cfg.model_id if source == "bedrock" else None,
              "generated_at": now_ms}
    deps.repo.update_incident(iid, status="CLOSED", closed_at=now_ms, outcome=outcome, metrics=metrics, report=report)
    _event(deps, iid, now_ms, "REPORT_READY", f"Report by {'Amazon Bedrock' if source == 'bedrock' else 'template'}")
    _event(deps, iid, now_ms, "CLOSED", outcome)
    name = inc.get("trainee_name")
    _publish(deps, deps.cfg.supervisor_topic, f"{_label(inc)}WristHeat resolved: {name} ({outcome.replace('_', ' ')})",
             "\n".join([f"Incident for {name} closed: {outcome.replace('_', ' ')}.",
                        f"Time to acknowledge: {metrics['time_to_ack_s']} s",
                        f"Time to confirmed recovery: {metrics['time_to_recovery_s']} s",
                        f"Minutes in RED: {metrics['minutes_in_red']}",
                        f"Incident: {_link(deps, iid)}"]))
    return {"incident_id": iid, "outcome": outcome}


_DEPS: Deps | None = None


def default_deps() -> Deps:
    global _DEPS
    if _DEPS is None:
        from wristheat.repo import DynamoRepo
        repo = DynamoRepo({k: os.environ.get(f"TABLE_{k.upper()}", "") for k in
                           ("sites", "trainees", "sessions", "minutes", "incidents")})
        _DEPS = Deps(repo, Clients(), Config.from_env())
    return _DEPS
