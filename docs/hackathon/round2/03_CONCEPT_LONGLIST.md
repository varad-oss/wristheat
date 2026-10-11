# R2-03 — Fresh Concept Longlist

**Size:** 42 concepts generated from three independent lenses, which reduce to **~38 distinct ideas** (four mechanisms surfaced in two lenses each). Five round-1 ideas were re-tested alongside them.

**Where the full detail lives.** Every concept has a full 18-field dossier in the evidence files:

| Fields 1–9 | Fields 10–18 |
|---|---|
| Problem | Architecture |
| User | AWS |
| Why it matters | MVP |
| Workaround / alternatives | Demo plan |
| Insight | Strongest video moment |
| Mechanism | Impact evidence |
| Distinctiveness | Risks |
| Why it isn't "feature + new UI" | Why others would build it |
| Data | Our distinguishing outcome |

| Lens | Concepts | Evidence file |
|---|---|---|
| Personal / household / mobility | P-01 … P-15 | [`evidence/A_concepts_personal_household.md`](evidence/A_concepts_personal_household.md) |
| Mechanism-first / cross-track | M-01 … M-12 | [`evidence/A_concepts_mechanism_first.md`](evidence/A_concepts_mechanism_first.md) |
| Community / campus / institutional | C-01 … C-15 | [`evidence/A_concepts_community_institutional.md`](evidence/A_concepts_community_institutional.md) |

**This file** indexes the concepts by problem/mechanism cluster, so that diversity is visible. It also records each concept's **round-2 status** after the audits in `05`.

**Status key:**
- **Audited:** went through competitor and feasibility audit (see 05).
- **Merged:** combined into another concept.
- **Dropped:** with the reason given.

---

## Cluster 1: Household electricity and cooling spend (Waste & Energy)

| ID | Name | Primary user | Mechanism (one line) | Status |
|---|---|---|---|---|
| P-01 / M-01 | Cliff Guard / Unit Cliff | Bill-payer in a free-unit state | Meter photo + weather-driven projection against the state's free-unit cliff → daily unit budget → next photo verifies | **Audited as "Bijli Budget"** |
| P-02 / M-02 | Bill X-ray | Any household | Bill history × cooling degree-days → weather-adjusted counterfactual ("saved X ± Y kWh" or "can't tell") | **Merged into Bijli Budget** (its strongest part) |
| P-03 | AC Fit | AC buyer | Label photo + city bin-hours replace the national ISEER profile → 10-year cost and tonnage | Dropped (once-in-a-decade decision; module at most) |
| P-04 | Setpoint Coach | AC household | IMAC prior + nightly setpoint steps + comfort votes → personal neutral setpoint | Merged as a lever into Bijli Budget |
| P-09 | Green Hours | ToD / EV household | Shiftable-load schedule against ToD or solar hours | Dropped (small stakes; patchy domestic ToD) |
| M-03 | GridShift | Developers / households | Defer jobs to low-carbon grid hours using Grid-India data | Dropped (common genre; weak marginal-carbon signal) |
| M-12 | Fix-or-Replace | Device owner | Device screenshot → embodied CO₂ → repair vs replace | Dropped (weak data) |
| C-11 | NightLoad | Campus estate office | Paired meter photos → after-hours kW vs essential load → switch-off walk → re-measured saving | Merged into Bijli Budget as institution mode |
| C-12 | ATR Proof | Campus / RWA | Bills + cooling degree-days → IPMVP baseline → verified savings for audit reports | Merged into Bijli Budget (same engine) |
| C-14 | Common-Roof | RWA | Common-area bills + roof + irradiance → solar split + AGM vote | Dropped (solar-ROI genre) |
| R1 | SunCheck | PM Surya Ghar owner | Satellite expected vs actual → diagnose → claim → verify | Dropped (**no real system data accessible to the team**) |

## Cluster 2: Heat — physiology, cooling devices, outreach, shade (Heat & Water)

| ID | Name | Primary user | Mechanism | Status |
|---|---|---|---|---|
| M-11 | WristHeat | Anyone exerting outdoors with a compatible watch; coaches and supervisors | Live watch HR → ECTemp Kalman core-temperature estimate × WBGT → heat-strain state, rest advice, verified recovery | **Audited** |
| P-05 / M-06 | CoolerCheck / Cooler Logic | Cooler household | Hourly wet-bulb → cooler outlet temperature → Cooler / Fan / Close-up schedule + litres | **Audited** |
| P-08 | Heat Buddy | Remote adult child | Home-specific indoor heat estimate → call schedule → escalation | Merged into Heat Roll-Call |
| C-05 | Heat Roll-Call | RWA volunteer | Forecast trigger → per-person check-in → backup → secretary escalation via timeouts | **Audited** |
| C-06 | ShadeSite | Campus estate / eco-club | Sun-path shadows over AWS canopy and buildings → greedy sapling siting by shade-minutes on walked paths | **Audited** |
| C-07 | Sapling Survival Ledger | Plantation organiser | Scheduled photo re-checks + heat-triggered watering rota → survival curves | Module of ShadeSite |
| R1 | HeatShift | Site supervisor | WBGT → next-day work-rest plan | Dropped (5 live competitors: Chhaon, ShiftShield, ₹800…) |

## Cluster 3: Water (Heat & Water)

