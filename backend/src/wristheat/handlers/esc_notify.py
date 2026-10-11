"""Step Functions task: escalation step 'notify' (spec §9)."""
import time

from wristheat import escalation
from wristheat.obs import logger, tracer


def _deps():
    return escalation.default_deps()


@tracer.capture_lambda_handler
def handler(event, context):
    logger.info("esc_notify", extra={"event": event})
    iid = event["incident_id"]
    now = int(time.time() * 1000)
    escalation.notify(_deps(), iid, now)
    return {"incident_id": iid}
