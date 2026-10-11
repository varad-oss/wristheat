"""ECTemp: Kalman-filter estimate of core temperature from heart rate (spec §7.2).

Buller et al. 2013; US patent 10702165B2; USARIEM T17-08. Initial variance per de Korte 2022.
"""
from collections.abc import Sequence

B0 = -7887.1
B1 = 384.4286
B2 = -4.5714
GAMMA2 = 0.000484  # process variance per minute (0.022²)
SIGMA2 = 356.5654  # measurement variance (18.88²)
CT0 = 37.1
V0 = 0.02


def step(ct: float, v: float, hr: float) -> tuple[float, float]:
    """One-minute filter update with the minute's mean heart rate."""
    v_p = v + GAMMA2
    c = 2 * B2 * ct + B1
    k = v_p * c / (c * c * v_p + SIGMA2)
    ct_new = ct + k * (hr - (B2 * ct * ct + B1 * ct + B0))
    v_new = (1 - k * c) * v_p
    return ct_new, v_new


def run(hrs: Sequence[float], ct: float = CT0, v: float = V0) -> list[tuple[float, float]]:
    """Runs the filter over per-minute heart rates; returns (ct, v) after each minute."""
    out = []
    for hr in hrs:
        ct, v = step(ct, v, hr)
        out.append((ct, v))
    return out
