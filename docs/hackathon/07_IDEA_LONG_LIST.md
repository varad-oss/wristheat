# 07 — Idea Long List (23 concepts)

## How to read this list

- **Diversity is forced across:**
  - **User:** households, supervisors, principals, wardens, officers, vendors, pickers, riders, farmers.
  - **Geography:** NCR, Bengaluru, Punjab, campus, rural, slum.
  - **Model:** B2C, B2B, B2G, community, NGO.
  - **Tech:** vision LLM, forecasts, satellites, IoT, voice.
- **Name and track:** names are working titles, deliberately avoiding the "-Guard/-Shield" cliché (see 01 §8). Each idea's track is in its heading.
- **Fields:** each concept answers the 16 required fields. "AWS" names only services that do a real job.

---

### I-01 · SunCheck: a rooftop solar check-up that enforces your free maintenance (Waste & Energy)

1. **One-liner:** Photograph your inverter. SunCheck compares what you made with what today's sunshine *should* have made, says why you're short, gets it fixed, and proves the fix worked.
2. **User:** A non-technical household with a 1–5 kW PM Surya Ghar system. For example: Sunita, Jaipur, 3 kW, installed in 2025.
3. **Pain:** Output silently falls to dust, droppings, trips and faults, losing 5–30% (FACT). Owners stop monitoring (FACT) and don't know about the free 5-year maintenance (FACT).
4. **Workaround:** A glance at the inverter number with no benchmark, then calling the vendor only when output hits zero.
5. **Core insight:** Rain is a free, natural panel cleaning. Each system's own post-rain performance against satellite irradiance is its baseline, so no sensors or vendor API are needed.
6. **Mechanism:**
   1. Photo or screenshot, read by a vision LLM into daily/lifetime kWh.
   2. Satellite global tilted irradiance (GTI) for the exact rooftop, plus rain history.
   3. Performance ratio (PR) series.
   4. Classify the shortfall: soiling slope, step fault, zero-day trip, or chronic low.
   5. Act: a rain-aware cleaning plan, or a vendor claim pack with MNRE SOP timers.
   6. Verify with post-action PR.
7. **Unique differentiator:** Independent and weather-normalised. Brand-agnostic via photos. Tied to an enforceable right and a verification loop.
8. **Why others won't copy:** Requires PV domain mechanics and knowing the 2026 MNRE SOPs. The obvious solar idea is pre-purchase.
9. **Data:** Open-Meteo satellite radiation (Himawari/IODC ~5 km); NASA POWER on AWS (climatology); rain; owner photos; system metadata (kWp, tilt, azimuth).
10. **AWS role:**
    - Bedrock (multimodal read; bilingual explanations and claim drafts).
    - Lambda (PV model with pvlib).
    - Step Functions (verify-after-action loop with waits).
    - EventBridge Scheduler (weekly check-ups, rain-aware nudges, SOP deadline timers).
    - DynamoDB (systems, readings, cases).
    - S3 (photos; NASA POWER open data).
    - SNS/SES (notifications); Amplify (mobile web).
11. **MVP:**
    - One system onboarded.
    - Photo → read → expected vs actual chart → diagnosis → action card.
    - Claim draft → verify loop on the next readings.
12. **3-min demo story:**
    - A real rooftop and a real inverter photo.
    - The chart shows actual drifting below expected since the last rain 40+ days ago.
    - "Losing ~3 units/day, ₹X/month."
    - Clean or claim.
    - Next readings: PR back up. "Recovered."
    - Tally card: kWh, ₹, kgCO₂, and the national scale.
13. **Measurable outcome:** kWh/day recovered, ₹/month, kgCO₂/year (CEA 0.675–0.710 t/MWh), and claim days-to-resolution.
14. **Biggest technical risk:** Satellite/model error vs real output; misreading photos; needing ≥2 weeks of daily data for trend detection.
15. **Biggest product risk:** Getting real systems' data this weekend. Owners may not care if savings feel "good enough".
16. **Competition risk:** Low. Solar ROI calculators will be common; post-install performance will be rare.

### I-02 · HeatShift: tomorrow's work-rest plan for a hot site (Heat & Water)

