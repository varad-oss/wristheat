# 10 — Phase 9 Scoring & Top-3 Deep Dive

## Part A — Phase 9: scoring the remaining concepts

These five concepts survived the red team (see 09).

**Method:**
- Each criterion is scored 1–10, then weighted.
- The weighted total is ×10, giving a 100-point scale.
- The crowding penalty is applied on that 100-point scale.

**Weights:**

| Criterion | Weight |
|---|---:|
| Problem severity | 15% |
| Originality | 15% |
| Differentiation | 15% |
| User value | 15% |
| Demo power | 10% |
| Meaningful AWS | 10% |
| Technical feasibility | 10% |
| UX clarity | 5% |
| Measurable impact | 5% |

**Crowding penalty:** 0 = highly differentiated · −2 = somewhat common · −5 = crowded · −10 = obvious.

### Scores

| Concept | Severity 15% | Originality 15% | Differentiation 15% | User value 15% | Demo 10% | AWS 10% | Feasibility 10% | UX 5% | Measurable 5% | Weighted (/100) | Crowding | **Final** |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|
| **I-01 SunCheck** | 7 | 9 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 82.0 | 0 | **82.0** |
| **I-02 HeatShift** | 9 | 8 | 8 | 7 | 7 | 7 | 7 | 7 | 5 | 75.0 | −2 | **73.0** |
| I-04 BinScore 2026 | 6 | 7 | 6 | 7 | 7 | 7 | 8 | 7 | 7 | 68.0 | −2 | **66.0** |
| **I-03 Clean-Air Windows** | 8 | 6 | 6 | 7 | 7 | 6 | 6 | 8 | 8 | 67.5 | −5 | **62.5** |
| I-05 TankerTruth | 5 | 8 | 8 | 6 | 5 | 5 | 5 | 6 | 6 | 61.5 | 0 | **61.5** |

### Why each score

**I-01 SunCheck**

| Criterion | Score | Reason |
|---|---|---|
| Severity | 7 | Large, silent, *national* clean-energy leakage: 50 lakh homes, 5–30% losses (FACT). Not life-threatening, hence not 9–10 |
| Originality | 9 | Nobody packages weather-normalised, rain-calibrated performance for subsidy-era owners (see 04) |
| Differentiation | 9 | The field's solar entries will be pre-purchase calculators (see 05) |
| User value | 8 | Units, ₹ and a maintenance right owners already have |
| Demo power | 8 | Real rooftop, real inverter, one number, and a verified recovery. Charts need design care |
| AWS | 8 | Bedrock vision is the brand-agnostic reader. Step Functions waits for real readings. EventBridge drives check-ups and SOP timers. NASA POWER comes from AWS Open Data |
| Feasibility | 8 | The satellite API was **verified working for India today** (see Part B). The PV maths is simple. Real data access is the only critical-path risk |
| UX | 8 | Photo in, verdict out |
| Measurable | 9 | kWh, ₹ and kgCO₂, measured on the next readings |
| Crowding | 0 | Highly differentiated |

**I-02 HeatShift**

| Criterion | Score | Reason |
|---|---|---|
| Severity | 9 | Health and lives, with 5.8% of working hours at stake (FACT) |
| Originality | 8 | WBGT scheduling is unseen in Indian tools |
| Differentiation | 8 | — |
| User value | 7 | The supervisor's incentive conflict |
| Demo | 7 | Off-season; needs a labelled historical replay |
| AWS | 7 | Solid but standard: Scheduler, Lambda, Polly, Bedrock |
| Feasibility | 7 | thermofeel plus the forecast is feasible. Calibrating the work-rest table takes care |
| UX | 7 | — |
| Measurable | 5 | Risk-hours avoided are *modelled*; there is no measured outcome this weekend |
| Crowding | −2 | Heat alerts are common at topic level |

**I-04 BinScore 2026**

| Criterion | Score | Reason |
|---|---|---|
| Severity | 6 | Compliance plus waste diversion |
| Originality | 7 | The regulatory hook is new |
| Differentiation | 6 | It lives next to the crowded waste-vision cluster |
| User value | 7 | Real campus users |
| Demo | 7 | Real bins on our campus |
| AWS | 7 | — |
| Feasibility | 8 | — |
| UX | 7 | — |
| Measurable | 7 | Contamination % trend |
| Crowding | −2 | — |

