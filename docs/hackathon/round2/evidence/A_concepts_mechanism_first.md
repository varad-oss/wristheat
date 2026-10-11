# Mechanism-first and cross-track concepts for AWS Environmental Hacks (India, Oct 2026)

Researcher notes, Fri 9 Oct 2026. The method starts from a mechanism and then finds the environmental problem it fits best. Inputs: 00_RULEBOOK, 02_WINNER_PATTERNS, 04_EXISTING_SOLUTIONS, 05_SUBMISSION_OVERLAP_MAP, 06_WHITESPACE_MAP, 07_IDEA_LONG_LIST, 09_RED_TEAM, plus about 45 WebSearch/WebFetch calls this session (no browser was used).

**Tags used throughout**
- **FACT**: verified this session, with a link. "(via 04/06)" means the earlier team doc verified it and it was not re-checked today.
- **INFERENCE**: our reasoning from facts.
- **HYPOTHESIS**: untested and must be validated.
- **KNOWN**: widely known and not re-verified today.

Environmental benefits are never stated as demonstrated unless they carry a FACT tag.

**Data-access checks made this session:**
- **NASA FIRMS area API:** a free MAP_KEY is needed, queries cover 1–10 days, and VIIRS NRT sources are included. FACT ([FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/area/csv)).
- **Open-Meteo air-quality API:** uses CAMS global at 0.4° (~45 km), 3-hourly, with a 5-day forecast, free for non-commercial use. FACT ([docs](https://open-meteo.com/en/docs/air-quality-api)).
- **Open-Meteo historical API:** ERA5 (0.25°) and ERA5-Land (0.1°) from 1940/1950 with a 5-day delay, including dew point and wet-bulb. Only 10 m and 100 m winds are listed. FACT ([docs](https://open-meteo.com/en/docs/historical-weather-api)).
- **Electricity Maps free tier:** "free for individual users and developers… outside of their commercial workplace". India coverage is not confirmed on the page. FACT ([free tier](https://electricitymaps.com/free-tier)).
- **JJM WQMIS reports:** state-level tables; no village-level export was visible, and a login role exists. FACT ([WQMIS](https://ejalshakti.gov.in/WQMIS/Report/rpt_tubewell_testing_source)).
- **PVOutput:** robots.txt blocked the fetch, so it could not be checked.

---

## Q1. Mechanism-first concepts (M-01 to M-12)

### Takeaway

Four mechanisms survive constraints A–G cleanly and avoid the crowded rows in 05:

1. A **threshold forecaster for India's free-electricity "cliffs"** (M-01).
2. A **weather-normalised bill counterfactual** (M-02). M-01 and M-02 merge naturally into one Waste & Energy product.
3. **Back-trajectory smoke attribution with a next-day verification check** (Air, M-04).
4. An **hourly "cooler or not" psychrometric planner** (Heat & Water, M-06; contrarian).

Three concepts that looked attractive fail on evidence:
- Carbon-aware compute scheduling (M-03) is common at hackathons. Intraday variation in Indian grid carbon is weak or ambiguous on a marginal basis, and AWS regions are already 100% renewable-matched.
- Rain-harvest simulation (M-08) already exists as the open-source Indian app SimTanka.
- Smartwatch core-temperature estimation (M-11) depends on a device and is validated only on research-grade straps.

### Cited Findings (concept dossiers, 18 fields each)

---

#### M-01 · Unit Cliff: stay under your free-electricity threshold (Waste & Energy)

**Mechanism family:** timing and threshold forecasting under uncertainty, plus a verification loop.

1. **Actual problem.** Several states give free or subsidised household electricity up to a unit threshold and charge sharply more just above it. Households cannot see where they stand mid-cycle, so they cross the threshold by small amounts. The energy used near the cliff is often discretionary: an extra AC hour, a geyser left on, a pump overrun.
2. **Primary user.** A household in Delhi, Karnataka or Punjab whose typical monthly use sits within about 15% of its threshold. For example: a Delhi family averaging 180–230 units in Sept–Oct.
3. **Why it matters (evidence).**
   - **Punjab** (FACT, [Business Today](https://www.businesstoday.in/latest/economy/story/punjabs-pspcl-issues-notification-for-300-units-of-free-electricity-342512-2022-07-24)):
     - 300 free units a month (600 per two-month cycle).
     - General-category consumers who exceed 600 units "will have to pay for the entire power usage".
     - SC, BC and BPL households pay only for the excess.
   - **Karnataka Gruha Jyothi** (FACT, [The News Minute](https://thenewsminute.com/karnataka/explained-how-karnataka-free-electricity-scheme-will-work-178121)):
     - The entitlement is the household's past average plus a 10% buffer, capped at 200 units.
     - Use above the entitlement is charged about ₹7 per extra unit.
     - Above 200 units the household pays "the entire bill amount as per regular billing".
   - **Delhi** (FACT, [Housing.com](https://housing.com/news/electricity-rates-in-delhi/)):
     - 0–200 units are free.
     - 201–400 units get a 50% subsidy capped at ₹800, so crossing 200 moves the bill from ₹0 to a positive amount.
     - The article contradicts itself on whether slabs apply marginally. **Gap:** confirm with a DISCOM tariff order.
   - **Scale:** "over 4 million consumers apply" for Delhi's subsidy (FACT, headline, [Business Standard](https://www.business-standard.com/article/economy-policy/over-4-million-consumers-apply-for-delhi-govt-s-electricity-scheme-subsidy-122121301002_1.html)).
   - **Information friction:** a registered RCT in Punjab (Punjabi & Barnwal, MSU, 2025) is built on the premise that households bunch below the 10 kWh/day threshold but cross it because "obtaining updated information about quantity consumed remains a major friction". Its treatment is a meter-reading tutorial, a per-day calculator and SMS reminders. **No results are published yet** (FACT, [AEA RCT registry](https://www.socialscienceregistry.org/trials/16183)).
4. **Current workaround and alternatives.**
   - People read the meter occasionally or wait for the bill.
   - DISCOM apps and smart-meter apps show consumption: 5.28 crore smart meters were installed nationally by Dec 2025, 3.90 crore under RDSS, with "near real-time monitoring… through mobile applications" (FACT, [SolarQuarter](https://solarquarter.com/2026/02/03/india-installs-over-5-28-crore-smart-meters-under-rdss-to-boost-power-sector-efficiency/)). Most households, however, still have conventional meters (INFERENCE from 5.28 crore vs about 30 crore consumers; the consumer total is KNOWN, not verified).
   - Bijli Bachao offers a state-wise bill calculator (FACT, exists: [Bijli Bachao](https://www.bijlibachao.com/?p=71)).
   - **What they fail to do:** none we found projects the end-of-cycle reading against *your* threshold with a weather-aware forecast and then turns the gap into a daily unit budget. **INFERENCE:** we did not audit every DISCOM app.
5. **Underlying insight.** A price discontinuity makes saving salient for a few days each cycle. The scarce input is not motivation but a *forecast*, made early enough to act. Cooling-season use is weather-driven, so a weather-aware projection beats the naive "units so far ÷ days so far × cycle length" (INFERENCE; see M-02 for the evidence that weather drives load).
6. **Mechanism.**
   1. A meter photo, smart-meter screenshot or last bill is read into a reading with a timestamp, and the user confirms it.
   2. The billing-cycle dates and state rule are applied (rule table: Delhi, Karnataka entitlement, Punjab category).
   3. The remaining-days consumption is forecast as a distribution: base load plus a cooling term from Open-Meteo forecast temperatures, fitted on the household's own past cycles.
   4. The output is P(cross threshold), the expected ₹ jump, and a daily unit budget.
   5. A ranked list of concrete cuts is shown (e.g. AC setpoint 24 °C, geyser timer), each with an estimated units-per-day saving.
   6. A reminder asks for the next photo, which **verifies** whether the household is on budget and re-plans.
7. **What makes it distinctive.** The cliff itself is the lever. The product is a probabilistic, rule-aware forecast plus a budget, with a verify loop at each reading. Generic bill calculators are retrospective.
8. **Why it is not an existing feature with a new UI.** DISCOM and smart-meter apps show *past* consumption. Unit Cliff computes a *forward probability of crossing a policy threshold* and the budget needed to avoid it, which needs the state rule engine plus a forecast. **INFERENCE:** if a DISCOM app adds this, we are replicated, but we found no evidence that one has.
9. **Data and verifiable sources.**
   - User meter photos or screenshots.
   - State scheme rules (links above).
   - Open-Meteo forecast and historical temperatures (FACT, historical API verified).
   - Tariff orders from DERC, KERC and PSERC (KNOWN; must pull exact slabs).
10. **Architecture.** Mobile web (Amplify), then API Gateway and Lambda for upload, then a reading extractor (Bedrock vision or Textract), then a confirm screen, then a forecast Lambda (statsmodels, or the AWS open-source Chronos-Bolt model on CPU as a challenger), then the rule engine, then a budget screen. EventBridge Scheduler sends reading reminders. A Step Functions verify loop waits for the next reading, compares it with the budget, and re-plans or celebrates. DynamoDB stores readings.
11. **Meaningful AWS use.**
    - Bedrock or Textract reads messy meter displays (seven-segment LCDs).
    - EventBridge Scheduler is the heartbeat.
    - Step Functions is the verify loop with real waits.
    - DynamoDB is the ledger.
    - Optionally, Chronos (AWS open source) for the forecast.
    - Each maps to a verb (P5 in 02).
12. **Smallest useful MVP.**
    - One state rule (Delhi) plus Karnataka as a second.
    - Two photo readings, then the crossing probability and the budget.
    - Ranked cuts.
    - The next reading verifies.
13. **Reproducible demo plan.** Teammates photograph their *own* home meters today and tomorrow, which gives real readings 24 h apart. Use last-bill history from their DISCOM app or bill. If no teammate's home is near a threshold, show the household as-is, plus a labelled "what-if: a Delhi household at 185 units on day 20" scenario. No outside cooperation is needed.
14. **Strongest video moment.** Photo, then a red gauge: "71% chance you cross 200 units by 31 Oct, a ₹640 jump. Stay under 4.8 units a day." The next morning's photo turns the gauge green: "On budget: 4.3 units yesterday."
15. **Evidence for expected impact.**
    - The RCT's premise (FACT) shows researchers consider information friction binding near Punjab's threshold. Effect size is unknown: **HYPOTHESIS**.
    - Units avoided near the cliff are real kWh at the margin. **Caveat (INFERENCE):** households well *below* the threshold could learn they have "headroom" and consume more (rebound), so show headroom carefully or not at all.
16. **Risks.**
    - *Technical:* meter OCR on old electromechanical meters; billing-cycle dates vary.
    - *Product:* the benefit is ₹-first and could read as "help people keep subsidies"; the environmental story must be kWh avoided.
    - *Competition:* a DISCOM smart-meter app could add it.
    - *Policy:* rules change, so keep the rule table versioned and cited.
17. **Why another team might build something similar.** "Electricity bill analyser plus tips" is an obvious generic idea; for example, a lablab.ai submission titled "VoltWise AI" appears in search results ([lablab](https://lablab.ai/submissions/btlj8333qspfz8jv43acaz0k); not opened). A team that knows the Delhi 200-unit rule may build a calculator.
18. **What would distinguish ours.** A forward *probability* of crossing, tied to a state-specific cliff, plus a verified daily budget loop, all on real meter photos taken during the event.

---

#### M-02 · Bill X-Ray: was it the heat, or your AC? (Waste & Energy; cross-track with Heat)

**Mechanism family:** counterfactual and attribution, plus messy artefact to decision, plus a verification loop.

1. **Actual problem.** A summer bill jumps and the household cannot tell whether that is weather (unavoidable), behaviour (changeable) or a degrading appliance (fixable: low refrigerant, a clogged filter, a failing fridge gasket). So they either do nothing or pay for the wrong fix.
2. **Primary user.** An urban household with 12+ months of bills and at least one AC or cooler; at 43% AC ownership in a Delhi survey, a large class (FACT, [Carbon Brief on Khosla et al. 2021](https://www.carbonbrief.org/guest-post-how-energy-demand-for-cooling-in-indias-cities-is-changing)).
3. **Why it matters.**
   - Delhi daily peak demand correlates 0.82 with the heat index, which explains about 67% of its variation. Delhi's 2025 peak came at 11:09 PM, driven by cooling (FACT, [CSE](https://www.cseindia.org/sharp-rise-in-summer-heat-and-humidity-in-delhi-jacks-up-cooling-demand-and-electricity-consumption-cse-12857)).
   - At household level, weather explains much of the bill variance (INFERENCE from the grid-level correlation).
4. **Current workaround and alternatives.**
   - Compare with last year's bill, ignoring weather.
   - Bill calculators (Bijli Bachao, above) compute charges, not attribution.
   - DISCOM and smart-meter apps show raw consumption.
   - In the US, weather-normalised billing analysis uses the established PRISM degree-day method (KNOWN; [ACEEE 1986 proceedings](https://www.aceee.org/files/proceedings/1986/data/papers/SS86_Panel9_Paper_30.pdf), title seen in search, not opened).
   - **What they fail to do:** we found no Indian consumer tool that separates weather from household-driven change. **INFERENCE**, based on limited search.
5. **Underlying insight.** Each household's own bill history and the local temperature record together are a cheap natural experiment. Fit "kWh = base + slope × cooling-degree-days", and the residual is the part *you* control. A rising slope after controlling for weather is the signature of degraded cooling equipment (INFERENCE from standard building-energy practice).
6. **Mechanism.**
   1. Bill photos or PDFs (often printing past months; **Gap:** verify per DISCOM) or a DISCOM-app screenshot are extracted into monthly kWh with billing dates.
   2. Open-Meteo ERA5 hourly temperature for the address gives cooling-degree-hours per billing period.
   3. A robust regression gives base load, cooling slope and residuals.
   4. Verdicts: "Weather explained +38%; you added +12%"; or "your cooling slope rose 30% vs last summer: service the AC or check the fridge"; each with ₹ and kWh.
   5. After a service, the next bill (or meter readings via M-01) **verifies** the slope dropped.
7. **What makes it distinctive.** Counterfactual attribution: "what would this bill have been in last year's weather", from the user's own data, plus a verification step after repair.
8. **Why it is not an existing feature with a new UI.** Existing tools display bills. This one fits a household-specific physical model and produces a counterfactual, not a summary. The LLM only reads the document; the maths is deterministic (P3 in 02).
9. **Data.**
   - User bills or screenshots.
   - Open-Meteo historical (ERA5 or ERA5-Land, FACT verified).
   - CEA grid emission factor for kgCO₂ (via 07: 0.675–0.710 t/MWh, KNOWN).
10. **Architecture.** S3 upload, then Textract AnalyzeDocument/Expense or Bedrock vision, then a confirm table, then a Lambda (pandas or statsmodels) for degree-day regression, then a verdict card and chart. Step Functions watches for a new bill (or the M-01 readings) to verify. DynamoDB stores history.
11. **Meaningful AWS use.** Textract or Bedrock reads PDFs and photos. Lambda runs the model. Step Functions runs the verify loop. S3 and DynamoDB store data. ERA5 is also on the AWS Open Data registry (KNOWN), which is an option instead of Open-Meteo.
12. **MVP.** Upload 12 bills, get a weather-vs-you split with one chart and one verdict, plus a "verify after fix" placeholder fed by M-01 readings.
13. **Demo plan.** Teammates' families' real bills, with permission and redacted numbers. No hardware. A fallback is a labelled sample bill set.
14. **Strongest moment.** Two bars, "May 2025" vs "May 2026": the extra ₹1,100 splits into "heat: ₹700 | you: ₹400". Then: "your AC is doing 25% worse per degree than last year".
15. **Impact evidence.** The household-level attribution accuracy is **HYPOTHESIS**: 12 monthly points with occupancy changes give noisy fits, so show confidence. Savings from fixing degraded ACs exist (KNOWN in general) but are not quantified for India here.
16. **Risks.**
    - *Technical:* only 12–24 data points; non-temperature drivers such as guests, exams and a new appliance; humidity matters too (wet-bulb is available).
    - *Product:* a once-a-year use case unless merged with M-01.
    - *Competition:* bill analysers are an easy idea.
17. **Why another team might build something similar.** "Upload your bill, get AI tips" is a generic prompt output.
18. **What distinguishes ours.** The weather counterfactual and the "cooling slope" equipment-health signal, verified after a fix.

**Merge note (INFERENCE):** M-01 (forward cliff forecast) and M-02 (backward attribution) share the same inputs, ledger and AWS spine. Together they make one product, "your meter, explained and budgeted". This is the strongest Waste & Energy candidate that does not need anyone else's solar system.

---

#### M-03 · GridShift: carbon-aware scheduling of compute and batch jobs on India's grid (Waste & Energy; contrarian)

**Mechanism family:** timing and shifting under uncertainty.

1. **Actual problem.** Flexible electricity loads (batch compute, CI, ML training on campus servers or laptops) run whenever they are submitted, not when grid carbon intensity is lowest.
2. **Primary user.** University research groups and student developers with campus GPUs or on-prem servers in India.
3. **Why it matters.** The intended evidence is weak or contrary:
   - CSEP (Tongia, 2022) found "limited seasonal and intraday variability" in Indian marginal emission factors for 2017–18. Variability could be up to 4× greater under 2030 assumptions, and coal meets demand changes more than half the time in more than half the states (FACT, [CSEP abstract](https://csep.org/Journals/current-and-future-estimates-of-marginal-emission-factors-for-indian-power-generation/)).
   - An Imperial College study using Delhi and Mumbai Tata Power data found "midday MEFs often exceed AEFs". Its simulated scheduler saved only about 0.7% of household CO₂ (FACT, [Imperial PDF](https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/uk-epics/A-Public-Data-Framework-for-Carbon-Intelligent-Load-Shifting.pdf)).
4. **Alternatives.**
   - The Green Software Foundation's Carbon Aware SDK (FACT, [GSF](https://carbon-aware-sdk.greensoftware.foundation/docs/overview)).
   - CATS, an open-source Climate-Aware Task Scheduler (FACT, [CATS docs](https://cats.readthedocs.io/en/stable/introduction.html)).
   - Existing hackathon builds: a Devpost "carbon-aware AI job scheduler" (FACT, [Devpost](https://devpost.com/software/carbon-aware-ai-job-scheduler)) and lablab "GreenQueue" (FACT, [lablab](https://lablab.ai/ai-hackathons/ai-infra-summit-hackathon/greenqueue)).
   - AWS states that 100% of electricity in 25 AWS regions was matched by renewables in 2025 (market-based, possibly including RECs) (FACT, [Amazon](https://sustainability.aboutamazon.com/products-services/the-cloud)).
5. **Insight.** None strong enough. On marginal emissions, shifting to solar hours may not cut CO₂ in India (INFERENCE from the Imperial and CSEP findings).
6. **Mechanism.** A Step Functions wrapper takes a job with a deadline, waits until the forecast lowest-intensity window, runs the job, then uses realised data to compute the counterfactual gCO₂.
7. **Distinctive?** No. It is a known pattern with OSS and prior hackathon entries.
8. **Existing feature with new UI?** Largely yes (Carbon Aware SDK and CATS).
9. **Data.** India hourly intensity needs Electricity Maps (non-commercial free tier; India zones not confirmed) or self-built data from Grid-India reports (**Gap:** we did not find a clean API).
10. **Architecture.** Step Functions plus EventBridge plus Lambda plus a DynamoDB job queue.
11. **AWS.** Strong structurally, but the "AWS is already renewable-matched" counterpoint undermines the story for AWS-hosted jobs (INFERENCE).
12. **MVP.** CLI submit, wait, run, report.
13. **Demo.** Feasible with no hardware.
14. **Moment.** A Step Functions graph waiting until 13:00. Weak environmental punch.
15. **Impact.** Likely small or ambiguous (FACT-based INFERENCE: about 0.7% in the Imperial simulation, for households).
16. **Risks.** Data access; the marginal-vs-average critique; the judge question "isn't AWS already green?".
17. **Why others build it.** It is a common green-software hackathon idea.
18. **Distinguisher.** Only an India-specific marginal-emissions model would distinguish it, and that is not feasible in 48 h.

**Verdict: DROP.**

---

#### M-04 · Smoke Trace: whose smoke is this, and is more coming tomorrow? (Air)

**Mechanism family:** data fusion (satellite fires × wind fields × ground PM2.5), plus attribution, plus a verification loop.

1. **Actual problem.** In Oct–Nov, residents, schools and local officials in Indo-Gangetic Plain (IGP) cities face PM2.5 spikes but cannot tell whether a given day's spike is regional crop-fire smoke, which is transient and arrives with certain winds, or local sources. They also cannot tell whether smoke will arrive tomorrow. This affects both timing decisions and public accountability.
2. **Primary user.** A school administrator, an RWA, or a local journalist or official in a non-Delhi IGP city such as Ludhiana, Lucknow, Kanpur or Patna, which have no source-apportionment service. The secondary user is a Delhi resident.
3. **Why it matters.**
   - Delhi's IITM Decision Support System (DSS) gives a sectoral and stubble share for Delhi only, on a 10 km grid.
   - The DSS runs only in winter on a 2021 emissions inventory, and "CAQM had temporarily suspended the DSS last year over data reliability concerns".
   - It reported stubble at 0.22% on 5 Oct and zero on 6 Oct (2025) (FACT, [Vajiram & Ravi summary](https://vajiramandravi.com/current-affairs/delhis-air-pollution-explained-how-the-dss-tracks-the-real-polluters/)).
   - Stubble fires in 2025 were 2,518 in Punjab (FACT via 07).
4. **Current workaround and alternatives.**
   - IITM DSS (above): Delhi only.
   - urbanemissions.info runs CAMx and WRF at 0.25° with 3-day forecasts and state- and district-level source-contribution charts, including open fires, plus a 24 h VIIRS fire map. It has **no API**; NetCDF is "upon request" (FACT, [urbanemissions](https://urbanemissions.info/india-air-quality-forecasts/)). It is the most serious competitor scientifically, but presentation-only.
   - NASA FIRMS fire maps and NOAA HYSPLIT trajectories are expert tools that are not joined to a city's PM readings (KNOWN).
   - **What they fail to do:** none closes the loop from "trajectory says smoke likely tomorrow" to "measured PM the next day: was it right?" in a citizen-facing tool (INFERENCE).
5. **Underlying insight.** Attribution does not need a full chemical transport model to be useful. A 24–48 h back-trajectory from the city, intersected with *where and when* satellites saw fires, gives an interpretable "smoke-exposure index". Forward trajectories give a "smoke-arrival window" for tomorrow. The next day's measured PM2.5 rise is a free, honest test of each prediction (INFERENCE).
6. **Mechanism.**
   1. Pick a city and date.
   2. Integrate an air parcel backwards 48 h using hourly wind fields (Open-Meteo 10 m/100 m winds verified; pressure-level winds **not verified**; NOAA GFS or ERA5 on AWS Open Data as fallback, KNOWN).
   3. Pull FIRMS VIIRS detections, weighted by fire radiative power, within a corridor around the path (FACT: the API allows 1–10-day windows).
   4. Compute a smoke-exposure index and a label: "regional smoke likely", "mixed" or "mostly local".
   5. Run the forward trajectory for tomorrow, giving an arrival window and an advisory (e.g. move outdoor PE before the arrival time, run purifiers from 18:00).
   6. Next day, compare with the nearest station's measured PM2.5 (OpenAQ) and keep a running hit-rate scoreboard.
7. **What makes it distinctive.** The public scoreboard of verified vs failed smoke predictions (honesty as an artifact, P4) and the per-city on-demand trajectory, rather than Delhi-only or display-only outputs.
8. **Why it is not an existing feature with a new UI.** HYSPLIT has no fire intersection, no PM verification and no advice. urbanemissions has no per-event attribution, no verification and no API. DSS covers Delhi only. The fusion plus verification is new (INFERENCE).
9. **Data.**
   - FIRMS (free key, FACT).
   - Open-Meteo winds (FACT) or GFS/ERA5 on AWS (KNOWN).
   - OpenAQ on AWS (FACT via 04).
   - CPCB has no open real-time API on data.gov.in (FACT via 04).
10. **Architecture.** A Lambda trajectory integrator (numpy RK2 on gridded winds), a FIRMS fetch Lambda, an S3 cache, and a Step Functions daily pipeline: trajectories, then index, then advisory, then a wait 24 h, then fetch PM, then score. Bedrock writes a bilingual explanation. Amazon Location Service or Leaflet draws the map. DynamoDB stores the scoreboard.
11. **Meaningful AWS use.**
    - Step Functions with a real 24 h wait-and-verify.
    - EventBridge daily trigger.
    - S3 Open Data (OpenAQ, GFS or ERA5).
    - Bedrock narrows to explanation only.
    - Location Service for maps.
12. **MVP.**
    - Three cities.
    - A back-trajectory map with fire dots.
    - Index and label.
    - A tomorrow arrival window.
    - A scoreboard seeded by a labelled backtest over Nov 2024 and Nov 2025.
13. **Demo plan.** Historical replay of a known Nov 2024 smoke episode (labelled), plus a live run on 10–11 Oct 2026. **Caveat:** fire counts may still be low in early October (DSS stubble share was ~0% in early Oct 2025, FACT above), so the live run may say "mostly local". That is honest, and the backtest carries the drama. No hardware or cooperation is needed.
14. **Strongest moment.** An animated trajectory snakes back from Lucknow across hundreds of Punjab fire dots: "Regional smoke likely: arrives ~02:00." Cut to the next day: the measured PM2.5 rose 70 µg/m³ at 03:00. A green tick on the scoreboard.
15. **Impact evidence.** Exposure reduction from timing advice is **HYPOTHESIS**. Attribution accuracy of single-level trajectories is limited (INFERENCE); the backtest hit-rate must be reported, not assumed.
16. **Risks.**
    - *Technical:* trajectory physics in 48 h (keep it 2D at one level and be explicit); wind-data plumbing.
    - *Product:* "information, not intervention" unless the advisory and timing step is crisp.
    - *Competition:* stubble-fire maps are moderately crowded (4 per 100 in 05).
    - *Optics:* "blaming farmers"; frame it as a source split, not blame.
17. **Why another team might build something similar.** FIRMS plus an AQI map is a known October combination (05).
18. **What distinguishes ours.** Trajectory intersection plus a next-day *verified* scoreboard plus an arrival-window advisory for non-Delhi cities.

---

#### M-05 · Dose Ledger: where your PM2.5 dose actually comes from, and the one change that cuts it most (Air)

**Mechanism family:** attribution, plus decision ranking, plus data fusion (routine × hourly ambient × microenvironment factors).

1. **Actual problem.** AQI apps report *ambient* concentration. People act on the most visible moments (the morning walk, the commute) while most of their inhaled dose may come from sleeping hours indoors or one high-exposure commute mode. Effort goes to the wrong lever.
2. **Primary user.** An urban adult or parent in a polluted city who is willing to change one habit or buy one thing.
3. **Why it matters.**
   - On-road PM2.5 vs ambient in Delhi (Goel et al. 2015, Atmos. Env.) (FACT, [PDF](https://urbanemissions.info/wp-content/uploads/docs/2015-12-AE-Delhi-On-Road-Exposures.pdf)):
     - AC car about 0.5×.
     - Metro carriage about 0.8×.
     - Walking, two-wheeler and auto about 1.1–1.4×.
     - Cycling dose per km about 9× an AC car.
   - Indoor PM2.5 in Delhi homes was "substantially worse than the values reported by the government monitors", with mean differences of +114 and +122 µg/m³ (FACT, [EPIC/BFI highlight](https://epic.uchicago.edu/wp-content/uploads/sites/5/2025/06/IAQ-Research-Highlight.pdf)).
   - Purifier ownership is 24.1% in high-SES vs 1.8% in low-SES households, and a month of real-time indoor data "did not result in higher investments" (same source, FACT). Information alone does not move behaviour.
4. **Current workaround and alternatives.**
   - IQAir, AQI.in and Google AQI give ambient readings (KNOWN, via 04).
   - Indoor monitors and purifiers (hardware).
   - I-23 Purifier Reality Check covers indoor sizing only.
   - **What they fail to do:** none ranks *your* levers by share of *your* dose (INFERENCE).
5. **Underlying insight.** Dose equals the sum of concentration × microenvironment factor × breathing rate × time. For most people the bedroom term (8 h) and the commute-mode term dominate, so ranking interventions by Δdose is simple arithmetic but counter-intuitive (INFERENCE; to be demonstrated with the user's own numbers).
6. **Mechanism.**
   1. A 60-second routine builder (home, sleep hours, commute mode and times, outdoor exercise), or an imported location history (**Gap:** Google Timeline export is now on-device; format unverified).
   2. Hourly ambient from OpenAQ (nearest station) and CAMS (Open-Meteo, 45 km, 3-hourly).
   3. Microenvironment factors from the literature, as ranges.
   4. A weekly dose pie by microenvironment.
   5. Interventions ranked by Δdose with uncertainty: bedroom purifier with door closed, metro vs auto, shifting the run to afternoon, keeping windows closed at night.
   6. The user picks one, and the next week's ledger shows the *modelled* change. Verification is modelled, not measured, and must be labelled.
7. **What makes it distinctive.** Personal dose attribution and ranking, not an AQI number.
8. **Why it is not an existing feature with a new UI.** It needs the exposure model, ranges and ranking. No consumer AQI app computes dose by microenvironment (INFERENCE).
9. **Data.** User routine; OpenAQ on AWS (FACT via 04); Open-Meteo AQ (FACT); factors from Goel 2015 (FACT).
10. **Architecture.** Lambda exposure engine, DynamoDB routines, an EventBridge weekly ledger, and Bedrock to explain the ranking. Optionally S3 Athena over OpenAQ.
11. **AWS.** S3 Open Data (OpenAQ) plus Athena; Lambda; EventBridge; Bedrock. Less load-bearing than M-04 (INFERENCE).
12. **MVP.** Routine form, dose pie, top three levers, a "commit to one" step, and the next-week ledger.
13. **Demo plan.** Teammates' real routines in Delhi or their own city with real station data. No hardware.
14. **Strongest moment.** "Your 6 AM walk is 7% of your dose; your bedroom at night is 46%. Close the door and run the purifier you already own: −31%."
15. **Impact evidence.** Δdose is modelled (**HYPOTHESIS**). Indoor factors are uncertain, since the EPIC data show indoor can exceed monitors, so ranges are needed.
16. **Risks.**
    - *Technical:* indoor-factor uncertainty is large.
    - *Product:* verification is modelled, so it fails P2 "verify" in spirit.
    - *Competition:* overlaps the personal-lens researchers and I-07 (timing).
17. **Why another team might build something similar.** A "personal exposure tracker" is a plausible AI-prompt output.
18. **Distinguisher.** Ranked levers with uncertainty, from Indian microenvironment measurements.

**Recommendation:** use M-05 as a *module* of M-04 ("smoke arrives 02:00: this is the lever that matters tonight"), not as a standalone.

---

#### M-06 · Cooler Logic: hour by hour, when your desert cooler helps, and when it only adds humidity and burns water (Heat & Water; contrarian, cross-track with Air)

**Mechanism family:** timing under uncertainty, plus data fusion (wet-bulb × temperature × PM2.5 forecasts), plus decision ranking.

1. **Actual problem.** Evaporative ("desert") coolers are India's mass cooling device. Their cooling collapses as humidity rises (monsoon, coastal cities), yet people run them anyway. That adds moisture indoors, raising humid-heat stress, and consumes water. Meanwhile the cheaper option, cross-ventilating at night when outdoor air is cooler, is under-used, and in winter-transition months it conflicts with outdoor PM.
2. **Primary user.** A lower- or middle-income household with a cooler and fans, no AC, in North, Central or West India (and coastal cities in Sept–Oct).
3. **Why it matters.**
   - Air coolers are owned by about 40% of surveyed households in UP and 23% in Maharashtra, vs about 3.5% with ACs (FACT, [Prayas 2019 survey of 3,000 HH](https://energy.prayaspune.org/our-work/article-and-blog/space-conditioning-focus-on-fans-and-air-coolers-for-efficiency)).
   - About 8 million coolers are sold a year (stated, unsourced, same page).
   - "BEE does not have a star-rating programme for air-coolers" (FACT, same page, 2019; may have changed, so it is a Gap).
   - Delhi's monsoon heat index reaches 46–50 °C "even when actual air temperatures are lower". Night-time cooling fell 42% vs 2001–10 (FACT, [CSE](https://www.cseindia.org/sharp-rise-in-summer-heat-and-humidity-in-delhi-jacks-up-cooling-demand-and-electricity-consumption-cse-12857)).
4. **Current workaround and alternatives.**
   - Habit: run the cooler all day, every season.
   - Manufacturer guidance is promotional: Symphony says coolers "handle humidity better than ACs" and concedes only in an FAQ that "if the humidity level is excessively high, the cooling efficiency may decrease", with no threshold (FACT, [Symphony](https://symphonylimited.com/how-air-coolers-can-be-more-effective-than-ac-during-the-monsoon/)).
   - IMD and AQI apps give heat or AQI but no device-mode decision (KNOWN).
   - **What they fail to do:** no tool tells a cooler owner *which hours* the cooler actually cools (INFERENCE).
5. **Underlying insight.** Direct evaporative cooler output is T_out = T_db − ε(T_db − T_wb) (FACT, [EnergyPlus reference](https://bigladdersoftware.com/epx/docs/9-6/input-output-reference/group-evaporative-coolers.html); ε about 0.7 in its examples). The wet-bulb depression (T_db − T_wb) is forecastable hourly. When it is small, the cooler gives almost no temperature drop but full humidity gain. A fan with ventilation or night flushing is then better, and water is saved (INFERENCE from physics).
6. **Mechanism.**
   1. Location, then Open-Meteo hourly T, RH, wet-bulb and dew point, plus CAMS PM2.5.
   2. Per hour, compute cooler supply temperature and moisture gain, the outdoor-vs-indoor delta (indoor estimated from a lag model or entered from a ₹0 option: the thermostat display on an AC remote, or a wall clock-thermometer many homes have), and the humid-heat index.
   3. A mode schedule: **Cooler** / **Fan + windows open** / **Windows closed (PM high)** / **Cooler + window cross-flow**.
   4. Water litres per day from cooler airflow (m³/h from the label) × moisture gain (INFERENCE, psychrometrics).
   5. Next day, re-run on *observed* weather to show the counterfactual: hours of useless cooler running avoided and litres saved, labelled as modelled.
7. **What makes it distinctive.** It turns a psychrometric fact into a device-mode schedule, and it is contrarian: "turn your cooler OFF now".
8. **Why it is not an existing feature with a new UI.** Weather apps show humidity but not the derived cooler effectiveness or mode decision. Some coolers have humidity control (KNOWN; not verified which models), but they do not forecast or advise across modes.
9. **Data.** Open-Meteo forecast and historical (FACT: wet-bulb and dew point are available in the historical API; forecast KNOWN via 06). CAMS PM2.5 (FACT). Cooler airflow from the user's label photo (Bedrock vision).
10. **Architecture.** Static mobile web (Amplify), a Lambda psychrometrics engine, an EventBridge daily 6 PM "tonight's plan" with Polly Hindi voice, DynamoDB plans, and a Step Functions next-day counterfactual on observed data.
11. **AWS.** Lambda (engine), EventBridge Scheduler (heartbeat), Polly (voice, for low-literacy users), Bedrock vision (reads the cooler spec label), Step Functions (verify on observed weather). Moderately load-bearing.
12. **MVP.** City picker, then a 24-hour mode strip, litres saved and one voice briefing, plus a next-day observed-weather replay.
13. **Demo plan.** Live for Chennai or Mumbai in Oct (humid; the cooler is mostly useless) vs a labelled replay of Delhi's dry May 2026 (cooler excellent) and a humid July 2026 day. No hardware.
14. **Strongest moment.** Split screen, the same cooler on two days. May: "−11 °C, run it." July: "−2 °C, adds 3 L of water vapour per hour to your room. Switch to fan + windows."
15. **Impact evidence.** Water and energy saved are modelled (**HYPOTHESIS**). Health benefit is not claimed; humid-heat risk is an indicator only.
16. **Risks.**
    - *Technical:* ε varies by pad condition; indoor temperature is unknown without a sensor (partial).
    - *Product:* off-season in North India in October (demo by replay plus coastal live).
    - *Competition:* very low (INFERENCE).
    - *Credibility:* judges may ask "where is verification?" Answer with an observed-weather counterfactual, not behaviour.
17. **Why another team might build something similar.** Heat alert bots are crowded (05), but a cooler-mode planner is unlikely (INFERENCE).
18. **Distinguisher.** Device-mode advice from wet-bulb physics, litres of water, and a Hindi voice plan.

---

#### M-07 · RO Right-Size: do you need RO at all? (Heat & Water; contrarian)

**Mechanism family:** messy artefact (lab report or utility data) to decision ranking.

1. **Problem.** Households install reverse-osmosis purifiers by default, wasting reject water and demineralising water even where the source does not need RO.
2. **User.** An urban household buying or servicing a purifier.
3. **Evidence.**
   - NGT (28 May 2019) told MoEFCC to prohibit RO where TDS < 500 mg/L and required ≥60% recovery, so up to 40% may be wasted. The earlier BIS 2015 standard required only 20% recovery (FACT, [Down To Earth](https://www.downtoearth.org.in/news/water/ban-ro-systems-if-dissolved-solids-are-less-than-500-mg-l-ngt-64795)).
   - Follow-up NGT order of 29 Jun 2021 (FACT exists, [India Environment Portal](https://indiaenvironmentportal.org.in/in-court/order-of-the-national-green-tribunal-regarding-wastage-of-water-due-to-use-of-reverse-osmosis-29062021)).
4. **Alternatives.** Brand technicians' "water test" before sale (a conflict of interest: INFERENCE); TDS-meter videos.
   - **What they fail to do:** give an independent decision across BIS IS 10500 parameters (not just TDS) plus reject-water reuse.
5. **Insight.** TDS alone is the wrong decision variable; the treatment choice depends on the contaminant class (microbial → UV/UF; fluoride, arsenic or high TDS → RO or specific media). Matching treatment to contaminant saves water without compromising safety (INFERENCE).
6. **Mechanism.**
   1. Photo of a lab report or municipal water-quality notice, or the user's source type and location.
   2. Parameters extracted.
   3. A rule engine against IS 10500 limits gives a treatment recommendation with confidence, the TDS-controller setting and reject-water litres per day.
   4. A reuse plan (mopping, plants).
   5. "Re-test" reminder.
7. **Distinctive.** Contrarian ("you may not need RO") and rule-based rather than chat.
8. **Not a feature reskin.** No neutral tool does this (INFERENCE).
9. **Data.**
   - JJM WQMIS: state-level, export unclear, login roles exist (FACT, checked above). Village-level open data **not confirmed**.
   - Urban utility water-quality data is sparse (KNOWN).
   - Realistically it depends on user lab reports, which requires a lab test (₹500–1,500; a purchase, so partial on A).
10. **Architecture.** Textract (tables), a Lambda rule engine, Bedrock explanation and DynamoDB.
11. **AWS.** Textract or Bedrock reading, plus Lambda.
12. **MVP.** Lab-report photo → decision card.
13. **Demo.** Sample lab reports (synthetic, labelled) unless a teammate has one.
14. **Moment.** "Your TDS is 180. RO would waste ~25 L/day here. UV + sediment is enough for this report."
15. **Impact.** Water saved is modelled (**HYPOTHESIS**). Safety risk if wrong.
16. **Risks.** *Health liability* (high); data access; low demo drama.
17. **Why others build it.** Unlikely.
18. **Distinguisher.** Parameter-based treatment matching plus reject-water accounting.

**Verdict: PARK** (liability plus data access).

---

#### M-08 · Rain Ledger: simulate your roof's rainwater on 30 years of real days (Heat & Water)

**Mechanism family:** simulation and what-if.

1. **Problem.** Societies and homeowners size rainwater-harvesting (RWH) tanks or recharge pits from annual averages. Bengaluru buildings often pay the fine rather than implement RWH: 39,213 residential buildings are penalised monthly, and "People are ready to pay penalty, but not to implement RWH" (FACT, [The Hindu via PressReader](https://www.pressreader.com/india/the-hindu-bangalore-9WW1/20240321/281556590815663)).
2. **User.** RWA committees and plot owners in Bengaluru and Chennai.
3. **Evidence.** Above. Rules apply to 30x40 ft sites (new, 2009) and 60x40 ft (old, 2021 amendment) (FACT, same).
4. **Alternatives.** **SimTanka**, a free open-source Indian smartphone app that runs a daily water balance on past daily rainfall to estimate reliability, with Bangalore and Jodhpur examples (FACT, [arXiv 2404.13080](https://arxiv.org/html/2404.13080v1)).
5. **Insight.** Reliability curves beat averages, but SimTanka already productises this.
6. **Mechanism.** Roof polygon on a map, then ERA5 daily rain (Open-Meteo, FACT), then a daily balance, then a tank-size vs reliability curve and tankers avoided.
7. **Distinctive.** Low (SimTanka).
8. **Reskin?** Largely yes.
9. **Data.** Accessible (ERA5; building footprints via Open Buildings, KNOWN).
10. **Architecture.** Lambda simulation plus a map.
11. **AWS.** Lambda; ERA5 on AWS Open Data (KNOWN).
12. **MVP.** A slider and curve.
13. **Demo.** No hardware.
14. **Moment.** "A 10 kL tank gives 61 dry-season days; 20 kL gives only 9 more."
15. **Impact.** Modelled.
16. **Risks.** Duplicates existing OSS; no verify step.
17. **Why others build it.** "RWH calculator" is a common idea.
18. **Distinguisher.** None strong.

**Verdict: DROP** (it might survive only as a sub-feature for an RWA product).

---

#### M-09 · Dust Docket: an evidence-to-closure agent for construction-dust violations (Air)

**Mechanism family:** an agent with tool use carrying out a multi-step process with human approval, plus a verification loop.

1. **Actual problem.** Citizens see uncovered debris, dry-cutting or missing sprinklers at construction sites. Complaints are filed but closure is self-reported by the agency; nobody checks whether the site was actually fixed.
2. **Primary user.** A resident or RWA member in a city with active construction. It is Delhi-first because of the dust-portal rules; other cities use CPGRAMS or municipal channels.
3. **Why it matters.**
   - The Green Delhi app received over 84,000 pollution complaints in 2024. MCD received 54,878 and marked 84.33% resolved, with 8,599 pending (FACT, [Deccan Herald](https://www.deccanherald.com/india/delhi/delhi-govt-receives-over-84000-pollution-complaints-through-green-delhi-app-this-year-3331687)). Resolution quality is not reported, which is a Gap.
   - DPCC's Dust Portal 2.0 (Jul 2026) requires sites ≥500 m² to register, install PM2.5 and PM10 sensors, provide CCTV RTSP feeds and file a 15-day self-audit on 12 parameters such as green net, sprinkling and anti-smog guns (FACT, [ThePrint/PTI](https://theprint.in/india/dpcc-rolls-out-dust-portal-2-0-to-tighten-monitoring-of-construction-related-pollution/2981137/)).
4. **Current workaround and alternatives.**
   - Green Delhi app, CPCB Sameer and CPGRAMS (KNOWN). They accept complaints and record "resolved".
   - **What they fail to do:** independent re-verification by the complainant (INFERENCE). The dust-portal data is not shown to be public (FACT: the article does not say so).
5. **Underlying insight.** The binding constraint is not filing but *closure verification*. A re-photo from the same spot after the agency marks a complaint "resolved", compared against the same 12-parameter checklist the site self-audits against, turns a complaint into a verifiable before/after (INFERENCE).
6. **Mechanism.**
   1. A photo or video and GPS go to a Strands agent with tools, which maps visible violations to the 12-parameter checklist (vision, with human confirmation).
   2. It looks up jurisdiction and the channel (rule table).
   3. It drafts a complaint with the checklist evidence; the human approves.
   4. The complaint goes by SES email to the listed officer, or as copy-paste text for the Green Delhi app.
   5. EventBridge Scheduler sets follow-up timers.
   6. When the user marks the agency "resolved", the agent asks for a re-photo, compares, and returns "verified fixed" or "escalate", drafting the next-level complaint or an RTI.
7. **Distinctive.** Closure verification against the regulator's own checklist.
8. **Not a reskin.** Existing apps end at "resolved" (INFERENCE).
9. **Data.** User photos; rule texts (FACT above); CAQM directions (KNOWN, [CAQM site](https://caqm.nic.in/)).
10. **Architecture.** Strands Agents SDK (AWS open source) on Lambda or App Runner, with tools: classify_photo (Bedrock vision), find_channel, draft_complaint, send_email (SES, gated by approval), schedule_followup (EventBridge Scheduler), compare_photos. Step Functions wraps it in a human-approval callback. DynamoDB stores the case file.
11. **AWS.** Strands (AWS OSS), Bedrock, Step Functions callback, SES, EventBridge Scheduler, DynamoDB. Strongly load-bearing.
12. **MVP.** One site, one complaint, a scheduled follow-up, a re-photo comparison, and a verified or escalate decision.
13. **Demo.** A real public-road construction site near campus (photos only from public space, faces and plates blurred). The re-photo step is shown the next day. **Caveat:** the agency response will not happen in 48 h, so the "resolved" state is simulated and labelled. *Do not send real complaints for the demo without real violations.*
14. **Moment.** Before/after photos side by side with the checklist: "green net still missing → escalated to DPCC with evidence."
15. **Impact.** Dust reduction is not demonstrable in 48 h (**HYPOTHESIS**).
16. **Risks.**
    - *Legal and ethical:* photographing private sites and false accusations. Mitigate with human approval and public-space-only photos.
    - *Product:* Delhi-centric.
    - *Competition:* the civic-complaint template (2 per 100 in 05).
17. **Why others build it.** A "pollution complaint app" is a template.
18. **Distinguisher.** Checklist-mapped evidence plus re-photo closure verification plus an agent with approval gates.

---

#### M-10 · Pledge Threshold: conditional commitments that make a society's green investment happen (Waste & Energy or Heat & Water; coordination)

**Mechanism family:** a coordination and matching mechanism (assurance contract).

1. **Problem.** Collective green actions in housing societies, such as a shared composter (required of bulk generators under SWM 2026, via 06), a common-area RWH or recharge pit (Bengaluru fines, above) or common-area solar, stall because nobody wants to commit first and AGMs struggle to reach agreement.
2. **User.** An RWA secretary or a motivated resident.
3. **Evidence.** In lab experiments, assurance payments raised provision rates of a threshold public good (e.g. 0.95/0.77/0.45 vs 0.80/0.53/0.13 for the first three units). A Rhode Island field pilot raised $4,377 from 66 residents; the authors describe it as a small-sample proof of concept (FACT, [Liu, Li & Swallow 2020](https://aeaweb.org/conference/2020/preliminary/paper/AAb8ddr9)).
4. **Alternatives.** WhatsApp polls; MyGate and NoBrokerHood society apps (KNOWN, notices and payments); Kickstarter-style crowdfunding (KNOWN).
   - **What they fail to do:** conditional, threshold-triggered commitments tied to a vendor quote and a compliance outcome (INFERENCE).
5. **Insight.** "I'll pay ₹150 a month if at least 40 flats do" removes first-mover risk. The trigger also converts into a ready vendor request (INFERENCE).
6. **Mechanism.**
   1. Proposal (vendor quote parsed from a PDF).
   2. Per-flat share computed.
   3. Conditional pledges through a link.
   4. Live progress.
   5. At the threshold: binding notice and vendor RFQ; on the deadline without the threshold: auto-release.
   6. After installation, a photo verifies, and monthly logs feed compliance.
7. **Distinctive.** The assurance-contract mechanic in an Indian RWA context.
8. **Not a reskin.** A poll has no conditionality or trigger (INFERENCE).
9. **Data.** User inputs only.
10. **Architecture.** API Gateway, Lambda, DynamoDB (conditional writes), EventBridge Scheduler (deadline), SES or SNS, Textract (quote).
11. **AWS.** DynamoDB, Scheduler, SES. Adequate but not striking.
12. **MVP.** One proposal, pledge links, threshold trigger and RFQ.
13. **Demo.** Needs several pledgers. The team plus friends pledge live, or labelled seeded pledges. A real society would be outside cooperation, which is optional.
14. **Moment.** The 40th pledge lands and the vendor RFQ auto-sends.
15. **Impact.** **HYPOTHESIS** (evidence is lab-based and not from India).
16. **Risks.** Weak physical quantity; overlaps the community-lens researchers; payments are not handled.
17. **Why others build it.** Group-buy apps exist.
18. **Distinguisher.** The threshold-conditional pledge tied to a compliance outcome.

**Verdict: PARK** (best as a module of BinScore or an RWH product).

---

#### M-11 · WristHeat: heat strain from the smartwatch you already own (Heat & Water; unusual, partial on A)

**Mechanism family:** data fusion (wearable heart rate × WBGT forecast) and verification.

1. **Problem.** Outdoor workers and athletes cannot tell when *their* body is overheating; WBGT forecasts are population-level.
2. **User.** Delivery riders, outdoor workers or student athletes with a budget smartwatch.
3. **Evidence.**
   - The ECTemp Kalman filter (Buller et al. 2013) estimates core temperature from heart-rate sequences. It was trained and validated on military personnel.
   - In NCAA athletes using a research-grade Zephyr chest strap: bias −0.19 °F, 95% limits of agreement −1.80 to +1.42 °F, CCC 0.643, 78% within ±1 °F.
   - Consumer wearables were **not tested** (FACT, [Hagen et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7739355)).
4. **Alternatives.** The OSHA-NIOSH app (heat index, FACT via 04); research-grade wearables (KNOWN).
5. **Insight.** The heart-rate series already carries a heat-strain signal.
6. **Mechanism.** Import an HR export, run ECTemp, compute the physiological strain index, overlay WBGT hours, suggest a rest plan, and compare later sessions.
7. **Distinctive.** High.
8. **Not a reskin.** Yes, but validity on consumer devices is unproven.
9. **Data.** HR export from Health Connect, Google Fit or Apple Health (KNOWN; formats unverified).
10. **Architecture.** Lambda Kalman filter plus forecast.
11. **AWS.** Lambda, S3; thin.
12. **MVP.** One session file to a core-temperature curve.
13. **Demo.** Requires a smartwatch and exercise (consumer device, allowed but not prioritised).
14. **Moment.** The estimated core temperature crosses 38.5 °C mid-run.
15. **Impact.** **HYPOTHESIS**; medical-claim risk.
16. **Risks.** Device dependency (A partial); validation; liability; October off-season.
17. **Why others build it.** Unlikely.
18. **Distinguisher.** The ECTemp algorithm.

**Verdict: DROP** for this event.

---

#### M-12 · Fix-or-Replace: the carbon and ₹ case for repairing your phone or laptop (Waste & Energy; e-waste)

**Mechanism family:** decision ranking, plus artefact (device screenshot) to decision, plus verification.

1. **Problem.** Students replace phones and laptops when a battery or screen degrades, adding to e-waste and embodied emissions, because repair costs and benefits are opaque.
2. **User.** Students and young professionals.
3. **Evidence.**
   - India is the third-largest e-waste generator, with 1.6 Mt in 2021–22.
   - Globally only 13.8 of 62 bn kg (about 22%) was formally collected and recycled in 2022 (FACT, [Drishti summary of Global E-waste Monitor 2024](https://www.drishtiias.com/daily-updates/daily-news-analysis/global-e-waste-monitor-2024/print_manually)).
   - Extending EU smartphone lifetimes by one year would save more than 2 Mt CO₂e a year, and manufacturing dominates smartphone impacts (FACT, [EEB 2019](https://eeb.org/en/?p=99997)).
4. **Alternatives.** Cashify (resale and repair), OEM service centres and India's Right to Repair portal (KNOWN).
   - **What they fail to do:** a model-specific, carbon-plus-₹ comparison (INFERENCE).
5. **Insight.** Embodied carbon per year of use is the metric; a ₹2,500 battery swap can halve it (INFERENCE).
6. **Mechanism.**
   1. A screenshot of "About phone" and battery health is read into model and health.
   2. Embodied CO₂ from the manufacturer's product environmental report (Apple and Google publish these; KNOWN, coverage varies).
   3. Repair price from user or OEM lists.
   4. Ranking: repair, refurbish, sell or replace, with kgCO₂e per year and ₹ per year.
   5. Booking checklist; after repair, a new screenshot verifies battery health.
7. **Distinctive.** Medium.
8. **Not a reskin.** Partly.
9. **Data.** Product environmental report PDFs (KNOWN, uneven for Indian brands); user screenshots.
10. **Architecture.** Bedrock vision, a Lambda ranker, DynamoDB.
11. **AWS.** Bedrock, Lambda; thin.
12. **MVP.** Screenshot to verdict.
13. **Demo.** Teammates' phones. No hardware.
14. **Moment.** "Battery 71%: a ₹2,800 swap saves 48 kgCO₂e vs a new phone."
15. **Impact.** Modelled (**HYPOTHESIS**).
16. **Risks.** Low environmental magnitude per user; data gaps for Indian brands.
17. **Why others build it.** E-waste ideas are common (05: e-waste locators).
18. **Distinguisher.** The model-specific embodied-carbon ranking.

**Verdict: PARK.**

### Inferences

- **Most Indian-specific and least crowded mechanism found: M-01.** It is a policy-created price discontinuity plus a forward forecast plus a verify loop. Evidence that information friction binds near the cliff comes from an RCT design (FACT, premise only). It needs only a phone and a meter, every teammate has real data, and it is reproducible. Pairing it with M-02 gives a past, present and future story of one meter, and makes Bedrock/Textract, Scheduler and Step Functions each a verb.
- **M-04 has the best video moment.** Its verify step is genuine: tomorrow's measured PM checks today's prediction. The live October timing may lack fires, though, so a labelled backtest must carry the demo.
- **M-06 is the most contrarian with low build risk.** Its verify step is weaker (an observed-weather counterfactual, not behaviour).
- **Rejected on evidence, not on taste:**
  - M-03: hackathon saturation; weak or ambiguous Indian intraday marginal signal; AWS already renewable-matched.
  - M-08: SimTanka exists.
  - M-11: device dependency and validation.
  - M-07: liability and data access.
  - M-10 and M-12: weak physical quantity.
- **Cross-track pairings worth considering (one track must be chosen for submission):**
  - M-04 + M-05 (Air): "smoke arrives at 02:00; your bedroom is 46% of your dose, so close the door".
  - M-06 + Clean-Air Windows (Heat & Water or Air): "ventilate now, or not", fusing wet-bulb and PM.
  - M-01 + M-02 + SunCheck-lite (Waste & Energy): see Q2.

### Gaps

- The exact Delhi slab application at 201 units: is the 50% subsidy applied to the whole bill or to slab charges? Sources conflict ([Housing.com](https://housing.com/news/electricity-rates-in-delhi/) vs [Brookings](https://www.brookings.edu/articles/delhis-inefficient-electricity-subsidies/), which describes 50% on energy charges below 400 units). Check the current DERC tariff order before building.
- Whether Indian DISCOM bills print 12-month consumption history (affects M-02 onboarding). Not verified; ask teammates to check their own bills.
- Telangana and other states' threshold rules were not verified, so they are excluded from claims.
- The Punjab RCT (AEARCTR-0016183) has no published results.
- Pressure-level wind availability in Open-Meteo for trajectories was not verified; fallback is GFS or ERA5 on AWS Open Data (KNOWN, not checked today).
- Cooler water-use figures: no measured source found; the per-model estimate must come from psychrometrics (INFERENCE).
- Whether any DISCOM app already offers threshold forecasts: not exhaustively checked.
- PVOutput India systems could not be fetched (robots.txt).

---

## Q2. Re-test of earlier ideas (SunCheck, HeatShift, TankerTruth, Clean-Air Windows, BinScore) against A–G and team concerns

### Takeaway

- SunCheck as designed fails constraint C/F for *this team this weekend* unless a real system's history is obtained within hours. It is also partially replicated: some inverter apps show PR% or forecasts, and MNRE now mandates daily generation flows to a National Portal.
- HeatShift and Clean-Air Windows survive only if broadened beyond one institution type and given an observed-data counterfactual.
- TankerTruth should be dropped.
- BinScore survives only as a compliance ledger with weights, not a vision classifier.

### Cited Findings

#### SunCheck (I-01): rooftop solar check-up

| Check | Result |
|---|---|
| A software-only | Pass |
| B buildable | Pass technically (pvlib + Open-Meteo GTI + vision read) |
| C data | **Fail for us now.** The team has no access to a real system's history. PVOutput could not be checked (robots-blocked) |
| D relevance | Pass (50 lakh homes, via 06) |
| E differentiation | **Partial** |
| F observable | Fails without real data |
| G AWS | Pass |

**Evidence on the replication concern:**
- Sungrow iSolarCloud lists "PR%", Delta lists "performance ratio", and Goodwe SEMS lists a "generation forecast".
- No inverter app was found listing weather-normalised baselines or soiling alerts; the source attributes "weather-adjusted baselines" only to third-party Solar Analytics (FACT, [Heaven Green Energy blog](https://www.heavengreenenergy.com/blog/how-to-monitor-solar-generation); secondary source, feature tables are summaries).
- MNRE now requires inverter OEMs to store data in India and push **daily cumulative generation via a uniform API to the National Portal**, mapped to serial numbers. Consumer access is not described (FACT, [Energetica India, 21 Aug 2026](https://www.energetica-india.net/news/mnre-mandates-inverter-level-data-storage-within-india-for-pm-surya-ghar-rooftop-solar-systems)).
- **INFERENCE:** within 6–18 months the government or OEMs could offer expected-vs-actual for owners, which shrinks the window. The rain-as-calibration diagnosis and the maintenance-claim loop are still not shown anywhere.

**Verdict: DROP as the primary concept,** unless by **Fri 20:00** a teammate or relative supplies ≥45 days of daily history (app screenshots) for a real system. If that happens, keep it as an **optional "solar mode" inside the M-01/M-02 meter product**:
- Net-metered homes' bills show import and export, and the same weather-normalisation engine flags falling export relative to satellite irradiance month by month.
- This is coarser than SunCheck, but needs no inverter access.

#### HeatShift (I-02): WBGT work-rest planner

- **Constraints:** A, B, C and G pass (Open-Meteo, thermofeel). D is partial (site supervisors are a real but narrow decider). E passes. F is partial (the plan is visible; verification was "check-ins (weak)").
- **Concerns:** too niche; off-season in October in North India; the supervisor's incentive.
- **Verdict: MODIFY or PARK.**
  - Broaden the user to *any scheduler of outdoor effort*: school sports coaches, college fests, gig riders' own shift choice, farm-labour contractors.
  - Replace the weak check-in with an **observed-weather counterfactual**: the next day, recompute WBGT from observations for the original vs shifted schedule and report "high-risk person-hours avoided (modelled from observed weather)".
  - Demo with a labelled May 2026 replay plus live coastal-city October data.
  - If the team wants Heat & Water, **M-06 Cooler Logic is the stronger, broader Heat & Water candidate.** HeatShift's WBGT engine could become M-06's outdoor mode.

#### TankerTruth (I-05): tanker volume verification

- **Constraints:** A passes (phone photos). C is partial (sump geometry and gauge readability). D is partial (water-stressed-city societies only). E passes. F is partial (accuracy unknown). G is thin.
- **Concerns:** niche; weak environmental framing (fairness more than environment, per 06's own "Weakness"); few sumps have readable gauges (07 #15).
- **Verdict: DROP.** Its one good idea ("the sump is a meter if you know its geometry") does not justify a standalone entry.

#### Clean-Air Windows (I-03): school timing

- **Constraints:** A–C pass (OpenAQ on AWS; CAMS FACT). D is partial (NCR schools; timetables are rigid). E passes (measured counterfactual). F passes. G passes.
- **Concerns:** "too niche"; topic crowding (school AQI alerts 6 per 100 in 05); CAMS is 45 km and 3-hourly (FACT above), so hour-level advice relies on station history.
- **Verdict: MODIFY.**
  1. Generalise the user to *any recurring outdoor activity*: sports academies, morning-walk groups, coaching institutes' outdoor breaks, delivery-hub loading. Add an iCal import so a user's own calendar is re-timed.
  2. Fuse M-04's smoke-arrival window as the forward signal: the station diurnal profile is the baseline, and the trajectory flags abnormal nights.
  3. Keep the measured counterfactual as the hero.
- This makes "M-04 Smoke Trace + Clean-Air Windows" the recommended Air entry, with M-05 dose ranking as an optional tab.

#### BinScore (I-04): SWM-2026 compliance loop

- **Constraints:** A and B pass. C passes (user photos and weights). D passes (bulk generators everywhere). E is partial (vision grading looks like the crowded "waste classifier", 8 per 100 in 05). F passes. G passes.
- **Concerns:** niche (wardens and RWAs); vision accuracy on messy bins; gaming.
- **Verdict: MODIFY or PARK.**
  1. Make the core a **mass-balance compliance ledger**: weights per stream per day, compost output, and the gap to on-site-processing obligations.
  2. Use photos only as random-audit evidence, not as the classifier.
  3. Add **M-10's threshold pledge** to fund the composter.
  4. Demo on the team's own hostel bins (real data feasible).
- Still weaker on "observable environmental result in 48 h" than M-01/M-02, since contamination trends need days.

### Inferences

- The team's three concerns are correct for SunCheck. **M-01/M-02 keep SunCheck's best traits** (weather-normalised expected vs actual, artefact reading, verify loop, Indian policy hook) **while removing its fatal dependency** (a real solar system's history). Every household has a meter and bills.
- For Air, the best reuse of earlier work is Clean-Air Windows' *measured counterfactual* plus M-04's *trajectory scoreboard*. The two share OpenAQ, Step Functions waits and the same "tomorrow's data checks today's call" story.

### Gaps

- Whether a teammate can obtain a real solar household's 45+ day history by Friday night is unknown (a team action item).
- No direct verification that any inverter app computes irradiance-based expected yield. The secondary blog suggests not, beyond Goodwe's forecast.

---

## Q3. Summary table and triage

### Takeaway

Recommended shortlist for the coordinator:

1. **M-01 + M-02 "meter explained and budgeted"** (Waste & Energy). Best overall on A–G, data the team itself holds, and an Indian policy hook.
2. **M-04 Smoke Trace, merged with Clean-Air Windows** (Air). Best demo; the track is crowded and October fire counts are uncertain.
3. **M-06 Cooler Logic** (Heat & Water). Contrarian, cheap to build, weaker verification.

### Cited Findings

Ratings are 1–10 and preliminary (INFERENCE); the evidence is in the Q1 dossiers. P = pass, Pt = partial, F = fail.

| ID | Name | Track | One-line mechanism | A | B | C | D | E | F | G | Distinct. | Build 48h | Demo | Data access | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-01 | Unit Cliff | Waste & Energy | Meter photo → weather-aware forecast of crossing a state free-unit cliff → daily budget → next photo verifies | P | P | P | P | P | P | P | 8 | 8 | 7 | 8 | **Shortlist (merge with M-02)** |
| M-02 | Bill X-Ray | Waste & Energy | Bill history × ERA5 degree-days → weather-vs-you counterfactual + cooling-slope health → verify after fix | P | P | P (Gap: bill history format) | P | P | P | P | 7 | 7 | 7 | 7 | **Shortlist (merge with M-01)** |
| M-03 | GridShift | Waste & Energy | Delay deferrable jobs to low-carbon grid hours; post-hoc gCO₂ counterfactual | P | P | Pt | Pt | F | P | P | 3 | 7 | 4 | 4 | Drop |
| M-04 | Smoke Trace | Air | Back-trajectory × FIRMS fires → smoke index + tomorrow arrival window → next-day PM check scoreboard | P | Pt | P | P | P | P | P | 7 | 6 | 9 | 7 | **Shortlist (merge with Clean-Air Windows)** |
| M-05 | Dose Ledger | Air | Routine × hourly PM × microenvironment factors → dose attribution → ranked levers | P | P | P | P | P | Pt (modelled verify) | Pt | 7 | 8 | 7 | 7 | Module of M-04 |
| M-06 | Cooler Logic | Heat & Water | Hourly wet-bulb depression → cooler / fan / ventilate / closed schedule + litres → observed-weather counterfactual | P | P | P | P | P | Pt | P | 8 | 8 | 7 | 8 | **Shortlist (Heat & Water)** |
| M-07 | RO Right-Size | Heat & Water | Lab report → IS 10500 rule engine → treatment choice + reject-water saved | Pt | P | Pt | P | P | Pt | Pt | 7 | 7 | 5 | 4 | Park (liability) |
| M-08 | Rain Ledger | Heat & Water | Daily water balance on 30 years of ERA5 rain → tank reliability curve | P | P | P | Pt | F (SimTanka) | P | Pt | 3 | 8 | 5 | 8 | Drop |
| M-09 | Dust Docket | Air | Strands agent: photo → 12-parameter checklist → approved complaint → timers → re-photo closure check | P | Pt | P | Pt | P | Pt (agency step simulated) | P | 6 | 6 | 7 | 7 | Reserve Air option |
| M-10 | Pledge Threshold | W&E / H&W | Assurance contract: conditional pledges → threshold trigger → vendor RFQ → install photo | P | P | P | P | Pt | Pt | Pt | 6 | 8 | 6 | 9 | Park (module) |
| M-11 | WristHeat | Heat & Water | Smartwatch HR → ECTemp Kalman core temperature × WBGT → rest advice | Pt | Pt | Pt | Pt | P | Pt | Pt | 8 | 5 | 6 | 5 | Drop |
| M-12 | Fix-or-Replace | Waste & Energy | Device screenshot → product-report embodied CO₂ → repair vs replace ranking → health re-check | P | P | Pt | P | Pt | P | Pt | 5 | 8 | 6 | 6 | Park |

**Re-test verdicts:**

| Earlier idea | A | B | C | D | E | F | G | Verdict |
|---|---|---|---|---|---|---|---|---|
| SunCheck | P | P | **F (no system history)** | P | Pt (PR%/forecast in some apps; MNRE National Portal API) | F without data | P | **Drop as primary.** Optional "solar mode" in M-01/M-02 only if ≥45 days of real history arrive by Fri 20:00 |
| HeatShift | P | P | P | Pt | P | Pt | P | **Modify or park.** Broaden to any outdoor scheduler, add an observed-weather counterfactual; prefer M-06 for Heat & Water |
| TankerTruth | P | P | Pt | Pt | P | Pt | Pt | **Drop** |
| Clean-Air Windows | P | P | P | Pt | P | P | P | **Modify.** Generalise to any recurring outdoor activity (iCal) and fuse with M-04's arrival window; keep the measured counterfactual |
| BinScore | P | P | P | P | Pt | P | P | **Modify or park.** A weight-based compliance ledger plus audit photos plus the M-10 pledge, demoed in the team's own hostel |

### Inferences

- If the team wants the least-crowded track with the strongest real-data demo they can produce themselves, the merged M-01/M-02 in Waste & Energy is it. It also inherits most of SunCheck's narrative strengths (weather-normalised expected vs actual, a policy hook, verify) without its data blocker.
- If they want the most cinematic video and accept Air-track crowding, choose M-04 plus Clean-Air Windows.

### Gaps

- The ratings are judgement calls from desk research. The buildability ratings especially assume a 2–4 person team comfortable with Python, Lambda and a front-end framework.
