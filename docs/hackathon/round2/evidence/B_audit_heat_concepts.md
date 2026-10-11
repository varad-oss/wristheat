# Heat & Water concept audit: CoolerCheck (A), WristHeat (B), Heat Roll-Call (C). Competition, physics and 40-hour feasibility (India, checked Fri 9 Oct 2026, ~22:00–23:30 IST)

Labels: **FACT** = sourced (link inline); **INFERENCE** = my reasoning from sourced facts or my own calculation; **HYPOTHESIS** = untested. "Prior notes" means `/home/claude/research_notes/Environmental Hacks concept reset/`. Live API calls were made in the built-in browser (Open-Meteo, GitHub API) on 9 Oct 2026 ~22:30 IST.

**Headline (INFERENCE):**
- **A. CoolerCheck:** the mechanism already exists as a consumer app: *Evaporative Cooler Forecaster* (iOS and Android, May 2025), which gives hourly/daily cooler, fan or A/C mode advice, predicted indoor temperature and humidity, pad-type settings and kWh/$ savings. Two of A's pitch claims are also physically wrong: "wastes water in humid hours" and "only adds humidity". A is buildable, but as an India localisation, not a new mechanism.
- **B. WristHeat:** the most differentiated idea in *this* competition. None of the 5 public worker-heat entries uses a body signal. But Garmin already ships an HR-based "Estimated Body Temperature" data field. ECTemp has never been validated on wrist optical HR. And feasibility hinges on whether the team's still-unknown watch broadcasts standard BLE heart rate. Noise, boAt and Fire-Boltt hold half of India's smartwatch market, and no broadcast feature was found for them.
- **C. Heat Roll-Call:** honest to demo and technically trivial on Step Functions. But it repeats the prior winner Suraksha's story (an elder, an escalation ladder, `waitForTaskToken`) and its AWS pattern. Commodity check-in-and-escalate services already exist abroad.

---

## A1. How many Indian households use evaporative coolers, and is there evidence they are run when they barely cool?

### Takeaway
Roughly 11–14% of Indian households own an air cooler, concentrated in hot-dry/composite north-central India (UP ~40% in a 2019 survey). About 8 million are sold a year. A BEE star label for coolers launched as voluntary in July 2025. I found **no quantitative study** of coolers being run in humid hours. There is only consumer-media advice ("in monsoon, switch the pump off, use fan mode, open a window") and manufacturer FAQs conceding lower efficiency in high humidity.