**I-03 Clean-Air Windows**

| Criterion | Score | Reason |
|---|---|---|
| Severity | 8 | Delhi's air (FACT) |
| Originality | 6 | The diurnal lever is known science |
| Differentiation | 6 | The thumbnail looks like an AQI app |
| User value | 7 | — |
| Demo | 7 | — |
| AWS | 6 | — |
| Feasibility | 6 | **Live CPCB data has no open API** (FACT); OpenAQ freshness is unverified; CAMS is 45 km for India |
| UX | 8 | — |
| Measurable | 8 | A measured counterfactual from station data |
| Crowding | −5 | The organisers suggest schools explicitly |

**I-05 TankerTruth**

| Criterion | Score | Reason |
|---|---|---|
| Severity | 5 | Fairness more than environment |
| Originality | 8 | — |
| Differentiation | 8 | — |
| User value | 6 | — |
| Demo | 5 | Needs a real delivery on camera |
| AWS | 5 | Thin |
| Feasibility | 5 | Gauge reading accuracy |
| UX | 6 | — |
| Measurable | 6 | — |
| Crowding | 0 | — |

### Judgment call: the top 3 is not simply the top 3 by score

**Selected for deep dive:** I-01 SunCheck, I-02 HeatShift, I-03 Clean-Air Windows.

**I-03 is chosen over I-04 BinScore 2026 (66.0 vs 62.5)** for three reasons:
1. BinScore sits in the **same track as SunCheck** (Waste & Energy), so it can't be our entry if SunCheck is.
2. Clean-Air Windows keeps a credible **Air-track option** open, in case the team prefers Air for the Delhi-season salience.
3. Its measured counterfactual is the stronger evidence story.

BinScore remains the documented backup if the Waste & Energy pick fails on data.

---

## Part B — Deep dive: I-01 SunCheck (Waste & Energy)

### B1. Problem validation

| Claim | Tag | Evidence |
|---|---|---|
| Scale | FACT | **50.06 lakh** PM Surya Ghar households, **~14.8 GW**, by July 2026. 5.06 lakh added in July alone; target 75 lakh by Dec 2026 |
| Average system size | INFERENCE | 14.8 GW ÷ 50.06 lakh ≈ **2.96 kW** |
| The blind spot | FACT | The government tracks installs, not generation. M2M monitoring is mandated for new installs only, with protocols not yet live. ~23 GW is unmonitored |
| Neglect | FACT | Industry estimates ~99% of owners stop monitoring. Owners call vendors only after faults. Many don't know about the **free 5-year maintenance** that is a condition of the subsidy |
| Physics of loss | FACT | Soiling accumulates ~0.4%/day in dry spells (IIT Bombay simulation). Dust and droppings cost 5–30%. Dust-heavy states need more frequent cleaning |
| Leverage exists | FACT | MNRE's 2026 complaint SOP (8 + 7 + 15 days, then deactivation; failing promised maintenance is listed as a violation). The warranty SOP gives 25-year power-output warranties |
| Disputes are real | FACT | A consumer court award for unmet solar savings (Jul 2026 headline) |

### B2. Target user validation

**Primary user:** an urban or semi-urban owner of a 2–3 kW PM Surya Ghar system, installed 2024–26, in a dry and dusty belt (Rajasthan, Gujarat, Delhi-NCR, UP, MP). Typically non-technical. The bill fell, so they assume the system is fine.

**Validate this weekend (must happen by Fri 14:00 IST):**
1. Find **2–3 real systems** among team families and friends. With 50 lakh homes, this is very likely (INFERENCE).
2. Collect from each:
   - Inverter app screenshots of **daily generation for 30–90 days**.
   - A photo of the inverter display.
   - Installation details: kWp, install date, roof type, approximate panel direction.
   - The vendor's name.
3. Ask each owner five questions, and with consent record a 10-second clip for the video:
   - When did you last check the output?
   - When did you last clean the panels?
   - Do you know about the 5-year free maintenance?
   - What happened the last time you called the vendor?
   - Would you photograph your inverter once a fortnight if it told you what you're losing?

**Kill criterion:** if no real daily history is obtainable by Fri 14:00, switch to HeatShift (Part C).

### B3. Datasets: verified today

