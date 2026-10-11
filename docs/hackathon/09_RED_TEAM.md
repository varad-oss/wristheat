# 09 — Adversarial Red Team (top 8)

Each idea is attacked by seven personas, then modified. Short, blunt answers.

| Code | Persona | The question they ask |
|---|---|---|
| A | Hackathon judge | Why should this win? |
| B | Competing team | How would I copy this? |
| C | User | Why would I actually use this? |
| D | Engineer | Can we build this reliably during the event? |
| E | Skeptic | What is fake, weak, assumed, or unnecessary? |
| F | Demo reviewer | Would this look impressive in three minutes? |
| G | AWS reviewer | Is AWS genuinely necessary or merely decorative? |

---

## 1. I-01 SunCheck: rooftop solar check-up (Waste & Energy)

| Persona | Attack | Answer / consequence |
|---|---|---|
| **A Judge** | "Why should this win?" | **For:** 50 lakh new solar homes, and nobody measures whether they work (FACT: generation blind spot). A real system diagnosed with satellite physics, a free maintenance right turned into a claim, and a *verified* recovery. A precise user and a physical metric (kWh, kgCO₂).<br>**Doubt:** "Is this environmental, or a money app?" |
| **B Competitor** | "How would I copy it?" | They'd build "solar dashboard + Bedrock chatbot". They'd miss rain-calibrated PR, brand-agnostic photo reading, and the SOP-timed claim and verify loop. Submissions are simultaneous, so there's no copying after our video. |
| **C User** | "I don't even open my inverter app. Why would I photograph it every week?" | **Real barrier.** |
| **D Engineer** | "What breaks?" | Vision misreads digits; the irradiance API is down; tilt and azimuth are unknown; there's no real data. |
| **E Skeptic** | "Satellite irradiance can be off 10–20% on hazy days. 'Soiling' could be a neighbour's new building. Doesn't MNRE's M2M monitoring solve this?" | Each needs an answer on screen. |
| **F Demo reviewer** | "Charts are boring." | A chart alone won't carry the video. |
| **G AWS reviewer** | "Is Step Functions just for show?" | Only if it doesn't wait for anything real. |

**Answers to the user's attack (C):**
- The first use is a one-shot backfill: screenshots of the app's daily-history screen give 30–90 days at once.
- After that, a photo of the lifetime-kWh counter every week or two is enough.
- The trigger is event-based: "no rain for 30 days", a dust storm, or a rate change.
- The payoff is spoken in units and ₹, plus the claim the vendor *must* answer.

**Answers to the engineer's attack (D):**
- Vision misreads: add a **confirm-what-we-read** step.
- Irradiance API down: fall back to NASA POWER, served from the AWS Open Data S3 bucket.
- Tilt and azimuth unknown: ask "flat roof / tilted frame", default tilt ≈ 15–20°, facing south, and expose the assumption.
- No real data: **secure one or two real systems' history by Friday 12:00.** This is the critical path.

**Answers to the skeptic's attack (E):**
- **Satellite error:**
  - Use *ratios* against the system's own post-rain baseline, so bias largely cancels.
  - Use 7-day windows and confidence bands.
  - Refuse to diagnose under low confidence.
- **Shading versus soiling:**
  - The MVP does not claim to tell them apart.
  - A slow decline that resets after rain means soiling.
  - A persistent shortfall that doesn't reset means "inspection needed": shading, wiring or modules.
- **M2M monitoring:**
  - Its data flows *up* to government servers, for new installs only, and protocols aren't live yet (FACT).
  - Owners get no diagnosis or action from it.
  - We could ingest M2M data later.
- **The vendor may ignore the claim:**
  - MNRE's SOP gives 8 + 7 days, then a show-cause notice, then deactivation, for failing promised maintenance (FACT).
  - We assemble evidence and track the clock. We don't promise outcomes.

**Answers to the demo reviewer (F):**
- Lead with **real rooftop footage**.
- Use one big number ("214 units lost since 26 Aug") and a health ring.
- Make the **verify** moment unmistakable: PR jumps after cleaning, or after a past rain.

**Answers to the AWS reviewer (G):**
- Step Functions is real if it **waits for the next reading** and then decides between "Resolved" and "Escalate to vendor".
- Bedrock vision is essential, because it is how the product stays brand-agnostic without inverter APIs.
- NASA POWER on the AWS Registry of Open Data is a genuine AWS data asset.
- Avoid decoration: no Cognito, SageMaker or Kinesis.

