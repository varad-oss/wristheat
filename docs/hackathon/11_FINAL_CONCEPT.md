# 11 — Final Concept: **SunCheck** (working name)

> **Superseded (9 Oct 2026).** Round 2 reopened ideation, and SunCheck was dropped as primary because the team has no access to a real system's generation history (constraint C). See [`round2/08_GO_NO_GO.md`](round2/08_GO_NO_GO.md) for the current recommendation. This file is kept for the record.

**Track:** 03 Waste & Energy (rooftop solar)

**One line:** Photograph your inverter. SunCheck compares what your panels made with what the sun actually delivered to your roof, tells you why you're short, gets it fixed under the free maintenance you're already owed, and proves the fix worked.

**Naming:** the name is open. Alternatives are *Dhoop Doctor* and *Watt's Missing*. We deliberately avoid the "-Guard/-Shield/-Kavach" pattern, which appeared in 99 of 1,180 titles at the last event.

---

## THE PROBLEM

Rooftop solar on India's 50 lakh new PM Surya Ghar homes silently loses 5–30% of its output to dust and faults. Nobody compares what each system produced with what the sun actually delivered, so owners never invoke the free five-year maintenance that would fix it.

## THE USER

A non-technical homeowner in a dry, dusty city of north-west or north India, such as Jaipur, Delhi-NCR or Ahmedabad.
- They have a **2–3 kW PM Surya Ghar system** installed in 2024–26 by an empanelled vendor who has moved on.
- They see a number on the inverter but no benchmark.
- Their bill went down, so they assume everything is fine.

## THE INSIGHT

**Rain is a free panel cleaning.**
- A system's own performance in the days right after rain, measured against **satellite sunshine for that exact roof and tilt**, is its clean baseline.
- From then on, a slow slide that resets after rain means dust.
- A drop that *doesn't* reset means a fault.
- Zero days mean trips or outages.

This turns a number nobody understands into a verdict anyone can act on, with no sensor, no inverter API and no installer cooperation.

The second half of the insight: **the fix is already paid for.**
- Empanelled vendors owe five years of free maintenance as a subsidy condition.
- Since June 2026, MNRE's complaint SOP can deactivate vendors that don't deliver it.
- Owners lack only the evidence and the clock.

## THE WEDGE

Two things every owner already has, but nobody has connected:
1. **The inverter screen or app.** Read from a photo or screenshot by vision AI, it is brand-agnostic and needs zero integrations. One history screenshot backfills months on the first day.
2. **The five-year free maintenance right**, which most owners don't know about.

**Entry moment:** the dry season (Oct–Jun in north and north-west India), when soiling accumulates and rain no longer cleans the panels.

## THE CORE MECHANISM

1. **READ.** The owner uploads an inverter screenshot or photo. Bedrock extracts daily or lifetime kWh, and the owner confirms the numbers before anything is used.
2. **EXPECT.** Hourly satellite **global tilted irradiance** for the roof's coordinates, tilt and azimuth, plus temperature, gives expected kWh. Daily rain history marks the natural cleanings.
3. **DIAGNOSE.** Deterministic rules on the performance ratio (PR) and soiling index, gated by confidence, return one of four verdicts:
   - **Healthy**
   - **Dusty panels** (with units lost per day)
   - **Off days** (outage or trip)
   - **Persistent shortfall: inspection needed**
4. **ACT.**
   - *Dusty panels:* a rain-aware cleaning plan ("dry week ahead, clean tomorrow 7 AM, safely").
   - *Inspection needed:* a **maintenance claim pack**. It contains the evidence chart, the 5-year maintenance clause and the MNRE SOP timeline. The owner sends it; SunCheck tracks the day-8 and day-15 clock.
5. **VERIFY.** A long-running workflow waits for the next readings, recomputes PR, and marks the case **Recovered** or escalates with fresh evidence.

## THE DIFFERENTIATOR

| What others build | What it does | SunCheck |
|---|---|---|
| Solar ROI calculators / subsidy chatbots | Answer "should I buy?" | Answers "is the system I bought working?" |
| Inverter apps | Show a number with no benchmark | Benchmarks against the sun that actually fell on *your* roof today |
| Alert services | Use manual thresholds (e.g. <40% for 2 days), so they miss 10–25% dust losses | Normalised by weather, so small losses become visible |
| Government M2M monitoring | Sends data *up* to central servers, for new installs, with protocols not live | Brings a diagnosis *back down* to the owner, for any system |
| Generic "AI sustainability assistant" | Chats | Reads, computes, acts, and **verifies** |

## THE OUTCOME

**For the owner:**
- Knows within a minute whether the system is healthy.
- Recovers lost units, roughly ₹ per month.
- Gets the vendor to honour maintenance, with evidence and a clock.

