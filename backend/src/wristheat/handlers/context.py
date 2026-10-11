"""Context Lambda: refreshes site WBGT and air quality from Open-Meteo (spec §8). Scheduled every 10 min."""
from __future__ import annotations

import json
import os
import time
import urllib.request
from typing import Callable

from wristheat import envctx
from wristheat.obs import logger, metric, tracer


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"user-agent": "wristheat/1.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))


def refresh_site(repo, site_id: str, now_ms: int, fetch: Callable[[str], dict] = http_json) -> dict | None:
    """Fetches and stores the site's env. On failure keeps the previous env and returns it."""
    site = repo.get_site(site_id) or {"site_id": site_id}
    lat, lon = float(site.get("lat", 22.3149)), float(site.get("lon", 87.3105))
    try:
        forecast = fetch(envctx.FORECAST_URL.format(lat=lat, lon=lon))
        try:
            air = fetch(envctx.AIR_URL.format(lat=lat, lon=lon))
            if air.get("error") or "current" not in air:
                raise ValueError(f"unexpected air payload: {str(air)[:200]}")
        except Exception:  # noqa: BLE001 — air is optional; WBGT still works
            logger.exception("air quality fetch failed")
            metric("ContextFetchErrors", 1, source="air")
            air = None
        env, hourly, coolest = envctx.build_env(forecast, air, lat, lon, now_ms)
    except Exception:  # noqa: BLE001
        logger.exception("context fetch failed; keeping previous env")
        metric("ContextFetchErrors", 1, source="forecast")
        return site.get("env")
    site.update(env=env.to_dict(), env_updated_at=now_ms, forecast=hourly, coolest_hour=coolest)
    repo.put_site(site)
    logger.info("context refreshed", extra={"site_id": site_id, "wbgt_c": env.wbgt_c, "flag": env.flag})
    return site["env"]


@logger.inject_lambda_context(clear_state=True)
@tracer.capture_lambda_handler
def handler(event, context):
    from wristheat.repo import DynamoRepo
    repo = DynamoRepo({"sites": os.environ["TABLE_SITES"]})
    site_id = (event or {}).get("site_id") or os.environ.get("SITE_ID", "kgp")
    env = refresh_site(repo, site_id, int(time.time() * 1000))
    return {"env": env}