1. **One-liner:** Turns tomorrow's hourly forecast into a WBGT-based shift plan a site supervisor signs, with Hindi voice check-ins for workers.
2. **User:** A construction site supervisor with 50 workers in Nagpur or Hyderabad.
3. **Pain:** Heat illness, lost hours (FACT: ILO projects 5.8% of hours lost by 2030), and no standard (FACT).
4. **Workaround:** "Avoid noon" advisories; workers push through.
5. **Core insight:** Heat risk depends on *task intensity × WBGT × hour*, so moving heavy tasks earlier cuts risk without cutting hours.
6. **Mechanism:**
   1. Forecast plus thermofeel gives hourly WBGT.
   2. A rest-ratio table per intensity.
   3. An optimiser assigns tasks to hours.
   4. Plan PDF plus voice briefing.
   5. Worker check-ins flag symptoms.
   6. Escalate to the supervisor.
7. **Unique differentiator:** Plans, not alerts. WBGT, not temperature.
8. **Why others won't copy:** WBGT and work-rest science is niche; the default heat idea is an alert bot.
9. **Data:** Open-Meteo hourly (temperature, RH, wind, radiation, wet-bulb); thermofeel; site task list.
10. **AWS role:** Lambda (WBGT + optimiser); EventBridge Scheduler (evening plan, hourly reminders); Bedrock (plain-language Hindi briefings); Polly (voice); DynamoDB; SNS.
11. **MVP:** Task list → next-day plan → voice briefing → check-in form → escalation.
12. **3-min demo story:**
    - A real May 2026 heatwave day (historical replay, labelled).
    - The naive plan shows 5.5 high-risk hours; HeatShift's plan shows 0.5, with the same output hours.
    - A worker reports dizziness and the supervisor is pinged.
