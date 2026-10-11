# R2-04 — Updated Competitor & Overlap Analysis

This file supersedes `../05_SUBMISSION_OVERLAP_MAP.md`, which was predicted from desk research. Everything here comes from evidence:

| Source | Scope | Collected |
|---|---|---|
| Live scan of Environmental Hacks projects | **111** projects with public repos or posts | 9 Oct, ~14:00 IST |
| GitHub API spot-check of student repos | Created since late Sep 2026 | 9 Oct, 22:15 IST |
| Per-concept competitor audits | Products, apps, papers, prior hackathon winners | 9 Oct, 21:50–22:30 IST |

Full evidence:
- [`evidence/A_live_competition.md`](evidence/A_live_competition.md)
- [`evidence/B_audit_*.md`](evidence/)

Tags: FACT · INFERENCE · HYPOTHESIS.

---

## 1. The field

| Measure | Value | Tag |
|---|---|---|
| Registrations | **8,653** (live API, 9 Oct 22:20 IST; 8,481 at 14:00) | FACT |
| Expected submissions | ~730 (600–900), using First Commit's registration-to-submission ratio | INFERENCE |
| Visible projects | 111 (≈15% of expected) | FACT |
| Track split of visible projects | Heat & Water 48% · Air 31% · Waste & Energy 22% | FACT (sample) |
| Organiser seed ideas copied | **Seed 1** (school air plan for the principal): 10 projects. **Seed 4** (flood commute from reports): ≥8. Seeds 5–6 (bin checker, solar payback): 4 each | FACT |
| Architecture pattern | "Deterministic engine + LLM explains", from the official SchemeProof build guide, now appears in many READMEs. **It no longer differentiates** | INFERENCE |

---

## 2. Overlap by cluster (live field)

| Cluster | Track | Live count | Tier |
|---|---|---:|---|
| Flood / waterlogging (maps, depth CV, routes) | H&W | 18–23 | **Crowded** |
| School air plan for the principal | Air | 10 | **Crowded** |
| Multi-hazard "command desks" | H&W | 8 | Crowded, weak |
| Stubble → smoke arrival / parali marketplaces | Air | 8 | Crowded |
| E-waste / kabadi photo-to-pickup | W&E | 7 | Crowded |
| Personal "safe outside?" AQI advisors | Air | 5 | Crowded |
| Worker heat / WBGT shift planners | H&W | 5 | Contested (Chhaon, ShiftShield, ₹800, HeatShift, a heat-safe shift planner) |
| AQI dashboards | Air | 5 | Crowded, weak |
| **Personal dose / departure-time / mode advisors** | Air | **6+** (ALive, EcoRoute AI, Breathe Route, better_AQI, AirTrace, RideClean) | **Crowded**: the audit found more than the 14:00 scan |
| Shade / heat-route / heat-pocket | H&W | 4 | Moderate |
| Drinking-water contamination alerts | H&W | 4 | Moderate |
| Water-supply leak / NRW verification | H&W | 4 | Moderate |
| Solar **pre-install** (payback, potential) | W&E | 4 | Moderate |
| Window / ventilation (Khidki, part of better_AQI) | Air | 2 | Moderate |
| **Rainwater harvesting** | H&W | **0** in the live field | Rare *in the event*, but see §3 |
| **Wearable / body-signal heat strain** | H&W | **0** | **Rare** |
| **Household bill / meter projection** | W&E | 0 in the 111 sample | Rare *in the sample*, but see §3 |
| Tanker verification · solar post-install · SWM bulk generators · ToD shifting · picker pricing | Various | 0 | Rare, but each fails a round-2 constraint |

---

## 3. Spot-check: student repos created since late Sep 2026

Source: GitHub search API, 9 Oct 22:15 IST. This captures the wider student scene, including other hackathons such as Smart India Hackathon (SIH) problem statements and private projects made public.

| Query | Hits | What they are | Tag |
|---|---:|---|---|
| `bijli created:>2026-09-25` | **21** | Bill explainers, bill calculators and saving assistants: BijliSaarthi, Bijli-Bill, bijli-bill-calculator, Bijlibot (9 Oct), BijliBaaz (7 Oct), BijliSmart_AI. Several are Pakistani bill decoders | FACT |
| `electricity meter subsidy created:>2026-09-25` | 1 | **BESCOM-Bill-Chatbot ("SmartBill")**: meter readings → consumption → Gruha Jyothi logic | FACT |
| `rainwater harvesting created:>2026-10-01` | **14** | RWH calculators and analysers, incl. HydroLens ("PS 53"), "Rooftop Rainwater Harvesting … On-Spot Assessment", rainwise-ai. **This is an SIH problem-statement genre** | FACT |
| `heat strain heart rate` / `smartwatch heat` / `web bluetooth heart rate heat` (since Sep) | **0** | — | FACT |
| `heart rate core temperature created:>2026-09-15` | 2 | Unrelated: a FHIR bridge and IoT patient vitals | FACT |

