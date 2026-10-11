"""Step Functions task: escalation step 'register' (spec §9)."""
from wristheat import escalation
from wristheat.obs import logger, tracer


def _deps():
    return escalation.default_deps()


@tracer.capture_lambda_handler
def handler(event, context):
    logger.info("esc_register", extra={"incident_id": event.get("incident_id"), "kind": event.get("kind")})
    iid = event["incident_id"]
    escalation.register(_deps(), iid, event["kind"], event["token"])
    return {"incident_id": iid}