| Dataset | Status | Detail |
|---|---|---|
| **Open-Meteo Satellite Radiation API** | **FACT, verified by direct call on 8 Oct 2026** | Jaipur (26.91 N, 75.79 E), 20° tilt, south-facing, 20 Sep–6 Oct 2026. **408 hourly values, zero nulls**. Daily GTI **5.5–6.5 kWh/m²** (e.g. 27 Sep 5.50, 3 Oct 6.48). Docs: Himawari and IODC cover India at ~5 km with ~30 min latency |
| **Open-Meteo forecast API** (past 60 days + 7-day forecast, daily precipitation) | **FACT, verified 8 Oct** | Jaipur's last rain ≥5 mm was **17 Sep 2026 (10.7 mm)**; small showers of 1–2 mm on 27–28 Sep; **forecast 8–14 Oct is dry** (0 mm, probability ≤12%) |
| **NASA POWER on AWS Open Data** (`s3://nasa-power`, Zarr, us-west-2, CC BY 4.0) | FACT | Long-term solar climatology; fallback irradiance. Solar latency 5–7 days, so it is the baseline source, not the live one |
| **CEA CO₂ baseline v22** | FACT | 0.675 tCO₂/MWh (FY25-26) |
| **User inputs** | — | Photos and screenshots, read by a Bedrock vision model with human confirmation |

**Sanity check (INFERENCE):**
1. GTI of ~6.2 kWh/m²/day × 3 kWp × PR 0.78 ≈ **14.5 kWh/day expected**.
2. That is ≈ 4.8 units/kW/day, consistent with the FACT rule of thumb of 4–5.5 units/kW/day.
3. **The engine's core input works for India today.**

**Demo-window insight (INFERENCE from verified data):**
- North-west India has been dry since mid-September, and the coming week is forecast dry.
- Panels there have likely accumulated soiling since the last rain.
- **A cleaning done this weekend should produce a recovery we can attribute to the cleaning, because no rain will confound it.**
- This is exactly the verification moment the winning pattern calls for (02 P2).

### B4. Data limitations and how we handle them

| Limitation | Handling |
|---|---|
| Satellite irradiance error on hazy or partly-cloudy days (INFERENCE: ~5–15% daily) | Use the *ratio* against the system's own post-rain baseline; 7-day rolling windows; confidence bands; no verdict below threshold |
| Panel tilt and azimuth unknown | Ask "flat or raised frame", default 15–20° south, show the assumption, and allow edits. GTI changes modestly with small tilt errors (INFERENCE) |
| Inverter day boundary or timezone quirks | Align to IST; ignore partial days |
| Grid outages (inverters stop under anti-islanding, INFERENCE) | "Off days" are labelled *outage or trip*, not blamed on the vendor |
| Export limits or curtailment | Detect flat-topped midday output if hourly data is available; the MVP flags it as "possible limit" only |
| Net-metering bill ≠ generation | We don't use bills for generation; the inverter is the source of truth |
| Rain threshold for "natural cleaning" (HYPOTHESIS: ≥5 mm/day) | Calibrate from each system's own post-rain PR step-ups; show the evidence |

### B5. Technical feasibility

The engine is deterministic and fits in about 300 lines of Python.

**Inputs:**
- Hourly GTI for the rooftop.
- Ambient temperature.
- Daily actual kWh.

**Steps:**
1. **Expected energy:** `E_exp = Σ_hours GTI × kWp/1000 × (1 + γ·(T_cell − 25))`
   - γ ≈ −0.4%/°C.
   - `T_cell ≈ T_amb + k·GTI`.
2. **Performance ratio:** `PR = E_actual / E_exp`.
3. **Clean baseline:** `PR_clean` = median PR over the 1–3 days after a rain of ≥X mm, or after a confirmed cleaning.
4. **Soiling index:** `SI = PR / PR_clean`.
5. **Verdicts (MVP):**

| Verdict | Rule |
|---|---|
| *Dusty panels* | SI declines with days since rain (slope below a threshold, decent fit), current SI < 0.92 |
| *Off days* | `E_actual ≈ 0` while `E_exp` is high |
| *Persistent shortfall: inspection needed* | `PR_clean` < 0.65 after rain, or a step drop that doesn't recover after rain |
| *Healthy* | None of the above, with confidence |