**INFERENCE from the spot-check:**
1. **Bill analysers are a crowded student genre** even though few appear in the 111-project sample. Some of the 21 "bijli" repos created during 8–9 Oct are likely Environmental Hacks entries, and judges will probably see several.
2. **RWH sizing is an SIH genre with many lookalikes.**
3. **Body-signal heat strain is genuinely empty.**

---

## 4. Per-concept competitor audit

For each concept:
- **Functional improvement?** Is it a genuine functional improvement, or a re-presentation of something that exists?

| Concept | Strongest existing alternatives (FACT) | What they fail to do (evidence) | Functional improvement? | Difference users would notice |
|---|---|---|---|---|
| **WristHeat** | GarminLabs "Estimated Body Temperature" Connect IQ field (2021, Garmin-only). Kenzen and SlateSafety (proprietary hardware). Equivital / Zephyr running ECTemp (pro straps). Garmin heat acclimation (status, not live risk). Apple wrist temperature (during sleep only) | No **consumer, cross-brand, browser-based** HR → core-temperature estimate fused with **local WBGT**. No supervisor view for a group | **In this competition: yes** (0 body-signal entries vs 5 weather-only heat planners). **Globally: re-presentation** of ECTemp | "It tells *me* when *I* should stop, from *my* heart, in *this* heat." Weather-only tools give everyone the same number |
| **Bijli Budget** | SmartBill (meter/bill OCR, Gruha Jyothi cliff, temperature-aware next-bill prediction). TPDDL in-browser meter self-read. 21 "bijli" repos. Opower (US, mid-cycle forecast + weather bill comparison). CalTRACK/OpenEEmeter (programme M&V). BRPL Opower trial in Delhi (0.32% saving) | No Indian app found gives a **pro-rated probability of crossing the cliff + daily budget**, or a **household weather-normalised "was it you or the weather?"** check (21 DISCOM Play listings read) | **Partly.** OCR and slab maths are re-presentation. **Weather-normalised verification + crossing probability** is a genuine improvement for Indian households | *(Illustrative numbers)* "Your bill rose 18%, but the weather explains 15 points. You're on track; 64% chance you stay under 200 units if you keep ≤ 5.1 units/day" |
| **Monsoon Replay** | SimTanka (open source, replays real daily rain). JNTU Jal Shakti Hackathon 2025 winner (roof on map + 30 years of rain → tank size). KSCST RWH Advisor and calculators. 14 RWH student repos | Multi-building aggregation from AWS Open Data + recharge-pit routing + tanker economics + uncertainty band + committee pack | **Mostly re-presentation + aggregation.** Improvement over annual-average calculators: capture 52–73% vs the 100% they imply | "Your 10 kL tank would have caught 73%, not 100%; overflow to recharge pits saves N tankers." The 73% is the audit's Bengaluru 2024 replay for a 1,000 m² roof, an upper bound because the model under-states cloudbursts |
| **CoolerCheck** | **Evaporative Cooler Forecaster** (Tenth Light Digital, iOS/Android, May 2025): hourly cooler/fan/AC advice, pad type, indoor temperature/RH, savings. WetBulbCast (iOS). Symphony's wet-bulb calculator | Not India-specific (desert-cooler ε, Hindi, dengue drain prompt) | **Re-presentation / localisation** | Small |
| **Heat Roll-Call** | France's fichier canicule; Philadelphia buddy system; NYC Be a Buddy; Australian Red Cross TeleRedi; Snug; **Suraksha (last event's 1st prize, same escalation pattern)** | No Indian scheme found | Improvement for India, but conceptually and technically a re-presentation of an established protocol and of Suraksha | "Looks like Suraksha" |
| **Dose Ledger** | ALive, EcoRoute AI, Breathe Route and 3+ more live entries. US EPA TracMyAir; Hong Kong PRAISE-HK | Only "a full past week from your own location history, every swap ranked by dose avoided per minute" is uncontested | Mostly re-presentation | Small vs live entries |
| **Window Planner** | Open Your Windows, Aerzeit, Khidki (in this event), Nihar et al. 2023 | — | Re-presentation; indoor PM benefit contested in Indian homes | Small |
| **ShadeSite** | WRI Cool Cities Lab: 1 m hourly shade from Overture + Meta canopy for 27 cities incl. Bhopal, Indore, Gwalior, Jabalpur. ShadeMap | Planting-**placement** optimisation is unclaimed | Partly | Real, but benefit deferred 5–10 years |
| **ReCheck** | FixMyStreet 4-week re-ask; Swachhata reopen; TrashOut | No "resolution half-life" / survival metric | **Yes** (new metric) | Real, but no data to show it in 46 h |

---

## 5. What makes a concept recognisably different now

1. **The input or decision nobody else in the field uses.**
   - The body's own signal (WristHeat).
   - A household's own policy threshold plus a weather counterfactual (Bijli Budget).
2. **A verification step judges can see.** This is no longer rare in the strong tail, so it must be **physical or quantified**, not a checkbox.
3. **Avoid organiser seed ideas.** Seeds 1 and 4 are heavily copied.
4. **Avoid SIH genres.** RWH (PS 53) and bill/OCR assistants have many student lookalikes regardless of the live sample.
