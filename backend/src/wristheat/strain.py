"""Physiological Strain Index, TB MED 507 heat flags, candidate levels, projection (spec §7.3–7.5)."""
from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from wristheat import ectemp

if TYPE_CHECKING:
    from wristheat.envctx import Env

FLAG_ORDER = ("NONE", "WHITE", "GREEN", "YELLOW", "RED", "BLACK")
STALE_MS = 45 * 60 * 1000

_FLAG_CUTS = ((32.2, "BLACK"), (31.1, "RED"), (29.5, "YELLOW"), (27.8, "GREEN"), (25.6, "WHITE"))


def psi(ct: float, hr: float, hr0: int) -> float:
    """Moran 1998 PSI, unrounded, clamped to [0, 10]."""
    value = 5 * (ct - 37.1) / (39.5 - 37.1) + 5 * (hr - hr0) / (180 - hr0)
    return min(10.0, max(0.0, value))


def flag_for_wbgt(wbgt_c: float | None) -> str:
    if wbgt_c is None:
        return "NONE"
    w = round(wbgt_c, 1)
    for cut, flag in _FLAG_CUTS:
        if w >= cut:
            return flag
    return "NONE"


def is_stale(env: "Env | None", now_ms: int) -> bool:
    return env is None or now_ms - env.updated_at > STALE_MS


def effective_flag(env: "Env | None", now_ms: int) -> str:
    """The flag the engine uses: NONE (body-only) when env is missing, stale or has no WBGT."""
    if env is None or is_stale(env, now_ms) or env.wbgt_c is None:
        return "NONE"
    return env.flag


def candidate_level(psi_value: float, ct: float, flag: str) -> Literal["GREEN", "AMBER", "RED"]:
    hot = flag in ("RED", "BLACK")
    warm = flag in ("YELLOW", "RED", "BLACK")
    if psi_value >= 7.0 or ct >= 39.0 or (psi_value >= 6.0 and hot):
        return "RED"
    if psi_value >= 5.0 or (psi_value >= 4.0 and warm):
        return "AMBER"
    return "GREEN"


def project_minutes_to_red(ct: float, v: float, hr_mean: float, hr0: int, flag: str, limit: int = 90) -> int | None:
    """Steps the filter forward at a constant HR; first n (1..limit) where the RED rule holds."""
    for n in range(1, limit + 1):
        ct, v = ectemp.step(ct, v, hr_mean)
        if candidate_level(psi(ct, hr_mean, hr0), ct, flag) == "RED":
            return n
    return None