**For the environment:**
- Every recovered kWh is clean power not replaced by grid power at **0.675 tCO₂/MWh** (CEA, FY25-26).
- National framing, stated as an assumption on screen: at a 10% average loss, PM Surya Ghar rooftops leak about 2 TWh, or ~1.4 Mt CO₂, a year.

**The quiet-by-design success state:** most check-ups say "Healthy. Here's the proof."

## THE DEMO MOMENT

**The recovery line.**
1. After the panels are cleaned, the next day's actual output **snaps back onto the satellite-expected line** on the chart.
2. The case's Step Functions execution flips from **Waiting → Recovered** on screen.
3. The tally reads **"+N units/day recovered — verified."**

**Why it's achievable this weekend (verified on 8 Oct):**
- Jaipur's last meaningful rain was 17 Sep.
- The 8–14 Oct forecast is dry.
- So any recovery after cleaning is attributable to the cleaning alone.

## AWS

AWS is genuinely part of the solution. Each service does a job the product can't do without.

| Service | Job |
|---|---|
| **Amazon Bedrock** (vision + text) | The *only* practical way to support every inverter brand without integrations: reads any screen, explains in Hindi or English, drafts the claim |
| **AWS Step Functions** | The verify loop is a workflow that waits *days* for new readings, then branches to recovered or escalate. This is the core of the product, not decoration |
| **Amazon EventBridge Scheduler** | Check-up nudges, dry-spell cleaning prompts, MNRE SOP deadline timers |
| **AWS Lambda** | The PV expectation and diagnosis engine |
| **Amazon DynamoDB** | Systems, readings, cases, evidence |
| **Amazon S3 + AWS Open Data (NASA POWER)** | Photos; the long-term solar baseline and fallback |
| **Amplify Hosting · SES · CloudWatch** | Mobile web app; notifications; the logs and graphs we show on screen |

The whole stack is serverless and pay-per-use, so it stays inside the Free Tier.

## COMPETITION

In the Waste & Energy track, expect the following (see 05):
- Waste image classifiers ("which bin?").
- Smart bins and collection routing.
- Scrap and kabadiwala marketplaces.
- E-waste locators.
- Gamified carbon trackers.
- EV charger finders.
- **Solar ROI calculators, rooftop-potential estimators and PM Surya Ghar subsidy chatbots.**

All of these stop at information. Almost none verify an outcome.

## OUR ADVANTAGE

1. **Post-install, not pre-purchase:** a lane competitors don't see.
2. **Physics plus a rain-calibration trick:** more accurate than thresholds, and impossible to stumble into from a generic prompt.
3. **A legal and institutional hook:** the 5-year maintenance condition and MNRE's 2026 complaint and warranty SOPs.
4. **Real data, verified feasible today:** satellite GTI and rain for India, confirmed by direct API calls.
5. **A verification loop on camera:** the strongest winner pattern from First Commit (see 02, P2).
6. **Built for where the user is:** a phone photo, Hindi and English, rupees, the owner's own vendor.

## WHAT WE REFUSE TO BUILD

| Out of scope | Why |
|---|---|
| Native mobile apps | Mobile web only |
| Hardware, IoT, sensors | — |
| Inverter cloud API integrations (any brand) | Photos and screenshots only |
| Accounts or auth beyond the minimum demo identity | — |
| WhatsApp Business API, Indian SMS (DLT), IVR | — |
| Maps, cleaner marketplace, payments, financing, carbon credits | — |
| ML model training or forecasting | Deterministic engine plus Bedrock reading only |
| Shading analysis, 3D roof modelling, string-level diagnostics | — |
| Time-of-day tariff optimiser | A "coming next" card at most |
| Submitting complaints to government portals for the user | The owner sends the pack |
| Languages beyond Hindi and English | — |
| A generic chatbot | — |

---

## Gates before and at the start of Phase 12

| Gate | Condition | If it fails |
|---|---|---|
| **G1, by 12:00 IST Fri 9 Oct** | Secure **≥1 real system** with 30+ days of daily generation history (screenshots), plus kWp, install date, roof type, approximate direction and vendor name. Owner consent for a short clip | By **Fri 14:00**, switch to the documented fallback **HeatShift** (see 10, Part C) |
| **G2** | Bedrock model access (vision-capable) enabled in the team AWS account | — |
| **G3** | Official deadline hour confirmed on the schedule page or Discord | Plan to internal deadline Sunday 16:00 IST until known |

Collecting user data and interviews is validation, not coding, so it is allowed before approval.

---

## ⛔ STOP: awaiting explicit approval

Research and concept selection (Phases 0–11) are complete. **No architecture or code has been written.**

On approval, Phase 12 produces `12_ARCHITECTURE.md` and `13_EXECUTION_PLAN.md`, using Superpowers and feature-dev, and builds one complete vertical slice first: read → expect → diagnose → act → verify.