**Reading photos:**
- A Bedrock multimodal model (Claude or Nova, whichever is enabled in the account) returns JSON of dates and kWh, or a lifetime counter.
- The user confirms or edits before anything is saved.

**Verification loop:**
1. Step Functions Standard: `WaitForReadings` (task token or a wait of N days).
2. `RecomputePR`.
3. `Choice`: recovered ≥ 0.95 × PR_clean → *Resolved*; else *Escalate*.
4. On escalation, the claim pack is regenerated with the new evidence.

**Scheduling:** EventBridge Scheduler handles:
- The fortnightly check-up nudge.
- "Dry spell ≥ 21 days and dry forecast → suggest cleaning".
- MNRE SOP timers: day 8 reminder, day 15 escalation.

**MVP complexity estimate (engineer-hours):**

| Component | Hours |
|---|---:|
| Vision ingest + confirm UI | 6 |
| Irradiance, rain and PV engine | 8 |
| Diagnosis rules + tests | 6 |
| Mobile web UI (onboard, check-up, case, claim) | 10 |
| Claim pack (Bedrock draft + chart) | 3 |
| Step Functions verify loop + Scheduler | 5 |
| IaC and deploy | 4 |
| **Build subtotal** | **~42** |
| Video and writeup | ~8 (separate) |

**Feasible with 3–4 people by Sunday morning.**

### B6. AWS services (each with a verb)

| Service | Job in the story |
|---|---|
| Amazon Bedrock (vision + text) | **Reads** any inverter screen; **explains** in Hindi or English; **drafts** the maintenance claim |
| AWS Lambda | **Computes** expected output and **diagnoses** |
| AWS Step Functions | **Waits** for new readings and **verifies** recovery, or **escalates** |
| Amazon EventBridge Scheduler | **Reminds** (check-ups), **suggests** cleaning in dry spells, **times** vendor SOP deadlines |
| Amazon DynamoDB | **Remembers** systems, readings, cases and evidence |
| Amazon S3 + AWS Open Data (NASA POWER) | **Stores** photos; **provides** the long-term solar baseline |
| Amazon SES / SNS | **Notifies** by email. Indian SMS requires DLT registration (KNOWN), so it is avoided for the MVP |
| AWS Amplify Hosting | **Serves** the mobile web app |
| CloudWatch | **Shows** the loop working, on screen in the video |

### B7. Demo sequence (target 2:50)

| Time | Beat |
|---|---|
| 0:00 | Rooftop B-roll. Text: "50 lakh Indian homes went solar in two years. Nobody checks if it's working." (FACT, sourced) |
| 0:12 | The owner on camera: "I don't know if it's working. The bill went down, so I assume it is." |
| 0:22 | Upload the inverter history screenshot. SunCheck reads 60 days, and the owner confirms |
| 0:40 | Expected (satellite) vs actual chart with rain markers. "After the 17 Sep rain your system ran at 0.82. Today it's 0.71. Dusty panels: ~1.6 units/day lost." *Numbers here are illustrative; the real ones come from the real system* |
| 1:00 | AWS on screen: a Bedrock read in CloudWatch logs; a Step Functions case **waiting** for post-cleaning readings |
| 1:10 | Action: "Dry week ahead, so clean tomorrow 7 AM (safe method)." A second card: "Your vendor owes you 5 years of free maintenance", with the claim pack (chart + clause + SOP clock) |
| 1:30 | Real cleaning B-roll |
| 1:45 | Next-day readings uploaded. The PR returns to baseline. Step Functions goes green: **Recovered** |
| 2:05 | Second system in 15 s: a step drop that doesn't recover → *Inspection needed* → claim sent → day-8 timer |
| 2:20 | Rigour montage: data sources, confidence band, "illustrative/assumption" labels, tests passing |
| 2:38 | Tally card: units/day recovered, ₹/month, kgCO₂/yr. National line: "At a 10% average loss *(assumption)*, that's ~1.4 Mt CO₂ a year." Repo and live URL |

### B8. Likely failure modes

| Failure | Mitigation |
|---|---|
| No real data by Friday | Kill criterion → HeatShift |
| The real system is **clean**, so there is no loss | That is still a valid, honest result: "Healthy, here's the proof." Show the *other* system, or a past dry spell in its history. Never fabricate |
| Vision misreads | Confirm step; unit tests on 10 sample screenshots |
| Satellite API rate limits or outage | Cache; fallback to NASA POWER (lagged) |
| Bedrock model access not enabled | Request on day 1; keep a Nova/Claude fallback |
| New-account limits (Lambda concurrency, CloudFront verification hold, seen in 01) | Plan Amplify Hosting; keep a local-mode recording plan |

