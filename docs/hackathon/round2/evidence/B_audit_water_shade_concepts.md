# Monsoon Replay (A) and ShadeSite (B): competition, data feasibility and a 40-hour build check (verified Fri 9 Oct 2026, ~21:50–23:30 IST)

Labels: **FACT** = sourced or observed in a live call made in this session; **INFERENCE** = reasoning from facts; **HYPOTHESIS** = untested claim. Live calls were made from the Claude desktop browser pane with keyless public endpoints only (Open-Meteo archive API; Overture S3 bucket and STAC; Meta/WRI CHMv2 S3 bucket; Overpass). Nothing was downloaded to disk; no sign-in.

Earlier work this builds on: C-06 ShadeSite and C-08 Monsoon Replay in `../Environmental Hacks concept reset/concepts_community_institutional.md`; M-08 Rain Ledger (dropped because of SimTanka) in `concepts_mechanism_first.md`; `data_access.md` (Open-Meteo verified for Delhi); `live_competition.md` (111 visible projects).

---

## A1. Does Open-Meteo's archive give usable daily monsoon rainfall for Indian cities, and how far is it from IMD?

### Takeaway
Daily rainfall is available keylessly up to yesterday (2026-10-08) for Bengaluru, Chennai and Pune. It is fine for "how much fell this season" storytelling, but **it is a model, not a gauge**. Monthly and seasonal totals were 12–48% off IMD figures in the four cases checked (in both directions). Totals for the same season differ by up to 53% depending on which model is chosen. Worst of all, **it misses the cloudburst days that drive tank overflow, which is the core of Monsoon Replay**: Bengaluru's record ~111 mm day (2 Jun 2024) shows up as 10–28 mm.

