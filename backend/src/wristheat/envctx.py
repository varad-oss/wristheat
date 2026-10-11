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
