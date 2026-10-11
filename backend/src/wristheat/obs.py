"""Observability: Powertools logger/tracer and EMF metrics, plus an in-memory record for tests."""
from __future__ import annotations

import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.metrics import MetricUnit, single_metric

NAMESPACE = "WristHeat"
logger = Logger(service="wristheat")
tracer = Tracer(service="wristheat")
RECORDED: list[tuple[str, float, dict]] = []


def metric(name: str, value: float = 1, unit: str = "Count", **dims: str) -> None:
    """Records one metric (EMF to stdout in Lambda). Never raises."""
    RECORDED.append((name, value, dims))
    if os.environ.get("WRISTHEAT_METRICS_OFF") == "1":
        return
    try:
        with single_metric(name=name, unit=getattr(MetricUnit, unit), value=value, namespace=NAMESPACE) as m:
            for k, v in dims.items():
                m.add_dimension(name=k, value=str(v))
    except Exception:  # noqa: BLE001 — metrics must never break a request
        logger.exception("metric emit failed", extra={"metric": name})
