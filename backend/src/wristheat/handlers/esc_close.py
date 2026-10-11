"""Step Functions task: escalation step 'close' (spec §9)."""
import time

from wristheat import escalation
from wristheat.obs import logger, tracer


def _deps():
    return escalation.default_deps()


@tracer.capture_lambda_handler
def handler(event, context):
    logger.info("esc_close", extra={"event": event})
    iid = event["incident_id"]
    now = int(time.time() * 1000)
    return escalation.close(_deps(), iid, now)