**Modifications adopted:**
1. **Lead with energy and carbon, then rupees.** Show the national arithmetic as a labelled assumption.
2. **Input modes:**
   - MVP: (a) history screenshot backfill, and (b) a lifetime-counter photo.
   - Later: (c) CSV export.
   - No brand APIs.
3. **Human confirmation on every AI read.**
4. **Confidence-gated diagnosis**, limited to three MVP verdicts: *Dusty panels*, *Off days / trips*, *Persistent shortfall: inspection needed*.
5. **The claim pack is a shareable document and message** with the evidence chart, the 5-year maintenance clause and the MNRE SOP clock. The owner sends it; we never file on portals on their behalf.
6. **Verification** comes from the Step Functions loop: wait for N new days, recompute PR, then resolve or escalate. In the demo, validate against a *past natural rain* as well.
7. **Time-of-day load shifting** (I-13) becomes a single "coming next" card. It is not built.

**After red team: strengthened, and remains #1.**

---

## 2. I-05 TankerTruth: tanker delivery verification (Heat & Water)

| Persona | Attack | Answer / consequence |
|---|---|---|
| A Judge | "What environmental problem does this fix?" | Mostly price fairness. It doesn't reduce groundwater extraction. **Criterion #1 weakness.** |
| B Competitor | — | Hard to copy, but few will try. |
| C User | "My sump has no gauge. It's dark down there. I won't dip a stick every delivery." | **Real barrier.** |
| D Engineer | — | Reading a dipstick from a photo is unreliable. Sump geometry must be measured by hand. |
| E Skeptic | — | **How common short-delivery is, is a HYPOTHESIS with no data.** The rate caps were temporary (four months, FACT). |
| F Demo reviewer | — | We need a real tanker delivery on camera this weekend, which is unlikely outside a tanker-dependent society. |
| G AWS reviewer | — | Bedrock vision + Lambda is fine, but thin. |

**Modification tried:** reframe as a "society water ledger" (consumption per flat, leak inference) to add an environmental benefit. That converges on NightFlow and needs hardware.

**After red team: weakened. Drops out of the top 3.**

---

## 3. I-02 HeatShift: WBGT work-rest planner (Heat & Water)

| Persona | Attack | Answer / consequence |
|---|---|---|
| **A Judge** | "Why should this win?" | Lives and livelihoods: 5.8% of working hours at risk (FACT); no national worker standard (FACT). It plans rather than alerts. **Doubt:** "It's October." |
| **B Competitor** | — | Heat bots are common; WBGT scheduling isn't. Low copy risk. |
| **C User (supervisor)** | "The contractor pays on output. Breaks cost money." | **Reframe:** the same total work hours, with heavy tasks moved to cooler hours. Less risk, less liability, matching state heatwave advisories. |
| **C User (worker)** | "Will the supervisor let me rest?" | The plan is visible to workers via a Hindi voice briefing. Symptom reports escalate. |
| **D Engineer** | — | Feasible. Hourly WBGT via thermofeel (Liljegren) from Open-Meteo inputs; a greedy task scheduler; Polly Hindi voices; an EventBridge 18:00 plan generator. |
| **E Skeptic** | "Forecast-grid WBGT ≠ a concrete slab at 2 PM." | Add a site-surface adjustment and a disclaimer. |
| | "The ACGIH table is US-derived." | State it as a reference standard. |
| | "Your outcome (risk-hours avoided) is modelled, not measured." | **Real weakness on the measurable-impact criterion.** |
| **F Demo reviewer** | — | The before/after plan is visual, and a Hindi briefing is memorable. A simulated site is weak. **Fix:** film a real campus construction site and its supervisor. Use a labelled May 2026 heatwave replay plus a live forecast for a hot southern city today. |
| **G AWS reviewer** | — | Legitimate: EventBridge Scheduler, Lambda, Polly, Bedrock, SNS, DynamoDB. |

**Modifications adopted:**
1. The user is a **campus construction contractor**, reachable this weekend.
2. Verification comes from worker check-ins: was the rest taken, and any symptoms. This is honest but weaker than SunCheck's.
3. The heatwave day is a labelled historical replay; the live forecast runs today for a hot city.

**After red team: solid #2, with a seasonality and measurement handicap.**

---

## 4. I-04 BinScore 2026: SWM Rules compliance loop (Waste & Energy)