### Cited Findings
- FACT: NSS 2020 asked separately about ACs and coolers: **5% of households owned an AC and 14% an air cooler.** Combined AC/cooler ownership is ~30% (year unstated), up from 2% in the early 1990s. Cooler ownership is concentrated in "arid central states" — [Data For India, *Cold comforts*](https://www.dataforindia.com/cold-comforts/)
- FACT: CLASP/BEE 2024 household survey (4,321 households, 20 states, explicitly *not* nationally representative):
  - Air coolers in ~11% of households overall: 13% urban, 8% rural.
  - By climate zone: ~19% in Composite, ~13% in Hot-Dry.
  - Coolers are ~2% of surveyed household electricity use.
  - No data on hours or months of use, and nothing on humid-season behaviour.
  — [CLASP report PDF](https://www.clasp.ngo/wp-content/uploads/2026/05/Report_Residential_Energy_Consumption_Survey_India.pdf); [DTE coverage, 12 May 2026](https://www.downtoearth.org.in/amp/story/energy/cooling-appliances-now-drive-indias-household-electricity-use)
- FACT: A Prayas survey (Feb–Mar 2019, 3,000 HH) found air coolers in **40% of households in UP and 23% in Maharashtra**, and ~8 million coolers sold per year. It has no data on hours, humidity or monsoon use — [Prayas](https://energy.prayaspune.org/our-work/article-and-blog/space-conditioning-focus-on-fans-and-air-coolers-for-efficiency)
- FACT: India launched its **first star-labelling programme for evaporative coolers** (BEE):
  - Voluntary from July 2025, with a mandatory phase "by July 2026" per CLASP.
  - Scope: direct evaporative coolers up to 6,000 m³/h, tested to **IS 3315:2024**.
  - Metric: EER star bands.
  — [CLASP launch note, May 2025](https://cprc-clasp.ngo/updates/india-launches-countrys-first-star-labeling-program-evaporative-coolers); [CLASP policy record](https://cprc-clasp.ngo/policies/standards-and-labeling-evaporative-air-coolers). This supersedes the "no BEE label" claim in prior notes P-05/M-06. Whether the mandatory phase took effect in July 2026 was not verified (Gap).
- FACT (consumer media, no data): ETV Bharat (14 Jul 2026) says that in the monsoon a cooler "adds more moisture" and makes rooms "stuffy". Its workarounds are: turn the pump off and run fan mode, leave a window or door open. Experts "generally recommend" AC instead. No RH thresholds or usage statistics are given — [ETV Bharat](https://www.etvbharat.com/en/lifestyle/ac-air-cooler-choice-monsoon-india-enn26071403854)
- FACT: Symphony's FAQ concedes only that "if the humidity level is excessively high, the cooling efficiency may decrease", with no threshold (prior notes M-06) — [Symphony](https://symphonylimited.com/how-air-coolers-can-be-more-effective-than-ac-during-the-monsoon/)

### Inferences
- INFERENCE: The addressable base is large in absolute terms (11–14% of ~300 M households, i.e. roughly 30–40 M households), but it is concentrated where coolers work well (hot-dry and composite zones) in the hot-dry months.
- INFERENCE: The "people run coolers when they barely cool" premise is plausible but **unquantified**. Treat it as a HYPOTHESIS on screen, not a FACT.

### Gaps
- No Indian survey of cooler hours by month or humidity was found. NSS, CEEW IRES 2020 and India Cooling Action Plan cooler-usage tables were not retrieved.
- Whether the BEE cooler label became mandatory in July 2026 was not verified.

---

## A2. Does the physics hold? Typical ε, the live mid-October check, and what the formula actually implies

### Takeaway
The outlet formula T_out = T_db − ε(T_db − T_wb) is textbook and matches the BIS definition. Typical ε runs from ~0.55–0.70 for wood-wool (aspen or coir) pads to ~0.75–0.93 for thick rigid or honeycomb media, with BIS requiring ≥65%.

Two common pitch claims **fail on physics**:
- **Water use:** evaporation equals cooling delivered, so a cooler automatically uses *less* water in humid hours. There is no "water wasted in humid hours" story.
- **"Only adds humidity":** the process keeps the wet-bulb temperature constant, so with a ventilated room it never makes heat stress worse. It just helps very little when the depression is small.

The only genuinely useless windows in mid-October are **nights and early mornings in humid cities** (depression ~1–2 °C). By day, coolers still cut 5–11 °C of dry-bulb in every city checked.

### Cited Findings
**Formula and ε values**
- FACT: IS 3315:1994 defines cooling efficiency as how closely the leaving-air dry-bulb approaches the entering-air wet-bulb. It requires **cooling efficiency ≥65%**, tested at inlet RH 25–55%. Its Annex A example is inlet 39.8 °C DB / 25 °C WB → outlet 29 °C, i.e. (39.8−29)/(39.8−25) ≈ 73% by my arithmetic. Pads are "wood wool or any other substitute" — [IS 3315:1994 (law.resource.org)](https://law.resource.org/pub/in/bis/S08/is.3315.1994.pdf)
- FACT: EnergyPlus models a direct evaporative cooler as T_out = T_db − ε(T_db − T_wb), with ε ≈ 0.7 in its examples (prior notes M-06) — [EnergyPlus I/O reference](https://bigladdersoftware.com/epx/docs/9-6/input-output-reference/group-evaporative-coolers.html)
- FACT (US DOE/PNNL Building America): "newer evaporative coolers have thick media with efficiencies of 75% to 93%"; an **aspen-fibre cooler is about 70% effective**. Other points from the same page:
  - Evaporative cooling works best where the 1% design wet-bulb is **below 70 °F (21.1 °C)**. Up to **74 °F (23.3 °C)** it still cools with reduced performance.
  - Direct coolers "increase rather than decrease the humidity".
  - Relief openings of **2 ft² per 1,000 CFM** are required (open windows or doors).
  — [BASC/PNNL](https://basc.pnnl.gov/resource-guides/evaporative-cooling-systems)
- FACT (Indian lab test, small room, Mar–Apr, inlet 30.8–35.2 °C): cooling efficiency was **57.1% for aspen wood wool, 55.7% for coconut coir and 64.4% for the two combined**. The paper's table labels are inconsistent — [Singh & Badholiya 2024, Lingaya's J.](https://lingayasvidyapeeth.edu.in/lingayas-journal/papers/vol-18-no1/Article6.pdf)

**Live Open-Meteo check, mid-October 2026**
- FACT (live call, 9 Oct 2026 ~22:30 IST): `api.open-meteo.com/v1/forecast?...&hourly=temperature_2m,relative_humidity_2m,wet_bulb_temperature_2m,dew_point_2m&forecast_days=16&timezone=Asia/Kolkata`. All 9 cities returned 384 hourly steps with **0 null wet-bulb values**. Summary for 10–16 Oct; "dep" = wet-bulb depression T_db − T_wb:

| City (grid) | Daily Tmax 10–16 Oct | dep at Tmax | T_wb at Tmax | Hours with T ≥ 28 °C | …dep ≥ 8 °C | …dep 5–8 °C | …dep < 5 °C |
|---|---|---|---|---|---|---|---|
| Jaipur (26.89, 75.83) | 32.6–34.8 (27.1 on 16th) | 11.1–13.5 | 20.4–21.5 | 77 | 73 | 4 | 0 |
| Ahmedabad (23.02, 72.60) | 35.7–38.1 | 12.9–15.7 | 20.7–23.5 | 137 | 114 | 23 | 0 |
| Nagpur (21.12, 79.12) | 33.0–35.9 | 10.7–15.5 | 20.4–22.3 | 102 | 81 | 21 | 0 |
| Hyderabad (17.40, 78.46) | 32.5–34.5 | 11.3–14.0 | 20.5–21.2 | 94 | 88 | 6 | 0 |
| Delhi (28.58, 77.19) | 26.5–33.5 | 3.7–10.5 | 22.8–23.4 | 70 | 34 | 35 | 1 |
| Lucknow (26.82, 80.93) | 29.0–31.3 | 5.1–7.7 | 23.6–24.0 | 53 | 0 | 42 | 11 |
| Kolkata (22.60, 88.32) | 28.9–34.0 | 3.6–9.3 | 24.1–25.3 | 72 | 8 | 30 | 34 |
| Chennai (13.11, 80.25) | 31.9–33.7 | 6.2–8.9 | 24.8–26.2 | 143 | 9 | 48 | 86 |
| Mumbai (19.09, 72.85) | 36.4–37.8 (dry spell) | 12.9–15.3 | 22.4–23.5 | 141 | 60 | 79 | 2 |

- INFERENCE (my computation from the same live data, Sat 10 Oct, ε = 0.7). Outlet RH comes from the psychrometer equation; HI is the NWS Rothfusz heat index; "WBGT-in" is the indoor proxy 0.7·T_wb + 0.3·T_a:

| City, hour | T / RH / T_wb | Cooler outlet T / RH | HI outdoor → outlet | WBGT-in outdoor → outlet |
|---|---|---|---|---|
| Ahmedabad 15:00 | 35.6 / 30% / 22.4 | 26.4 / 71% | 35.6 → 26.9 | 26.4 → 23.6 |
| Nagpur 15:00 | 35.6 / 22% / 20.3 | 24.9 / 66% | 34.0 → 25.2 | 24.9 → 21.7 |
| Jaipur 15:00 | 33.8 / 30% / 21.3 | 25.1 / 72% | 33.0 → 25.5 | 25.0 → 22.4 |
| Chennai 15:00 | 31.8 / 56% / 25.0 | 27.0 / 85% | 35.5 → 30.3 | 27.0 → 25.6 |
| Kolkata 15:00 | 30.9 / 55% / 24.0 | 26.1 / 84% | 33.5 → 26.9 | 26.1 → 24.6 |
| Chennai 06:00 | 26.9 / 88% / 25.3 | 25.8 / 96% | 30.5 → 26.9 | 25.8 → 25.4 |
| Lucknow 06:00 | 22.0 / 93% / 21.1 | 21.4 / 98% | 22.7 → 22.1 | 21.4 → 21.2 |
| Delhi 06:00 | 22.2 / 92% / 21.1 | 21.4 / 97% | 22.9 → 22.2 | 21.4 → 21.2 |

**Water and dengue**
- INFERENCE (psychrometrics): direct evaporative cooling is adiabatic, so it keeps T_wb constant.
  - Water evaporated ≈ ρ·Q·c_p·ΔT / h_fg. For an actual airflow of 2,000 m³/h at ε = 0.7, that gives roughly **8.8 L/h at Ahmedabad 15:00**, ~4.5 L/h at Chennai or Kolkata 15:00, and **~0.6–1.1 L/h at Lucknow or Chennai 06:00**.
  - Litres per unit of cooling are essentially constant (~1 L per 0.68 kWh of sensible cooling). So switching off in humid hours saves little water, because little was being evaporated.
  - In prior notes, P-05's demo line "Pump off… save 18 L today" in Kolkata is therefore misleading. A full Kolkata day of cooler use evaporates on the order of 30 L, but that water buys ~4–5 °C of daytime cooling. It is a trade, not waste.
- FACT (dengue angle, timely in October): an NCDC note says conventional desert coolers are "potential breeding grounds" for *Aedes aegypti*. It cites a Delhi study in which coolers were **>50% of dengue vector breeding places**, and says "weekly larviciding or cleaning is required", which is often not done — [NCDC note](https://ncdc.mohfw.gov.in/wp-content/uploads/2024/04/File616.pdf).
- FACT: a Kolkata 2003–06 survey found air coolers held ~18% of immature *Aedes*, and coolers were dry (no immatures) only in Dec–Feb — [SE Asian J Trop Med Public Health 2007](https://www.tm.mahidol.ac.th/seameo/2007_38_3/06-3931.pdf).

### Inferences
- INFERENCE: The core formula **holds**. Which advice it produces depends heavily on the comfort metric:
  - Under heat index, the cooler wins in every daytime hour checked, even in Chennai and Kolkata (−5 to −7 °C HI).
  - Under an indoor WBGT proxy, the gain is only 1.4–3.2 °C even in dry cities. That is because WBGT is 70% wet-bulb, which evaporative cooling cannot change.
  - The team must choose and disclose the metric; judges with physics backgrounds will ask.
- INFERENCE: "When to use only a fan" has a clean, defensible rule: depression < ~3 °C (ΔT < ~2 °C at ε 0.7). In mid-October that is almost entirely **night and early-morning hours in humid or post-monsoon cities** (Lucknow, Delhi, Kolkata, Chennai at 06:00 show 0.9–1.6 °C depressions). For north and central India's daytime it is rarely binding until coolers are no longer needed.
- INFERENCE: The strongest honest October angles are:
  1. Overnight "pump off, fan only" in humid places: saves pump energy, avoids damp.
  2. "Season over: drain and dry the tank" before dengue persists, triggered when the forecast shows the cooler won't be needed for N days.
  3. Tank-refill litres planning in dry cities (an Ahmedabad or Nagpur cooler at ~2,000 m³/h may evaporate ~60–90 L over a 10-hour day).

  All are modelled, not verified.
- INFERENCE: Mumbai shows an unusual dry spell (Tmax 37–38 °C at RH 24–26%), so "coastal = useless" is not reliable. The forecast-driven approach is what catches this.

### Gaps
- No measured ε for Indian honeycomb (cellulose) pads was retrieved. The 0.75–0.93 range is US thick media (PNNL).
- No Indian field data on room-level performance (recirculation, ventilation) was found.
- Actual vs rated airflow of desert coolers (needed for litres) was not found. Rated air delivery is measured with a dry pad (IS 3315 cl. 9.2.3), so real flow is lower.

---

## A3. Do existing apps, smart coolers or calculators already advise on wet-bulb or humidity?

### Takeaway
**Yes, the core mechanism exists.**
- *Evaporative Cooler Forecaster* (Tenth Light Digital / John Pierce; iOS and Android; released May 2025, updated Jun 2026, 1K+ Android downloads) forecasts hourly and daily when to use Cooling, Fan or A/C mode. It also shows predicted indoor temperature and humidity, lets the user set pad type and humidity tolerance, and estimates kWh/$ saved vs A/C.
- *WetBulbCast* (iOS) forecasts 10-day hourly wet-bulb explicitly for swamp-cooler decisions.

Indian brands offer only reactive room-sensor "auto/humidity" modes or a generic embedded wet-bulb calculator. None found does forecast-driven mode advice, litres accounting or dengue-drain prompts.

### Cited Findings
- FACT: **Evaporative Cooler Forecaster** (iOS):
  - Dashboard of the indoor temperature and humidity the cooler would produce now.
  - "Forecast for hours and days ahead" indicating when to use Cooling mode, when Fan mode helps, and when to switch to A/C.
  - $ and kWh savings vs A/C, plus annual reports.
  - Settings for comfort zone, humidity tolerance and energy rates.
  - **Pad type setting (Aspen, DuraCool mesh, Honeycomb, CellDek)**.
  - Released 22 May 2025; <1,000 downloads; 5.0 from 2 ratings.
  — [mwm.ai listing of App Store data](https://mwm.ai/ja/apps/evaporative-cooler-forecaster/6745530908)
- FACT: The Android version (Tenth Light Digital) has the same feature set, 1K+ downloads, was last updated 25 Jun 2026, and carries ads and in-app purchases. India availability is not explicit — [Google Play](https://play.google.com/store/apps/details?id=com.tenthlight.evaporative_cooler&hl=en_IN)
- FACT: **WetBulbCast** (Rob Boer, free iOS/watchOS) calls wet-bulb "the single most important number for swamp cooler effectiveness". It shows 10-day hourly wet-bulb from Apple WeatherKit, but no outlet temperature or water use — [App Store](https://apps.apple.com/app/id6761316594)
- FACT: **Symphony** (India's largest cooler brand) has a "Wet Bulb Calculator" page. It frames wet-bulb as something to check "before venturing outdoors" and embeds a generic **Omni Calculator wet-bulb widget** (iframe `omnicalculator.com/embed/all/wet-bulb`). There is no cooler-performance logic (observed in browser 9 Oct 2026) — [Symphony wet-bulb calculator](https://symphonylimited.com/wet-bulb-calculator/)
- FACT: Symphony lists "Humidity Control" and an auto mode that adjusts fan speed "based on room temperature and humidity levels", plus IoT app control. It describes no pump-off or fan-only mode triggered by humidity or wet-bulb — [Symphony smart features 2025](https://symphonylimited.com/smart-features-in-modern-air-coolers-what-consumers-expect-in-2025/)
- FACT: **Bajaj COOL.iNXT** (IoT cooler) has a room temperature/humidity sensor. Its "Auto Mode" sets fan speed and cooling from room readings, and it has a low-water indicator and app remote control. No outdoor weather data — [Bajaj COOL.iNXT](https://cool.inxt.bajajelectricals.com/)
- FACT: **Crompton Optimus 65 IoT** has "humidity control" (mechanism unexplained), an app with scheduling and timers, but no weather or wet-bulb advice — [Crompton blog](https://www.crompton.co.in/blogs/air-coolers-guide/optimus-65-iot-your-smart-air-cooler-this-summer)
- FACT: The Studio Matrx (India) evaporative cooler calculator takes manual T/RH, assumes ~85% effectiveness, and has no forecast, hourly plan or water figures (prior notes P-05) — [Studio Matrx](https://www.studiomatrx.org/utilities/evaporative-cooler-calculator)

### Inferences
- INFERENCE: Ruthless novelty verdict: A's core mechanism (forecast wet-bulb → hourly cooler/fan/AC mode, predicted indoor conditions, pad-type ε, energy savings) **already exists as a shipped app**. It is obscure, US-oriented and has <1–2K downloads, so most judges won't know it. But a judge who searches "evaporative cooler forecast app" will find it.
- INFERENCE: What is genuinely new for India would be:
  - desert-cooler ε defaults from IS 3315 and Indian pad tests;
  - Hindi or regional language;
  - a physically correct litres ledger;
  - the dengue "drain the tank" season-end prompt;
  - learning ε from user input.

  These are incremental. None is a new mechanism.

### Gaps
- Whether *Evaporative Cooler Forecaster* is available on the Indian Play Store or App Store was not confirmed.
- The Symphony, Bajaj and Crompton apps were not installed or inspected beyond marketing pages.

---

## A4. Can verification or ε-learning work without hardware?

### Takeaway
Not credibly. Phone ambient temperature and humidity sensors are rare and self-heated, and browsers expose no ambient-temperature API. "Was it comfortable?" taps cannot identify ε. ε-learning needs a thermometer reading of outlet air. That is allowed only if the team already owns one, and fever thermometers usually can't read room-temperature air.

### Cited Findings
- FACT: Phone humidity sensors are "the rarest sensor" in the phyphox device database. Galaxy S4-era devices had a Sensirion SHTC1, and internal readings are affected by phone heat (one user saw +1–2 °C). Forum members suggest an external Bluetooth sensor instead — [phyphox forum](https://phyphox.org/forums/showthread.php?tid=963)
- FACT (prior notes §5): Web apps can use Geolocation and DeviceMotion. Web Bluetooth is Chromium-only. Nothing in that catalogue offers ambient temperature — [data_access.md §5, MDN BCD](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)

### Inferences
- INFERENCE: With ε as the only unknown, a single reading of outlet-air temperature plus the concurrent forecast T_db and T_wb identifies ε directly. That requires a thermometer the household owns; buying one is disallowed.
- INFERENCE: Comfort taps confound ε with airflow, room size, occupancy and personal preference, so "learns each cooler's ε" from feel is not supportable. Default ε by pad type (wood wool ~0.6–0.7, honeycomb ~0.8) is the honest approach.
- INFERENCE: A defensible verification for the demo is **hindcast verification**: rerun yesterday's plan on observed weather from the Open-Meteo archive and show forecast vs observed depression. This verifies the forecast, not the room.

### Gaps
- I did not check whether any common Indian-owned device (AC remote displays, wall clocks with thermometers) reports room temperature reliably.

---

## B1. ECTemp: exact parameters, validation (including wrist/optical HR), open-source implementations, licensing

### Takeaway
ECTemp is a scalar extended Kalman filter on **minute-averaged HR**. Its published parameters are:
- a = 1 and γ² = 0.000484 (γ = 0.022);
- HR = −4.5714·CT² + 384.4286·CT − 7887.1;
- σ² = 356.5654 (σ ≈ 18.88);
- CT₀ = 37.1 °C, v₀ = 0.

Lab validation on chest-strap or ECG HR is good: bias ≈ 0 and limits of agreement ±0.45–0.63 °C. Field results are wider (LoA up to ±1.2 °C). Accuracy is poor at the dangerous end: sensitivity < 50% for core temperature above 39 °C in elite athletes. **No validation with consumer wrist optical HR was found.**

The method is **US-Army patented** (US10702165B2, active, expiry est. 2033). USARIEM requires a licence for commercial use. The only GitHub code found is a 2025 Oxford multi-model variant that fits its own parameters.

### Cited Findings
**Algorithm and parameters**
- FACT: USARIEM's page describes the algorithm:
  - Inputs are a starting core temperature and per-minute HR.
  - It is a Kalman filter that treats HR as a noisy observation of core temperature.
  - Reported accuracy: bias −0.03 °C, SD 0.32, LoA ±0.63 °C, RMSE 0.30 °C.
  - It cites Buller et al. 2013, *Physiol Meas* 34:781–798.
  - It provides an in-page JavaScript estimator "for demonstration purposes only".
  - "Functions for academic or personal use, and licensing for commercial use" are obtained by contacting USARIEM.

  — [USARIEM CBT algorithm](https://usariem.health.mil/index.cfm/research/products/cbt_algorithm). The page returned "Request Rejected" in the built-in browser, so the JS source could not be inspected.
- FACT (patent and USARIEM tech report agree):
  - Measurement model HR = −4.5714·CT² + 384.4286·CT − 7887.1.
  - Linearised slope c = −9.1428·CT + 384.4286.
  - Process variance increment **0.000484** (= 0.022²).
  - Gain K = v·c / (v·c² + **356.5654**); σ² ≈ 18.88².
  - The Looney 2017 report initialised v₀ = 0 with CT₀ = the first observed CT.

  — [US10702165B2 (Google Patents)](https://patents.google.com/patent/US10702165): b0 −7887.1, b1 384.4286, b2 −4.5714, σ = 18.88; [Looney et al. 2017, USARIEM T17-08 (DTIC)](https://apps.dtic.mil/sti/pdfs/AD1031877.pdf)
- FACT: Patent US10702165B2: assignee US Department of the Army, inventor Mark J. Buller, priority 2012-12-20, granted 2020-07-07, status "Active", anticipated expiration **2033-12-16** (Google's estimate) — [Google Patents](https://patents.google.com/patent/US10702165)
- FACT: An updated ECTemp uses a sigmoid HR–CT relation (Looney 2018; Buller 2020). de Korte 2022 used CT₀ 37.0 °C and v₀ 0.02 on minute-averaged HR — [de Korte et al. 2022](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.882254/full)

**Validation**
- FACT (Buller presentation): 9 studies, 87 subjects, >50,000 points, bias −0.03 °C, 95% within ±0.63 °C, "on par" with rectal/oesophageal probe agreement.
  - CBRNE units: bias 0.02, LoA ±0.48.
  - MIT Lincoln Lab independent check, 30 Marines in Okinawa: bias 0.01, **LoA ±1.20**.
  - PSI = 5·(CT−CT₀)/(39.5−CT₀) + 5·(HR−HR₀)/(180−HR₀). Bands: <5 low, 5–6 moderate, 7–8 high, 9–10 very high.
  - Validation populations were primarily military.

  — [Buller, "RT PSI Assessment" (NRT)](https://nrt.org/sites/58/files/RT%20PSI%20Assessment%20-%20M.%20Buller.pdf)
- FACT: NCAA football, Zephyr BioHarness 3 chest-strap ECG with embedded ECT, 1-min updates:
  - bias −0.19 °F, LoA −1.80 to +1.42 °F, CCC 0.643, 78% within ±1 °F;
  - for lean players (≤6% body fat), CCC 0.515 and 62% within ±1 °F.
  - Consumer wearables were not discussed.

  — [Hagen et al. 2020 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7739355/)
- FACT: 101 Dutch elite athletes, Polar V800 chest strap, cycling at ~31.6 °C and 74% RH:
  - bias 0.15 °C, LoA ±0.45 °C (the paper reports SD inconsistently), RMSE 0.35 °C, r 0.86;
  - at peak core temperature, LoA ±0.92 °C;
  - **sensitivity <50% for thresholds >39.0 °C**, mainly from false negatives;
  - the authors say the algorithm "should not solely be used to identify athletes at risk".

  — [de Korte et al. 2022](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.882254/full)
- FACT: Washington farmworkers (35 in 2015; 75 in a 2019 intervention): bias −0.14 °C, LoA ±0.76 °C with a 37.1 °C baseline. The HR device is not stated in the abstract — [Egbert 2021, UW thesis](https://digital.lib.washington.edu/researchworks/items/34213275-4ed3-4f8b-88fc-72d675246a4d/full)
- FACT: At rest (circadian), using Equivital EQ-02 HR: MESOR bias −0.24 °C and r 0.68 overall — [Looney et al. 2017](https://apps.dtic.mil/sti/pdfs/AD1031877.pdf)
- FACT: Laxminarayan et al. 2018 (J Appl Physiol), "Individualized estimation of human core body temperature using noninvasive measurements", exists. I did not read its content — [PMC6032092](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6032092/)
- FACT (wrist optical HR in general): across consumer and research wearables, absolute HR error during activity was **on average 30% higher than at rest**. Devices differed in how they tracked changes in activity; skin tone had no significant effect — [Bent et al. 2020, npj Digit Med (DOAJ abstract)](https://doaj.org/article/80ba2cc27bce46bf8b4662d44edc2cff)

**Implementations (GitHub search via API, 9 Oct 2026)**
- FACT: The query "core body temperature heart rate" returned 9 repos. Relevant ones:
  - `Oxford-NIL/PSSK-TCBK`: code for "Core Body Temperature Estimation from Heart Rate via Multi-Model Kalman Filtering and Variance-Based Fusion", Python, Jul 2025, no licence. It fits its own a, γ, b0–b2, σ per activity state and does **not** hard-code Buller's values.
  - `swiftraccoon/CoreVitals`: logs Polar H10 + greenTEG CORE, MIT licence, so it depends on a purchased CORE sensor.
  - No PyPI or GitHub "ECTemp" package was found.

  — [GitHub API search](https://api.github.com/search/repositories?q=core+body+temperature+heart+rate); [PSSK.py](https://raw.githubusercontent.com/Oxford-NIL/PSSK-TCBK/main/PSSK.py)

### Inferences
- INFERENCE (my simulation of the published filter, CT₀ 37.1, 10 min at 80 bpm then the stated load):

  | Scenario | Peak estimated CT | Crossings |
  |---|---|---|
  | 60-min commute walk at 105 bpm | 37.6 °C | none |
  | 30-min run at 150 bpm, then 20 min at 100 bpm | 38.2 °C | crosses 38.0 °C at minute 33 |
  | 45 min hard at 165 bpm | 38.8 °C | 38.0 °C at minute 28; 38.5 °C at minute 42 |

  Implications:
  - A demo needs **sustained vigorous exercise**.
  - A commute will barely move the estimate.
  - The estimate is a deterministic, smoothed transform of the HR history: environment enters only through heat-induced HR drift.
- INFERENCE: The parameters are fully specified in public documents. The team can implement ECTemp in ~30 lines and cross-check against the USARIEM web estimator, if it loads from India. Licensing is a commercial issue, not a hackathon blocker, but the video should credit USARIEM and the patent.

### Gaps
- The Buller 2013 paper text and the "Seng 2016" validation were not retrieved. I found no study validating ECTemp on wrist PPG from Garmin, Apple, Samsung, Amazfit or Noise.
- The USARIEM JS estimator could not be loaded in the browser ("Request Rejected").

---

## B2. Can a Chrome web page read heart rate from the team's watch (Web Bluetooth), and what are the export fallbacks?

### Takeaway
Web Bluetooth can read the standard Heart Rate Service on Chrome for Android, Windows, macOS and ChromeOS, but not on iOS. Watches that broadcast standard BLE HR:
- many Garmin models (Virtual Run / Broadcast HR);
- all COROS (one connection, phone unpaired);
- Polar Ignite 2/3 and Unite ("HR sensor mode");
- Amazfit on Zepp OS 3+ (Balance, Active, GTR/GTS 4, T-Rex 3, Bip 6…);
- some Huawei watches and bands ("HR Data Broadcasts");
- probably Xiaomi Band 10 via "Share HR" (Pulsoid does not say so explicitly); Bands 7–9 need a paid relay app.

The **Galaxy Watch does not broadcast natively**. The **Apple Watch** needs the HeartCast app, which uses the iPhone as the BLE peripheral. For **Noise, boAt and Fire-Boltt** (50% of Indian smartwatch shipments) I found no broadcast feature. File exports (Samsung Health CSV, Health Connect ZIP, Apple export) are fallbacks, with unverified HR density.

### Cited Findings
- FACT: Web Bluetooth is "available in ChromeOS, Chrome for Android 6.0, Mac (Chrome 56) and Windows 10 (Chrome 70)". Linux needs a flag. It requires HTTPS and a user gesture, and the documentation's own examples use `heart_rate` / `heart_rate_measurement` — [Chrome for Developers](https://developer.chrome.com/docs/capabilities/bluetooth). MDN BCD: Safari, iOS and Firefox are unsupported (prior notes §5) — [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)

**Watches by brand**
- FACT, Garmin: Bluetooth broadcast via "Virtual Run" (or Broadcast HR) on FR245/945 and Fenix 6, with more models per comments. Apple, Fitbit, Suunto and Samsung were "not broadcasting" (as of 2020). The BLE pairing window times out after ~30–40 min unless an activity is started — [DC Rainmaker 2020](https://dcrainmaker.com/2020/04/garmin-wearable-broadcasting.html)
- FACT, Pulsoid compatibility page:
  - Native BLE: Garmin FR245/945/255/55/745, Fenix 6 Pro and 7. Garmin ANT+ broadcasting "won't work".
  - Xiaomi Mi Band 7–9 need the paid Notify app; Mi Band 10 via "Share HR".
  - Apple Watch and Wear OS only via Pulsoid's own watch apps (internet relay), with low-accuracy warnings for many Wear OS watches.
  - Huawei Band 8–11 and Watch Fit 3 are listed.

  — [Pulsoid monitors](https://www.blog.pulsoid.net/monitors)
- FACT, Amazfit: "Heart Rate Push" uses the **standard BLE Heart Rate Profile** on Zepp OS ≥3.0 (Balance, Balance 2, Active, Active 2, GTR 4, GTS 4, T-Rex Ultra, T-Rex 3, Bip 6). Some models broadcast only during a workout. HypeRate links a web-Bluetooth receiver tool — [HypeRate blog](https://blog.hyperate.io/post/amazfit-heart-rate-push-live-bluetooth-heart-rate-streaming-with-zepp-os-hyperate-compatible/)
- FACT, Huawei: Settings → "HR Data Broadcasts" lets "third-party devices and apps" connect. Single-connection devices disconnect from Huawei Health during the broadcast. Watch 5 and Ultimate 2 support it only in Battery saver mode — [Huawei support](https://consumer.huawei.com/ca/support/content/en-us15827504/)
- FACT, Polar: "HR sensor mode" shares HR over Bluetooth on **Ignite 2, Unite, Ignite 3** — [Polar support](https://support.polar.com/en/troubleshooting-ignite-2-hr-sensor-mode)
- FACT, COROS: Broadcast HR over ANT+ or Bluetooth from the Toolbox. For Bluetooth the watch must first be disconnected from the phone, and "only ONE Bluetooth connection can be allowed" — [COROS support](https://support.coros.com/hc/en-us/articles/360040256991-Broadcast-heart-rate)
- FACT, Samsung: a community feature request (topic created 29 Jul 2025) asks for BLE HR broadcasting on Galaxy Watch, implying none exists. No Samsung staff reply — [Samsung Community](https://us.community.samsung.com/t5/Galaxy-Watch/Feature-Request-Heart-Rate-Broadcasting-via-BLE-for-Galaxy-Watch/td-p/3314341)
- FACT, Apple: **HeartCast** (free) sends Apple Watch HR to BLE fitness apps and equipment (Zwift, Peloton…). The iPhone appears to handle the Bluetooth link — [App Store](https://apps.apple.com/app/id1499771124)
- FACT, India market: in 2025 smartwatch shipments fell 17.6% and ASP was US$26.5. Shares: **Noise 26.6%, boAt 14.1%, Fire-Boltt 9.7%**. "Advanced smartwatches" were 3.2% of smartwatches — [FoneArena summarising IDC](https://www.fonearena.com/blog/476987/indian-wearable-shipments-2025.html)

**Export fallbacks**
- FACT, Apple Watch: background HR "as often as every five seconds" on Series 12 / Ultra 4. Workout sampling interval is not stated — [Apple support](https://support.apple.com/en-AU/120277)
- FACT (secondary source): Samsung Health "Download personal data" gives a ZIP of CSV or JSON with `com.samsung.health.heart_rate` (timestamp + bpm). The sampling interval is not stated, and the delivery method is described as an emailed link — [TakeoutDay guide](https://takeoutday.org/guides/how-to-export-samsung-health-data). Reliability is moderate; this is an aggregator.
- FACT: Health Connect can export a "Health Connect.zip" to cloud storage on Android 14+, daily, weekly or monthly. Contents and format are not documented on the page — [Google Android help](https://support.google.com/android/answer/15323271?hl=EN-GB)
- FACT (prior notes §5): Fitbit Web API turns off 30 Oct 2026; Garmin's API is business-only; Strava API terms ban AI use.

### Inferences
- INFERENCE: **Decision gate for tonight:** the team should check its watch's settings for "Broadcast HR / HR sensor mode / Heart Rate Push / HR Data Broadcasts" and test with Chrome on Android (any Web Bluetooth HR demo, e.g. HypeRate's tool or a 20-line page).
  - If the watch is a Noise, boAt, Fire-Boltt or Galaxy Watch, the live path is HYPOTHESIS-to-UNSUPPORTED. They would need an export file, which forfeits the "live" moment.
  - If it is an Apple Watch, HeartCast plus Chrome on a laptop reading the iPhone peripheral is PLAUSIBLE-UNTESTED.
- INFERENCE: The "smartwatch you already own" premise conflicts with the Indian market: about half of watches sold are brands with no documented HR broadcast or export. The realistic target user is a Garmin, Amazfit, Huawei, Polar or COROS owner (athletes, enthusiasts), not a delivery rider with a ₹1,500 watch.

### Gaps
- Noise, boAt, Fire-Boltt, Honor, OnePlus, realme: no documentation found either way on BLE HR broadcast or raw HR export (searched; nothing relevant).
- HR sampling density in Samsung, Health Connect and Apple exports during workouts was not verified.
- Garmin Connect "Export Original" FIT was not re-verified this session.

---

## B3. Who already does HR-based (or sensor-based) core temperature or heat strain?

### Takeaway
Garmin already shipped the core mechanism to consumers in 2021 (a GarminLabs "Estimated Body Temperature" Connect IQ field from HR). Industrial wearables (Kenzen, SlateSafety; Equivital and Zephyr implementing ECTemp) and the CORE heat-flux sensor cover the professional market. Mainstream watches show only sleep skin-temperature deviations (Apple) or retrospective heat-acclimation scores (Garmin). Within this hackathon, none of the five public worker-heat projects uses any body signal.

### Cited Findings
- FACT: **GarminLabs "Estimated Body Temperature"** Connect IQ data field estimates core body temperature during exercise from heart rate and graphs it in Garmin Connect. It is described as "only an estimate", not for fever, "not medical devices" (Garmin Italy blog, 24 Mar 2021). The algorithm is not named — [Garmin IT blog](https://www.garmin.com/it-IT/blog/running/lapp-connect-iq-stima-temperatura-corporea/)
- FACT: Zephyr BioHarness 3 has embedded ECT (Hagen 2020, above). Equivital EQ-02 HR was used for ECTemp analyses (Looney 2017, above).
- FACT: SlateSafety (upper-arm band) estimates core temperature. Against an ingestible pill (20 nurses doing CPR, 71–85 °F): bias ≈ +0.03–0.04 °C, LoA ≈ ±0.6 °C, RMSE 0.27 °C, updates every 15 s. The study was funded by SlateSafety's equipment supply — [Callihan et al. 2023 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9865127/)
- FACT: A peer-reviewed paper titled "Accuracy of Algorithm to Non-Invasively Predict Core Body Temperature Using the Kenzen Wearable Device" exists (content not retrieved, blocked by a captcha) — [PMC8701050](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8701050/)
- FACT: The CORE body-temperature sensor integrates with Garmin Connect IQ (search result; purchased hardware) — [corebodytemp.com](https://corebodytemp.com/blogs/connectivity/garmin-connectiq)
- FACT: Garmin heat acclimation:
  - a 0–100% retrospective score from GPS activities when outdoor temperature (phone weather) exceeds 22 °C;
  - needs ≥4 training days;
  - no real-time core temperature or heat-strain warning is described;
  - supported on FR745/945/955, Fenix 6/7, Epix 2, Instinct 2 and others.

  — [Gadgets & Wearables 2022](https://gadgetsandwearables.com/2022/08/28/garmin-heat-altitude-performance-acclimation/)
- FACT: Apple Watch wrist temperature is sampled **only during sleep** (every 5 s) and shown as nightly deviation from baseline. It "cannot provide wrist temperature measurements on demand", is "not a thermometer" and is not a medical device — [Apple support](https://support.apple.com/en-gb/102674)
- FACT: None of Chhaon, ShiftShield, ₹800, HeatShift or Heat-safe shift planner uses smartwatch HR or core-temperature estimation (READMEs read 9 Oct 2026; see Q-Overlap below).

### Inferences
- INFERENCE: Novelty is high *within this competition* and moderate *globally*. "HR → estimated core temperature on a consumer watch" exists (GarminLabs). What B could add:
  - running it for non-Garmin watches in a browser;
  - fusing it with forecast WBGT (environment plus body);
  - Indian-language rest and hydration advice.

  That is a re-presentation plus fusion, not a new algorithm.
- INFERENCE: The WBGT half of B is exactly what Chhaon and ShiftShield already do (Liljegren on Open-Meteo). B's distinct value is the body signal.

### Gaps
- Whether the GarminLabs field is still in the Connect IQ store in 2026, and what algorithm it uses, was not verified.
- No consumer app found estimating core temperature from Samsung or Apple HR (searched; nothing found, but app stores were not searched exhaustively).

---

## B4. Regulatory risk in India, and is it demonstrable in October?

### Takeaway
CDSCO's final Medical Device Software guidance (reported 30 Jul 2026) brings "any software intended for a medical purpose" under the MDR 2017 A–D classes and excludes "general wellness apps". A tool that claims to estimate core temperature to *prevent heat illness* sits near the line. Frame it as an exertion/heat-strain *indicator*, not a measurement or diagnosis.

October is demonstrable: exercise-driven HR rise is the same physiology, and afternoon highs of 33–38 °C persist in Ahmedabad, Nagpur, Hyderabad and Mumbai this week. There is no ground-truth core thermometer, though, so the estimate itself cannot be verified on camera.

### Cited Findings
- FACT: CDSCO has finalised guidance on medical device software:
  - Scope covers SaMD, SiMD, AI-enabled software and some mobile apps.
  - It **excludes "general wellness apps"**, without defining wellness.
  - Standalone software is classified by target condition and the significance of its information.
  - Emergo's article is dated 30 Jul 2026; the effective date is not stated.

  — [Emergo by UL](https://www.emergobyul.com/news/india-cdsco-finalizes-guidance-medical-device-software)
- FACT: Garmin's own framing: "only an estimate", not for fever, "not medical devices… should not be used to diagnose, treat, cure, or prevent any disease" — [Garmin IT blog](https://www.garmin.com/it-IT/blog/running/lapp-connect-iq-stima-temperatura-corporea/)
- FACT: de Korte 2022 recommends the algorithm for heat-acclimation monitoring (target 37.75–38.75 °C), not as the sole tool to flag at-risk athletes — [de Korte 2022](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.882254/full)
- FACT: The live forecast for 10–16 Oct gives afternoon Tmax of 35.7–38.1 °C in Ahmedabad, 33.0–35.9 °C in Nagpur, 32.5–34.5 °C in Hyderabad and 36.4–37.8 °C in Mumbai (A2 table, live Open-Meteo call).

### Inferences
- INFERENCE: Safe framing:
  - Use "heat-strain index (estimated, research algorithm)".
  - Show bands, not a °C number, or show the °C number with ±0.6 °C (lab) / ±1.2 °C (field) error bars.
  - Never claim to detect heat stroke. Defer to IMD/NDMA advisories and "stop and seek help" symptom rules.
  - Credit USARIEM and the patent, and say "non-commercial prototype".
- INFERENCE: The demo can show a real teammate on a real 30–45 min hard run or cycle, with live HR → ECTemp → PSI and WBGT overlay. It cannot show that the number is *right*. Oral or ear thermometers are not valid core references during exercise (HYPOTHESIS; not researched).

### Gaps
- The CDSCO guidance text and its wellness definition were not read directly (secondary source only).
- No Indian occupational heat-strain standard for HR/PSI thresholds was researched.

---

## C1. Existing community heat check-in programmes, and evidence that check-ins reduce harm

### Takeaway
The check-in and escalation pattern is well established abroad:
- France's *fichier canicule*: registry, daily calls, police visit if no answer.
- Philadelphia's "buddy system" inside its heat warning system.
- NYC's *Be a Buddy*.
- Australian Red Cross *TeleRedi*: heatwave welfare calls with "escalation procedures".
- US police telephone-reassurance programmes and the Snug app: miss a check-in → emergency contacts → wellness check.

India has no such programme in sources found; HAPs are criticised for lacking elderly outreach. Evidence of benefit is indirect: social contact is protective in case-control studies (OR 0.40), and system-level evaluations (Philadelphia, Ahmedabad) cannot isolate the check-in component.

### Cited Findings
- FACT: Lyon's *fichier canicule*: CCAS phones registered vulnerable people daily during orange alerts and asks police to visit if there is no answer (prior notes C-05) — [Ville de Lyon](https://www.lyon.fr/demarche/personnes-agees/inscription-sur-le-fichier-canicule)
- FACT: Philadelphia's Hot Weather-Health Watch/Warning System:
  - Media urge "buddies" (friends, relatives, neighbours) to visit elderly people daily.
  - It also runs a Heatline, nursing-home contacts, utility shut-off moratoria and extended senior-centre hours.
  - Estimated **~117 lives saved 1995–98** (2.6 per warning day) for ~$210k cost.
  - Caveats: the no-displacement assumption inflates the estimate; R² 0.04; the package is evaluated as a whole.

  — [Ebi, Teisberg et al. (BAMS; U. Delaware page)](https://www1.udel.edu/SynClim/Teisberg_BAMS.htm)
- FACT: NYC *Be a Buddy*:
  - Run by NYC DOHMH with community organisations in Brownsville, East Harlem and Hunts Point.
  - Volunteers build relationships with vulnerable older "buddies" and check on them in emergencies; phone, text and virtual since COVID.
  - Serves >1,000 people; no formal evaluation on the page.

  — [Fund for Public Health NYC](https://fphnyc.org/blog/social-cohesion/)
- FACT: Australian Red Cross **TeleRedi** (WA expansion, 20 Jan 2026): free wellbeing calls during heatwaves to older or isolated people. If there is no answer or the person seems unwell, volunteers "activate escalation procedures" — [Red Cross media release](https://www.redcross.org.au/media/releases/2026/teleredi-wa/)
- FACT: Commodity daily check-in services already implement the escalation ladder:
  - **Snug**: free app; a missed check-in within 10 min notifies emergency contacts with last location. A $20/month plan calls the user, then can request an in-person wellness check.
  - **Police/sheriff telephone reassurance programmes**: no answer → emergency contact → backup contacts → police dispatch.

  — [Savvy Senior, The Gazette, 10 Mar 2026](https://gazette.com/2026/03/10/savvy-senior-is-your-aging-parent-safe-at-home/)
- FACT: Meta-analysis of six case-control studies (1,065 heat-wave deaths):

  | Factor | Pooled OR (95% CI) |
  |---|---|
  | Confined to bed | 6.44 |
  | Not leaving home daily | 3.35 |
  | Unable to care for self | 2.97 |
  | Living alone | 2.09 (0.7–6.5), n.s. |
  | **Social contacts/activities** | **0.40 (0.2–0.8), protective** |
  | Home AC | 0.23 |
  | Visiting cool environments | 0.34 |
  | Fans | 0.60, n.s. |

  — [Bouchama et al. 2007, Arch Intern Med](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/413470)
- FACT: Ahmedabad HAP evaluation:
  - Est. **1,190 avoided deaths/year** (95% CI 162–2,218) post-HAP.
  - IRRs for >40 °C and >45 °C days were not statistically significant.
  - It is an ecological pre/post design that cannot separate components.
  - "Vulnerable population identification" is *not* described as a HAP component.

  — [Hess et al. 2018 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6236972/)
- FACT: DTE (30 Mar 2026) lists HAP gaps: weak outreach to rural and remote areas, weak geriatric integration, and planning that overlooks older adults living alone. It describes **no** Indian elderly check-in or buddy programme. Ahmedabad trains ASHAs — [Down To Earth](https://www.downtoearth.org.in/amp/story/climate-change/indias-elderly-face-deadly-toll-as-heatwaves-intensify)
- FACT: AWS SMS to India needs TRAI DLT registration (PAN/TAN/GSTIN/CIN), so it is not feasible for students in 48 h (prior notes) — [AWS docs](https://docs.aws.amazon.com/sms-voice/latest/userguide/registrations-sms-senderid-india.md)

### Inferences
- INFERENCE: Evidence supports the *mechanism* (social contact protects; isolation kills). No trial isolates "buddy check-in" as the effective ingredient, so impact claims must stay at "coverage KPI" level (e.g. "100% of registered vulnerable people contacted within 2 h").
- INFERENCE: C is a functional improvement *for India* (no programme found). It is a re-presentation of an established international protocol, and the software pattern is commodity.

### Gaps
- NDMA's heat-wave guidelines were not retrieved to check for buddy or check-in recommendations; my search did not surface them.
- France's post-2003 evaluation (Fouillet 2008) was not retrieved.
- No Indian NGO (HelpAge India etc.) heat check-in scheme was found; the search returned nothing specific.

---

## C2. How would judges see the similarity to Suraksha, and can C be demoed honestly without outside people?

### Takeaway
Similarity is high: same victim (an older person), same mechanism (tiered human escalation with timeouts), same AWS centrepiece (Step Functions `waitForTaskToken` plus EventBridge), and a demo arc ending in a person being notified. The differences (forecast trigger, a community roster of many residents, volunteer buddies, a coverage KPI) are real but subtle in a 3-minute video. An honest demo is easy: teammates act as buddies on their own phones, residents are synthetic and labelled, and the heat day is a labelled replay.

### Cited Findings
- FACT (OBSERVED in prior notes): Suraksha's video (1st prize, previous tour event):
  - A Galaxy Watch is dropped and the watch asks "Are you okay?" in Hindi.
  - A dashboard shows Escalation Progress (Neighbour NOTIFIED, Building Security NOTIFIED, Daughter PENDING) and a real phone rings.
  - Its architecture diagram has a "Proactive & Family Escalation" zone with **Step Functions, Web Push `waitForTaskToken` and EventBridge "every minute"**.

  — [winner_videos.md, Suraksha @1:03–2:48](https://www.youtube.com/watch?v=XVr34XeXvlE)
- FACT: The `.waitForTaskToken` pattern pauses a task until `SendTaskSuccess` or `SendTaskFailure` returns the token. `HeartbeatSeconds` makes the task fail with `States.Timeout` if no token arrives. It works only in Standard workflows and up to the 1-year execution limit — [AWS Step Functions docs](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html)
- FACT: Open-Meteo archive (data through yesterday) and forecast are keyless and verified for India (prior notes §2), so a labelled replay of a real May heat day is available.

### Inferences
- INFERENCE: A judge who saw Suraksha will likely read C as "Suraksha with a weather trigger". The story elements and the AWS service shown are nearly the same. Differentiation must be visible in the first 20 s:
  - many residents and many volunteers, not one family;
  - triggered by forecast, before anything happens;
  - a coverage board.
- INFERENCE: There is probably no live heatwave trigger in mid-October. The hottest of the 9 cities checked peaks at 38.1 °C (Ahmedabad, 10–16 Oct forecast). The plains heatwave threshold I recall from IMD (≥40 °C plus a departure from normal) was not re-verified this session. The trigger will therefore need a configurable threshold or a labelled replay, which weakens the "live" feel.
- INFERENCE: Outside-person dependence is avoidable, but the core impact (volunteers actually respond) is untestable in the demo.

### Gaps
- Whether the same judges will judge this tour event is not known.

---

## Q-Overlap. The five public Environmental Hacks worker-heat projects, and overlap with A, B and C

### Takeaway
All five are weather-only planners: WBGT or heat index from Open-Meteo, mapped to work/rest or schedules. None uses wearables, coolers or community elderly check-ins. **A and C do not overlap them.** **B overlaps in output** (personal heat-strain status plus rest/hydration advice, closest to HeatShift's "personal heat-strain score"). It is distinct in input, because B uses a body signal.

### Cited Findings (READMEs read 9 Oct 2026)
- FACT: **Chhaon** (souvikDevloper/chhaon):
  - Users: construction supervisors and crews.
  - Hourly WBGT via a Liljegren 2008 port on Open-Meteo, against ACGIH limits.
  - Hindi break announcements (EventBridge, Polly) and a Step Functions illness protocol with a 30-min re-check.
  - Bedrock assistant; replays of real May 2024 weather.
  - Wearable / core temperature / coolers / elderly check-ins: no.

  — [README](https://raw.githubusercontent.com/souvikDevloper/chhaon/HEAD/README.md)
- FACT: **ShiftShield** (gufran-09/Shift-Shield):
  - Site-adjusted WBGT (pywbgt, Liljegren) → NIOSH work-rest bands.
  - Supervisor-acknowledged break records via HMAC links; anonymous QR worker confirmation.
  - SAM, Lambda, EventBridge, DynamoDB, SNS, Bedrock Nova Pro.
  - Wearable / core temperature / coolers / Step Functions check-ins: no.

  — [README](https://raw.githubusercontent.com/gufran-09/Shift-Shield/HEAD/README.md)
- FACT: **₹800** (himanshu748/rs800):
  - CP-SAT schedules an outdoor worker's jobs around heat-index bands, maximising income.
  - Lambda, API Gateway, DynamoDB, Amplify; Hindi.
  - Wearable / core temperature / coolers / check-ins: no.

  — [README](https://raw.githubusercontent.com/himanshu748/rs800/HEAD/README.md)
- FACT: **HeatShift** (ansh-logics/Environmental-Hacks-Heatshift):
  - Gig and outdoor workers.
  - **0–100 personal heat-strain score** from Open-Meteo WBGT-based model, a work/rest/hydration plan and a relief-point map.
  - Worker status check-ins with a coordinator summary (no escalation).
  - AWS planned, not deployed.
  - Wearable / core temperature / coolers / elderly check-ins: no.

  — [README](https://raw.githubusercontent.com/ansh-logics/Environmental-Hacks-Heatshift/HEAD/README.md)
- FACT: **Heat-safe shift planner** (Mehulsri07/heat-shift-bot):
  - Rajasthan construction supervisor.
  - A Strands agent on Bedrock wraps a Python engine (NWS heat index + IMD cut-offs); Polly Hindi WhatsApp voice notes.
  - Android (Capacitor).
  - Wearable / core temperature / coolers / check-ins: no.

  — [README](https://raw.githubusercontent.com/Mehulsri07/heat-shift-bot/HEAD/README.md)

### Inferences
- INFERENCE: B must not lead with "WBGT work/rest plan". That is the crowded cluster (5 of 111 visible projects, ~33 extrapolated per prior notes). Lead with "your own heart is the sensor".
- INFERENCE: A and C sit in empty space within this event. C's risk comes from the *previous* event's winner, not from this event's field.

### Gaps
- New projects posted after the prior scan (9 Oct ~14:00 IST) were not re-scanned.

---

## Verdict for the coordinator

### A. CoolerCheck

**(i) Capability table (main user journey)**

| Step | Status | Basis |
|---|---|---|
| Location → hourly T, RH, T_wb for 16 days (India) | **VERIFIED** | Live Open-Meteo, 9 cities, 384 h, 0 null wet-bulb (A2) |
| Outlet T = T_db − ε(T_db − T_wb) per hour | **VERIFIED** | IS 3315, EnergyPlus, PNNL; computed live (A2) |
| ε default by pad type (wood wool ~0.55–0.70; thick or honeycomb ~0.75–0.93; BIS ≥0.65) | **VERIFIED-BUT-CONSTRAINED** | Indian honeycomb ε not measured; US media figures used |
| Mode strip: Cooler / Fan-only / Close up and ventilate | **VERIFIED-BUT-CONSTRAINED** | The answer depends on the comfort metric (HI vs WBGT); "cooler makes it worse" is not supported for a ventilated room |
| Litres of water per day | **VERIFIED-BUT-CONSTRAINED** | Deterministic psychrometrics, but needs real airflow (label is dry-pad free delivery); ±30–50% (INFERENCE). "Water wasted in humid hours" is **UNSUPPORTED** by physics |
| kWh per day | **PLAUSIBLE-UNTESTED** | Label wattage × hours; trivial |
| Learn each cooler's ε from user feedback | **UNSUPPORTED** | Comfort taps cannot identify ε; phone ambient sensors are rare or self-heated (A4). PLAUSIBLE-UNTESTED only with a thermometer the household already owns |
| Scheduled "switch now" / "drain tank" push via EventBridge Scheduler + web push | **PLAUSIBLE-UNTESTED** | Standard AWS; not built |
| Verification of benefit | **UNSUPPORTED** (measured); **VERIFIED** (forecast hindcast vs Open-Meteo archive) | No room sensor |

**(ii) Minimum working demonstration (no outside person, data or hardware)**
- A live Open-Meteo split screen for the same evening:
  - Ahmedabad or Nagpur at 15:00: outlet ~25–26 °C, ΔT ~9–11 °C, "Cooler ON", ~9–10 L/h at 2,000 m³/h.
  - Lucknow or Chennai at 06:00: ΔT ~0.6–1.1 °C, "Pump off, fan only".
- Plus a labelled archive replay of a dry May day and a humid July day for Delhi.
- Plus a 16-day "season over → drain and dry the tank this week (dengue)" prompt.
- Plus a hindcast check of yesterday's forecast vs observed.
- The ε assumption is shown on screen.

**(iii) Strongest skeptical objection, and is it answerable?**
- *"People can feel when their cooler stops working. Water use is self-limiting so there are no real savings. And an app already does exactly this (Evaporative Cooler Forecaster, 2025)."*
- **Partly answerable.** The India-specific angles (desert-cooler ε, litres planning, dengue drain prompt, Hindi, overnight humid-hour rule) are real. But the "saves water and stops humidity harm" pitch must be dropped, and the mechanism is not new.

**(iv) Functional improvement vs re-presentation**
- **Re-presentation (localisation)** of a mechanism shipped in May 2025 (Evaporative Cooler Forecaster; WetBulbCast).
- It is a functional improvement over what Indian households actually have. Symphony offers only a generic embedded wet-bulb calculator; Bajaj and Crompton auto modes react to room sensors without forecasts.
- But the measurable benefit is small and modelled, and the key physics claims in prior notes P-05/M-06 need correction.

### B. WristHeat

**(i) Capability table**

| Step | Status | Basis |
|---|---|---|
| Live HR from the team's watch into a Chrome page (Web Bluetooth HRS) | **VERIFIED-BUT-CONSTRAINED** | API documented (Chrome on Android/Win/Mac). Works only if the watch broadcasts standard HRS: Garmin (many), COROS, Polar Ignite 2/3 and Unite, Amazfit Zepp OS 3+, some Huawei, probably Xiaomi Band 10. **Not** Galaxy Watch; Apple only via HeartCast/iPhone (PLAUSIBLE-UNTESTED); Noise, boAt, Fire-Boltt undocumented (likely UNSUPPORTED). **The watch model is unknown, so this is a gate** |
| Fallback: exported workout file → minute HR | **PLAUSIBLE-UNTESTED** | Samsung CSV, Health Connect ZIP and Apple export exist; HR density unverified |
| ECTemp estimate from HR | **VERIFIED** | Parameters fully public (patent, USARIEM T17-08); implemented and simulated here |
| Accuracy of ECTemp with wrist optical HR | **UNSUPPORTED** | No validation found; validations use chest straps or ECG; optical error is ~30% higher in activity |
| WBGT from forecast at the user's location | **VERIFIED** | Open-Meteo inputs; Liljegren implementations already used by Chhaon and ShiftShield |
| PSI band plus rest/hydration advice | **VERIFIED-BUT-CONSTRAINED** | PSI formula published; advice must be framed as wellness (CDSCO guidance) |
| Real-time AWS loop (ingest → Lambda/IoT → alert) | **PLAUSIBLE-UNTESTED** | Standard services; not built |
| October demonstrability | **VERIFIED-BUT-CONSTRAINED** | A 30–45 min hard session (≥150–165 bpm) moves the estimate to 38–38.8 °C in my simulation; afternoon Tmax 33–38 °C in several cities. **No ground truth**, so the estimate is unverifiable on camera |

**(ii) Minimum working demonstration**
- A teammate wearing their own broadcasting watch runs or cycles 30–40 min in the afternoon.
- A Chrome (Android) page shows live HR → ECTemp curve → PSI band, alongside forecast WBGT for that location.
- An alert fires at PSI ≥7 (or estimated CT ≥38.5) with rest and water advice.
- An implementation cross-check overlays the same HR series run through the published equations, plus de Korte/Buller error bands.
- If the watch cannot broadcast, use the teammate's own exported workout file as a **labelled** replay. That is weaker.

**(iii) Strongest skeptical objection, and is it answerable?**
- *"That 'core temperature' is just smoothed heart rate. It can't tell heat from effort or nerves. It has never been validated on wrist optical sensors. It misses more than half of cases above 39 °C. And Garmin already shipped it in 2021."*
- **Only partly answerable.** You can cite military, athlete and farmworker validations, show environment fusion via WBGT, and position it as a strain *indicator*. The validity gap on wrist PPG and the Garmin precedent remain.

**(iv) Functional improvement vs re-presentation**
- Within this competition, a **genuine differentiator**: the only body-signal entry versus 5 weather-only planners.
- Globally, it **re-presents** an existing mechanism (GarminLabs field; Equivital, Zephyr, Kenzen, SlateSafety) for non-Garmin watches with WBGT fusion.
- Highest demo-risk of the three, and it depends on tonight's watch check.

### C. Heat Roll-Call

**(i) Capability table**

| Step | Status | Basis |
|---|---|---|
| Consent-based registry (resident, buddy, backup, secretary) | **PLAUSIBLE-UNTESTED** | CRUD on DynamoDB; DPDP consent wording needed |
| Forecast trigger (Open-Meteo + EventBridge Scheduler) | **VERIFIED** (data) / **VERIFIED-BUT-CONSTRAINED** (October) | None of the 9 cities checked goes above 38.1 °C on 10–16 Oct, so a threshold or labelled replay is needed |
| Per-person escalation (Step Functions `waitForTaskToken` + `HeartbeatSeconds` → backup → secretary) | **VERIFIED** | AWS docs |
| Notifying buddies on real phones | **VERIFIED-BUT-CONSTRAINED** | SMS blocked by DLT; use web push, Telegram bot or SES |
| Live coverage board and day-after summary | **PLAUSIBLE-UNTESTED** | Trivial |
| Real-world response by volunteers | **UNSUPPORTED** in demo | Teammates role-play |

**(ii) Minimum working demonstration**
- 6 synthetic, labelled residents and 3 teammates as buddies on their own phones.
- A labelled replay of a real May heat day triggers executions.
- One buddy deliberately times out → backup → secretary receives ORS and cooling-room instructions.
- The Step Functions graph and coverage board show "6/6 contacted in 1 h 50 m".

**(iii) Strongest skeptical objection, and is it answerable?**
- *"This is Suraksha (last winner) with a weather trigger — same elder, same escalation ladder, same `waitForTaskToken`. And Snug or a WhatsApp group does it."*
- **Weakly answerable.** You can cite community scale, forecast-before-harm, the precedents (fichier canicule, TeleRedi, Be a Buddy) and Bouchama's social-contact OR 0.40. But the story and AWS pattern overlap is obvious, the impact is unmeasurable in a demo, and October has no live heatwave.

**(iv) Functional improvement vs re-presentation**
- A functional improvement **for India** (no Indian programme found; HAPs criticised for lacking elderly outreach).
- Technically and conceptually a **re-presentation** of an established protocol and of Suraksha's architecture.
- Easiest to build and demo honestly, but the highest "seen it" risk with judges from the same organiser.

**Comparative note (INFERENCE):**

| Concept | Build risk | Novelty | Stance |
|---|---|---|---|
| A | Lowest | Weakest (an app already exists) | Only competitive with the corrected physics and the dengue/season-end angle |
| B | Highest (watch gate tonight) | Best in-competition | Pursue only if the team's watch passes the Web Bluetooth test before ~01:00 IST |
| C | Low | Prior-winner déjà vu | Avoid unless the video makes the community-scale, forecast-first difference unmistakable in the first 20 s |