| ID | Name | Primary user | Mechanism | Status |
|---|---|---|---|---|
| C-08 | Monsoon Replay | RWA committee / campus | Overture roofs (Athena) × real past daily rain → tank and recharge water balance → capture curve, tanker-equivalents, committee pack | **Audited** |
| M-08 | Rain Ledger | Household | 30-year daily water balance → tank reliability curve | Merged into Monsoon Replay (SimTanka exists) |
| C-09 | Rain-Check | Ward engineer / RWA | Crowd waterlogging reports × hourly rain → per-spot onset threshold | Dropped (rain resolution too coarse; flood cluster crowded) |
| M-07 | RO Right-Size | RO household | Lab report → IS 10500 rules → treatment choice + reject water saved | Dropped (liability; source TDS unknown) |
| P-12 | RO Reject Planner | RO household | Litres × recovery ratio → reject volume and reuse | Dropped (same data gap) |
| R1 | TankerTruth | Society manager | Sump photos → delivered litres vs invoice | Dropped (measurement accuracy; weak environmental link) |

## Cluster 4: Air exposure, mobility and housing choices (Air)

| ID | Name | Primary user | Mechanism | Status |
|---|---|---|---|---|
| P-06 / M-05 | Dose Ledger | Commuter | Trips × hourly PM × mode factors × inhalation → weekly dose → ranked swaps → next-week check | **Audited** |
| P-07 | Window Planner | Non-AC household | 24-hour optimisation trading cooling degree-hours against PM let in | **Audited** |
| P-10 | Mode Switch Trial | Commuter | Randomised ABAB self-trial → personal confidence intervals on time, ₹, CO₂ and dose | Merged into Dose Ledger |
| P-11 | Old Vehicle Exit | Owner of an old vehicle | RC photo + state rules → keep / sell / scrap NPV | Dropped (legal churn) |
| P-13 | Rent Check | Renter / student | Address → surface temperature, low-lying score, PM → flat comparison | Dropped (GIS-heavy, weak decision frequency) |
| P-15 | Trigger Diary | People with asthma | Symptoms × lagged exposure → personal threshold | Dropped (needs weeks of logs; medical risk) |
| M-04 | Smoke Trace | NCR residents | Back-trajectory × FIRMS fires → smoke arrival window → next-day PM check | Dropped (5 live stubble-smoke entries) |
| C-03 | Half-Office | NCR office manager | ILP picks the 50% on-site set under GRAP Stage III to cut vehicle-km and exposure | Dropped (NCR-only, seasonal) |
| C-04 | GRAP Runbook | Institution | Stage change → per-asset obligations → owner tasks with proof | Dropped (overlaps the school-planner cluster) |
| R1 | Clean-Air Windows | School / principal | Station diurnal profile → re-timed outdoor periods | Dropped (10 live school planners) |

## Cluster 5: Civic, institutional and coordination

| ID | Name | Primary user | Mechanism | Status |
|---|---|---|---|---|
| C-02 | ReCheck | Reporter / RWA | Scheduled re-checks after "resolved" + photo comparison → clean-survival curve, resolution half-life | **Audited** |
| C-01 | Right Desk | Citizen | Photo → jurisdiction + rule → evidence pack → SLA escalation | Dropped (crowded civic genre) |
| M-09 | Dust Docket | Resident near construction | 12-parameter dust checklist → approved complaint → timers → re-photo closure | Dropped (agency step simulated) |
| M-10 | Pledge Threshold | Neighbourhood | Conditional pledges → threshold trigger → vendor RFQ | Dropped (thin moat; module) |
| C-13 | PoolDrop | Households with e-waste | Pledges → threshold locks pickup → certificates | Dropped (thin moat) |
| C-15 | Obligation Radar | Institution | Questionnaire → threshold rules → obligations calendar | Dropped (reporting-oriented) |
| R1 | BinScore 2026 | Hostel warden | Bin photos → contamination per wing → compliance pack | Dropped (waste-vision cluster; 4 live bin-photo projects) |

## Cluster 6: Waste and consumption

| ID | Name | Primary user | Mechanism | Status |
|---|---|---|---|---|
| C-10 | FestLoop | Event organiser | Headcount × menu × serveware → stream kg plan → post-event weigh-in reconciliation | Dropped (no defensible Indian coefficients) |
| P-14 | Cook-Right | Home cook | Leftover log → per-dish quantity forecast | Dropped (food-waste genre) |

---

## Diversity check

| Dimension | Coverage |
|---|---|
| **Users** | Households, commuters, renters, AC buyers, people exercising or working outdoors, coaches and supervisors, RWA committees, volunteers, campus estate offices, wardens, event organisers, office managers, complaint reporters |
| **Mechanisms** | Measurement & verification (M&V) counterfactual, threshold projection, physiological state estimation, psychrometrics, water balance, dose attribution, escalation ladders, survival analysis, placement optimisation, assurance contracts, integer programming, back-trajectories |
| **Data sources** | User photos and bills; own watch heart rate; Open-Meteo forecast and archive; CAMS; FIRMS; OpenAQ; Overture on AWS; CHMv2 canopy on AWS; Grid-India; scheme rules |
| **Tracks** | By each concept's primary track, across the 42 generated: Waste & Energy 20 · Heat & Water 13 · Air 9. Seven are cross-track, e.g. P-07 Air × Heat, P-10 Energy × Air |

---

## What went to audit

Nine concepts were audited: the strongest by constraint fit, plus at least one per cluster. SunCheck was re-tested as the tenth.

| Audited concept | Track |
|---|---|
| Bijli Budget (incl. NightLoad and ATR Proof) | Waste & Energy |
| WristHeat | Heat & Water |
| CoolerCheck | Heat & Water |
| Heat Roll-Call | Heat & Water |
| Monsoon Replay | Heat & Water |
| ShadeSite | Heat & Water |
| Dose Ledger | Air |
| Window Planner | Air |
| ReCheck | Waste & Energy / civic |
| SunCheck (re-test) | Waste & Energy |
