# R2-02 — Revised Problem & Mechanism Map

This file replaces the "whitespace" framing of `../06_WHITESPACE_MAP.md` with a map of **recurring decisions that fail**, and the **mechanism** that could fix each. The problem maps for each lens, with full citations, are in:
- [`evidence/A_concepts_personal_household.md`](evidence/A_concepts_personal_household.md)
- [`evidence/A_concepts_community_institutional.md`](evidence/A_concepts_community_institutional.md)
- [`evidence/A_concepts_mechanism_first.md`](evidence/A_concepts_mechanism_first.md)

Tags: FACT · INFERENCE · HYPOTHESIS.

---

## 1. What changed since round 1

| Round-1 belief | Round-2 evidence | Tag |
|---|---|---|
| Whitespace = "information without intervention" | The visible strong tail of the live field already names a decider, an action and a verification loop (ShiftShield, LeakLedger, JalSakshi, SiltProof…). That framing is now **table stakes** | FACT (111-project scan) / INFERENCE |
| Air is the most crowded track | **Heat & Water** is: 48% of 111 visible projects, driven by ~23 flood/waterlogging entries. Air is 31%; **Waste & Energy is 22%** | FACT (sample) |
| Worker WBGT planners and school clean-hour planners are whitespace | Both are now contested: 5 worker-heat planners, 10 school-air planners | FACT |
| Rooftop-solar post-install, tanker verification, SWM bulk-generator compliance, ToD shifting and picker pricing are rare | **Still rare** (0 found), but each fails a round-2 constraint (data access, outside stakeholder, or small stakes) | FACT / INFERENCE |
| Field size | ~730 submissions expected (8,653 registrations × First Commit's 8.6% submission ratio; plausible 600–900) | FACT (registrations, live API) / INFERENCE |
| Deadline unknown | **Submissions open Sun 11 Oct 08:00 IST and the event ends Sun 11 Oct 20:00 IST** (`end_date 2026-10-11T14:30:00Z`) | FACT (WeMakeDevs API, checked 9 Oct 22:20 IST) |

---

## 2. Recurring decisions that fail today

The **Data** column shows whether data exists and how it was verified. The **Feedback?** column shows whether the decider ever learns if the action worked.

| # | Recurring decision | Decider | How often | Data exists? | Why it fails today | Feedback? | Season fit (Oct) |
|---|---|---|---|---|---|---|---|
| D1 | How many AC/cooler hours fit this billing cycle before I lose the free-unit benefit? | Bill-payer in a threshold state (~5 crore households; ~3.5 crore in true-cliff states) | Daily, Apr–Oct | Meter register, weather forecast, scheme rules (FACT, partly verified) | The cliff is discovered on the bill. No DISCOM app found projects against it (21 listings checked) | No | Weak in north, OK in south |
| D2 | Did my saving work, or was it the weather? | Any household | Monthly | Bill history + ERA5 (FACT) | Weather swamps behaviour; "my bill went up" is unexplained | No | **Live hook: Oct 2026 is hotter than Oct 2025 in Delhi** (~95 vs 66 cooling degree-days) |
| D3 | Cooler, fan or close up, hour by hour? | 14% of households nationally use coolers (FACT, per notes) | Hourly, Apr–Sep | Hourly wet-bulb (FACT) | Humidity cancels evaporative cooling. But **an app already does this** (Evaporative Cooler Forecaster, 2025) | No | Weak |
| D4 | Should I keep exerting in this heat right now? | Anyone working, training or testing outdoors | Per session | Live heart rate from own watch (VERIFIED-BUT-CONSTRAINED by model); WBGT (FACT) | Weather tools give one number for everyone. **The body's response is ignored.** Jharkhand 2024: 12 candidates died in a 10 km recruitment run (FACT) | Partly (HR) | Afternoons still 33–38 °C in several cities (FACT) |
| D5 | Is this neighbour OK in today's heat? | RWA volunteer | Heatwave days | Forecasts (FACT) | No Indian registry/check-in scheme found (FACT, not exhaustive) | No | Off-season |
| D6 | Which mode/time for my commute (dose)? | Commuter | Daily | CAMS 45 km keyless; stations need a key (FACT) | Apps show ambient AQI, not dose. **But 6+ live entries already do dose** | No | Smog season starting |
| D7 | Open windows tonight? | Non-AC household | Daily | Temperature + PM forecasts (FACT) | A real trade-off, but the indoor PM benefit is contested and unverifiable without a sensor | No | Smog season |
| D8 | How big should our RWH tank/pit be, and is it worth it? | RWA committee | Yearly | Overture roofs (VERIFIED) + daily rain (VERIFIED-BUT-CONSTRAINED, −48% to +33% vs IMD) | Calculators use annual averages and imply 100% capture | No | NE monsoon starting (Chennai) |
| D9 | Where to plant for shade on paths people walk? | Campus estate / eco-club | Yearly | Canopy height CHMv2 on AWS (VERIFIED); no Indian building heights (UNSUPPORTED) | Plantation counts saplings, not shade delivered | No | Neutral |
| D10 | Did the "resolved" complaint stay fixed? | Reporter / RWA | Per complaint | No timestamped open data (FACT) | Closure is the metric, not durability | No | Neutral |
| D11 | Was the tanker short? Is the price fair? | Society manager | Per delivery | User photos only | Informal market | No | Off-season |
| D12 | Is my rooftop solar under-performing? | PM Surya Ghar owner | Weekly | Satellite irradiance (VERIFIED); **owner data unavailable to the team** | Owners stop monitoring | No | Good, but no data |

---

## 3. Mechanism families

These are the reusable "why it would work" engines behind the concepts. Each family records whether the mechanism appears in the competition: in the live field of 111 projects, and in student repos created in Sep–Oct 2026.

| Mechanism | What it does | Defensible because… | Already common in the field? | Concepts |
|---|---|---|---|---|
| **M&V counterfactual** (weather-normalised baseline) | Separates the household's behaviour from the weather | An engineering standard (IPMVP / CalTRACK) that no Indian consumer tool packages (FACT for the listings checked) | Bill analysers are common: **21 "bijli" repos since 25 Sep** (FACT, GitHub API). Weather normalisation is rare | Bijli Budget |
| **Threshold projection with probability** | P(cross the policy cliff before cycle end) → daily budget | Policy-specific; pro-rating rules (FACT, TPDDL) | SmartBill (BESCOM) predicts the next bill with temperature; no probability or budget found | Bijli Budget |
| **Physiological state estimation** (Kalman filter on HR → core temperature, ECTemp) | Turns a consumer heart-rate stream into an estimated heat-strain state | Published USARIEM model with public parameters; validated on chest straps (±0.63 °C) | **0 of 111 live projects; 0 GitHub repos** for heat strain from HR since Sep (FACT) | WristHeat |
| **Psychrometric scheduling** | Wet-bulb → cooler outlet → mode by hour | Physics | **An app exists** (Evaporative Cooler Forecaster, WetBulbCast) | CoolerCheck |
| **Daily-replay water balance** | Real daily rain through tank and overflow | Changes the sizing answer (52–73% capture vs the 100% implied) | SimTanka, a Jal Shakti 2025 winner, and **14 RWH repos since 1 Oct** (SIH PS 53 genre) | Monsoon Replay |
| **Dose attribution** | Trips × PM × mode factors → ranked swaps | Literature factors | **6+ live entries already** (ALive, EcoRoute AI, Breathe Route…) | Dose Ledger |
| **Escalation ladder with timeouts** | Buddy → backup → secretary | Step Functions `waitForTaskToken` | Same pattern as last event's 1st prize (Suraksha) | Heat Roll-Call |
| **Durability measurement** (survival curve) | Re-checks after "resolved" | New metric (resolution half-life) | Rare | ReCheck |
| **Greedy placement over a shade model** | Plant where marginal shade-minutes are highest | Placement optimisation unclaimed | WRI Cool Cities already maps shade for 27 cities | ShadeSite |

---

## 4. Where a better solution is now possible (and why)

| Gap | Why now | Why teams miss it | Tag |
|---|---|---|---|
| **Body-aware heat risk** | Web Bluetooth can read the standard heart-rate service in Chrome. Garmin, COROS, Polar, Amazfit (Zepp OS 3+) and some Huawei watches broadcast it. The ECTemp parameters are public | Heat entries all start from weather. Wearable APIs are closed (Fitbit and Garmin cloud), so teams assume wearables are off-limits | FACT / INFERENCE |
| **Weather-adjusted household bills** | ERA5 and forecasts are keyless (FACT). Free-unit schemes cover ~5 crore households (FACT, partial) | Bill tools stop at OCR and slab maths | FACT / INFERENCE |
| **Event-scale rainfall replay for societies** | Overture footprints are queryable in place on AWS (VERIFIED) | Calculators use annual averages | FACT |

---

## 5. Constraints that now filter every concept

These come from the user's brief, checked against evidence.

| Code | Constraint | Practical test |
|---|---|---|
| A | Software-only | Runs on a phone, laptop or the team's own watch; nothing bought |
| B | 48-hour feasibility | The main journey is built and filmed by **Sun 16:00 IST** (internal), 4 h before the real 20:00 cutoff |
| C | Accessible data | Each data step is VERIFIED or VERIFIED-BUT-CONSTRAINED, with no unverified critical dependency |
| D | Broad relevance | The underlying decision recurs for many people across cities; no single outside stakeholder is required |
| E | Genuine differentiation | The mechanism is not present in the live field and not trivially present in a mainstream product |
| F | Observable result | An action → a visible result **inside the video**, ideally physical and in one take |
| G | AWS | Each service performs a verb in the story |