### B9. Judge objections and answers

| Objection | Answer |
|---|---|
| "Is this environmental?" | Lost solar kWh are replaced by grid power at 0.675 tCO₂/MWh (FACT). Lead with kWh and CO₂ |
| "Won't government M2M monitoring fix this?" | M2M sends data to central servers for new installs, and its protocols aren't live (FACT). It doesn't tell owners what to do. We'd consume it later |
| "How accurate is satellite irradiance?" | We use ratios against the system's own post-rain baseline, with confidence gating, and show the band |
| "Why would anyone photograph an inverter?" | One screenshot backfills months. After that it's a fortnightly photo, prompted only when it matters, with rupees and a claim as the payoff |
| "Business model?" | Free for owners. Later B2B2C for DISCOMs or state nodal agencies (owner-facing performance), and for vendors who want to *prove* their service. INFERENCE, not built |

### B10. What would have to be true for SunCheck to win

1. **At least one real system** shows a real, explained shortfall, *or* a verified "healthy", on real data.
2. **The verify step happens on camera**, from real post-cleaning or post-rain readings.
3. **A judge understands "expected vs actual" within 10 seconds.** This requires one big number and one chart, not a dashboard.
4. **AWS is visibly the loop:** read (Bedrock), compute (Lambda), wait and verify (Step Functions), remind and time (Scheduler).
5. **The environmental quantity leads**, with rupees second.
6. **The video meets the 02 template:** captions, a real rooftop, a tally card, ≤2:55.
7. **No other Waste & Energy entry ships a weather-normalised, post-install solar loop.** INFERENCE: likely true (see 05).

---

## Part C — Deep dive: I-02 HeatShift (Heat & Water)

### C1. Problem validation

| Claim | Tag | Evidence |
|---|---|---|
| Labour hours | FACT | ILO projects 5.8% of working hours lost by 2030 (~34M full-time jobs). *The Lancet* estimates 181 billion labour hours lost in 2023 |
| Heat illness | FACT | 2024: ~48,000 suspected heatstroke cases and 159 deaths. 2025 (Mar–Jun): 7,192 suspected cases, under-counted |
| Regulatory gap | FACT | No national worker heat standard; only Tamil Nadu's factory rules; heatstroke not an occupational disease under ESI. Heat action plans rarely address workers |

### C2. Target user

**A campus construction contractor or site supervisor** (reachable this weekend on our own campus), and their 20–100 workers.

**Validate:** film a 2-minute interview with a supervisor about how they handle summer heat today.

### C3. Competing solutions

| Solution | What it is | Gap |
|---|---|---|
| OSHA-NIOSH Heat Safety Tool (US) | Heat-index app | Ignores sun load; US-centric (see 04) |
| IMD and NDMA alerts | District-level warnings | No task guidance |
| SEWA insurance | Compensation | Comes *after* the exposure |

**No Indian work-rest planner was found** (INFERENCE).

### C4. Datasets

| Dataset | Tag | Detail |
|---|---|---|
| Open-Meteo forecast | FACT | Hourly temperature, humidity, dew point, wet-bulb, wind and radiation, up to 16 days; no key |
| ECMWF thermofeel | FACT | Apache-2.0; WBGT by the Liljegren method from these inputs |
| Work/rest reference | FACT, example | Mesonet-adapted guidance: at WBGT ~29.4–31.1 °C, moderate work ~40/20 min; above 32.2 °C, heavy work ~10/50 min. **The final table must be transcribed from a primary standard** (ACGIH TLV or ISO 7243) and cited |

### C5. Data limitations

- Forecast grid ≠ site microclimate (concrete slabs, enclosed spaces). Add a surface-type adjustment and a disclaimer.
- Reference tables assume acclimatisation and standard clothing.
- **Outcome is modelled**: high-risk person-hours avoided. Measured outcomes need a season of real site data.

### C6. Feasibility and AWS

