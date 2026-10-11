"""Site environment context: Open-Meteo inputs, Liljegren WBGT, heat flag (spec §8)."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Env:
    wbgt_c: float | None
    flag: str
    pm25: float | None
    us_aqi: int | None
    updated_at: int
    temp_c: float | None = None
    rh: float | None = None
    wind_ms: float | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict | None) -> "Env | None":
        if not d:
            return None
        return cls(
            wbgt_c=d.get("wbgt_c"), flag=d.get("flag", "NONE"), pm25=d.get("pm25"),
            us_aqi=d.get("us_aqi"), updated_at=int(d.get("updated_at", 0)),
            temp_c=d.get("temp_c"), rh=d.get("rh"), wind_ms=d.get("wind_ms"),
        )


# --- Solar position, WBGT and Open-Meteo parsing (context Lambda only; numpy/thermofeel imported lazily) ---

import math  # noqa: E402
from datetime import datetime, timedelta, timezone  # noqa: E402

FORECAST_URL = ("https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,"
                "shortwave_radiation,direct_radiation"
                "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,"
                "shortwave_radiation_instant,direct_radiation_instant"
                "&wind_speed_unit=ms&timezone=auto&forecast_days=2")
AIR_URL = ("https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
           "&current=pm2_5,pm10,us_aqi&timezone=auto")


def cossza(lat: float, lon: float, when_utc: datetime) -> float:
    """Cosine of the solar zenith angle (NOAA approximation)."""
    doy = when_utc.timetuple().tm_yday
    hour = when_utc.hour + when_utc.minute / 60 + when_utc.second / 3600
    g = 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    ha = math.radians((hour * 60 + eqt + 4 * lon) / 4 - 180)
    la = math.radians(lat)
    return math.sin(la) * math.sin(decl) + math.cos(la) * math.cos(decl) * math.cos(ha)


def wbgt_liljegren_c(t_c, rh, p_hpa, wind10_ms, ssrd, direct, cz) -> float | None:
    """Open-field WBGT (°C) via thermofeel 2.3.0 Liljegren. None when an input is missing or the result is NaN."""
    if any(x is None for x in (t_c, rh, p_hpa, wind10_ms, ssrd, direct, cz)):
        return None
    import numpy as np
    import thermofeel

    fdir = min(1.0, max(0.0, direct / ssrd)) if ssrd >= 1 else 0.0
    arr = lambda x: np.array([float(x)])  # noqa: E731
    k = thermofeel.calculate_wbgt_liljegren(arr(t_c + 273.15), arr(rh), arr(p_hpa), arr(max(wind10_ms, 0.0)),
                                            arr(max(ssrd, 0.0)), arr(fdir), arr(cz))
    value = float(np.asarray(k).ravel()[0]) - 273.15
    return None if math.isnan(value) else value


def _local_to_utc(local_iso: str, offset_s: int) -> datetime:
    return (datetime.fromisoformat(local_iso) - timedelta(seconds=offset_s)).replace(tzinfo=timezone.utc)


def build_env(forecast_json: dict, air_json: dict | None, lat: float, lon: float,
              now_ms: int) -> tuple[Env, list[dict], dict]:
    """Current env, next-24-h hourly WBGT forecast and the coolest hour (05:00–19:00 local)."""
    from wristheat.strain import flag_for_wbgt

    if not isinstance(forecast_json, dict) or forecast_json.get("error") or "current" not in forecast_json \
            or "hourly" not in forecast_json:
        raise ValueError(f"unexpected forecast payload: {str(forecast_json)[:200]}")
    offset = int(forecast_json.get("utc_offset_seconds", 0))
    cur = forecast_json["current"]
    cz = cossza(lat, lon, _local_to_utc(cur["time"], offset))
    w = wbgt_liljegren_c(cur["temperature_2m"], cur["relative_humidity_2m"], cur["surface_pressure"],
                         cur["wind_speed_10m"], cur["shortwave_radiation"], cur["direct_radiation"], cz)
    air = (air_json or {}).get("current") or {}
    env = Env(wbgt_c=round(w, 1) if w is not None else None, flag=flag_for_wbgt(w), pm25=air.get("pm2_5"),
              us_aqi=air.get("us_aqi"), updated_at=now_ms, temp_c=cur["temperature_2m"],
              rh=cur["relative_humidity_2m"], wind_ms=cur["wind_speed_10m"])

    h = forecast_json["hourly"]
    cur_hour = cur["time"][:13]
    start = next((i for i, t in enumerate(h["time"]) if t[:13] >= cur_hour), 0)
    forecast, coolest = [], None
    for i in range(start, min(start + 24, len(h["time"]))):
        when = _local_to_utc(h["time"][i], offset)
        hw = wbgt_liljegren_c(h["temperature_2m"][i], h["relative_humidity_2m"][i], h["surface_pressure"][i],
                              h["wind_speed_10m"][i], h["shortwave_radiation_instant"][i],
                              h["direct_radiation_instant"][i], cossza(lat, lon, when))
        point = {"t": int(when.timestamp() * 1000), "wbgt_c": round(hw, 1) if hw is not None else None,
                 "flag": flag_for_wbgt(hw)}
        forecast.append(point)
        local_hour = int(h["time"][i][11:13])
        if hw is not None and 5 <= local_hour <= 19 and (coolest is None or hw < coolest["wbgt_c"]):
            coolest = {"local": f"{local_hour:02d}:00", "wbgt_c": round(hw, 1)}
    return env, forecast, coolest or {}


def load_site_env(repo, site_id: str, now_ms: int) -> Env | None:
    site = repo.get_site(site_id)
    return Env.from_dict(site.get("env")) if site else None
