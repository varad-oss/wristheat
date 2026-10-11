# 06 — Whitespace Map

Each gap is described as one row:

> **USER + PAIN + DATA + CONTEXT + INTERVENTION** = where existing solutions (see 04) are weak and the field (see 05) is thin.

Every opportunity then answers the four required questions:
- Why does the gap exist?
- Why hasn't it been solved well?
- Why could we solve it now?
- Why won't a hackathon team think of it?

The **search lens** names which kind of gap it is, from the brief's list:
- Unserved user or workflow
- Unused data combination
- Missing intervention or feedback loop
- Measurement exists but action doesn't
- Prediction exists but decisions don't
- Information exists but behaviour doesn't change
- Tools too broad
- Needs contextual recommendation
- Offline or low-connectivity
- Institutional workflow

---

## W1 — First-time rooftop solar owners: "Is my system actually working?"

| Component | Content |
|---|---|
| USER | A household that installed 1–5 kW under PM Surya Ghar in 2024–26, typically non-technical. The vendor's attention has moved to the next sale |
| PAIN | Output silently drops (dust, droppings, inverter trips, bad wiring or shading). The bill still falls, so the loss is invisible. The owner has a **free 5-year maintenance right** but doesn't know it or can't prove a problem |
| DATA | Inverter daily and lifetime kWh, on the display or app, read via **photo or screenshot**. Satellite irradiance on the panel plane for the exact rooftop: Open-Meteo Himawari/IODC, ~5 km, hourly, global tilted irradiance (GTI) with tilt/azimuth. NASA POWER climatology on **AWS Open Data**. Daily rainfall |
| CONTEXT | **50 lakh homes and counting, ~1 lakh new ones every 6 days.** The government's "generation blind spot". The M2M mandate covers new installs only. MNRE's 2026 complaint SOP can **deactivate vendors that fail promised maintenance** |
| INTERVENTION | Expected vs actual, then a diagnosis (soiling, fault, outage, or chronic under-performance), then an action (rain-aware cleaning plan, or a vendor maintenance claim with an evidence pack and SOP timers), then **verify recovery** from the next readings |

**Search lens:** measurement exists but action doesn't · missing feedback loop · unserved user · unused data combination (satellite irradiance + owner photos + rain).

**The key mechanism insight: rain is a free, natural panel cleaning.**
- The system's own performance ratio (actual ÷ satellite-expected) in the days after meaningful rain is its *clean baseline*.
- Satellite bias largely cancels in that ratio (same site, same model).
- Patterns then separate cleanly:
  - **Slow decline since the last rain:** soiling. The slope is the soiling rate.
  - **Sudden step down:** a fault.
  - **Low even right after rain:** installation, shading or under-capacity.
  - **Zero days:** an outage or inverter trip.
- Status: INFERENCE grounded in standard PV performance-ratio practice. The rain threshold needs calibration (HYPOTHESIS: ~5 mm/day).

| Question | Answer |
|---|---|
| **Why does the gap exist?** | The scheme was designed and measured on installations and subsidy disbursal (FACT). After-sales is the vendor's job, with no independent referee. Utility-scale plants solve this with pyranometers and SCADA; homes have neither |
| **Why hasn't it been solved well?** | Inverter apps show *a* number with no benchmark, are brand-siloed, and get abandoned (FACT: "~99% stop monitoring"). Alert products use manually set thresholds (FACT: Qbits uses <40% for two days), which miss 10–25% soiling losses. The government's M2M data flows *up* to central servers, not *back* to owners as advice |
| **Why could we solve it now?** | ~5 km satellite irradiance with panel-plane GTI is now available for India at ~30-minute latency (FACT). Vision LLMs on Bedrock can read any inverter screen or app screenshot without brand APIs. MNRE's 2026 SOPs create enforceable timelines a tool can track |
| **Why won't a hackathon team think of it?** | The obvious solar ideas are *pre-purchase* (ROI calculators, rooftop potential, subsidy chatbots). Post-install O&M is invisible unless you own a system or read MNRE office memos. Rain-as-calibration needs PV domain knowledge |

