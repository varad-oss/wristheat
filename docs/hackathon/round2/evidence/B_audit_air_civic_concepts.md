# Air and civic concept audit: Dose Ledger (A), ReCheck (B), Window/Ventilation Planner (C), as of Fri 9 Oct 2026, ~22:00 IST

Tags: FACT = sourced or observed in a live call (source given). INFERENCE = judgement drawn from facts. HYPOTHESIS = untested claim.
Live checks ran in the built-in browser on 9 Oct 2026 between 21:50 and 22:30 IST: OpenAQ S3 archive, OpenAQ Explorer, Open-Meteo forecast and air-quality APIs, CPCB CCR, the OpenCity CKAN API, and GitHub. Nothing was signed into, submitted or downloaded to disk.

---

## A1. Dose Ledger: Indian exposure factors by mode, indoor/outdoor ratios, and inhalation rates

### Takeaway
Citable Indian factors exist for every mode in the journey. They disagree with each other by 1.5–3× depending on study, season and route, so a ledger must carry ranges rather than point values. The weakest term is also the largest share of weekly dose: indoor time at home. Delhi evidence ranges from indoor PM2.5 *below* outdoor (68% average at 11 sites) to indoor PM2.5 more than 100 µg/m³ *above* government monitors (winter, about 1,500 homes).

### Cited Findings

**Commute microenvironments (Delhi unless noted)**

| Mode | Ratio to ambient (Goel et al. 2015) | Absolute PM2.5, Maji et al. 2021 (Feb 2018) | Other Indian values | Breathing rate used by Goel (USEPA 2011) |
|---|---|---|---|---|
| Walk | ~1.4 ("~40% higher") | 259 ± 102 µg/m³ | — | 15 L/min ≈ 0.9 m³/h |
| Cycle | ~1.1 (other studies 1.5–3.4) | — | 59.8 µg/m³, highest of 4 modes (IIT Roorkee/Prana Air, 9–15 Feb 2023) | 35 L/min ≈ 2.1 m³/h |
| Motorised two-wheeler | ~1.3 (Y = 1.0 above 150 µg/m³ ambient; 1.7 below) | — | — | 10 L/min ≈ 0.6 m³/h |
| Auto-rickshaw | ~1.3 | "Rickshaw" 266 ± 159 µg/m³ (type of rickshaw not confirmed) | **Apte et al. 2011:** in-vehicle geometric mean 190 vs ambient 130 µg/m³; mean in-vehicle/ambient ratio **1.5**; black carbon 3.6×; ultrafine particle number 8.4× | 0.6 m³/h |
| Car, windows open, no AC | ~1.3 | 149 ± 13 µg/m³ | — | 0.6 m³/h |
| Car with AC | **~0.5** | 89 ± 30 µg/m³ | 40.2 µg/m³, lowest (IIT Roorkee/Prana 2023) | 0.6 m³/h |
| Bus (AC and non-AC) | ~1.2 | Bus 113 ± 14 µg/m³ | AC bus 40.8 µg/m³ (IIT Roorkee/Prana 2023) | 0.6 m³/h |
| Metro carriage | **~0.8** | **72 ± 11 µg/m³ (lowest)** | 55.8 µg/m³, about 1.39× AC car (IIT Roorkee/Prana 2023) | 0.6 m³/h |
| Bus stop / metro station | ~1.2 / ~1.3 | — | — | — |

