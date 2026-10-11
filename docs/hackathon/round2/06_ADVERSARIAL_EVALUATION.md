# R2-06 — Adversarial Evaluation of the Five Finalists

This file red-teams the five finalists from 05. Each finalist is attacked by six personas, then **revised or rejected**. Earlier effort spent on an idea earned it no protection.

Personas: **J** skeptical judge · **C** competitor building the same idea · **U** user deciding whether it's worth it · **E** senior engineer · **I** impact reviewer · **A** audience seeing the video for the first time.

---

## 1. WristHeat: body-aware heat strain from the watch you already wear

| Persona | Attack | Assessment |
|---|---|---|
| **J** | "That 'core temperature' is just smoothed heart rate. It can't tell heat from effort or nerves. It's never been validated on wrist optical sensors, it misses more than half of cases above 39 °C, and Garmin shipped this in 2021." | **Strongest objection.** The validity gap on wrist PPG is real (❌ in 05). Garmin's field exists but is Garmin-only and has no environment, group or recovery logic |
| **C** | "I'd add WBGT to my existing heat planner and call it personal." | The five live heat planners are weather-only. Body-signal ingestion via Web Bluetooth is unfamiliar ground, so copying it in the remaining 46 h is unlikely (INFERENCE) |
| **U** (runner, outdoor worker, coach) | "My watch already shows heart rate. Why do I need this?" | HR alone doesn't say *when to stop in this heat*. The useful output is "you have ~9 min at this effort before the strain limit; slow to 140 or rest in shade". **For a coach or supervisor watching several people at once, the value is clearer** |
| **U** (Noise / boAt owner, ~half of India's market) | "Doesn't work with my watch." | True today (undocumented). The breadth claim must be honest: standard-BLE watches and chest straps now, export import otherwise |
| **E** | "BLE in the browser is flaky. Optical HR drops out during sprints. One teammate's watch is a single point of failure." | Mitigations: the Kalman filter tolerates gaps (it predicts through them); record the raw HR stream so every take can be replayed deterministically; test the watch tonight; keep a labelled-replay fallback |
| **I** | "You can't show that anyone was protected. 'Lives saved' is unsupported." | Correct. Claim only what's observable: the alert fired before the threshold, the person rested, recovery was verified. Cite chest-strap validation numbers, and label the wrist gap |
| **A** | "Someone running in the sun, a number climbing, the phone says stop, they stop, the number falls. Got it." | **The strongest first-watch legibility of the five.** It matches the physical-event pattern of both top-two winners (01 §principles 1–2) |

**Revisions adopted:**
1. **Reframe the output.** It is a *heat-strain early warning* (estimate ± band), not a thermometer. Show the published accuracy and the wrist caveat on screen.
2. **Fuse environment with body.**
   - *Before the session:* a WBGT forecast for the spot recommends the lowest-strain start hour.
   - *During the session:* the live estimate gives **time to limit** at the current effort.
   - This makes it heat-*environment* decision support, not a fitness gadget.
3. **Add a supervisor or coach view.** One screen shows several people. One is live from a teammate's watch; the others are labelled replays of real recorded sessions. This serves the people who actually decide: PE teachers, run organisers, recruitment-test officials, site supervisors.
4. **Verified recovery loop.** After an alert, the person is cleared only when the estimate falls below a threshold *and* HR recovery confirms it. This is the visible "verify" moment.
5. **Device honesty.** Name the watches that work; support chest straps; import exported workouts for everyone else.

**Verdict:** **Survives (revised), conditional on the watch gate.** Residual risk: validity on wrist sensors, which can be framed but not eliminated.

---

## 2. Heat Roll-Call: community heat check-ins with escalation

| Persona | Attack | Assessment |
|---|---|---|
| **J** | "This is Suraksha with a weather trigger: same elder, same escalation ladder, same `waitForTaskToken`. The organisers judged that last month." | **Strongest objection, and it is fatal.** On-screen overlap is obvious within the first 20 s |
| **C** | Many teams can build a check-in bot | — |
| **U** | "Our society already has a WhatsApp group." | — |
| **E** | Easy to build | — |
| **I** | No October heatwave (no city > 38.1 °C over 10–16 Oct), so everything is a replay. Coverage is the only KPI | — |
| **A** | "Seen it." | — |

**Verdict:** **Rejected.** Good for India in principle, wrong for this competition.

---

## 3. Bijli Budget: "Was it you or the weather?" plus the free-unit cliff

| Persona | Attack | Assessment |
|---|---|---|
| **J** | "Another snap-your-meter bill app. SmartBill already does OCR, the Gruha Jyothi cliff and a temperature-aware prediction. Smart meters will make photos pointless. Twelve noisy bills can't detect a 5–10% change. Delhi's Opower trial saved 0.32%." | **Strongest objection.** It is only partly answerable (05 §2.2) |
| **C** | 21 "bijli" repos since 25 Sep; several will be in this event | High overlap at a glance |
| **U** | "I just want to know why my bill went up and whether I'll lose my free units." | Real need. The "weather vs you" answer is novel to Indian users |
| **E** | Feasible. The risks are rule-pack accuracy (Delhi at 201 units is unresolved) and meter OCR at 53–80% | Mitigate with a confirm step |
| **I** | Savings evidence is weak (0.32% in Delhi; 7% in a Ghaziabad summer study). Claim only "avoided cliff crossings" and low single-digit % | — |
| **A** | "A bill chart with a probability. Which part is new?" | **The differentiator is invisible unless shown side by side with a naive analyser** |

**Revisions adopted:**
1. **Lead with verification.**
   - Open with a real October 2026 vs October 2025 comparison for a teammate's Delhi household. **This October had ~95 cooling degree-days by the 24th vs 66 in all of Oct 2025 (FACT).**
   - Show a naive analyser that blames the user, beside the weather-adjusted answer.
2. **Cliff as probability.** "P(staying under the pro-rated threshold) = X% at ≤ Y units/day," with the band shown.
3. **OCR is plumbing**, not the pitch.
4. **Verify on screen with meter photos days apart,** normalised by cooling degree-hours. Show "can't tell yet" when the band is too wide.

**Verdict:** **Survives (revised).** It is the safest build with the broadest reach, but the ceiling is capped by genre crowding.

---

## 4. Monsoon Replay: RWH sizing from real roofs and real monsoons

| Persona | Attack | Assessment |
|---|---|---|
| **J** | "SimTanka and last year's Jal Shakti winner already do this. Your rain is a 9–28 km model that misses the cloudbursts that make tanks overflow." | **Strongest objection.** Only partly answerable |
| **C** | 14 RWH student repos since 1 Oct (SIH PS 53 genre) | — |
| **U** | A committee wants "how big, what will it cost, will it pay back". The ₹/tanker framing works. Annual-average tools overstate capture | Real value |
| **E** | Easy. Overture via Athena or DuckDB is verified, and the maths is trivial | — |
| **I** | The replay is a model, not a measurement. Rain bias runs −48% to +33% vs IMD. Results are upper bounds | — |
| **A** | An animated tank filling and overflowing over a real monsoon is clear, and a map of real roofs looks good | — |

**Revisions adopted:**
- Show a **three-model rainfall band**, the IMD comparison and the direction of bias.
- Aggregate across **multiple buildings** from AWS Open Data.
- Add **recharge-pit routing**, **tanker ₹** and a **committee pack**.
- Pitch Chennai's north-east monsoon season and Bengaluru's penalty.

**Verdict:** **Survives as #3 (revised).** Low build risk, medium-low novelty, constrained data credibility.

---

## 5. CoolerCheck: when the desert cooler actually cools

| Persona | Attack | Assessment |
|---|---|---|
| **J** | "Evaporative Cooler Forecaster (2025) already does hourly cooler/fan/AC advice with pad type and savings." | **Strongest objection, and it is fatal for novelty** |
| **I** | The round-1 claims "wastes water in humid hours" and "adds humidity harm" are wrong on physics | — |
| **A** | October is the end of the cooler season in the north. The "drain the tank, dengue" angle is real but small | — |

**Verdict:** **Rejected.** It could survive only as a small feature inside a heat product.

---

## Outcome

| Finalist | Strongest objection | Answerable? | Decision |
|---|---|---|---|
| WristHeat | Wrist-HR core-temperature estimate is unvalidated; Garmin precedent | Partly (framing, band, fusion, recovery loop) | **Top 3: revised, gated** |
| Bijli Budget | Another bill app; noisy verification | Partly (lead with weather counterfactual, side-by-side) | **Top 3: revised** |
| Monsoon Replay | Prior art; rainfall model error | Partly (band, aggregation, economics) | **Top 3: revised** |
| Heat Roll-Call | Suraksha déjà vu | No | Rejected |
| CoolerCheck | Same app already exists | No | Rejected |
