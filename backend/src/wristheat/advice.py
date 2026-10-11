"""Wearer advice text, EN and HI, verbatim from spec §7.7."""
from __future__ import annotations

PM25_INDOORS = 60  # India's 24-h PM2.5 standard, µg/m³

_TEXT = {
    "CALIBRATING": ("Sit still — measuring your resting heart rate.",
                    "स्थिर बैठें — आपकी आराम की हृदय गति मापी जा रही है।"),
    "GREEN": ("Strain low. Keep drinking water.", "तनाव कम है। पानी पीते रहें।"),
    "AMBER": ("Strain rising. Slow down and drink water.", "तनाव बढ़ रहा है। गति धीमी करें और पानी पिएँ।"),
    "RED_OUT": ("Stop now. Rest in shade and cool down with water.",
                "अभी रुकें। छाँव में आराम करें और पानी से शरीर ठंडा करें।"),
    "RED_IN": ("Stop now. Rest indoors — outdoor air is poor (PM2.5 {pm25} µg/m³).",
               "अभी रुकें। अंदर आराम करें — बाहर की हवा खराब है (PM2.5 {pm25} µg/m³)।"),
    "RECOVERING_OUT": ("Recovering. Stay in shade until cleared.", "रिकवरी जारी है। साफ़ संकेत मिलने तक छाँव में रहें।"),
    "RECOVERING_IN": ("Recovering. Stay indoors until cleared.", "रिकवरी जारी है। साफ़ संकेत मिलने तक अंदर रहें।"),
    "RECOVERED": ("Recovery confirmed. Resume only at an easier pace.",
                  "रिकवरी की पुष्टि हुई। अब केवल धीमी गति से दोबारा शुरू करें।"),
}


def is_indoors(pm25: float | None) -> bool:
    return pm25 is not None and pm25 > PM25_INDOORS


def advice_for(state: str, pm25: float | None, alert: str) -> dict[str, str]:
    if alert == "RECOVERED":
        key = "RECOVERED"
    elif state in ("RED", "RECOVERING"):
        key = f"{state}_{'IN' if is_indoors(pm25) else 'OUT'}"
    else:
        key = state if state in _TEXT else "GREEN"
    en, hi = _TEXT[key]
    if "{pm25}" in en:
        value = str(int(round(pm25)))
        en, hi = en.replace("{pm25}", value), hi.replace("{pm25}", value)
    return {"en": en, "hi": hi}