---

## W2 — Construction site supervisors: "Who works when, tomorrow, without anyone collapsing?"

| Component | Content |
|---|---|
| USER | A site supervisor or contractor running 20–200 outdoor workers in North, Central or South India |
| PAIN | Heat illness and lost hours (FACT: ILO projects 5.8% of hours lost by 2030). There is no national standard (FACT). Workers skip breaks to hit targets (FACT for garment workers) |
| DATA | Hourly forecast of temperature, humidity, wind, solar radiation and **wet-bulb temperature** (Open-Meteo, FACT). **WBGT via ECMWF thermofeel** (Liljegren method, FACT). A work-intensity × WBGT rest-ratio table (ACGIH/ISO-style, KNOWN) |
| CONTEXT | State advisories shift outdoor hours in heatwaves (KNOWN). Most heat action plans ignore workers (FACT) |
| INTERVENTION | A next-day plan: heavy tasks moved to cooler hours, rest cycles per hour, water and shade checkpoints, and a voice check-in for workers in Hindi, signed off by the supervisor. Verify it was followed via check-ins (weak) |

**Search lens:** prediction exists but decisions don't · institutional workflow · tools too broad (district-level warnings).

| Question | Answer |
|---|---|
| **Why does the gap exist?** | Heat is treated as a weather and health warning, not an operations-planning input. WBGT isn't measured on Indian sites |
| **Why hasn't it been solved well?** | Worker-facing tools are US-centric (OSHA-NIOSH app) and use heat index, which ignores sun load. Indian systems stop at district warnings |
| **Why could we solve it now?** | Free hourly forecasts with radiation and wet-bulb, plus an open WBGT library (FACT) |
| **Why won't a hackathon team think of it?** | The default heat idea is an "alert + tips" bot. In October, heat isn't top of mind in Delhi |

---

## W3 — Schools, sports coaches and morning walkers in NCR: "When today is least bad"

| Component | Content |
|---|---|
| USER | School principals and PE coordinators; residential society walking groups; sports academies |
| PAIN | Assemblies, PE and morning walks fall in the worst hours of winter days. Overnight to mid-morning PM2.5 is ~1.8× the afternoon low (FACT, US Embassy data). GRAP decisions are day-level and binary (FACT) |
| DATA | The nearest station's own hourly history (OpenAQ on AWS, FACT) gives a *station-specific* diurnal profile. CAMS forecasts give the multi-day trend: coarse, 45 km and 3-hourly for India (FACT). GRAP stage notices |
| CONTEXT | Smog season is Oct–Jan. Schools already receive GRAP circulars |
| INTERVENTION | A daily "clean window" timetable swap (e.g. PE from period 1 to period 5), an indoor fallback plan, and a parent notice. **Verify** with the *measured* station value at the chosen hour versus the original slot. That is a real counterfactual, computed from real data |

**Search lens:** information exists but behaviour doesn't change · needs contextual recommendation · institutional workflow.

| Question | Answer |
|---|---|
| **Why does the gap exist?** | AQI tools report levels; nobody owns "re-time the day". Hourly forecasts are too coarse for India, so products avoid hour-level advice |
| **Why hasn't it been solved well?** | The diurnal cycle is well known to scientists but rarely productised. Using each station's *own history* sidesteps forecast coarseness |
| **Why could we solve it now?** | OpenAQ's archive on S3, and Bedrock to draft bilingual notices |
| **Why won't a hackathon team think of it?** | Many *will* do school AQI alerts (FACT: the organisers suggest it). Few will notice the timing lever. Risk: our version reads as "another school AQI app" in the thumbnail |

---

## W4 — Campus hostels, messes and RWAs under SWM Rules 2026: "Are we compliant, and is segregation actually happening?"