13. **Measurable outcome:** High-risk person-hours avoided; productive hours preserved.
14. **Biggest technical risk:** WBGT estimation error; optimiser complexity.
15. **Biggest product risk:** Supervisors' incentives favour output; in October the heat story is off-season.
16. **Competition risk:** Low–medium (heat alerts are crowded; planning isn't).

### I-03 · Clean-Air Windows: when today is least bad, for this school (Air)

1. **One-liner:** Each morning it tells a school which periods are safest for PE and assembly, using its nearest station's own hourly pattern, then proves the exposure avoided.
2. **User:** A PE coordinator or principal at an NCR school.
3. **Pain:** Outdoor activity in the worst hours (FACT: overnight to 10 AM PM2.5 is ~1.8× the afternoon low).
4. **Workaround:** Cancel everything on GRAP days, or ignore AQI.
5. **Core insight:** Within-day timing is a bigger lever than within-city routing, and the station's own recent diurnal profile beats coarse forecasts for India.
6. **Mechanism:**
   1. OpenAQ history gives a station-specific hourly profile.
   2. Today's trend comes from CAMS plus the latest readings.
   3. The timetable optimiser swaps outdoor periods.
   4. A bilingual parent notice is drafted.
   5. **Verify** with the measured PM2.5 at the chosen hour vs the original.
7. **Unique differentiator:** A timetable change plus a measured counterfactual.
8. **Why others won't copy:** Most will send "AQI is bad" alerts.
9. **Data:** OpenAQ (S3/API); Open-Meteo CAMS; school timetable; GRAP status.
10. **AWS role:** S3 Open Data (OpenAQ); Lambda; EventBridge Scheduler (06:30 daily plan); Bedrock (notices); DynamoDB; SES/SNS.
11. **MVP:** One school, one station, daily plan, notice, next-day verify.
12. **3-min demo story:** 8:00 assembly vs a 12:20 slot, then the measured exposure, 40 kids, µg/m³·h avoided, then a GRAP Stage III day triggering the indoor plan.
13. **Measurable outcome:** Student-µg/m³·hours avoided per week.
14. **Biggest technical risk:** Station data gaps; CAMS coarseness; school hours may miss the afternoon minimum.
15. **Biggest product risk:** Timetables are rigid.
16. **Competition risk:** **High at the topic level** (schools on bad days is suggested by the organisers).

### I-04 · BinScore 2026: SWM Rules compliance loop for hostels and societies (Waste & Energy)

1. **One-liner:** Wardens photograph bins. Vision grading scores each wing's segregation, nudges the worst floor, and auto-builds the bulk-generator compliance pack.
2. **User:** A hostel warden or estate office; an RWA secretary.
3. **Pain:** New four-stream and on-site wet-waste duties (FACT), environmental compensation (FACT), and no visibility of segregation.
4. **Workaround:** Paper registers and occasional drives.
5. **Core insight:** Compliance is driven by *where* contamination happens (which wing, which day), not by awareness posters.
6. **Mechanism:**
   1. Daily bin photos per wing are graded by a vision LLM for contamination per stream.
   2. Weights are logged.
   3. Leaderboard and targeted nudges.
   4. Monthly compliance PDF.
7. **Unique differentiator:** A regulatory hook plus a per-wing feedback loop.
8. **Why others won't copy:** Requires knowing the 2026 rules. Others classify single items.
9. **Data:** User photos, weights, rule thresholds.
10. **AWS role:** Bedrock vision; S3; Lambda; DynamoDB; EventBridge (daily summaries); SES.
11. **MVP:** Two wings, a week of photos, scores, nudge, compliance pack.
12. **3-min demo story:** Wing B's dry bin is 40% wet waste; a nudge goes out; three days later it's 12%; the monthly pack is generated.
13. **Measurable outcome:** Contamination %; kg correctly segregated; kg composted.
14. **Biggest technical risk:** Vision grading accuracy on messy bins.
15. **Biggest product risk:** Institutions may game photos.
16. **Competition risk:** Medium (waste vision is crowded; the compliance framing is rare).

### I-05 · TankerTruth: did we get 12,000 litres? (Heat & Water)

1. **One-liner:** The facility manager photographs the sump gauge before and after a tanker. TankerTruth computes litres delivered, checks the price against the official cap, and flags short-delivery.
2. **User:** A society facility manager in Bengaluru.
3. **Pain:** Price gouging (FACT) and unverified volumes (HYPOTHESIS).
4. **Workaround:** Trust, or argue.
5. **Core insight:** The sump *is* a meter if you know its geometry.
6. **Mechanism:** Two photos, read by vision, give the volume delta. That is compared with the invoice, then a rate-card check, then a monthly pattern.
7. **Unique differentiator:** Verification rather than booking.
8. **Why others won't copy:** Not obvious; it requires a physical measurement trick.
9. **Data:** Photos, sump dimensions, rate card (FACT).
10. **AWS role:** Bedrock vision; Lambda; DynamoDB; SNS.
11. **MVP:** Sump setup, delivery check, dispute note.
12. **3-min demo story:** An invoice for 12,000 L against a measured 9,800 L, giving an 18% short delivery, then the monthly loss.
13. **Measurable outcome:** Litres and ₹ recovered.
14. **Biggest technical risk:** Gauge-reading accuracy.
15. **Biggest product risk:** Weak environmental framing; few societies have readable gauges.
16. **Competition risk:** Low.

### I-06 · NightFlow: find the building leak from the 2 AM water level (Heat & Water)

1. **One-liner:** A ₹500 level sensor on the overhead tank. When nobody is using water at night and the level still drops, that's a leak.
2. **User:** An RWA plumber or facility manager.
3. **Pain:** Hidden leaks and overflowing tanks (INFERENCE). Utility NRW is ~38% (FACT), and buildings add their own losses.
4. **Workaround:** Notice a damp wall months later.
5. **Core insight:** Minimum night flow, the standard utility leak method, scaled down to one tank.
6. **Mechanism:** ESP32 ultrasonic sensor sends to IoT Core, which builds a night drawdown baseline, which raises a leak alert.
7. **Unique differentiator:** A utility-grade method at building scale.
8. **Why others won't copy:** Medium; the IoT itself is common.
9. **Data:** Sensor time series.
10. **AWS role:** IoT Core; Timestream or DynamoDB; Lambda; SNS.
11. **MVP:** One tank with simulated leaks.
12. **3-min demo story:** A night graph with a leak introduced and an alert.
13. **Measurable outcome:** Litres per night saved.
14. **Biggest technical risk:** Hardware time; sensor noise.
15. **Biggest product risk:** Install friction.
16. **Competition risk:** Medium.

### I-07 · Walk-Shift: move the 6 AM walk to 4 PM (Air)

1. **One-liner:** Weekly WhatsApp/voice nudges to elderly walking groups showing how much smog they avoid by walking in the afternoon.
2. **User:** Senior-citizen walking groups in Delhi parks.
3. **Pain:** Morning walks fall in the worst hours (FACT, diurnal profile).
4. **Workaround:** Walk anyway, or stay home.
5. **Core insight:** Habit plus the diurnal cycle.
6. **Mechanism:** Station profile, best window, group nudge, then a weekly exposure report.
7. **Unique differentiator:** Timing as the intervention.
8. **Why others won't copy:** Medium.
9. **Data:** OpenAQ, CAMS.
10. **AWS role:** Lambda; EventBridge; Polly; SNS.
11. **MVP:** One park group.
12. **3-min demo story:** Exposure comparison and a shift nudge.
13. **Measurable outcome:** µg/m³·h avoided.
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** Habit change is slow; the WhatsApp API is gated.
16. **Competition risk:** Medium. **Will merge into I-03.**

### I-08 · GRAP-Ready: plan dusty work before the curbs land (Air)

1. **One-liner:** For NCR construction managers: forecasts which days GRAP curbs are likely and re-sequences dust-heavy tasks.
2. **User:** A site manager.
3. **Pain:** Work stoppages under Stage III–IV (KNOWN).
4. **Workaround:** React when orders arrive.
5. **Core insight:** Curbs follow AQI trajectories that can be partially anticipated.
6. **Mechanism:** AQI trend forecast, stage-probability estimate, schedule re-sequencing.
7. **Unique differentiator:** A business-continuity framing that also reduces dust.
8. **Why others won't copy:** Medium.
9. **Data:** CAMS, CPCB history, GRAP orders.
10. **AWS role:** Lambda; EventBridge; Bedrock; DynamoDB.
11. **MVP:** One site schedule.
12. **3-min demo story:** Stage probability rises, so earthwork is pulled forward.
13. **Measurable outcome:** Idle days avoided.
14. **Biggest technical risk:** Forecast skill.
15. **Biggest product risk:** The incentive is commercial; the environmental gain is indirect.
16. **Competition risk:** Low.

### I-09 · Straw Link: get the baler to the field before the match (Air)

1. **One-liner:** Matches Punjab farmers who are about to harvest with baler operators and straw buyers, prioritised by each village's fire history.
2. **User:** Custom hiring centres; farmers.
3. **Pain:** A short harvest-to-sowing window, so fires happen (FACT: 2,518 Punjab fires in 2025).
4. **Workaround:** Burning, or government CRM machines that arrive late (INFERENCE).
5. **Core insight:** Fires are a logistics-timing failure.
6. **Mechanism:** Fire history plus harvest calendar, priority queue, booking.
7. **Unique differentiator:** Logistics, not detection.
8. **Why others won't copy:** Medium.
9. **Data:** FIRMS, village lists.
10. **AWS role:** Lambda; DynamoDB; SNS; Location Service.
11. **MVP:** A simulated district.
12. **3-min demo story:** Fire-prone villages are prioritised and a baler is routed.
13. **Measurable outcome:** Acres baled instead of burned.
14. **Biggest technical risk:** Data access.
15. **Biggest product risk:** Users are unreachable this weekend; the demo would be fully simulated.
16. **Competition risk:** Medium.

### I-10 · Vendor Heat Card (Heat & Water)

1. **One-liner:** A voice-first daily heat plan for street vendors: hours to shade, nearest free water, and when their heat-insurance trigger fires.
2. **User:** A Mumbai vegetable vendor.
3. **Pain:** 89% have no free drinking water (FACT); lost hours.
4. **Workaround:** Thermocol shade (FACT).
5. **Core insight:** Parametric insurance already pays on thresholds, so vendors should see them coming.
6. **Mechanism:** Forecast, IVR call, water-point map, trigger tracker.
7. **Unique differentiator:** Built for informal workers.
8. **Why others won't copy:** High barrier.
9. **Data:** Forecast, water points (crowdsourced).
10. **AWS role:** Amazon Connect/Polly; Lambda.
11. **MVP:** IVR demo.
12. **3-min demo story:** Call, plan, trigger alert.
13. **Measurable outcome:** Hours of heat exposure.
14. **Biggest technical risk:** Connect phone numbers in India.
15. **Biggest product risk:** Reach.
16. **Competition risk:** Low.

### I-11 · Kabadi Ledger (Waste & Energy)

1. **One-liner:** A daily scrap price board plus digital receipts for waste pickers, building a verifiable record of what they divert from landfill.
2. **User:** A waste picker or kabadiwala.
3. **Pain:** Price opacity and exclusion from EPR (FACT).
4. **Workaround:** Trust the dealer.
5. **Core insight:** Receipts create bargaining power and EPR eligibility.
6. **Mechanism:** Price crowdsourcing, a receipt with photo and weight, a ledger.
7. **Unique differentiator:** Built for pickers, not households.
8. **Why others won't copy:** High (needs user knowledge).
9. **Data:** User-generated.
10. **AWS role:** Lambda; DynamoDB; Bedrock (voice entry).
11. **MVP:** A receipt flow.
12. **3-min demo story:** A picker sells 12 kg of PET and gets a receipt plus a price comparison.
13. **Measurable outcome:** ₹ earned, kg diverted.
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** Can't reach users; simulated.
16. **Competition risk:** Medium (marketplaces).

### I-12 · E-Drive: a campus e-waste drive that ends in a certificate (Waste & Energy)

1. **One-liner:** Students log old devices, the drive is scheduled with an authorised recycler, and each donor gets a recycling certificate.
2. **User:** A campus sustainability club.
3. **Pain:** E-waste in drawers; 13.97 lakh tonnes nationally (FACT).
4. **Workaround:** Kabadiwala, or the drawer.
5. **Core insight:** Batching on campus makes formal recycling viable.
6. **Mechanism:** Device logging, a batch threshold, recycler booking, certificates.
7. **Unique differentiator:** Campus batching.
8. **Why others won't copy:** Medium.
9. **Data:** User entries, recycler list.
10. **AWS role:** Lambda; DynamoDB; SES.
11. **MVP:** A drive flow.
12. **3-min demo story:** 120 devices batched and a pickup confirmed.
13. **Measurable outcome:** kg collected.
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** Recycler partnership.
16. **Competition risk:** Medium.

### I-13 · ToD Shift: run the pump at noon (Waste & Energy)

1. **One-liner:** Reads smart-meter and tariff data and schedules shiftable loads into cheap solar hours.
2. **User:** A smart-metered household.
3. **Pain:** Peak tariffs 10–20% higher (FACT).
4. **Workaround:** None.
5. **Core insight:** Solar-hour pricing aligns cost and carbon.
6. **Mechanism:** Tariff, load inventory, schedule, bill verification.
7. **Unique differentiator:** Tariff-aware.
8. **Why others won't copy:** Medium.
9. **Data:** Tariff orders, meter exports.
10. **AWS role:** Lambda; Bedrock (bill parsing); EventBridge.
11. **MVP:** One bill.
12. **3-min demo story:** Shifting the pump and washing machine saves ₹X.
13. **Measurable outcome:** ₹, kWh shifted.
14. **Biggest technical risk:** Meter data access.
15. **Biggest product risk:** Uneven rollout.
16. **Competition risk:** Low. **Candidate extension of I-01.**

### I-14 · Basement Watch (Heat & Water)

1. **One-liner:** Warns society managers to move cars before the basement floods, using a rainfall nowcast and the building's own flood history.
2. **User:** An RWA in Bengaluru or Gurugram.
3. **Pain:** Flooded basements and cars.
4. **Workaround:** WhatsApp panic.
5. **Core insight:** Each basement has its own rainfall threshold.
6. **Mechanism:** Nowcast, threshold, alert, post-event threshold update.
7. **Unique differentiator:** Per-building thresholds.
8. **Why others won't copy:** Low barrier.
9. **Data:** Rain forecast, event logs.
10. **AWS role:** Lambda; EventBridge; SNS.
11. **MVP:** One building.
12. **3-min demo story:** A storm and an alert 90 minutes ahead.
13. **Measurable outcome:** Cars moved.
14. **Biggest technical risk:** Nowcast skill.
15. **Biggest product risk:** Seasonal.
16. **Competition risk:** **High** (flood tools are crowded).

### I-15 · Cool Roof Planner (Heat & Water)

1. **One-liner:** From a photo of a tin roof, estimates indoor heat gain and recommends low-cost cool-roof fixes and the relevant state scheme.
2. **User:** A low-income household or NGO surveyor.
3. **Pain:** Tin-roof homes overheat (KNOWN).
4. **Workaround:** Fans, sacks on the roof.
5. **Core insight:** Roof material dominates indoor heat in informal housing.
6. **Mechanism:** Photo, material classification, heat estimate, fix recommendation.
7. **Unique differentiator:** Photo to retrofit.
8. **Why others won't copy:** Medium.
9. **Data:** Photos, forecasts.
10. **AWS role:** Bedrock vision; Lambda.
11. **MVP:** A survey flow.
12. **3-min demo story:** Roof photo, plan, estimated −3 °C.
13. **Measurable outcome:** Indoor °C (modelled).
14. **Biggest technical risk:** Modelling accuracy.
15. **Biggest product risk:** Can't verify outcomes.
16. **Competition risk:** Low.

### I-16 · Classroom Air Balancer (Air)

1. **One-liner:** With a ₹2,500 CO₂/PM sensor, tells the teacher exactly when to open windows: CO₂ is rising but outdoor PM is at its lowest.
2. **User:** A teacher.
3. **Pain:** Closed windows push CO₂ up; open windows let PM in.
4. **Workaround:** Guess.
5. **Core insight:** Ventilation is a trade-off with a computable optimum.
6. **Mechanism:** Sensor, outdoor feed, schedule.
7. **Unique differentiator:** Two-pollutant trade-off.
8. **Why others won't copy:** Medium.
9. **Data:** Sensor plus OpenAQ.
10. **AWS role:** IoT Core; Lambda.
11. **MVP:** One room.
12. **3-min demo story:** CO₂ curve plus window prompts.
13. **Measurable outcome:** ppm-hours.
14. **Biggest technical risk:** Hardware.
15. **Biggest product risk:** Sensor cost and availability this weekend.
16. **Competition risk:** Low.

### I-17 · Shuttle Pool (Waste & Energy)

1. **One-liner:** Pools campus trips to the station or market into EV shuttle runs, replacing private autos.
2. **User:** Students on a large campus.
3. **Pain:** Fragmented trips.
4. **Workaround:** Individual autos.
5. **Core insight:** Demand clusters by time.
6. **Mechanism:** Requests, pooling, dispatch.
7. **Unique differentiator:** Campus-specific.
8. **Why others won't copy:** Low barrier.
9. **Data:** Requests.
10. **AWS role:** Lambda; Location; AppSync.
11. **MVP:** A booking flow.
12. **3-min demo story:** Ten requests become two runs.
13. **Measurable outcome:** km avoided.
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** Needs a fleet.
16. **Competition risk:** Medium.

### I-18 · Borewell Commons (Heat & Water)

1. **One-liner:** Neighbours log borewell water depth monthly, compare it with CGWB trends, and site recharge pits where the drop is fastest.
2. **User:** A peri-urban community.
3. **Pain:** Falling water tables; 730 over-exploited units (FACT).
4. **Workaround:** Drill deeper.
5. **Core insight:** Citizen depth logs fill the CGWB gaps.
6. **Mechanism:** Logs, map, recharge recommendations.
7. **Unique differentiator:** Community data.
8. **Why others won't copy:** Medium.
9. **Data:** User logs, CGWB.
10. **AWS role:** Lambda; DynamoDB; Location.
11. **MVP:** A log flow.
12. **3-min demo story:** Depth map and pit sites.
13. **Measurable outcome:** Recharge volume (modelled).
14. **Biggest technical risk:** Data sparsity.
15. **Biggest product risk:** Slow feedback (months).
16. **Competition risk:** Medium.

### I-19 · Dumpsite Fire Watch (Air)

1. **One-liner:** Satellite thermal anomalies over legacy dumpsites trigger alerts to municipal officers before smouldering fires become Ghazipur-scale events.
2. **User:** A municipal solid-waste officer.
3. **Pain:** Landfill fires cause toxic smoke (KNOWN).
4. **Workaround:** Respond after smoke appears.
5. **Core insight:** Thermal anomalies precede visible fires.
6. **Mechanism:** FIRMS, dumpsite polygons, alerts.
7. **Unique differentiator:** Dumpsite focus.
8. **Why others won't copy:** Medium.
9. **Data:** FIRMS, dumpsite list.
10. **AWS role:** Lambda; EventBridge; SNS.
11. **MVP:** Historical replay.
12. **3-min demo story:** An anomaly over a past fire, then an alert.
13. **Measurable outcome:** Lead time.
14. **Biggest technical risk:** Resolution (375 m).
15. **Biggest product risk:** No real user this weekend.
16. **Competition risk:** Low.

### I-20 · Ward Heat Atlas (Heat & Water)

1. **One-liner:** Builds ward-level heat-vulnerability maps from land-surface temperature, census and tree data, and drafts heat action plan sections.
2. **User:** A municipal heat officer.
3. **Pain:** Heat action plans are not localised (FACT).
4. **Workaround:** Consultants.
5. **Core insight:** Localisation is data assembly.
6. **Mechanism:** Landsat LST plus census, an index, then a plan draft.
7. **Unique differentiator:** Plan-ready output.
8. **Why others won't copy:** Medium.
9. **Data:** Landsat on AWS, census.
10. **AWS role:** S3 Open Data; Lambda; Bedrock.
11. **MVP:** One city.
12. **3-min demo story:** Map and plan PDF.
13. **Measurable outcome:** None direct.
14. **Biggest technical risk:** GIS effort.
15. **Biggest product risk:** "Big problem solved vaguely".
16. **Competition risk:** Medium.

### I-21 · Mess Loop (Waste & Energy)

1. **One-liner:** Weighs plate waste per dish at the campus mess and feeds it back into the menu and portions.
2. **User:** A mess manager.
3. **Pain:** Food waste.
4. **Workaround:** None.
5. **Core insight:** Waste is dish-specific.
6. **Mechanism:** Weigh, classify, menu insight.
7. **Unique differentiator:** Per-dish.
8. **Why others won't copy:** Low barrier.
9. **Data:** Weights, photos.
10. **AWS role:** Bedrock; Lambda.
11. **MVP:** One meal.
12. **3-min demo story:** Dish X wasted 30%, so the portion is cut.
13. **Measurable outcome:** kg saved.
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** Crowded.
16. **Competition risk:** **High** (≥4 food-waste entries at First Commit).

### I-22 · Rider Shield (Air / Heat & Water)

1. **One-liner:** Heat- and AQI-aware shift windows and rest stops for delivery riders.
2. **User:** Gig riders.
3. **Pain:** Exposure.
4. **Workaround:** None.
5. **Core insight:** Platforms control timing.
6. **Mechanism:** Forecast, shift suggestions.
7. **Unique differentiator:** Rider-specific.
8. **Why others won't copy:** Medium.
9. **Data:** Forecasts.
10. **AWS role:** Lambda; SNS.
11. **MVP:** An app mock.
12. **3-min demo story:** Safer shift suggestion.
13. **Measurable outcome:** Exposure hours.
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** The decision-makers (platforms) are unreachable.
16. **Competition risk:** Medium.

### I-23 · Purifier Reality Check (Air)

1. **One-liner:** Enter room size, purifier model and windows, and it tells you the real indoor PM2.5 and the runtime you need, given today's outdoor air.
2. **User:** A Delhi household.
3. **Pain:** Under-sized or misused purifiers (INFERENCE).
4. **Workaround:** Trust the box.
5. **Core insight:** CADR, room volume and air changes are simple physics.
6. **Mechanism:** Mass-balance model, then advice.
7. **Unique differentiator:** Physics, not marketing.
8. **Why others won't copy:** Medium.
9. **Data:** Purifier specifications, OpenAQ.
10. **AWS role:** Lambda; Bedrock (spec-sheet read).
11. **MVP:** A calculator.
12. **3-min demo story:** Photo of the box, then the verdict.
13. **Measurable outcome:** µg/m³ indoors (modelled).
14. **Biggest technical risk:** Low.
15. **Biggest product risk:** Small problem; no verify without a sensor.
16. **Competition risk:** Low.