| Persona | Attack | Answer / consequence |
|---|---|---|
| A Judge | — | Regulatory relevance plus real campus bins. **Risk:** the first glance reads "waste classifier #47". |
| B Competitor | — | Easy to *appear* similar. |
| C User (warden) | "Another app for my staff." | The incentive is avoiding environmental compensation (FACT) and an automatic report. |
| D Engineer | — | Vision grading of contamination on messy bins needs a rubric and calibration photos. Feasible. |
| E Skeptic | — | The portal's report format isn't public (INFERENCE), so a "compliance pack" risks looking invented. The threshold applies per entity, not per hostel. |
| F Demo reviewer | — | Real campus bins and a before/after contamination % are good footage. |
| G AWS reviewer | — | Bedrock vision, S3, Lambda, DynamoDB, EventBridge. Fine. |

**Modifications:** lead with "which wing contaminates the dry bin", not "classify this item". Call the output a *summary for your compliance filing*, not the filing itself.

**After red team: viable backup (#4).** It is held back by its crowded neighbourhood.

---

## 5. I-06 NightFlow: tank-level leak detection (Heat & Water)

| Persona | Attack | Answer / consequence |
|---|---|---|
| D Engineer | — | Needs a sensor, a microcontroller, connectivity and nights of data. Not credible to install and gather by Sunday. Without hardware, the core is simulated. |
| E Skeptic | — | Without real nights of data, the "verify" is fake. |

**After red team: rejected for this event.** Revisit with hardware time.

---

## 6. I-13 ToD Shift: time-of-day tariff load shifter (Waste & Energy)

| Persona | Attack | Answer / consequence |
|---|---|---|
| C User | — | Most households don't yet see a domestic time-of-day bill (rollout uneven, INFERENCE). Savings per household are small. |
| D Engineer | — | Meter interval data is DISCOM-specific and hard to obtain. |
| A Judge | — | Fine, but thin. |

**After red team: merged into SunCheck as a future card.**

---

## 7. I-08 GRAP-Ready: construction planning around GRAP curbs (Air)

| Persona | Attack | Answer / consequence |
|---|---|---|
| A Judge | "You're helping construction schedule around anti-pollution rules?" | **Reputational risk.** |
| E Skeptic | — | GRAP-stage forecasting is unvalidated, and the environmental gain is indirect. |

**After red team: rejected.**

---

## 8. I-03 Clean-Air Windows: outdoor-activity timing (Air)

| Persona | Attack | Answer / consequence |
|---|---|---|
| **A Judge** | — | Relatable in Delhi now, and the **measured counterfactual** is strong. **Doubt:** "I've seen ten school-AQI apps today." |
| **B Competitor** | — | Easy to imitate at topic level. The timing lever is the only moat. |
| **C User (PE teacher)** | "The timetable is fixed. The cleanest hour (4–5 PM) is after school." | Within school hours the gain is smaller. HYPOTHESIS: 20–40%, to be measured from station data. |
| **D Engineer** | — | Feasible. OpenAQ station history (S3/API) gives an hourly profile; CAMS gives the trend. **Must confirm OpenAQ freshness for CPCB stations**, given that data.gov.in has no API (FACT). |
| **E Skeptic** | "A 14-day average profile can mislead on foggy or windy days. The station isn't the school." | State it as a proxy and update with same-morning readings. |
| **F Demo reviewer** | — | Smog visuals are powerful in October. A thumbnail-level resemblance to the crowd is the risk. |
| **G AWS reviewer** | — | OpenAQ on the AWS Registry of Open Data is genuine. Plus Lambda, EventBridge, and Bedrock for bilingual notices. |

**Modifications:**
- Generalise to "outdoor windows for institutions": schools, sports academies, walking groups (merging I-07).
- Lead with the measured counterfactual: "same kids, same day, 41% less PM2.5".
- Add an indoor fallback (folding in I-23).

**After red team: best Air-track option (#3).** Still the most crowded neighbourhood.

---

## Red-team outcome

| Idea | Before red team | After red team | Status |
|---|---|---|---|
| I-01 SunCheck | Strong | **Stronger** (input modes, confidence gating, verify loop, energy-first framing) | **Top 3** |
| I-02 HeatShift | Strong | Solid (seasonality and modelled-outcome handicaps) | **Top 3** |
| I-03 Clean-Air Windows | Medium | Medium+ (counterfactual-led, institution-general) | **Top 3** (Air representative) |
| I-04 BinScore 2026 | Medium+ | Medium+ | Backup |
| I-05 TankerTruth | Strong on paper | Weak (environmental link, measurement, footage) | Out |
| I-06 NightFlow | Strong on paper | Infeasible this weekend | Out |
| I-13 ToD Shift | Medium | Merged into SunCheck | Out (future card) |
| I-08 GRAP-Ready | Medium | Reputational risk | Out |