### Cited Findings
**Live API calls (FACT, 9 Oct 2026 ~21:50 IST)**
- **Endpoint:** `https://archive-api.open-meteo.com/v1/archive?latitude=…&longitude=…&start_date=2024-01-01&end_date=2026-10-08&daily=precipitation_sum&timezone=Asia/Kolkata&models=<m>`. HTTP 200, no key.
- **Freshness:** `best_match` returned non-null values through **2026-10-08**. `era5` ended at **2026-10-03** (5-day lag).
- **ERA5-Land:** `era5_land` returned **all-null precipitation** for all three cities, so it is unusable for rain.
- **Best match is IFS:** for 2024 in Bengaluru, `best_match` was identical to `ecmwf_ifs` (same JJAS total and same daily values for 1–5 June). It is therefore the ECMWF IFS 9 km model. Docs say Best Match combines IFS HRES, ERA5 and ERA5-Land — [Open-Meteo historical docs](https://open-meteo.com/en/docs/historical-weather-api) (FACT, via data_access.md).
- **Grid points returned:**
  - Bengaluru: best_match 12.97, 77.56; ERA5 13.0, 77.5.
  - Chennai: 13.11, 80.25 and 13.0, 80.25.
  - Pune: 18.52, 73.87 and 18.5, 73.75.

**Seasonal totals from Open-Meteo, mm (FACT, live)**

| City | Model | JJAS 2024 | JJAS 2025 | JJAS 2026 | OND 2024 | OND 2025 | Max day 2024 |
|---|---|---|---|---|---|---|---|
| Bengaluru | best_match (IFS) | 559 | 578 | 485 | 363 | 230 | 35.0 |
| Bengaluru | ERA5 | 661 | 527 | 319 | 354 | 205 | 49.5 |
| Chennai | best_match | 512 | 581 | 378 | 847 | 965 | 158.4 (30 Nov) |
| Chennai | ERA5 | 398 | 286 | 192 | 727 | 552 | 148.8 |
| Pune | best_match | 1,246 | 914 | 706 | 125 | 94 | 74.5 |
| Pune | ERA5 | 1,401 | 1,269 | 1,146 | 109 | 131 | 87.6 |

- **Model spread, Bengaluru JJAS 2024, same location (FACT, live):** best_match/IFS 559 mm; ERA5 661; `ecmwf_ifs025` 697; `ecmwf_ifs_analysis_long_window` 853. The largest is 53% above the smallest.

**Comparison with IMD or observed figures (sources as cited; Open-Meteo values are FACT, live)**

| Case | Observed | Open-Meteo best_match | ERA5 | IFS 0.25° | Gap (best_match) |
|---|---|---|---|---|---|
| Bengaluru, 2 Jun 2024, single day | "around 111 mm" in one evening; 140.7 mm over two days — [Business Standard](https://www.business-standard.com/india-news/bengaluru-rains-break-133-yr-old-record-city-registers-wettest-june-day-124060300279_1.html) | 1 Jun 28.0, 2 Jun 10.3, 3 Jun 0.6 | 9.5 / 5.9 / 5.5 | — | ~4× under on the peak day; 2-day sum ≤38 mm vs 140.7 mm |
| Bengaluru, May 2025 month | 307.9 mm to 26 May (wettest May on record; normal 128.7 mm) — [Deccan Herald](https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fbengaluru%2Fbengaluru-breaks-record-for-wettest-may-in-history-3557572) | 159 (whole month) | 203 | 122 | −48% |
| Pune Shivajinagar, June 2024 | 252 mm, "wettest June in a decade", per IMD as reported by a weather blog — [Vagaries](https://www.vagaries.in/2024/06/pune-recorded-wettest-june-in-decade.html) (secondary) | 203 | 222 | 217 | −19% |
| Chennai district, OND 2025 | 724.8 mm actual vs 809.6 mm normal (−10%) — [IMD Chennai NE monsoon 2025](https://mausam.imd.gov.in/chennai/mcdata/ne_monsoon_2025.pdf) | 965 | 552 | 926 | +33% (ERA5 −24%) |

- IMD Chennai's heaviest daily falls in OND 2025 were 21–26 cm at north-Chennai stations on 2 Dec 2025 (Ennore 26 cm, Parrys 25 cm) — [IMD Chennai NE monsoon 2025](https://mausam.imd.gov.in/chennai/mcdata/ne_monsoon_2025.pdf). Open-Meteo's Chennai max for that date was 142.3 mm (FACT, live). Its grid point is central Chennai, so this is not a like-for-like station comparison.
- **Illustrative replay (FACT that the computation ran; INFERENCE as to meaning).** Assumptions: 1,000 m² roof, runoff coefficient 0.8, 5 kL/day non-potable demand, calendar 2024 daily rain, no first-flush loss. It was run in-browser on the live Open-Meteo series.
  - **Bengaluru (best_match, 1,081 mm):** 865 kL of roof runoff. A 5 kL tank uses 61%, 10 kL 73%, 20 kL 83%, 50 kL 96%, 100 kL 100%.
  - **Bengaluru (ERA5, 1,216 mm):** a 10 kL tank uses 69%; 50 kL uses 90%.
  - **Chennai (best_match, 1,611 mm):** 1,288 kL of runoff. A 5 kL tank uses 43%, 10 kL 52%, 20 kL 60%, 50 kL 74%, 100 kL 80%.
  - An annual × area × coefficient calculator implicitly reports 100% for every tank size.

### Inferences
- **Inherited optimism (INFERENCE).** The daily replay changes the sizing answer a lot in bursty climates: in Chennai a 10 kL tank captures about half of what the annual formula implies. But the reanalysis underestimates exactly those burst days, so Monsoon Replay on Open-Meteo will **overstate** small-tank capture. It inherits optimism, just less than an annual formula has.
- **Choose a model and say why (INFERENCE).** Model choice moves totals by tens of percent, so the app must name its model and show a band. A min–max across best_match, ERA5 and IFS 0.25° is cheap: three calls.
- **Bias-correct at the monthly level (INFERENCE).** Scale each month's daily series to IMD monthly station totals where the team can cite them (e.g., Bengaluru May 2025 = 307.9 mm). This fixes volume but not burst shape.
- **Prefer a gauge where available (INFERENCE).** The only real fix for bursts is a gauge series: IMD 0.25° gridded rainfall (station-based), KSNDMC hobli gauges, or a user-uploaded CSV. None was verified keyless in this session.
- **Do not demo Pune's 2024 replay (INFERENCE).** Pune JJAS 2024 at 1,246–1,401 mm on the grid looks implausible for rain-shadow Shivajinagar (a June figure of 252 mm extrapolates far lower). The coarse grid is picking up Western Ghats rain. Pune is a bad demo city on reanalysis; Bengaluru or Chennai are safer.

### Gaps
- No IMD seasonal JJAS total for Bengaluru city 2024/2025 was found to compare directly; IMD gridded rainfall (`imdlib`/`imdR`) availability for 2024–2026 and keyless access were not verified (download not attempted).
- Observed Chennai rainfall for Cyclone Michaung (4 Dec 2023) not retrieved; Open-Meteo shows 255.8 mm best_match / 208.4 mm ERA5 (FACT, live) but there's no comparison.
- KSNDMC (Karnataka) telemetric rain-gauge data access not checked.

---

## A2. Overture buildings: Indian footprint density and keyless query path

### Takeaway
**Verified dense and keyless.** A live DuckDB-WASM query against Overture's public S3 parquet returned about 950–2,600 buildings per ~1.2 km² box in Bengaluru, Pune, Chennai and Delhi, with roof areas computed. **Heights are essentially absent**: 0 to 6 per box carry `height`. Footprints are therefore solid for Monsoon Replay but not enough on their own for ShadeSite.

### Cited Findings
- **Bucket and release (FACT, live listing of `https://overturemaps-us-west-2.s3.amazonaws.com/?list-type=2&prefix=release/`):**
  - Latest release is `2026-09-23.1`.
  - `theme=buildings/type=building/` holds **512 parquet files, 276.9 GB**.
  - The Registry gives bucket `arn:aws:s3:::overturemaps-us-west-2/release/`, us-west-2, no AWS account needed, monthly updates, CDLA-Permissive-2.0 (ODbL for OSM-derived data), and lists **Amazon Athena** under Tutorials — [AWS Registry: Overture](https://registry.opendata.aws/overture/).
- **Locating files with STAC (FACT, live):** `https://stac.overturemaps.org/2026-09-23.1/buildings/building/collection.json` lists a bbox per file, and each item JSON gives AWS and Azure hrefs plus row counts.
  - Bengaluru falls in `part-00282` (bbox 76.76–78.52 E, 12.13–13.37 N; 4,921,260 rows; 128 row groups).
  - Pune falls in `part-00292`, Chennai in `part-00287`, Delhi north-west in `part-00398`.
  - **So a bbox query needs to touch only one ~500 MB file.**
- **CORS (FACT, live):** the regional endpoint `overturemaps-us-west-2.s3.us-west-2.amazonaws.com` returned 206 to a cross-origin range request. The path-style global endpoint did not.

**Live DuckDB-WASM 1.29.0 queries on 0.01° × 0.01° boxes, ~1.2 km² (FACT, live, release 2026-09-23.1)**

| Box | Buildings | With `height` | With `num_floors` | Primary source mix | Footprint area |
|---|---|---|---|---|---|
| Bengaluru, Koramangala (77.620–77.630, 12.930–12.940) | **2,588** | **0** | 22 | OSM 2,370 · Google Open Buildings 164 · Microsoft 54 | **418,842 m²** total; median 119 m² |
| Pune, Kothrud (73.805–73.815, 18.500–18.510) | 2,043 | 6 | 17 | OSM 1,051 · Google 785 · MS 207 | — |
| Chennai, Anna Nagar (80.205–80.215, 13.080–13.090) | 2,088 | 0 | 0 | OSM 1,573 · Google 273 · MS 242 | — |
| Delhi, DTU area (77.110–77.120, 28.745–28.755) | 953 | 0 | 9 | Google 555 · OSM 240 · MS 158 | — |

- **Query times in the browser (FACT, live):**
  - First query on a file: over 45 s, mostly reading the footer and row-group statistics over residential broadband.
  - Repeat query on the same file: **0.58 s**.
  - Three-city run: 33 s.
  - Footprint-centroid extraction with the spatial extension: 58 s.
- **Docs (FACT):** OSM has the highest conflation priority. ML-derived roofprints (Microsoft, Google Open Buildings) fill gaps and have lower precision, "most pronounced in the Global South". Heights are merged between matches with IoU > 0.5. The theme counts "2.5 billion buildings and counting" — [Overture buildings guide](https://docs.overturemaps.org/guides/buildings). Overture added Google Open Buildings in Dec 2023 — [Overture blog](https://overturemaps.org/blog/2023/overture-buildings-theme-hits-2-3b-buildings-with-addition-of-google-open-buildings-data/).

### Inferences
- **Footprint coverage is no longer the risk for Monsoon Replay (INFERENCE).** The remaining risks:
  - Deciding which buildings belong to a "society". The user should draw or confirm a polygon.
  - Roof area vs. collectable area: terraces, solar panels, water tanks and paved areas.
- **Athena (INFERENCE).** An Athena `CREATE EXTERNAL TABLE` over the release path, with a bbox predicate, is the AWS-visible version of the same query. The Registry points to Athena tutorials. It was **not executed** here (no AWS credentials in this session).

### Gaps
- Athena query cost and latency were not measured.
- OSM landuse=residential and gated-complex boundaries (for auto-selecting a society) were not checked.
- Google Open Buildings v3 and Microsoft footprints were not queried directly; they are already inside Overture.

---

## A3. Competitors for RWH sizing: what exists and what it misses

### Takeaway
The "replay real past rainfall through a tank" idea is **not new**.
- **SimTanka** (free, open source, Indian) already runs a daily water balance on the last five years of real daily rain and reports reliability against tank size.
- A **Jal Shakti Hackathon-2025 winner** (JNTU Hyderabad) already does "pick your roof on a satellite map → 30 years of rain → tank size".
- Annual-average calculators are everywhere.

What nobody visibly combines is:
- multi-building aggregation from open footprints;
- tank *plus* recharge-pit overflow routing;
- tanker-equivalent ₹ at a cited local rate;
- an uncertainty band;
- a committee-ready decision pack.

### Cited Findings
- **SimTanka (FACT):**
  - Runs a daily water balance for a covered tank: inflow capped at tank volume, demand subtracted, level floored at zero.
  - Reports historical reliability over the past 5 years and a 30-day probability of meeting demand.
  - Inputs: catchment area, runoff coefficient, tank volume, a daily demand array and the current level.
  - Rain comes from Visual Crossing (2018–2022 examples).
  - Calls itself "free and open-source" (simtanka.org). Its author describes the 5-year window as ad hoc.
  - The paper does not mention multiple roofs, recharge pits or cost/tanker outputs.
  - Source: Vikram Vyas, 16 Apr 2024 — [arXiv 2404.13080](https://arxiv.org/html/2404.13080v1). An iOS listing exists — [App Store](https://apps.apple.com/ke/app/simtanka/id6446281690).
- **Jal Shakti Hackathon-2025 winner, "Hydro Harvesting AI" (FACT):**
  - Built by Shivakumar Induri, 3rd-year GeoInformatics student at JNTU Hyderabad, who won ₹1 lakh from the Jal Shakti Minister on World Water Day 2026.
  - The user selects the roof on a satellite map to get its area; the app analyses 30 years of rainfall "through AI" and recommends tank size and pipe diameter.
  - It was being developed for submission to Jal Shakti by 30 Apr 2026; public availability was not indicated — [ETV Bharat, 24 Mar 2026](https://www.etvbharat.com/en/technology/rainwater-harvesting-system-with-a-jntu-student-develops-hydro-harvesting-ai-enn26032405752).
- **Studio Matrx calculators (FACT):**
  - A Sept 2026 "rainwater tank sizer" for 10 Indian cities.
  - Annual rainfall × area × coefficient × filter efficiency minus first flush; the monthly profile is a shaped estimate.
  - Rain figures are "IMD long-term averages".
  - No overflow computation, no reliability metric, no tanker equivalents. It does do payback.
  - It is internally inconsistent on the BWSSB plot threshold — [Studio Matrx tank sizer](https://www.studiomatrx.org/utilities/rainwater-tank-sizer).
- **KSCST "RWH Advisor" app (FACT):** by KSCST with UNESCO support (2016). Gives tank size, installation cost and nearby experts; also on the web. Its method is not described — [Deccan Herald, 22 Mar 2016](https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fbengaluru%2Fapp-answers-all-rwh-queries-2056026).
- **BWSSB (FACT):** has issued capacity guidelines for RWH structures, but there is "no penalty for not meeting them". No BWSSB calculator was described — [Citizen Matters, Dec 2023](https://citizenmatters.in/bengaluru-rainwater-harvesting-bwssb-kscst-water/).
- **Student and other repos (FACT, live GitHub API search `rainwater created:>=2026-09-20`):** **54 repositories** matched. Examples:
  - "Rooftop Rainwater Harvesting Artificial Recharge On-Spot Assessment Web Application" (7 Oct 2026; "instant, customized recommendations for tank sizes and cost estimates").
  - `rainwater-harvesting-calculator` (6 Oct).
  - `RainReady – Rainwater Harvesting Planner` (28 Sep).
  - `Rainwater-Harvesting-Optimizer` (24 Sep).
  - `rainwise-ai` (6 Oct).
  - `JALNETRA-AI` (GeoImpathon 1.0, NASA POWER rain, Google Cloud Run, explicitly no tank sizing) — [repo](https://github.com/Janicebenita/JALNETRA-AI).
  - `HydroLens` ("365-day storage simulation" with overflow, but **synthetic** rainfall and manually drawn roofs; Gemini on Render, no AWS; labelled "PS 53") — [repo](https://github.com/Rithvik-7/HydroLens).
  - Event affiliation of most of these is unknown.
- **Earlier notes (FACT, via `concepts_mechanism_first.md`):** M-08 Rain Ledger was dropped because SimTanka productises the reliability curve.

### Inferences
- **Against annual-average tools (Studio Matrx, KSCST, most student calculators) — INFERENCE:** a daily replay is a **genuine functional improvement**. The A1 replay shows a 10 kL tank capturing 52–73% of runoff, not 100%.
- **Against SimTanka and the Jal Shakti winner — INFERENCE:** the replay itself is **re-presentation**. The defensible increments are:
  1. **Multi-roof aggregation.** All of a society's buildings come from Overture via Athena, with no roof drawing.
  2. **Recharge-pit routing of overflow,** with a user-set infiltration rate.
  3. **Tanker-equivalent ₹ and a cost split.**
  4. **An honest uncertainty band** across models plus an IMD-month bias correction.
  5. **A decision pack** a committee can vote on.

  None of these is individually novel. The combination for a multi-building society appears unclaimed among the sources seen (INFERENCE from absence).
- **Competition (INFERENCE):** RWH calculators are a heavily trodden student genre right now (54 new repos in 3 weeks), so a judge will have seen several. The novelty margin is thin.

### Gaps
- Whether SimTanka's app supports multiple catchments or recharge (the paper is silent; the app was not inspected).
- Whether the Jal Shakti winner app is public.
- The CGWB/India-WRIS RWH calculator and the Catch the Rain portal tools were not found or inspected. A PIB document on Catch the Rain 2026 exists — [PIB, Jul 2026](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jul/doc2026719925701.pdf) (not read).
- Vendor calculators (Rainwater Club, etc.) were not inspected.

---

## A4. Policy hooks: mandates and penalties (Bengaluru, Chennai, Delhi, Mumbai) and 2025–26 changes

### Takeaway
Mandates exist in all four cities, but enforcement checks **presence, not function**. Recent pressure is moving toward *functional* RWH: in July 2025 Delhi Jal Board withdrew rebates from 119 Dwarka societies with non-functional systems. That is the hook for a replay that shows what a system *would* catch. No 2025–26 rule change was found for Bengaluru, Chennai or Mumbai.

### Cited Findings
- **Bengaluru (FACT), [Citizen Matters, 7 Dec 2023](https://citizenmatters.in/bengaluru-rainwater-harvesting-bwssb-kscst-water/):**
  - **Who is covered:** the BWSSB Amendment Act 2011 covers 60×40 ft plots and above, and new properties on 30×40 ft sites.
  - **Penalties (2015 regulations):** residential, 25% of the water bill for the first 3 months, then 50%; non-residential, 50% then 100%.
  - **Who pays:** in October (2023), 39,703 defaulting properties paid ₹1.95 crore, an average of ₹491 each.
  - **Coverage:** 1.9 lakh of 10.8 lakh connections (~18%) have RWH.
  - **Enforcement:** BWSSB inspects at new connections from photos, and residents say it does not check function.
  - The Hindu (Mar 2024) reported 39,213 residential buildings fined monthly and that people "are ready to pay penalty, but not to implement RWH" — [PressReader / The Hindu](https://www.pressreader.com/india/the-hindu-bangalore-9WW1/20240321/281556590815663).
- **Bengaluru tanker rates (FACT):** district-administration fixed rates from 6 Mar 2024, including GST — [The News Minute](https://thenewsminute.com/amp/story/karnataka/bengaluru-district-administration-introduces-fixed-rates-for-water-tankers):

| Capacity | Within 5 km | 5–10 km |
|---|---|---|
| 6,000 L | ₹600 | ₹750 |
| 8,000 L | ₹700 | ₹850 |
| 12,000 L | ₹1,000 | ₹1,200 |

- **Delhi (FACT), [CSR Journal, 25 Jul 2025](https://thecsrjournal.in/djb-informs-ngt-withdrawal-rebate-water-bills-societies-dwarka/):**
  - RWH has been mandatory since 2012. Non-compliance costs 1.5× the water bill; installed systems earn a 10% rebate.
  - On 22 Jul 2025, DJB told the NGT it had **withdrawn the 10% rebate from 119 Dwarka societies** whose RWH was "not found to be functional". It also issued disconnection notices and sought environmental compensation.
  - Test results: 19 societies had fecal coliform in RWH pits; 9 pits were dry.
  - Separately, a headline reports the Delhi government suggested environmental compensation of up to ₹5 lakh for properties without functional RWH — [Outlook](https://www.outlookindia.com/national/delhi-govt-suggests-slapping-environmental-compensation-of-up-to-rs-5l-on-properties-without-functional-rainwater-harvesting-system-news-300610) (headline only, not read).
- **Chennai (FACT), [The News Minute, 2 Sep 2019](https://www.thenewsminute.com/amp/story/tamil-nadu/9000-houses-issued-notices-chennai-corp-install-rainwater-harvesting-systems-108206):**
  - Tamil Nadu made RWH mandatory in 2003. CMDA issues building NOCs only with RWH.
  - In 2019 the Corporation inspected 2.72 lakh houses: 1.62 lakh had RWH, about 38,000 needed repairs, about 70,000 lacked it, and 9,000 notices were issued with a 15-day deadline.
  - This is old data; no 2025–26 Chennai change was found.
- **Mumbai (FACT), [Citizen Matters, 17 Jul 2024](https://citizenmatters.in/mumbai-rainwater-harvesting-lags-behind/):**
  - RWH has been mandatory for new buildings since 2002, certified by a consultant for the Occupation Certificate (OC).
  - About 3,000 of an estimated 20,000 societies had RWH (2007–2021). Societies let systems lapse after the OC; storage covers about 2 days of flushing.
  - The promised property-tax rebate never appeared; no penalties were mentioned. The 300 m² plot threshold was not confirmed in the text.
- **Hyderabad (FACT, via C-08):** ~17,000 non-compliant buildings face penalties — [Realty Today](https://therealtytoday.com/news/over-17000-buildings-in-hyderabad-to-face-penalties-for-non-compliance-with-rainwater-harvesting-rules).

### Inferences
- **Recommended framing (INFERENCE):** "Is your pit *functional*, and would it have *caught* last monsoon?" The Delhi functional-RWH enforcement (2025) is the strongest recent hook. Bengaluru's 25–50% bill penalty gives a ₹ comparator: penalty paid vs tankers avoided.
- **Monsoon Replay is not a compliance certificate (INFERENCE).** It shows design capture, not whether a pit works, so the video must not imply verification of an existing pit.

### Gaps
- BWSSB's capacity norms (litres per m² of roof or paved area) were not fetched.
- No verified 2025–26 changes were found for Bengaluru, Chennai or Mumbai.
- The Delhi plot-size threshold was not found in the fetched source.

---

## A5. Is October a good time to pitch this, and is a replay convincing?

### Takeaway
**Timing is better than it looks.**
- The 2026 south-west monsoon was India's 4th-lowest since 2001, and a strong El Niño is present.
- For Chennai and Bengaluru the north-east monsoon (Oct–Dec), which IMD forecasts as "normal" for the South Peninsula, is just starting. For Chennai, OND is the main rain season.

**The weak points:**
- Maharashtra societies' AGMs had to be held by 30 Sept, so "AGM-ready" should become "committee or special-meeting ready".
- A replay is a model. Its credibility rests on visibly matching IMD season totals, which Open-Meteo does not reliably do.

### Cited Findings
- **2026 south-west monsoon (FACT):** 759.4 mm, 87% of LPA, 4th-lowest since 2001 and 13th-lowest since 1901. 17 of 36 subdivisions (42% of area) were deficient. Monthly: June 65%, July 101%, August 84%, September 92% of LPA — [The Bridge Chronicle, 1 Oct 2026](https://www.thebridgechronicle.com/news/nation/india-fourth-lowest-monsoon-rainfall-2026-october-forecast-agn97).
- **IMD outlook, 30 Sep 2026 (FACT), [IMD OND press release](https://mausam.imd.gov.in/Forecast/marquee_data/Press_Release%20OND_30-09-2026.pdf):**
  - OND 2026 for South Peninsular India: **normal, 88–112% of LPA** (LPA ≈ 334.1 mm).
  - October 2026, all-India: below normal (<85% of LPA).
  - "**Strong El Niño** is present … expected to strengthen"; IOD neutral.
- **Open-Meteo agrees 2026 was dry (FACT, live, best_match).** JJAS 2026 was below both 2024 and 2025 in all three cities: Bengaluru 485 vs 559/578 mm; Chennai 378 vs 512/581; Pune 706 vs 1,246/914.
- **Chennai's main season (FACT):** Chennai district's OND normal is 809.6 mm — [IMD Chennai](https://mausam.imd.gov.in/chennai/mcdata/ne_monsoon_2025.pdf).
- **Maharashtra AGM deadline (FACT):** housing societies must hold the AGM by 30 September (Section 75, Maharashtra Cooperative Societies Act). Missing it can disqualify office-bearers — [Punekar News, 16 Sep 2026](https://www.punekarnews.in/?p=244996).
- **Credibility evidence (FACT, from A1):** Open-Meteo vs IMD gaps of −48% to +33%; peak-day under-capture of about 4×.

### Inferences
- **Pitch line (INFERENCE):** "2026's monsoon failed and El Niño is building. Here is what your roofs sent down the drain this year and in 2024, and what a tank plus a pit would have saved before summer 2027's tanker season."
- **For Chennai, a forward-looking variant (INFERENCE):** "The NE monsoon starts now; size before December."
- **What a replay can claim (INFERENCE).** It is convincing only for statements of the form "rain that fell on these roofs (a model estimate, shown against IMD's season total)". It is not convincing as a forecast of savings. The result card should carry the IMD season total beside the model total.

### Gaps
- No evidence found on when Karnataka or Tamil Nadu apartment associations hold AGMs.
- Summer 2027 tanker-price forecasts were not available.

---

## B1. Meta/WRI canopy height on AWS: coverage, tile access, accuracy for India

### Takeaway
Use **CHMv2**, the DINOv3-based version (S3 objects dated Jan 2026, paper Mar 2026), not v1.
- **Access works keylessly:** a Bengaluru tile was opened and windows read in-browser in ~3.4 s, with plausible values for parks, a lake and a runway.
- **The limits are serious at footpath scale:**
  - imagery mostly from 2018–2020;
  - Maxar geolocation error averaging 8.7 m;
  - no India-specific validation;
  - 17–26% of interior points of mapped buildings carry canopy ≥3 m, so the raster must be masked with footprints.

### Cited Findings
- **Registry (FACT):** "Version 2 High Resolution Canopy Height Maps (CHMv2)" by Meta and WRI, global, at `s3://dataforgood-fb-data/forests/v2/global/dinov3_global_chm_v2_ml3/` (us-east-1, `--no-sign-request`). GeoTIFF plus GeoJSON observation dates; CC BY 4.0; papers arXiv 2603.06382 and 2508.10104 — [AWS Registry: CHMv2](https://registry.opendata.aws/dataforgood-fb-forestsv2).
  - **License conflict:** the paper says AWS S3 access is "under the DINOv3 license" — [arXiv 2603.06382](https://arxiv.org/html/2603.06382). Check before claiming CC BY in the video.
  - v1 (the earlier `alsgedi_global_v6_float` product) remains in the Registry — [AWS Registry: v1](https://registry.opendata.aws/dataforgood-fb-forests/).
- **Live listing and reads (FACT, 9 Oct 2026 ~22:00 IST):**
  - **Layout:** prefixes `chm/` (COGs named by **zoom-10 quadkey**) and `metadata/` (per-tile GeoJSON), plus `tiles.geojson` (58.9 MB index).
  - **Bengaluru tile:** Koramangala falls in quadkey `1233033120`. `chm/1233033120.tif` is **228.4 MB**, last modified 2026-01-13.
  - **Neighbouring tiles:** 92–282 MB. Metadata GeoJSONs for Bengaluru tiles are **9–19 MB each**; one is too big to fetch casually.
  - **Header (geotiff.js 2.1.3):**
    - 32,768 × 32,768 px at 1.1943 m (EPSG:3857)
    - uint8, 512 × 512 internal tiles
    - 14 images (full resolution plus overviews)
    - **no GDAL nodata tag** (0 means both no-data and "no canopy")
  - **Speed:** HTTP range requests returned 206 in 0.7 s. Two 500 m windows (~181k px each) read in **3.4 s** total.
- **Sanity windows (FACT, live, CHMv2 tile 1233033120):**

| Window | Share of pixels ≥3 m | ≥10 m | Mean | Max |
|---|---|---|---|---|
| Cubbon Park core, 500 m | 0.73 | 0.64 | 13.75 m | 41 m |
| Lalbagh core, 300 m | 0.60 | 0.47 | 8.88 m | 29 m |
| Koramangala residential, 500 m | 0.53 | 0.30 | 6.01 m | 29 m |
| Chickpet market, 300 m | 0.14 | 0.05 | 1.44 m | 25 m |
| Ulsoor Lake water, 200 m | 0.03 | 0.03 | 0.50 m | 22 m |
| HAL airport runway, 200 m | 0 | 0 | 0 | 0 |

  A "KR Market" window was discarded: Overture showed only 8 buildings there, so the coordinates were off.
- **Building-mask test (FACT, live):**
  - **Method:** CHMv2 sampled at interior points of Overture buildings ≥150 m².
  - **Koramangala** (n = 206): median **0 m**; **26%** ≥3 m; 7% ≥10 m.
  - **Chickpet** (n = 48): median 0 m; **17%** ≥3 m; 8% ≥10 m.
- **CHMv2 paper (FACT), [arXiv 2603.06382](https://arxiv.org/html/2603.06382):**
  - **Imagery:** Maxar Vivid2 (~0.6 m GSD); **about 80% of images are from 2018–2020**. The map is single-date, not attributable to one year.
  - **Accuracy:** MAE **3.0 m vs 4.3 m** for v1; R² **0.86 vs 0.53**. Against GEDI: MAE 3.1 m, RMSE 6.4 m.
  - **Geolocation:** Maxar averages **8.7 m**; high off-nadir views displace tree footprints.
  - **Other caveats:** sparse-tree landscapes are more uncertain; usage notes advise **masking built-up areas**; no urban, street-tree or India-specific metrics.
  - **Release:** 213,109 COGs of 32,768 × 32,768 px (22.65 TB).
- **Cloud-native mirror (FACT):** Source Cooperative hosts a CORS-enabled mirror with `tiles.parquet`, `acq_dates.parquet`, STAC and multiscale GeoZarr — [README](https://data.source.coop/tge-labs/meta-chm-v2/README.md).
- **Vintage risk in Bengaluru (FACT):** 19,268 trees were felled from 2023 to 2026, largely for metro, road-widening and flyover projects (GBA data) — [Deccan Herald, Jul 2026](https://www.deccanherald.com/india/karnataka/bengaluru/cost-of-b-luru-s-growth-19-000-trees-axed-in-3-yrs-4062477).

### Inferences
- **Access is solved; registration and currency are the risks (INFERENCE).** An 8.7 m mean geolocation error is larger than the 1.5–3 m width of most footpaths, and canopy lost since 2018–2020 along metro and flyover corridors will still show as shade.
- **Mask by footprints (INFERENCE).** The 17–26% hit rate on building interiors could be overhanging trees, buildings newer than the imagery, misregistration or model leakage. Any of these would make a roof "cast a tree shadow". Mask CHM with Overture footprints, and treat building shadows separately.
- **Use the right tile set for a Lambda (INFERENCE).** Read via the Source Cooperative mirror or the Meta bucket with `rasterio` windowed reads. A 1 km² campus window is about 700k px, trivially small.

### Gaps
- No India-specific accuracy assessment of CHMv1 or CHMv2 was found.
- The per-tile acquisition-date raster/GeoJSON for Bengaluru was not read (file size).
- Tiles for Delhi, Chennai and Pune campuses were not opened; the bucket is global, so this is assumed by analogy.

---

## B2. Building heights for India

### Takeaway
There is **no ready, AWS-hosted, accurate per-building height for Indian cities.**
- **Overture:** heights are essentially empty (0–6 per ~2,000 buildings).
- **Google Open Buildings 2.5D Temporal:** covers India and is the best option, but lives on Earth Engine/GCS, has a 4 m effective resolution, and is unvalidated in the Global South.
- **UT-GLOBUS:** RMSE 9.1 m, too coarse for 2–4 storey shadows.

### Cited Findings
- **Overture (FACT, live, A2 table):** `height` is present on 0 of 2,588 (Koramangala), 6 of 2,043 (Kothrud), 0 of 2,088 (Anna Nagar) and 0 of 953 (DTU) buildings. `num_floors` is present on 22, 17, 0 and 9 buildings respectively.
- **Google Open Buildings 2.5D Temporal (FACT), [Google Research](https://sites.research.google/gr/open-buildings/temporal); [Earth Engine catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1?hl=en):**
  - **Coverage:** India is on the country list. Annual 2016–2023; effective ~4 m resolution, rasters at 0.5 m.
  - **Accuracy:** height MAE **1.5 m, evaluated only in North America, Europe and Japan**; "accuracy in the Global South is likely lower, especially for tall buildings".
  - **Caveats:** heights must be masked with the presence band; tree occlusion causes artifacts.
  - **Access:** Earth Engine (registration) or the GCS bucket `open-buildings-temporal-data/v1` via a Colab notebook.
  - **License:** CC BY 4.0 or ODbL.
- **UT-GLOBUS (FACT):**
  - **Coverage:** more than 1,200 cities (1,088 ingested in Earth Engine).
  - **Accuracy:** building-level RMSE **9.1 m** against US LiDAR.
  - **Distribution:** 53.5 GB on Zenodo (Asia.zip 16.4 GB); CC BY 4.0.
  - **Indian cities:** not confirmed in the pages read — [GEE community catalog](https://gee-community-catalog.org/projects/utglobus/); [Zenodo](https://zenodo.org/records/11156602).
- **ShadeMap's fallback (FACT):** buildings without height are set to 3.1 m (one storey) — [ShadeMap help](https://shademap.app/help).

### Inferences
- **A 40-hour plan for heights (INFERENCE):**
  1. Default heights by footprint size or class, editable by the user.
  2. Optionally, a pre-exported Google 2.5D raster for the single demo campus, copied into S3 with attribution.

  Either way, label building heights as **assumed**. On a campus, buildings matter less than trees for walkway shade at 1–4 pm in May, when the sun is high, so the error is tolerable (INFERENCE).
- **Height error vs. shadow length (INFERENCE).** At a solar elevation of ~60°, a 1.5–3 m height error moves the shadow tip by about 0.9–1.7 m. A 9 m error moves it by about 5 m, which rules out UT-GLOBUS.

### Gaps
- Google 2.5D accuracy in Indian cities is unknown.
- UT-GLOBUS coverage of Indian cities was not checked (it needs the coverage .gpkg).
- OSM `building:levels` density was not measured beyond Overture's `num_floors`.

---

## B3. Shadow-casting tools: what exists, and does ShadeMap (or WRI) already do this?

### Takeaway
Shadow casting itself is commodity.
- **ShadeMap** already shows global building and tree shadows and hours-in-sun.
- **WRI's Cool Cities Lab** already runs 1 m hourly SOLWEIG shade from Overture buildings, UT-GLOBUS heights and the WRI/Meta canopy, **including four Indian cities**, with a "shade change" scenario layer.

What none of the sources claims is **choosing where to plant N saplings to maximise future shade-minutes on paths people walk**. That optimisation is ShadeSite's only defensible novelty.

### Cited Findings
- **ShadeMap (FACT), [ShadeMap help](https://shademap.app/help):**
  - "A global simulation of mountain, building and tree shadows for any date and time."
  - Buildings come from OSM, Overture and Mapbox; the tree dataset is not named.
  - Layers: "Hours in the sun" and "Annual sunlight".
  - Premium LiDAR data is sold per km²; missing heights default to 3.1 m; errors "can vary by several meters".
  - No API or planting optimisation is mentioned.
- **WRI Cool Cities Lab (FACT), [shade layer](https://coolcities.wri.org/data-and-methods/shade); [shade change](https://coolcities.wri.org/data-and-methods/shade_change); [home](https://coolcities.wri.org/):**
  - **Model:** shade from buildings and trees at 3 pm via open-source **SOLWEIG**, 1 m, hourly, on the hottest day of the past five years.
  - **Inputs:** OpenUrban, OSM, **Overture**, **UT-GLOBUS** and **WRI/Meta tree canopy**.
  - **Scenarios:** the "Shade cover—change" layer models an infrastructure scenario.
  - **Cities:** 27, including **Bhopal, Gwalior, Indore and Jabalpur**.
  - **Audience:** city officials; CC BY 4.0.
  - The pages do not say the tool ranks planting locations.
- **pybdshadow (FACT), [PyPI](https://pypi.org/project/pybdshadow):** v0.3.5 (3 Jan 2024), BSD. Building shadows from footprints, heights and suncalc sun position; sunshine time on ground and roofs. **No tree or raster canopy support.**
- **CoolWalks (FACT), [arXiv 2405.01225](https://arxiv.org/html/2405.01225v2):**
  - Shaded routing with a sun-aversion parameter, on Manhattan, Barcelona and Valencia; open-source Julia (`henrik-wolf/CoolWalks`).
  - **Buildings only:** "We considered as a first step buildings only and not trees, due to availability issues with tree data."
  - Notes incomplete OSM sidewalks.
- **pvlib (INFERENCE / known):** pvlib-python provides solar position (NREL SPA). It was not re-verified in this session.

### Inferences
- **Expect the WRI question (INFERENCE).** A judge who knows WRI will ask "isn't this Cool Cities Lab?". The answer has to be placement optimisation for a campus or ward user plus a pedestrian weighting. A shade *map* alone is re-presentation.
- **Engineering route (INFERENCE):** a numpy ray-march on a combined height raster (CHM masked by buildings, plus building heights) along the sun azimuth.
  - **Per sun position:** shift the height raster along the azimuth and check whether the shifted height exceeds distance × tan(elevation).
  - **Size:** 1 km² at 1.2 m with about 24 sun positions is a few seconds in Lambda.
  - **Why not a library:** pybdshadow cannot do trees; SOLWEIG (UMEP) is heavier to wire in 40 h.

### Gaps
- ShadeMap's tree data source and Indian coverage are unconfirmed.
- Whether Cool Cities Lab exposes per-tree or what-if planting tools inside its app was not checked (the app was not opened).
- WRI's processing code repository was not located.

---

## B4. Competitors and precedents for sapling siting and urban shade planning in India

### Takeaway
Indian practice and reporting show the gap ShadeSite targets:
- **Ludhiana's 2024 heat-map plantation** sited trees by satellite heat (LST) and land availability (NGO/RWA land), leaving roads and pavements out.
- **Down To Earth (Jul 2026)** argues drives cluster in urban forests and peripheries rather than streets and footpaths.
- **CSE's 2026 toolkit** is an ENVI-met report, not a siting tool.

No Indian tool was found that ranks planting spots by pedestrian shade.

### Cited Findings
- **Ludhiana (FACT), [Mongabay India, 18 Jul 2025](https://india.mongabay.com/2025/07/a-heat-map-based-plantation-programme-turns-into-a-missed-opportunity/):**
  - A heat-map plantation programme launched in 2024 used a ward-wise Punjab Remote Sensing Centre satellite heat map (orange wards 4–6 °C warmer).
  - A year on, it was "lacklustre". Officials were unaware, leadership changed twice, and planting went to NGO, industry and RWA land, so roads, pavements and working-class areas were left out.
  - Only one government-maintained site could be identified; the monitoring database is not public.
- **Down To Earth (FACT), [10 Jul 2026](https://www.downtoearth.org.in/urbanisation/missing-canopy-cities-must-rethink-where-they-plant-trees):**
  - Plantation drives are concentrated in urban forests and peripheral sites; cities should plant along streets, footpaths, markets and public spaces.
  - Varanasi planted 250,000 saplings in one day; Mumbai lost 523 trees in one day (6 Jul 2026).
  - Mentions CSE's "CoolIT" interactive tool and a June 2026 Supreme Court recognition of the right to walk (as reported).
- **CSE (FACT), [CSE, 1 Jun 2026](https://www.cseindia.org/reclaiming-heat-resilient-public-spaces-a-simulation-toolkit-for-urban-heat-mitigation-13135):** "Reclaiming Heat-Resilient Public Spaces: a simulation toolkit". It is an **ENVI-met-based report** (10 sites in Delhi, Jaipur, Mysuru, Pune and Leh) for planners, not a software tool.
- **Earlier notes (FACT, via C-06/C-07):**
  - 10.35 crore saplings were planted in one school drive — [DoSEL](https://dsel.education.gov.in/sites/default/files/update/Ek_Ped_Maa_Ke_naam_2-0.pdf).
  - Survival averaged 33.51% in Uttarakhand — [CAG](https://cag.gov.in/uploads/download_audit_report/2024/9_Chapter-5_IoCAA-067b7207e116ad2.51862799.pdf).
  - Parasols achieve about 56% of a street tree's UTCI reduction — [ICUC12](https://meetingorganizer.copernicus.org/ICUC12/ICUC12-703.html).
- **WRI Cool Cities Lab (FACT, B3):** covers Bhopal, Gwalior, Indore and Jabalpur.

### Inferences
- **Benefit framing (INFERENCE).** The strongest Indian framing is "plant where the mature crown will shade the walk, not where land is free". Ludhiana shows LST-based siting fails on pavements.
- **The deferred-benefit objection stands (INFERENCE).** Saplings shade nothing for years. The tool should show year-5 and year-10 crown scenarios and recommend shade structures as interim options.

### Gaps
- The Green Delhi app, Bengaluru and Pune tree-census tools and city tree plans were not inspected for siting logic.
- No Indian municipal planting-siting software was found.
- The CSE "CoolIT" tool was not opened.

---

## B5. Realistic 48-hour scope for ShadeSite and the biggest GIS risk

### Takeaway
A **single-campus** MVP is feasible in ~40 h. It reads CHMv2 tiles from S3, uses Overture footprints with assumed heights and OSM/Overture footways, ray-marches shade for 11:00–16:00 on a May day, and greedily picks 10 spots.
- **Ward scale is not feasible:** sidewalks are largely unmapped.
- **Biggest GIS risk:** misregistration and staleness. CHMv2 (8.7 m mean geolocation error, 2018–2020 imagery), Overture footprints and OSM footways are each accurate to several metres, while the target (a 2 m footpath) is narrower than the error.

### Cited Findings
- **Footpath mapping density (FACT, live DuckDB query on Overture `transportation/segment`, release 2026-09-23.1, subtype = road):**
  - **Koramangala**, 0.01° box: 337 residential, 55 tertiary, 29 secondary and 28 service segments vs **27 footway and 8 sidewalk** segments.
  - **IISc campus** (77.560–77.575, 13.012–13.026): **101 footway, 28 steps, 24 path**.
  - **IIT Delhi campus** (77.185–77.200, 28.540–28.550): 20 footway, 19 path, 5 steps, 3 pedestrian, 1 sidewalk.
  - DTU and Kothrud queries returned empty, probably because the file was matched to the wrong STAC bbox (not resolved).
  - The public Overpass instance returned HTTP 504 / runtime errors during this session.
- **Data errors that compound (FACT):** CHMv2 geolocation and off-nadir displacement (B1); 17–26% of building interiors show canopy ≥3 m (B1); ML-derived footprints have lower precision in the Global South ([Overture guide](https://docs.overturemaps.org/guides/buildings)); Overture heights absent (B2).
- **Access cost (FACT, B1/A2):** one CHMv2 tile is 228 MB, but window reads are about 2 s; the first Overture file query costs a footer read (over 45 s in a browser).

### Inferences
- **Scope (INFERENCE):** one campus the team can photograph (its own college, or IISc / IIT Delhi as public examples). Path demand weights come from OSM gates, bus stops and canteens, or user-drawn "main walks". Shade-minutes come for one May day and today's date.
- **Self-validation without outsiders (INFERENCE):** teammates photograph 3–5 walkway points at a fixed time today or tomorrow, and the model is run for that timestamp. This checks registration and vintage visibly.
- **Mitigations (INFERENCE):**
  - Evaluate shade on 6–10 m path corridors, not centrelines.
  - Mask CHM with building footprints.
  - Print "canopy imagery ~2018–20" on the map.
  - Let users erase or add trees by clicking.
- **Build estimate (INFERENCE):**
  - Data plumbing: 8–10 h.
  - Shadow ray-march plus greedy optimiser: 8–12 h.
  - UI map, time slider and planting pins: 10–12 h.
  - Video and polish: 6 h.

  That is 32–40 h for 2–4 people, with little slack. Monsoon Replay is about 25–30 h (INFERENCE).

### Gaps
- Not prototyped: shadow ray-march runtime and the visual quality of CHM-derived shadows.
- Species crown-growth curves for Indian native street trees were not sourced.

---

## C. Overlap with the 111 visible Environmental Hacks projects (from `live_competition.md`) and new repos

### Takeaway
- **No visible Environmental Hacks project does RWH sizing.** But 54 "rainwater" repos created since 20 Sep 2026 show the genre is crowded at other hackathons and in coursework.
- **For ShadeSite, four visible projects sit in the heat/shade space** (two shade or heat-aware routers, a heat-pocket mapper and a facility heat-resilience engine). None does planting placement.

### Cited Findings
- **Overlaps with B, all Heat & Water (FACT, `live_competition.md`, scanned 9 Oct ~14:00 IST):**
  - **#74 CHHAYA**, "shade- and flood-aware pedestrian routing" — [teamaekovera-glitch/chhaya](https://github.com/teamaekovera-glitch/chhaya).
  - **#73 HeatRoute**, "thermal-aware pedestrian routing" — [matorverse/HeatRoute](https://github.com/matorverse/HeatRoute).
  - **#72 HEPo**, "urban heat pockets from geotagged temperatures".
  - **#71 HeatCredit**, "heat-resilience decision engine for schools, hospitals and facilities, within a budget".
  - The matrix rates "facility/municipal heat prioritisation, heat pockets, shade routes" as **moderate (4)**.
- **Adjacent to A (FACT, same file):**
  - **#59 JalTaap**: heat, floods, drought, groundwater, tankers and leaks on one desk.
  - **#83 JalSanket**: groundwater telemetry triage.
  - **#85**: Maharashtra drought water ops.
  - **#86 Second Tap**: STP water reuse.
  - The organiser seed #3 (tanker predictor) had **0** direct takers. "Groundwater / drought / ponds" is rated moderate–low (3).
  - No project mentions rainwater harvesting.
- **Outside the event (FACT, live GitHub search, A3):** 54 repos match "rainwater" since 20 Sep 2026. They include tank-size and cost calculators (7 Oct), a 365-day storage simulator with synthetic rain (HydroLens), and a geospatial urban rainwater decision-support tool (JALNETRA-AI, GeoImpathon). Event affiliation is mostly unknown.

### Inferences
- **A (INFERENCE):** uncontested inside the visible Environmental Hacks sample, but judges may have seen RWH calculators elsewhere. Moderate risk of a "seen it" reaction.
- **B (INFERENCE):** shade routing (CHHAYA, HeatRoute) is the nearest neighbour. ShadeSite must look like *planning where to plant*, not *routing through shade*.

### Gaps
- The 111-project scan is about 8 hours old; new projects since then are unknown.
- GitHub search covered names and descriptions only.

---

## Verdict for the coordinator

### A. Monsoon Replay

**(i) Capability table for the main journey**

| Step | Status | Evidence |
|---|---|---|
| 1. User picks a society or campus on a map; buildings fetched from Overture on AWS | **VERIFIED** (keyless DuckDB on S3, live). Athena in the team's own account is **PLAUSIBLE-UNTESTED** | A2: 2,588 buildings in Koramangala; STAC maps the area to a single file |
| 2. Roof area per building and total | **VERIFIED** | A2: 418,842 m² footprint in the Koramangala box; per-building areas computed with DuckDB spatial |
| 3. Decide which buildings form "the society" | **PLAUSIBLE-UNTESTED** | User draws or confirms a polygon; OSM complex boundaries not checked |
| 4. Daily rainfall for past monsoons (2024, 2025, 2026) | **VERIFIED-BUT-CONSTRAINED** | A1: live through 2026-10-08; totals −48% to +33% vs IMD; peak days ~4× under; model spread 53% |
| 5. Day-by-day tank water balance with overflow | **VERIFIED** (trivial computation, run live) | A1: 10 kL tank uses 73% (Bengaluru) / 52% (Chennai) of runoff |
| 6. Recharge-pit routing of overflow | **PLAUSIBLE-UNTESTED** | Needs a user infiltration-rate assumption; physics is simple |
| 7. Tanker-equivalents and ₹ | **VERIFIED-BUT-CONSTRAINED** | A4: Bengaluru fixed rates, 2024 (₹600 per 6,000 L within 5 km); market rate is user input |
| 8. Mandate or penalty check (BWSSB, DJB) | **VERIFIED-BUT-CONSTRAINED** | A4: Bengaluru and Delhi rules sourced; BWSSB capacity norms and Mumbai threshold not fetched |
| 9. Committee or AGM pack (Bedrock) | **PLAUSIBLE-UNTESTED** | Standard generation |
| 10. Proof that the replay matches reality | **UNSUPPORTED** beyond a rainfall-total cross-check | No metered RWH data; only model vs IMD totals |

**(ii) Minimum working demonstration (no outside person, privileged data or hardware)**
1. **Site:** a real Bengaluru (or Chennai) apartment complex. Athena (or DuckDB) on `s3://overturemaps-us-west-2/release/2026-09-23.1/theme=buildings/` pulls its footprints, shown in the console.
2. **Rain:** Open-Meteo daily rain for 2024, 2025 and 2026, as three models with a min–max band. One labelled IMD monthly bias-correction example: May 2025 IMD 307.9 mm vs model 159 mm.
3. **Replay:** three tank sizes plus a recharge pit, animated over the 2026 monsoon, with a capture-vs-size curve.
4. **Economics:** tanker-equivalents at the cited Bengaluru 2024 rate, and penalty paid vs tankers avoided.
5. **Output:** a one-page pack.

Label tanker ₹, runoff coefficient and infiltration rate as assumptions. Label rainfall as "model estimate, ERA5/IFS".

**(iii) Strongest skeptical-judge objection**
> "SimTanka (open source) and the Jal Shakti Hackathon-2025 winner already do roof → historical daily rain → tank size. Your rain is a 9–28 km model that misses the cloudbursts that make tanks overflow, so your capture numbers are optimistic."

**Partly answerable.**
- *The part that cannot be fully answered:* the novelty margin is thin. Differentiate on multi-building aggregation from AWS Open Data, recharge routing, ₹ and tankers, the uncertainty band, and the committee output.
- *The data part:* answer it by showing the band, the IMD comparison and the direction of bias ("small-tank capture is an upper bound").
- *Full answer:* fixing bursts needs gauge data, which was not verified keyless in this session.

**(iv) Functional improvement or re-presentation?**
- **vs. annual-average calculators** (Studio Matrx, KSCST RWH Advisor, most student repos): a **functional improvement**, evidenced by the live replay: capture of 52–73% vs the 100% they imply.
- **vs. SimTanka and the Jal Shakti winner:** **mostly re-presentation plus aggregation**. The genuinely new function is multi-building, recharge-routed sizing with tanker economics.
- **Overall (INFERENCE):** low build risk (~25–30 h) and good timing (deficient 2026 monsoon, strong El Niño, NE monsoon starting). Medium-low novelty, and constrained data credibility.

### B. ShadeSite

**(i) Capability table for the main journey**

| Step | Status | Evidence |
|---|---|---|
| 1. Pick a campus; read canopy height from AWS | **VERIFIED** | B1: CHMv2 tile `1233033120.tif` read keylessly; 500 m windows in ~1.7 s each |
| 2. Canopy accurate at footpath scale | **VERIFIED-BUT-CONSTRAINED** | B1: MAE 3.0 m; Maxar geolocation 8.7 m; imagery ~80% 2018–20; 17–26% of building interiors ≥3 m; 19,268 Bengaluru trees felled 2023–26 |
| 3. Building footprints | **VERIFIED** | A2 |
| 4. Building heights | **UNSUPPORTED** in Overture (0–6 per ~2,000); **PLAUSIBLE-UNTESTED** via Google 2.5D (GCS/EE, unvalidated in India); fallback is assumed storeys | B2 |
| 5. Walkable paths | **VERIFIED-BUT-CONSTRAINED** | B5: good on campuses (IISc 101 footways); not in neighbourhoods (Koramangala: 8 sidewalk segments vs 337 residential roads) |
| 6. Pedestrian demand weights | **UNSUPPORTED** from open data | Proxy (gates, bus stops) or user-drawn; HYPOTHESIS that the proxy is adequate |
| 7. Sun position and shadow casting over CHM plus buildings | **PLAUSIBLE-UNTESTED** | B3: pvlib exists; pybdshadow and CoolWalks are buildings-only; WRI uses SOLWEIG; custom numpy ray-march needed |
| 8. Greedy placement of N saplings by marginal shade-minutes | **PLAUSIBLE-UNTESTED** | Standard algorithm; not found in any competitor |
| 9. Benefit timing (sapling to mature crown) | **HYPOTHESIS** | No growth curves sourced; benefit is deferred by years |
| 10. Validation | **PLAUSIBLE-UNTESTED** | Teammates photograph shadows on their own campus at a set time and compare with the model run for that timestamp |

**(ii) Minimum working demonstration**
1. **Site:** the team's own campus, or IISc / IIT Delhi as public examples.
2. **Data:** a CHMv2 window from S3 (masked by Overture footprints), buildings with labelled assumed storeys, and Overture/OSM footways.
3. **Shade:** a ray-marched shade time-lapse for 11:00–16:00 on a May day, giving each walkway's shaded fraction.
4. **Placement:** a greedy pick of 10 planting spots, each with a mature-crown assumption.
5. **Validation:** a "today at 14:00" model frame beside teammates' photos of the same walkway.

No outside person is needed.

**(iii) Strongest skeptical-judge objection**
> "WRI's Cool Cities Lab already computes 1 m SOLWEIG shade from Overture plus Meta canopy for Indian cities (Bhopal, Indore, Gwalior, Jabalpur), with scenario layers, and ShadeMap shows tree shadows anywhere. Your canopy is 2018–20 imagery with 8.7 m geolocation error, your buildings have no heights, and your saplings won't shade anyone for 5–10 years."

**Partly answerable.**
- *Answerable:* novelty is placement optimisation for a campus user, plus the photo check. Neither WRI (city officials, baseline and scenario maps) nor ShadeMap (viewing) claims it.
- *Only mitigable:* data-quality issues, through corridor buffers, footprint masking, user edits and labels.
- *Unavoidable:* the deferred benefit. Show year-5 and year-10 crowns, and suggest interim shade sails.

**(iv) Functional improvement or re-presentation?**
- **vs. ShadeMap and Cool Cities shade maps:** placement optimisation is a **genuine new function**, but only if the optimiser is the hero of the demo. A shade map alone would be re-presentation of WRI's work.
- **vs. LST heat-map plantation siting (Ludhiana):** a clear functional improvement in targeting walkers.
- **Overall (INFERENCE):** higher novelty than A, but high GIS risk (registration, stale canopy, no heights) and a tight 32–40 h build. Moderate competition (CHHAYA and HeatRoute nearby). The judge-visible benefit is deferred.

**Bottom line (INFERENCE):**
- **A is the safer build** with a weaker novelty claim. Its credibility hinges on showing the model-vs-IMD band honestly.
- **B is the more novel idea** with the bigger execution risk.

If either is chosen:
- **A:** lead with multi-building aggregation from AWS Open Data plus recharge plus tanker ₹, in Bengaluru or Chennai (not Pune), with the uncertainty band on screen.
- **B:** restrict to one campus, make the optimiser and the photo check the hero, and label canopy vintage and assumed heights.