| Component | Content |
|---|---|
| USER | Campus estate office, hostel wardens, mess managers, RWA secretaries |
| PAIN | Universities and societies are **bulk waste generators** (FACT). They must segregate four streams and process wet waste on site or obtain certificates (FACT). Environmental compensation applies; reporting is digital (FACT). Segregation quality is invisible day to day |
| DATA | Bin photos (vision-graded contamination), daily weights entered by staff, compost output |
| CONTEXT | The rules have applied since 1 Apr 2026 (FACT). Institutions lack tools |
| INTERVENTION | Per-wing contamination score, then targeted nudges, then a monthly compliance pack. Verify via the contamination trend |

**Search lens:** institutional workflow · new obligation without tooling.

| Question | Answer |
|---|---|
| **Why does the gap exist?** | The rules are six months old |
| **Why hasn't it been solved well?** | Waste tools target households or municipalities, not bulk-generator compliance |
| **Why could we solve it now?** | Vision LLMs grade bin photos; rule thresholds are explicit (FACT) |
| **Why won't a hackathon team think of it?** | Most will build "which bin does this go in?" classifiers. The regulatory hook needs reading the 2026 rules |

---

## W5 — Housing societies on tankers: "Did we get what we paid for?"

| Component | Content |
|---|---|
| USER | Society facility managers in water-stressed cities (Bengaluru, Chennai, Delhi periphery) |
| PAIN | Price spikes (FACT: ₹1,800–2,000 per 12,000 L before the caps). Unverified volumes and short-delivery (HYPOTHESIS). Groundwater-sourced tankers (INFERENCE) |
| DATA | Sump level before and after delivery (dipstick or gauge photo) × sump geometry gives litres. Official rate card (FACT) |
| INTERVENTION | Per-delivery verification, then dispute evidence, then a monthly demand and leak trend |

**Search lens:** measurement absent at the point of transaction · community workflow.

| Question | Answer |
|---|---|
| **Why does the gap exist?** | Informal market, cash or UPI, no metering at delivery |
| **Why hasn't it been solved well?** | Booking apps focus on supply, not verification |
| **Why could we solve it now?** | Phone photos + vision reading + geometry |
| **Why won't a hackathon team think of it?** | Most see tankers as a marketplace problem |
| **Weakness** | The environmental impact is indirect (fairness > environment). Measurement accuracy is uncertain |

---

## W6 — Smart-metered households on time-of-day tariffs: "Run the pump at noon"

| Component | Content |
|---|---|
| USER | Households with smart meters, especially rooftop solar owners |
| PAIN | Solar hours are 10–20% cheaper and peak hours 10–20% costlier (FACT), yet loads aren't shifted |
| DATA | Tariff orders, meter interval data, solar generation |
| INTERVENTION | A shiftable-load schedule (pump, washing machine, geyser, EV), then bill verification |

**Search lens:** information exists but behaviour doesn't change.

| Question | Answer |
|---|---|
| **Why does the gap exist?** | The tariff structure is new and its rollout uneven (INFERENCE) |
| **Why hasn't it been solved well?** | Meter data access is DISCOM-specific |
| **Why could we solve it now?** | The tariffs exist from 2025 (FACT) |
| **Why won't a hackathon team think of it?** | Low salience |
| **Weakness** | Data access and state-by-state variation. **Best used as a W1 extension**, not standalone |

---

## W7 — Street vendors on heat days

| Component | Content |
|---|---|
| USER | Vendors, 89% of whom have no free drinking water (FACT) |
| INTERVENTION | Heat-hour plan, water points, and a parametric-insurance trigger tracker (SEWA, FACT) |

| Question | Answer |
|---|---|
| **Why does the gap exist?** | Vendors are excluded from heat action plans (FACT) |
| **Why hasn't it been solved well?** | Low digital access |
| **Why could we solve it now?** | Voice and IVR via Polly or Connect (INFERENCE) |
| **Why won't a hackathon team think of it?** | Out of sight for students |
| **Weakness** | Users are hard to reach and the demo is weak in October |

---

## W8 — Waste pickers: price transparency and receipts

| Component | Content |
|---|---|
| USER | Informal pickers, who handle 60–70% of recyclables but are excluded from EPR (FACT) |
| INTERVENTION | Daily price board, digital receipts, and verified collection records that could feed EPR credits |