Sources for the table:
- Goel et al. 2015: 8.1 km IIT Delhi–UPSC route; Jan–May 2014; 41 days, 75 tours, 150 one-way trips; one DustTrak, so in-vehicle and ambient were not simultaneous; ambient 130–250 µg/m³. Ratio Y falls non-linearly as ambient rises — FACT, [Goel et al., Atmos. Env. 123 (2015)](https://urbanemissions.info/wp-content/uploads/docs/2015-12-AE-Delhi-On-Road-Exposures.pdf)
- Goel's dose result at 165 µg/m³ ambient over 5 km trips: per km, cycling dose is about 4× two-wheeler, 9× AC car and 4× auto-rickshaw. Per hour the ratios are about 10×, 20× and 9× — FACT, same source
- Apte et al. 2011: 62 auto-rickshaw trips (about 160 h) on 31 days, 22 Feb–26 May 2010. In-vehicle PM2.5 was about 11% higher in the morning. In- and near-roadway sources made up 30% of in-vehicle PM2.5. A 1.9 h/day auto commute "is as least as large as full-day exposures" in high-income countries (stated for particle number) — FACT, [Apte et al., Atmos. Env. 2011](https://ce.berkeley.edu/sites/default/files/assets/users/kirchstetter/Apte%20et%20al%2C%20Particles%20in%20Auto-Rickshaw%20Exhaust%2C%20Atm%20Env%202011.pdf)
- Maji et al. 2021: respiratory deposition dose per km was walking 84.7 ± 33.4, rickshaw 15.8 ± 9.5 and non-AC car 9.7 ± 0.9 µg/km. Rickshaw is about 3.7× metro and walking about 3.6× metro by concentration — FACT, [Maji et al., Atmos. Pollut. Res. 12(2) 2021](https://uwe-repository.worktribe.com/output/6946307)
- IIT Roorkee (Dr Amit Agarwal) with Prana Air: 405 trips over 7 days by 6 participants. Walking and auto were not reported. This is an industry blog, not peer-reviewed — FACT, [Prana Air blog](https://www.pranaair.com/blog/prana-air-partnered-with-iit-roorkees-civil-engineering-dept-to-track-transport-pollution-in-delhi/)
- **Conflict:** the metro is 0.8× ambient and among the cleanest modes in Goel 2015 and Maji 2021, but 1.39× AC car and close to cycling (55.8 vs 59.8) in the 2023 IIT Roorkee/Prana data. Bus is ~1.2× ambient in Goel but nearly equal to AC car (40.8 vs 40.2) in Prana — FACT (sources above)

**Indoors at home**
- **Delhi winter (Nov–Feb), about 1,548 homes:** indoor PM2.5 was "substantially worse than the values reported by the government monitors", with mean differences of +114.4 (low SES) and +122.3 µg/m³ (high SES). Purifier ownership was 24.1% (high SES) vs 1.8% (low SES), yet indoor PM2.5 was only about 10% lower in high-SES homes. A 4-week real-time monitor did not raise purchases of purifiers or door seals — FACT, [EPIC India highlight (Greenstone, Lee, Sahai)](https://epic.uchicago.edu/wp-content/uploads/sites/5/2025/06/IAQ-Research-Highlight.pdf)
- **Delhi, Jan 2019:** 11 sites (restaurants, offices, homes) measured with AirVisual Nodes averaged indoor = 68% of outdoor. 9 of 11 were below outdoor; places with windows open constantly were excluded. This is a purifier vendor's blog, not peer-reviewed — FACT, [Smart Air](https://smartairfilters.com/en/blog/india-delhi-indoor-outdoor-air-pollution/)
- **Agra, 14 homes, Oct 2007–Mar 2008:** I/O ratios for PM2.5 and smaller were "close to or above 1.00" in roadside and rural homes and "less than 1.00" in urban homes. Indoor means were 135–173 µg/m³ — FACT, [Massey et al., Building & Env. 2009, via WASHplus](https://blogs.washplus.org/iaqupdates/2009/08/india-indooroutdoor-relationship-of-particles-in-residential-homes/index.html)
- **Literature review (mostly non-Indian):** the residential PM2.5 infiltration factor ranges 0.3–0.82, and penetration is about 1 for open windows — FACT, [Chen & Zhao, Atmos. Env. 45 (2011)](https://air.tongji.edu.cn/__local/3/C9/9C/4711FB5EE11CB782EEDD165D79A_7292F630_AB313.pdf)
- **Naturally ventilated buildings without indoor sources** have I/O "close to 1", rising above 1 with indoor sources such as cooking — FACT (literature summary), [Nihar et al., ERIS 3 025002 (2023)](https://doi.org/10.1088/2634-4505/acc88f)

**Inhalation rates**
- Goel 2015 used USEPA 2011 minute ventilation: cycle 35 L/min, walk 15 L/min, all motorised modes 10 L/min — FACT, [Goel 2015](https://urbanemissions.info/wp-content/uploads/docs/2015-12-AE-Delhi-On-Road-Exposures.pdf). Sleep and sedentary rates were not re-verified in this session (see Gaps).

### Inferences
- **The values support a range-based model, not a precise one.** A defensible default table:
  - AC car 0.5 (0.4–0.7); metro 0.8 (0.6–1.4); bus 1.2 (0.9–1.5); auto 1.3–1.5 (1.1–2.0); two-wheeler 1.3 (1.0–1.7); walk 1.4 (1.1–2.0); cycle 1.1–1.5 (1.1–3.4).
  - Home indoors 0.7–1.0 with no indoor source, but possibly above 1 in winter or with cooking.
  - These ranges are INFERENCE assembled from the FACT rows above.
- **The arithmetic says home dominates, not the commute** (INFERENCE, illustrative).
  - Assumed day: 14 h home at factor 0.9 and ~0.45 m³/h; 8 h office at 0.7 and 0.5 m³/h; 1.5 h auto commute at 1.4 and 0.6 m³/h.
  - Result: the commute is roughly 10–15% of daily inhaled mass, and home is about 60%.
  - A ledger that only covers trips misses most of the dose. The counter-intuitive "your bedroom is the lever" result (M-05) is real, but it rests on the least certain factor.
- **The ranking is only trustworthy where swaps differ by more than the factor uncertainty.** "Auto → metro" (≈0.8 vs ≈1.4 in two of three studies) and "walk 30 min beside a road → AC cab" are robust. "Bus → metro" is not robust: the studies disagree in sign.

### Gaps
- No Indian study measures *personal* weekly dose with time-activity diaries that could validate a ledger end to end. None was found in this session; not exhaustively searched.
- CSE, TERI and IIT Kanpur commuter studies were not located in the time available. Chennai (Nagendra group) and Bengaluru values were not collected, so non-Delhi factors are missing.
- Sleep and sedentary inhalation rates (USEPA Exposure Factors Handbook ch. 6) were not fetched. Values of about 0.25–0.3 m³/h are recalled, not verified, so treat them as HYPOTHESIS until checked.
- Maji 2021's "rickshaw" may be auto or cycle-rickshaw; the abstract does not say.

---

## A2. Dose Ledger: can a team get hourly PM2.5 for Indian cities this weekend?

### Takeaway
- **Keyless and live:** only CAMS via Open-Meteo. It is one 0.4° cell for all of central Delhi, and on 5 Oct it read **55–95% above** co-located stations while tracking their hourly shape (r = 0.52–0.87).
- **Station truth:** lags everywhere. The keyless OpenAQ S3 archive is about 4.5 days behind (newest file 5 Oct). The keyed OpenAQ API showed Delhi CPCB/DPCC stations "Updated 2 days ago".
- **Google Air Quality API:** has 500 m resolution, India with the CPCB index, and 30 days of hourly history, but needs a billing account.
- **CPCB's own endpoints:** the old ones no longer respond.

### Cited Findings
- **OpenAQ S3 archive (live, 9 Oct 21:51 IST):** stations 50, 235, 5626, 6356, 10486, 11603 (Delhi) and 11613 (Pune) all have their **newest file dated 2026-10-05**, last modified 2026-10-08 18:30 UTC. Station 8118 has no October files — FACT, live listing of `https://openaq-data-archive.s3.amazonaws.com/?list-type=2&prefix=records/csv.gz/locationid=<ID>/year=2026/month=10/` ([Registry](https://registry.opendata.aws/openaq/))
- **Contents of the 5 Oct files:**
  - PM2.5 at 15-minute cadence, 73–83 rows from 03:30 IST to midnight.
  - Daily mean PM2.5: Punjabi Bagh 63.3, Anand Vihar 56.5, DTU-CPCB 61.1, Chandni Chowk-IITM 49.7 µg/m³.
  - Station hourly range at DTU: 27 µg/m³ at 11:00 to 121 µg/m³ at 03:00 (4.5× diurnal swing).
  - FACT, live parse of `location-<ID>-20261005.csv.gz`.
- **CAMS (Open-Meteo) vs stations, 5 Oct, hourly:**
  - Open-Meteo returned **identical** PM2.5 for all three Delhi points (a single CAMS cell), with a daily mean of 96.6.
  - Station means were 56.7 (Anand Vihar), 62.1 (DTU) and 50.0 (Chandni Chowk).
  - Hourly correlation was r = 0.73, 0.87 and 0.52 (n = 21 hours each).
  - Example at 03:00: CAMS 140 vs DTU 121; at 11:00: CAMS 61 vs DTU 27.
  - FACT, live calls to `air-quality-api.open-meteo.com/v1/air-quality?...&start_date=2026-10-05&end_date=2026-10-05` and the S3 files above.
- **Open-Meteo AQ terms:** keyless for non-commercial use; 0.4° (~45 km); <10,000 calls/day; `past_days` up to 92 — FACT, [Open-Meteo AQ docs](https://open-meteo.com/en/docs/air-quality-api), [terms](https://open-meteo.com/en/terms) (via earlier data_access notes)
- **OpenAQ v3 API:**
  - Free tier is **60 requests/minute and 2,000/hour**, scoped to the user's key. Sign-up is at explore.openaq.org/register — FACT, [OpenAQ rate limits](https://docs.openaq.org/using-the-api/rate-limits)
  - The key docs say only "Sign up at explore.openaq.org/register to get your API key". Whether issuance is instant or needs email verification is **not stated** — FACT, [OpenAQ API key](https://docs.openaq.org/using-the-api/api-key)
- **OpenAQ freshness for Indian stations (live, 9 Oct ~22:10 IST):** the Explorer pages for "DTU, New Delhi - CPCB" (5626) and "Anand Vihar, New Delhi - DPCC" (235) both say "**Updated 2 days ago**", and the last-24-hour chart shows "No data in selected time range". DTU is listed as "Reference grade", owner CPCB, reporting since 09/03/2018 — FACT, [OpenAQ Explorer 5626](https://explore.openaq.org/locations/5626), [235](https://explore.openaq.org/locations/235)
- **Google Air Quality API:**
  - "covers over 100 countries with a resolution of 500 x 500 meters"; history up to 30 days hourly; forecast "up to 96 hours" — FACT, [overview](https://developers.google.com/maps/documentation/air-quality/overview)
  - **India is covered**, with default index `ind_cpcb` — FACT, [coverage](https://developers.google.com/maps/documentation/air-quality/coverage)
  - `extraComputations: POLLUTANT_CONCENTRATION` returns a `pm25` entry in `MICROGRAMS_PER_CUBIC_METER` (shown in the docs example) — FACT, [current conditions](https://developers.google.com/maps/documentation/air-quality/current-conditions)
  - History uses `history:lookup` with `hours` or `period` and pagination — FACT, [history](https://developers.google.com/maps/documentation/air-quality/history)
  - **Pricing:** one SKU, "Air Quality Usage" (Essentials), **10,000 free events/month**, then $5 per 1,000 up to 100k — FACT, [Maps pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
  - Billing must be enabled — FACT, [usage and billing](https://developers.google.com/maps/documentation/air-quality/usage-and-billing) (via data_access notes)
- **CPCB CCR:**
  - `https://app.cpcbccr.com/caaqms/rss_feed` returned **404** (GET) and **405** (POST). The legacy POST endpoints (`caaqms_landing_map_all`, `aqi_station_all_india`, `aqi_all_Parameters`) returned **405**.
  - `/ccr/` is now a static Next.js page of links ("All India CAAQMS Portal", "Data Repository").
  - `airquality.cpcb.gov.in` failed to load from the user's browser.
  - FACT, live calls 9 Oct ~22:00 IST.

### Inferences
- **For a retrospective weekly ledger (Sun 11 Oct), use:**
  - **CAMS** for the full week (keyless, every hour, but one value for the whole city and biased high on 5 Oct).
  - **Station data where it exists:** the S3 archive up to ~5–6 Oct, or the OpenAQ API with a teammate's free key up to ~7–9 Oct.
  - **Google AQ** if a teammate already has a Maps billing account. A week of hourly history per location is a handful of events, well inside 10,000/month.
- **Within a city, CAMS cannot tell routes apart.** Every Delhi point gets the same number, so "route swap" levers are not supported by keyless data. Only **time** swaps (diurnal shape, r up to 0.87) and **mode** swaps (literature factors) are.
- **CAMS diurnal amplitude looked muted on 5 Oct** (CAMS 61→140 vs DTU 27→121). Departure-time savings computed on CAMS will be roughly right in direction and uncertain in size (INFERENCE, one day).
- **No documented keyless live CPCB API exists today.** Scraping undocumented portal endpoints would breach "data public/legal" in spirit (INFERENCE).

### Gaps
- Whether OpenAQ key issuance is instant (not documented; sign-up not attempted, by instruction).
- Google AQ hourly-history accuracy in India vs CPCB stations (not testable without billing).
- aqi.in, SAFAR and urbanemissions forecast endpoints were not probed; time was spent on CPCB and OpenAQ.
- Only one day (5 Oct) of CAMS-vs-station comparison; bias may differ in smog episodes.

---

## A3. Dose Ledger: Google Maps Timeline export in 2026

### Takeaway
Export is a one-file JSON from the phone with a well-documented (third-party) structure: visits, activity segments with a mode guess, and paths. But **Timeline is off by default**. A teammate can produce a week's file in minutes **only if they had already opted in**. Otherwise they can log Sat–Sun from now or type a routine. There is no auto-rickshaw class, so the user must confirm the mode.

### Cited Findings
- "Timeline is off by default for your Google Account and can only be turned on if you opt in." Data "comes directly from your device"; Timeline is not available on computers; an optional encrypted backup goes to Google's servers — FACT, [Google Maps Help](https://support.google.com/maps/answer/6258979?hl=en)
- **Android path:** Settings → Location → Location services → Timeline → "Export Timeline data" ("Download a copy of visits and routes from this device"). It requires authentication and produces "a single .JSON file" — FACT, [Android Authority, 16 Oct 2024](https://www.androidauthority.com/android-google-maps-location-history-3491255/). The same steps appear in [MileageWise's help](https://www.mileagewise.com/help/how-to-import-trips-from-google-maps-timeline-on-android-devices/)
- **In-app path:** Google Maps app → Settings → Personal content → Export Timeline data. The source does not specify the OS — FACT, [Dawarich](https://dawarich.app/blog/whats-inside-your-google-timeline-export/)
- **Format:**
  - The file is usually `location-history.json` or `Timeline.json`, with top-level `semanticSegments`, `rawSignals` and `userLocationProfile`.
  - Visits carry `startTime`, `endTime`, UTC-offset minutes and `visit.topCandidate` {`placeId`, `semanticType`, `placeLocation.latLng`}.
  - Activities carry `activity.start/end.latLng` and `activity.topCandidate.type`.
  - `timelinePath` holds points written as strings like `"50.05°, 14.34°"`.
  - `frequentPlaces` labels HOME and WORK.
  - FACT, [Dawarich](https://dawarich.app/blog/whats-inside-your-google-timeline-export/)
- **Activity types:** WALKING, RUNNING, CYCLING, IN_PASSENGER_VEHICLE, IN_BUS, IN_TRAIN, IN_SUBWAY, FLYING, MOTORCYCLING, SKIING, SAILING. Classification "is sometimes inaccurate", for example bus vs driving — FACT, [Dawarich timeline statistics](https://dawarich.app/tools/timeline-statistics/)
- **Failures and history:** export failures are reported ([Google Maps Community thread, Mar 2025](https://support.google.com/maps/thread/334584618/exporting-local-google-maps-timeline-fails?hl=en), title only). Past trips may be missing on a new phone unless backup was on ([MileageWise](https://www.mileagewise.com/help/how-to-import-trips-from-google-maps-timeline-on-android-devices/)) — FACT

### Inferences
- **Parsing is easy:** 2–3 hours for segments, mode mapping and lat/lng string parsing (INFERENCE).
- **Mode mapping needs a confirm step:**
  - Auto-rickshaw and e-rickshaw will appear as IN_PASSENGER_VEHICLE or MOTORCYCLING.
  - Delhi Metro should appear as IN_SUBWAY or IN_TRAIN.
  - Bus/car confusion is documented.
- **Ask the team tonight whether anyone has Timeline on.** If nobody does, the "real week" claim collapses to a 2-day log plus a typed routine.

### Gaps
- No real 2026 export file was inspected. The field names come from a third party, not Google's documentation (Google publishes none).
- iOS export behaviour was not confirmed from a primary source.

---

## A4. Dose Ledger: competitors (market and in-event)

### Takeaway
**Per-trip dose with "leave later / take another mode / take another route" is already built by at least 6 visible Environmental Hacks teams.** One of them, ALive, is a polished Delhi dosimeter with a ledger. Research tools (US EPA TracMyAir, HKUST PRAISE-HK) already do dose by microenvironment from time-activity. What remains uncontested is narrow:
- a *retrospective* week from real location history that includes indoor hours;
- swaps ranked by dose avoided per minute;
- a week-over-week check.

### Cited Findings
**In-event (README text read live, 9 Oct ~22:20 IST)**
- **ALive** (GC-WORK11/alive-mirror): "Delhi PM2.5 dosimeter"; the user types a trip and gets candidate routes, each "priced" with an inhaled-dose band.
  - Air field: CAMS + FIRMS + 52 WAQI/DPCC stations fused every 15 min (Kalman + kriging, ±σ), validated on 3,550 station pairs (MAE 22.0 µg/m³).
  - It has a per-device ledger (`/v2/ledger`) and cites "walking ≈28× metro per km".
  - Built on ECS Fargate, DynamoDB and S3 in ap-south-1. No weekly attribution or departure-time ranking is described.
  - FACT, [README](https://raw.githubusercontent.com/GC-WORK11/alive-mirror/main/README.md)
- **EcoRoute AI** (Kishores57/envh): "recommends a route or departure time that minimizes estimated pollution exposure", e.g. "if leaving 35 minutes later reduces exposure by 33%". Uses an API Gateway `/departure-times` route and SageMaker XGBoost — FACT, [repo](https://github.com/Kishores57/envh)
- **Breathe Route** (PranayBhardwaj29/breathe-route; new since the earlier scan): a "Best Time to Leave" engine showing cyclists how shifting a trip by an hour "can cut particulate inhalation by up to 35%", using CAMS — FACT, [repo](https://github.com/PranayBhardwaj29/breathe-route)
- **better_AQI:** a "Cleanest Commute" exposure planner comparing bicycle, two-wheeler/auto, car with AC filter and walking to compute inhaled µg. Also an indoor purifier countdown that models window leakage, and a school "optimal mid-day ventilation window" — FACT, [repo](https://github.com/akshayaparida/better_AQI)
- **AirTrace / BreatheWise:** compares routes by "travel time versus inhaled particulate exposure", with school ventilation guidelines — FACT, [repo](https://github.com/AkibRaza3723/AirTrace)
- **RideClean** (Goyamjain06): delivery riders' "day's dose so far", cigarette equivalent and best time — FACT, [repo](https://github.com/Goyamjain06/goyam_aws)

**Market and academic**
- **US EPA TracMyAir:** predicts "individual air pollution exposure and dose for … PM2.5 and ozone". Inputs are location, 24 h of time-activity, home details (including "number of open windows") and activity level. Output is a dose pie per microenvironment plus a six-day comparison. It covers the 48 contiguous US states, targets researchers, and the page says "no longer updated" — FACT, [EPA snapshot](https://19january2025snapshot.epa.gov/air-research/tracmyair-web-application-researchers)
- **PRAISE-HK (HKUST):** the app "tracks … our personalized exposure budget throughout the day" across outdoor, indoor and transport microenvironments. It "shows users when, where and during what activity they receive the largest dose" and what to do to reduce it. Hong Kong only; article dated Nov 2021; current status unknown — FACT, [HKUST](https://hkust.edu.hk/news/personalized-real-time-air-quality-informatics-system-exposure-hong-kong-praise-hk)
- **HazeDose:** an inhaled-dose estimation system using wearable sensors (Sydney research) — FACT, [arXiv 2005.13745](https://ar5iv.labs.arxiv.org/html/2005.13745)
- **IQAir AirVisual:** an exposure dashboard "based on the WHO guidelines", where the user assigns Home, Work and Outdoor data sources to track "daily pollution exposure". No dose, activity attribution or swaps are described — FACT, [IQAir](https://shop.iqair.com/blogs/news/how-to-set-up-my-personal-pollution-exposure-tracking)
- **Plume Labs** was acquired by AccuWeather in Jan 2022 — FACT, [TechCrunch](https://techcrunch.com/2022/01/24/accuweather-acquires-air-pollution-startup-plume-labs)

### Inferences
- **A judge who has seen ALive, EcoRoute or Breathe Route will read Dose Ledger as "another dose calculator"** unless the first 30 seconds show something they cannot do (INFERENCE):
  - a whole week, from real location history, *including home and office hours*;
  - a ranked list mixing a departure-time change, a mode change and an indoor change on one "µg avoided per minute" axis;
  - honest bands.
- **No consumer product found ranks a person's behavioural swaps by dose per minute of inconvenience over a real week** (INFERENCE from absence in the sources read; the search was not exhaustive). TracMyAir and PRAISE-HK are the nearest academic analogues: dose by microenvironment, no swap ranking.

### Gaps
- Current status of the Plume Labs app (whether discontinued) was not established.
- AQI.in, Airly, SAMEER and Google Maps' AQI layer were not inspected for exposure features in this session.
- GitHub repository search is incomplete: it returned 73 repos for the event keywords and is rate-limited. More dose projects likely exist.

---

## B. ReCheck: data, prior art, recurrence evidence and honest demo

### Takeaway
- **Closure re-verification is rare but not unprecedented.** FixMyStreet re-asks the reporter at 4 weeks (and every 4 weeks while unfixed). The Swachhata app lets the citizen reopen. A "resolution half-life" metric was not found anywhere.
- **The ICMyC open log is real and keyless** (16,071 Bengaluru complaints, Jan 2019–Jul 2022), but it has **no resolution timestamp or status history**. It cannot back-test a half-life, only a "repeat-complaint interval" proxy.
- **The live demo can be honest without outsiders** (team re-photographs 3–5 spots over 36 h). It yields a tiny curve, not a credible half-life.

### Cited Findings
- **ICMyC dataset (live via the CKAN API, 9 Oct):**
  - Resource "I Change My City Complaints Log - 2019 - 2022", CSV, 8.38 MB, datastore active, CC BY-SA.
  - **16,071 rows.**
  - Fields: `created_at, ward_id, title, description, sub_category_id, civic_agency_id, location, address, latitude, longitude, ward_title, category_*, sub_category_title, civic_agency_title, complaint_status_title, comment_count`.
  - **No resolved/closed timestamp and no status history.**
  - The second resource is a 200-row ward aggregate.
  - FACT, [OpenCity CKAN package_show](https://data.opencity.in/api/3/action/package_show?id=i-change-my-city-data) and `datastore_search` calls
- **ICMyC final-status counts:** Open 8,817; Resolved 4,937; On-the-Job 1,653; **Re-opened 332**; Rejected 220; Closed 112. Agencies are Bengaluru's (e.g. BBMP). Date formats are mixed ("1-1-2019 06:33" and "7/31/2022 14:03"), spanning 1 Jan 2019 to 31 Jul 2022 — FACT, live datastore pull
- **Garbage, debris, dump and burning complaints:** 4,300, by year 2019: 2,125; 2020: 1,352; 2021: 590; 2022 (Jan–Jul): 233.
  - Top sub-category: "Clearance Of Garbage Dump Or Black Spot" (3,110).
  - "Stop/Prevent Burning Of Garbage": 33.
  - Final status: Resolved 1,996; Open 1,945; On-the-Job 260; **Re-opened 112**.
  - FACT, live computation
- **Repeat-location proxy:**
  - Rounding to 4 decimals (~11 m) gives 366 spots with more than one garbage complaint (983 complaints).
  - Excluding clusters over 15 (likely geocode defaults; e.g. 12.9716, 77.5946, the Bengaluru centroid, appears 11×): 588 inter-complaint gaps.
  - 201 gaps are same-day duplicates and 300 fall between 7 and 365 days.
  - Median gap 39 days; IQR 0–164 days.
  - FACT, live computation; the interpretation as recurrence is INFERENCE.
- **FixMyStreet:** a survey goes "four weeks after a user reports a problem". The user can change the state; re-opening makes the comment mandatory. If not fixed, another survey follows four weeks later (opt-in). Admins see counts and percentages — FACT, [FixMyStreet surveys](https://fixmystreet.org/running/surveys/). Some councils let reporters set "not fixed" — FACT, [FAQ](https://www.fixmystreet.com/faq)
- **Swachhata app (2017 description):** the sanitary inspector marks "resolved"; "You can reopen the complaint if the response does not satisfy you"; garbage dumps have a 12-hour SLA — FACT, [The Better India](https://www.thebetterindia.com/96351/swachhtaa-app-ministry-of-urban-development/amp/)
- **TrashOut:** volunteers can return to a reported dump "to check if the place has been cleaned or not"; more than 100,000 dumps logged (2017) — FACT, [ICT.io](https://ict.io/en/?p=29604)
- **Recurrence evidence:**
  - Bengaluru's garbage monitoring portal showed **5,445 active black spots, up from ~3,200 a month earlier** — FACT, [Siasat, 10 Jun 2026](https://www.siasat.com/bengalurus-garbage-crisis-worsens-as-black-spots-surge-to-5445-3486126/amp/)
  - BBMP's chief aims to clear black spots "permanently"; the article names no re-inspection mechanism — FACT, [Deccan Herald, 6 Jul 2025](https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fbengaluru%2Faiming-to-clear-all-black-spots-permanently-says-bbmp-chief-3617543)
  - Mapusa black spots "re-appear immediately after the garbage is lifted" — FACT, [Free Press Journal, Oct 2023](https://www.freepressjournal.in/goa/goa-incessant-waste-dumps-continue-to-mar-mapusas-image)
  - Earlier notes: 1,109 Hyderabad GVPs reappeared; fake closure photos in Gurugram — FACT via C-02.
- **In-event overlap (live GitHub read):**
  - "CivicLens — Every garbage truck becomes a city inspector … files its own tickets with photo proof" — FACT, [repo](https://github.com/Divyanshu-kumar14/CivicLens)
  - "CivicTrack — … Citizen Complaint Tracking Platform" — FACT, [repo](https://github.com/peddireddyleela2006-ui/CivicTrack)
  - HawaCommand "econometrically verifies the efficacy of every intervention" (Air, anti-smog machines) — FACT, [repo](https://github.com/shankywho/HawaCommand)
  - No visible entry re-checks closed complaints over multiple intervals (INFERENCE; partial search).
- **Prior art for the term:** a search for "half-life" with civic complaint recurrence or survival analysis found only generic survival tutorials (time-to-disposition of building complaints, not durability of a fix) — FACT, [tidymodels case study](https://www.tidymodels.org/learn/statistics/survival-case-study/)

### Inferences
- **ReCheck measures something new.** Existing systems record *time to closure* (SLA) or a single reporter check at 4 weeks. A multi-interval clean-survival curve per spot or ward is not produced by FixMyStreet, Swachhata, TrashOut or ICMyC as far as these sources show. The metric is a functional addition, not a re-skin.
- **The ICMyC back-test must be relabelled.** It is "repeat complaints at the same spot". The median 39-day gap and the ~300 multi-week repeats show recurrence is common in real data, but it measures neither closure-to-reappearance time nor a true half-life. The 2019→2022 volume decline shows ICMyC itself faded.
- **Bengaluru's black-spot portal is a candidate live data source** (counts per day) but was not inspected (HYPOTHESIS that it exposes spot-level data).

### Gaps
- Whether Swachhata/MoHUA or ULB portals publish closure timestamps or reopen counts (not found).
- The Bengaluru "garbage monitoring portal" URL and its openness.
- Whether Bedrock vision can reliably judge "same place, garbage present" across angles and lighting was not tested.
- No evidence that a public durability metric changes municipal behaviour (HYPOTHESIS).

---

## C. Window/Ventilation Planner: evidence, existing apps, verifiability

### Takeaway
- **The premise checks out on tonight's Delhi forecast.** The coolest hours (02:00–06:00, ~22 °C) carry the highest modelled PM2.5, and the hottest afternoon hours the lowest (r = −0.45 over 72 h).
- **The benefit side for Indian homes is weak or contradictory.** One Delhi winter study found window state did not substantially change indoor PM. A Delhi field trial found indoor PM far above outdoor monitors in winter, implying indoor sources.
- **Close analogues already exist:**
  - consumer "when to open windows" apps, including one combining temperature and AQI;
  - an academic "natural-ventilation hours" model for Delhi and Bengaluru;
  - two in-event projects (Khidki, better_AQI).
- **No benefit can be verified without an indoor sensor.**

### Cited Findings
- **Live forecast, Delhi (28.61, 77.21), from Fri 22:00 IST:**
  - Temperature / CAMS PM2.5: 22:00 24.4 °C / 62; 02:00 23.0 / 69; 06:00 22.2 / 62; 10:00 28.1 / 53; 14:00 32.2 / 59; 18:00 29.4 / 63; Sat 22:00 25.9 / 62 µg/m³.
  - Pearson r(temperature, PM2.5) over 72 h = **−0.45**.
  - FACT, live calls to `api.open-meteo.com/v1/forecast` and `air-quality-api.open-meteo.com` (keyless).
- **Indoor response to windows in India:**
  - **Delhi, peak winter, 1 site, 10 days:** opening or closing windows did not substantially change indoor PM2.5 or PM10 — FACT, [Singh, Mondal & Dewan 2022 (Chitkara JTMGE)](https://tmg.chitkara.edu.in/paper-html.php?pId=2457)
  - **IIT Bombay controlled room tests:** PM2.5 *exfiltration* factor 22% with door and window closed, 26% with the window open, 27% with both open ("slight" change) — FACT, [Chimurkar & Phuleria, EGU23-170](https://meetingorganizer.copernicus.org/EGU23/EGU23-170.html)
  - **Literature:** I/O was higher with windows open in two studies and the opposite in one; "no uniform conclusion"; infiltration factor 0.3–0.82 — FACT, [Chen & Zhao 2011](https://air.tongji.edu.cn/__local/3/C9/9C/4711FB5EE11CB782EEDD165D79A_7292F630_AB313.pdf)
  - **Delhi winter homes:** indoor PM2.5 exceeds government monitors by +114 to +122 µg/m³. High-SES households given information opened doors and windows more, with an associated 8.6% PM2.5 decline (authors: possible, not proven) — FACT, [EPIC](https://epic.uchicago.edu/wp-content/uploads/sites/5/2025/06/IAQ-Research-Highlight.pdf)
- **Academic analogue (Nihar et al. 2023, New Delhi and Bangalore):**
  - Models hours when natural ventilation is feasible from outdoor temperature and PM2.5.
  - Delhi winter outdoor PM2.5 above 250 µg/m³ "sharply reduced natural ventilation feasibility even though winter temperatures were favorable"; in summer, heat was the main constraint.
  - Bangalore's largest drop came in October (Diwali). The study did not model when occupants open windows.
  - FACT, [ERIS 3 025002](https://doi.org/10.1088/2634-4505/acc88f)
- **Classroom evidence (cited secondarily):**
  - Rawat et al. 2025 (Surrey): visual CO₂ alarms cut classroom CO₂ by 19.5% — FACT, [Earth Notes bibliography](https://www.earth.org.uk/bibliography/rawat2025acoustic.html); DOI 10.1016/j.scitotenv.2025.179543.
  - The claims that PM *rose* with window opening and that teachers' decisions were "driven mainly by classroom temperature" come from the Khidki spec's summary. The abstract was robots-blocked, so these are FACT only as reported by [Khidki SPEC.md](https://github.com/bhavya-jpg/khidki/blob/main/docs/SPEC.md).
- **Consumer apps (2026):**
  - **"Open Your Windows"** (iOS): "one simple answer: is right now a good time to open the windows?" A rule engine over temperature, **air quality (AQI)**, humidity, dew point, pollen, gusts and rain, with a "short-term outlook"; 11 ratings — FACT, [App Store](https://apps.apple.com/app/id6762444284)
  - **Aerzeit:** looks 48 h ahead for stretches within the user's temperature range, with optional humidity and **air-quality** filters, min/max opening durations, and open/close alerts; first released Jul 2026 — FACT, [listing](https://mwm.ai/apps/aerzeit-when-to-open-windows/6787749300)
  - **OpenAir:** temperature, dew point, rain and wind only; "does not measure … air quality" — FACT, [listing](https://mwm.ai/apps/openair-window-weather/6777466080)
- **In-event:**
  - **Khidki** (Air): classroom digital twin plus optimiser trading PM2.5 against CO₂, with a cold-exposure penalty.
    - PM penetration factors: closed 0.8, cracked 0.95, open 1.0; deposition 0.2 h⁻¹.
    - IoT sensor tiers, simulated if absent; Step Functions; a Pareto benchmark against 5 policies on CAMS 2025.
    - FACT, [SPEC.md](https://github.com/bhavya-jpg/khidki/blob/main/docs/SPEC.md)
  - **better_AQI:** an "optimal mid-day ventilation window" and a purifier countdown with window leakage classes — FACT, [repo](https://github.com/akshayaparida/better_AQI)

### Inferences
- **The joint quantity is the only differentiator:** "cooling degree-hours gained vs µg PM let in", optimised over 24 h for a *non-AC home*. The idea (combine temperature and air quality to time window opening) is already shipped (Open Your Windows, Aerzeit), modelled academically (Nihar 2023) and built in this event for classrooms (Khidki). It is a **re-presentation with a better objective function**, not a new capability.
- **The PM side of the trade-off may be near zero in leaky Indian homes** (Singh 2022; IIT Bombay "slight" change), while indoor sources dominate in winter (EPIC). If so, the plan is mostly a temperature plan. A skeptical judge can raise this, and the team cannot rebut it without a sensor.
- **The seasonal window is short in Delhi.** Nights of ~22 °C now and cooler through November make cooling demand vanish when smog peaks. The concept is most relevant in Mar–May and Oct, outside peak smog (INFERENCE, consistent with Nihar 2023).
- **Tonight's CAMS diurnal swing is small (53–69 µg/m³)** against the 4.5× station swing seen on 5 Oct. A plan built on CAMS will understate the PM penalty of night opening.

### Gaps
- No Indian measurement of residential infiltration factor with windows open vs closed across multiple homes was found.
- No validated single-zone thermal time constants for Indian RCC homes were collected.
- No consumer app was found that schedules windows for Indian cities using CPCB-indexed PM. Absence is not proven.

---

## Verdict for the coordinator

### A. Dose Ledger

**(i) Capability table (main journey)**

| Step | Status | Evidence |
|---|---|---|
| Import a real week of trips from Google Timeline JSON | PLAUSIBLE-UNTESTED | Export path and JSON fields documented (Android Authority; Dawarich). **Timeline is off by default** (Google Help), so it works only for a teammate who had opted in. No file inspected |
| Fallback: manual routine entry or 2-day PWA GPS log | PLAUSIBLE-UNTESTED (low risk) | No external dependency |
| Confirm mode per segment (auto, metro, bus …) | VERIFIED-BUT-CONSTRAINED | Activity enum has IN_SUBWAY, IN_BUS, MOTORCYCLING, IN_PASSENGER_VEHICLE but no auto-rickshaw; bus/car confusion documented |
| Hourly ambient PM2.5 for each trip-hour (keyless) | VERIFIED-BUT-CONSTRAINED | CAMS via Open-Meteo, live: one 0.4° value for all Delhi points; 5 Oct mean 96.6 vs stations 50–62 (+55–95%); hourly r = 0.52–0.87 |
| Station PM2.5 for the same week | VERIFIED-BUT-CONSTRAINED | OpenAQ S3, live: newest file 5 Oct (~4.5-day lag). OpenAQ API (free key; 60/min, 2,000/h): Explorer shows Delhi CPCB/DPCC "Updated 2 days ago" |
| Google AQ (500 m, 30-day hourly history, PM2.5 µg/m³) | PLAUSIBLE-UNTESTED | Docs only; billing account required; 10,000 free events/month |
| Apply cited mode, microenvironment and inhalation factors | VERIFIED-BUT-CONSTRAINED | Goel 2015, Apte 2011, Maji 2021, IIT Roorkee 2023 give values, but they conflict (metro 0.8× vs ≈1.4× AC car); the indoor factor is the most uncertain (EPIC indoor ≫ monitor) |
| Weekly ledger and attribution by activity | PLAUSIBLE-UNTESTED (arithmetic) | Low build risk; accuracy bounded by the two rows above |
| Rank swaps by dose avoided per minute (time, mode, indoor) | VERIFIED-BUT-CONSTRAINED | Time swaps rest on the CAMS diurnal shape; mode swaps on factors; **route swaps UNSUPPORTED** because CAMS gives one value city-wide. Travel times: OSRM keyless (earlier notes); Amazon Location PLAUSIBLE-UNTESTED |
| Next week's data checks the change | UNSUPPORTED within the hackathon | Needs ≥7 days; the "check" is a modelled dose from logged behaviour, not a measurement |

**(ii) Minimum working demonstration (no outsiders, no hardware, no privileged data)**
1. A teammate's own Timeline JSON if they have one. Otherwise a 2-day PWA GPS log (Sat–Sun) plus a typed weekday routine, labelled.
2. S3 upload → Step Functions: parse → enrich with CAMS hourly (plus OpenAQ S3 station values for days ≤ 5 Oct, shown as a "measured vs model" strip) → dose with low/central/high factors → DynamoDB.
3. A ledger screen: share of week's µg by home, office, each commute leg.
4. Top three swaps on one axis (µg avoided per extra minute) with bands. Only swaps whose band excludes zero are shown.
5. A "next week" card as a **labelled replay**: re-run the ledger on the same routine with the committed swap applied. Optionally a real Sat-vs-Sun A/B, honestly labelled n = 1.
6. Bedrock writes the plain-language explanation only.

**(iii) Strongest skeptical objection, and whether it is answerable**
- **Objection:** "ALive, EcoRoute and Breathe Route already price trips and suggest leaving later. Your ambient is a 45 km model biased ~1.6–1.9× high on 5 Oct; your mode factors disagree across studies; your verification is a model of a model."
- **Partly answerable:**
  - Show the week-level, indoor-inclusive attribution, which no in-event README describes.
  - Show the robustness filter (rank only swaps that survive factor ranges).
  - Show the station-vs-CAMS strip as an honest calibration.
- **Not answerable:** "did the dose actually fall?" No sensor exists, so that cannot be measured.

**(iv) Functional improvement or re-presentation?**
- **Mostly re-presentation, with one functional increment.** Per-trip dose, mode comparison and departure-time advice exist in ≥6 event projects (ALive, EcoRoute AI, Breathe Route, better_AQI, AirTrace, RideClean). Dose-by-microenvironment from time-activity exists in TracMyAir (US, research) and PRAISE-HK (HK).
- **The increment:** a retrospective week from the user's *own* location history, including indoor hours, with cross-type swaps ranked per minute of inconvenience. No source found does exactly this (INFERENCE, non-exhaustive).
- **Data fit for India:** adequate for *relative* time and mode levers, inadequate for route levers or absolute µg.

### B. ReCheck

**(i) Capability table**

| Step | Status | Evidence |
|---|---|---|
| Register a spot (GPS ±15 m + reference photo) in a PWA | PLAUSIBLE-UNTESTED (low risk) | Standard browser geolocation and camera; not tested here |
| Mark "resolved" (by authority, or team-declared in the demo) | PLAUSIBLE-UNTESTED (trivial) | User-declared flag; no authority needed |
| Schedule re-checks at +6 h / +24 h / +72 h / +7 d / +30 d | PLAUSIBLE-UNTESTED | EventBridge Scheduler one-time schedules (AWS docs, earlier notes); not called |
| Notify the watcher | VERIFIED-BUT-CONSTRAINED | No SMS without DLT (earlier notes); use SES sandbox, web push or Telegram |
| Vision judgement: same place? garbage present? | PLAUSIBLE-UNTESTED | Bedrock multimodal is plausible; angle and lighting variance untested |
| Clean-survival curve and half-life per spot/ward | VERIFIED-BUT-CONSTRAINED | Kaplan–Meier is standard. Demo n of 3–5 spots over ≤36 h gives no meaningful half-life |
| Historical back-test on public data | VERIFIED-BUT-CONSTRAINED | ICMyC: 16,071 Bengaluru complaints with lat/lon, category and final status (332 Re-opened), but **no closure timestamps**. Only a repeat-complaint proxy is possible (366 repeat spots; median gap 39 d among 588 gaps; geocode-default contamination) |
| Ward scorecard and "structural GVP" flag | PLAUSIBLE-UNTESTED | Rules over the above |

**(ii) Minimum working demonstration**
1. Fri night: the team registers 3–5 litter spots on or near campus (reference photo plus GPS).
2. Sat morning: each spot is cleaned by the team or by scheduled housekeeping. "Resolved" is clearly marked "team-declared".
3. EventBridge prompts a teammate at +6, +12, +24 and +36 h. Re-photos are judged by Bedrock vision and stored in S3/DynamoDB.
4. One real curve from those spots: "2 of 5 reverted within 24 h", stated as counts, not a half-life.
5. A second panel uses ICMyC repeat-complaint intervals, labelled "proxy: repeat complaints at the same spot, Bengaluru 2019–22".
6. A third panel uses a compressed-time simulated cohort to show what a ward half-life would look like, labelled "simulated".

**(iii) Strongest skeptical objection, and whether it is answerable**
- **Objection:** "Who will re-photograph a dump at day 7 and day 30? FixMyStreet already re-asks at 4 weeks. Your back-test has no closure timestamps, and your live curve is 5 spots over 36 hours."
- **Answerable in part:**
  - Show the low-effort 10-second re-check by any passer-by or the original reporter, versus FixMyStreet's single reporter questionnaire.
  - Admit the proxy openly.
- **Not answerable:** volunteer fatigue and adoption. No evidence either way; HYPOTHESIS.

**(iv) Functional improvement or re-presentation?**
- **Genuine functional improvement on the metric.** Closure SLAs and one-shot reopen or questionnaire flows exist (Swachhata reopen, FixMyStreet 4-week survey, TrashOut "check if cleaned"). No source found computes multi-interval durability or a "resolution half-life". Recurrence is well documented (Bengaluru 5,445 active black spots in Jun 2026, up from ~3,200 a month earlier; Mapusa; Hyderabad).
- **Weaknesses:** the evidence it can *show* in 46 hours is thin, and the track is Waste & Energy with a civic-app-heavy field.

### C. Window/Ventilation Planner

**(i) Capability table**

| Step | Status | Evidence |
|---|---|---|
| Hourly temperature forecast | VERIFIED | Open-Meteo forecast, keyless, live tonight (Delhi 22.2–32.2 °C over the next 24 h) |
| Hourly outdoor PM2.5 forecast | VERIFIED-BUT-CONSTRAINED | CAMS ~4.5 days usable; 0.4° cell; tonight's diurnal swing 53–69 vs station 27–121 on 5 Oct |
| Indoor temperature response to windows open/closed | PLAUSIBLE-UNTESTED | Needs building time constants; no Indian calibration found |
| Indoor PM2.5 response to windows open/closed (Indian homes) | UNSUPPORTED (as a quantified claim) | Delhi study: no substantial change; IIT Bombay: "slight"; review: inconsistent; EPIC: indoor ≫ outdoor in winter |
| 24 h optimiser (cooling degree-hours vs PM dose) | PLAUSIBLE-UNTESTED (trivial DP) | — |
| Verify the plan helped, without an indoor sensor | UNSUPPORTED | No consumer-device proxy for indoor PM; only subjective comfort feedback |

**(ii) Minimum working demonstration**
1. Pick a city → tonight's Open-Meteo temperature and CAMS PM2.5.
2. A 24 h open/closed plan with price tags, e.g. "Open 14:00–17:00 instead of 02:00–06:00: 1.1 °C less cooling, ~X% less PM let in". All indoor numbers are labelled "model, assumed infiltration 0.6–1.0".
3. An asthma toggle that re-weights the plan.
4. Lambda optimiser, EventBridge Scheduler reminders, DynamoDB.

**(iii) Strongest skeptical objection, and whether it is answerable**
- **Objection:** "'Open Your Windows' and Aerzeit already time windows on temperature plus air quality, and Khidki does this with sensors in this very track. Leaky Indian homes barely change indoor PM when you close the window, and you can't measure anything."
- **Not answerable within the constraints.** The objection is backed by the Delhi window study and the IIT Bombay result.

**(iv) Functional improvement or re-presentation?**
- **Re-presentation.** The quantified trade-off objective is a modest refinement of shipped consumer apps, an academic model (Nihar 2023) and two in-event builds (Khidki, better_AQI). Its benefit for Indian homes is unproven and unverifiable without hardware.
- **Recommendation (INFERENCE):** use it, if at all, as a secondary card inside A ("tonight: keep the bedroom closed 01:00–06:00").

### Cross-concept ranking (INFERENCE)
1. **B ReCheck** has the clearest *functional* novelty and an honest, outsider-free demo. Its risks are thin live evidence and a civic-app-crowded perception.
2. **A Dose Ledger** has the strongest data and science backing for relative levers. Its risks are heavy in-event overlap (ALive and others), an unverifiable outcome, and the Timeline opt-in.
3. **C** is not recommended as a standalone entry.