| Service | Job |
|---|---|
| Lambda | thermofeel and numpy maths; a greedy task-to-hour scheduler |
| EventBridge Scheduler | 18:00 next-day plan; hourly break reminders |
| Bedrock | Plain-language Hindi briefing |
| Polly | Hindi voice |
| DynamoDB | Plans and check-ins |
| SES / web push | Notifications. Avoid Indian SMS because of DLT registration |

**Complexity:** ~40 engineer-hours.

### C7. Demo sequence

| Time | Beat |
|---|---|
| 0:00 | Site B-roll and the supervisor quote |
| 0:15 | Labelled historical replay of a May 2026 heatwave day |
| 0:35 | The naive plan shows 5.5 high-risk hours. HeatShift's plan shows 0.5, with the same output hours |
| 1:20 | Hindi voice briefing |
| 1:40 | A worker check-in flags dizziness, and the supervisor is alerted |
| 2:00 | Live: tomorrow's plan for a hot city today |
| 2:20 | Rigour: WBGT method and reference table |
| 2:40 | Tally |

### C8. Failure modes and objections

| Issue | Answer |
|---|---|
| "It's October." | Labelled replay plus a live hot-city forecast |
| "Modelled outcome only." | Admitted; show plan-compliance check-ins as a leading indicator |
| "Supervisors won't care." | Same output hours, lower liability |

### C9. What would have to be true for HeatShift to win

1. A **real supervisor** on camera endorses the plan format.
2. The before/after plan is instantly legible.
3. Judges accept a modelled outcome. This is its biggest handicap against SunCheck.
4. The heat season is irrelevant to the judges. **INFERENCE: it partly isn't.**

---

## Part D — Deep dive: I-03 Clean-Air Windows (Air)

### D1. Problem validation

| Claim | Tag | Evidence |
|---|---|---|
| Delhi's air | FACT | 2025 annual PM2.5 was 96 µg/m³ |
| Diurnal swing | FACT | Overnight to 10 AM PM2.5 is ~1.8× the 4–5 PM low (US Embassy, winter 2015–16) |
| Day-level policy | FACT | GRAP hybrid-schooling directives are day-level |

### D2. Target user

**A PE coordinator at an NCR school.** Secondary users: walking groups and sports academies.

### D3. Competing solutions

AQI apps, GRAP circulars, and the school-alert entries we expect (see 05). The only moat is the **timing lever plus a measured counterfactual**.

### D4. Datasets and limitations

| Source | Tag | Limitation |
|---|---|---|
| CPCB real-time data | FACT | **No open API** on data.gov.in |
| OpenAQ on AWS | — | **Freshness for CPCB stations is unverified.** Must be confirmed in the first hour |
| OpenCity CSVs | FACT | Public-domain historical station files exist (e.g. ITO 2017–2023), good for diurnal profiles but not live |
| CAMS via Open-Meteo | FACT | Global domain, ~45 km, 3-hourly for India |

**Risk:** the live feed is the weak link.

### D5. Feasibility, AWS and complexity

**Services:** S3 Open Data (OpenAQ), Lambda, EventBridge Scheduler (06:30), Bedrock (bilingual notices), SES.

**Complexity:** ~32 engineer-hours, *if* live data works.

### D6. Demo sequence

| Time | Beat |
|---|---|
| 0:00 | Smog B-roll and the 8:00 assembly |
| 0:20 | Station profile for this school |
| 0:40 | Swap PE to period 5, and send the parent notice |
| 1:20 | Next day: **measured** PM2.5 at the chosen slot vs the original |
| 1:50 | GRAP Stage III day triggers the indoor plan |
| 2:30 | Tally: student-µg/m³·hours avoided |

### D7. Failure modes and objections

| Issue | Answer |
|---|---|
| Stale data | Kills the live demo |
| Gain within school hours may be small | HYPOTHESIS: 20–40% |
| "Another school AQI app" | The thumbnail problem. Lead with the counterfactual |

### D8. What would have to be true for Clean-Air Windows to win

1. Live, fresh station data reachable via OpenAQ.
2. A real measured reduction of ≥30% within school hours on actual days.
3. A UI that doesn't look like an AQI app.
4. Standing out in the most crowded track.

---

## Part E — Recommendation

**Proceed with I-01 SunCheck in the Waste & Energy track.**