| Question | Answer |
|---|---|
| **Why does the gap exist?** | Informality |
| **Why hasn't it been solved well?** | Marketplaces bypass pickers (INFERENCE) |
| **Why could we solve it now?** | Phones are ubiquitous (INFERENCE) |
| **Why won't a hackathon team think of it?** | Most build "Uber for scrap" |
| **Weakness** | We can't reach real pickers this weekend, so the demo would be simulated |

---

## W9 — Delivery and gig riders: exposure-aware shift planning

| Component | Content |
|---|---|
| USER | Riders; the platforms that schedule them |
| INTERVENTION | Heat- and AQI-aware shift windows and rest stops |

**Weakness:** the platforms are the deciders and aren't reachable; riders can't change slots freely (INFERENCE).

---

## W10 — NCR construction sites: "GRAP-ready" task planning

| Component | Content |
|---|---|
| USER | Site managers |
| PAIN | Stage III–IV construction curbs halt work (KNOWN) |
| INTERVENTION | Use AQI trend forecasts to pull dust-heavy tasks forward and plan around likely bans |

**Weakness:** GRAP stage forecasting is uncertain, and the incentive is commercial (INFERENCE).

---

## Ranking the whitespace

| Rank | Opportunity | Gap strength | Data availability | Demo-ability this weekend | Verify step possible | Environmental quantity |
|---|---|---|---|---|---|---|
| 1 | **W1 Solar post-install** | Very high | High (satellite + photos) | High (real systems, real data) | **Yes** (post-rain or post-cleaning PR) | kWh, kgCO₂ |
| 2 | **W2 WBGT work-rest** | High | High (forecasts + thermofeel) | Medium (October; historical replay) | Weak | Heat-risk hours |
| 3 | **W3 Clean-air windows** | Medium | Medium (OpenAQ history; CAMS coarse) | High in NCR now | **Yes** (measured counterfactual) | µg/m³·h avoided |
| 4 | W4 SWM 2026 compliance | Medium-high | Medium (user-generated) | Medium | Yes (trend) | kg segregated |
| 5 | W5 Tanker verification | Medium | Medium | Medium | Yes | Litres |
| 6 | W6 ToD shifting | Medium | Low (meter access) | Low | Yes (bill) | kWh shifted |
| 7–10 | W7–W10 | Varies | Low–medium | Low | Weak | — |

---

## Sources

The sources are as cited in 03 and 04. Key ones:
- [DTE generation blind spot](https://www.downtoearth.org.in/amp/story/energy/as-rooftop-solar-scales-up-india-confronts-a-generation-blind-spot)
- [ETV Bharat on maintenance](https://etvbharat.com/en/bharat/rooftop-solar-push-under-pm-surya-ghar-yojana-crossed-37-lakh-but-maintenance-a-challenge-enn26070705272)
- [MNRE complaint SOP](https://solarquarter.com/2026/06/25/mnre-introduces-strict-sop-to-address-consumer-complaints-against-solar-vendors-under-pm-surya-ghar-scheme/)
- [Open-Meteo Satellite Radiation API](https://open-meteo.com/en/docs/satellite-radiation-api)
- [Qbits](https://qbitsenergy.com/blog/whatsapp-solar-monitoring/)
- [thermofeel](https://github.com/ecmwf/thermofeel)
- [Open-Meteo forecast API](https://open-meteo.com/en/docs)
- [r.i.c.e. Delhi hourly PM2.5](https://riceinstitute.org/maps/hourly-variation-in-pm-2-5-in-delhi-december-2015-january-2016/)
- [OpenAQ on AWS](https://registry.opendata.aws/openaq/)
- [SWM Rules 2026](https://www.drishtiias.com/daily-updates/daily-news-analysis/solid-waste-management-swm-rules-2026/print_manually)
- [Bengaluru tanker rates](https://businesstoday.in/india/story/bengaluru-water-crisis-district-administration-fixes-rates-for-water-tanker-services-420502-2024-03-07)
- [ToD tariffs](https://eastmojo.com/national/2023/06/23/new-power-tariff-rule-save-up-to-20-for-usage-during-solar-hours/)