| Rank | Concept | Why |
|---|---|---|
| 1 | **SunCheck** | Highest score (82.0), zero crowding penalty, **data feasibility verified today**, and a real verification moment available this weekend thanks to a dry forecast in north-west India |
| 2 | HeatShift | Fallback if no real solar data is obtained by Fri 14:00 IST |
| 3 | Clean-Air Windows | Only if the team insists on the Air track *and* OpenAQ freshness checks out |

---

## Sources

- **Solar**
  - [SolarQuarter: PM Surya Ghar 50 lakh](https://solarquarter.com/2026/08/07/pm-surya-ghar-scheme-crosses-50-lakh-rooftop-solar-installations-adds-record-5-06-lakh-homes-in-july-2026/)
  - [DTE: generation blind spot](https://www.downtoearth.org.in/amp/story/energy/as-rooftop-solar-scales-up-india-confronts-a-generation-blind-spot)
  - [ETV Bharat: maintenance challenge](https://etvbharat.com/en/bharat/rooftop-solar-push-under-pm-surya-ghar-yojana-crossed-37-lakh-but-maintenance-a-challenge-enn26070705272)
  - [pv magazine: soiling](https://www.pv-magazine-india.com/2021/07/10/the-long-read-the-impact-of-dust-on-solar-panels-matters)
  - [MNRE complaint SOP](https://solarquarter.com/2026/06/25/mnre-introduces-strict-sop-to-address-consumer-complaints-against-solar-vendors-under-pm-surya-ghar-scheme/)
  - [MNRE warranty SOP](https://www.jsalaw.com/wp-content/uploads/2026/05/JSA-Prism-Energy-May-2026-SOP-on-warranty-claims.Final_.pdf)
  - [Business Today: court award](https://www.businesstoday.in/latest/trends/story/rooftop-solar-failed-to-deliver-promised-savings-court-orders-renewable-energy-firm-to-pay-rs25265-541205-2026-07-06)
  - [Outlook Money: 4–5.5 units/kW/day](https://www.outlookmoney.com/personal-finance-news/pm-surya-ghar-muft-bijli-yojana-everything-you-need-to-know-and-amount-of-subsidy)
  - [CEA CO₂ baseline v22](https://cea.nic.in/wp-content/uploads/baseline/2026/09/User_Guide__Version_22.0.pdf)
- **Data, verified by direct call 8 Oct 2026**
  - [Open-Meteo Satellite Radiation API docs](https://open-meteo.com/en/docs/satellite-radiation-api) and the archive endpoint `satellite-api.open-meteo.com/v1/archive` (Jaipur, tilt 20°, azimuth 0)
  - [Open-Meteo forecast API docs](https://open-meteo.com/en/docs) and the `api.open-meteo.com/v1/forecast` daily precipitation call (past 60 days + 7-day forecast)
  - [NASA POWER on AWS](https://registry.opendata.aws/nasa-power/)
- **Heat**
  - [The Week (PTI RTI)](https://www.theweek.in/wire-updates/national/2025/07/27/del4-climate-heat-rti.html)
  - [Newslaundry/IndiaSpend](https://www.newslaundry.com/amp/story/2026%2F04%2F13%2Fas-india-braces-for-summer-informal-workers-have-little-heat-protection)
  - [thermofeel](https://github.com/ecmwf/thermofeel)
  - [St Olaf WBGT work/rest guidelines (Mesonet-adapted)](https://wp.stolaf.edu/ehs/files/2024/05/WBGT-Work-and-Rest-Guidelines.pdf)
  - [OSHA-NIOSH Heat Safety Tool](https://heathealth.info/resources/osha-niosh-heat-safety-tool-app)
- **Air**
  - [CREA NCAP 2026](https://energyandcleanair.org/publication/2026-progress-report-on-national-clean-air-programme/)
  - [r.i.c.e. Delhi hourly PM2.5](https://riceinstitute.org/maps/hourly-variation-in-pm-2-5-in-delhi-december-2015-january-2016/)
  - [data.gov.in AQI resource (no API)](https://www.data.gov.in/resource/real-time-air-quality-index-various-locations)
  - [OpenAQ on AWS](https://registry.opendata.aws/openaq/)
  - [OpenCity ITO CPCB data 2017–2023](https://data.opencity.in/dataset/delhi-hourly-air-quality-reports/resource/ito-cpcb-aqi-data-2017-2023)
  - [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)
