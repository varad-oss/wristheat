# Personal, Household & Mobility Lens: Problem Map and Concepts (Environmental Hacks, 9 Oct 2026)

**Scope.** This file covers decisions made by individuals and households: cooling, electricity bills, water use, commuting, personal exposure, vehicles and food. Community, institutional and mechanism-first concepts belong to other researchers.

**Starting point.** We extend 03, 04 and 05 and do not repeat them. Earlier ideas (SunCheck, HeatShift, TankerTruth, Clean-Air Windows, BinScore) are not reused.

**Tags.**
- **FACT:** sourced, with a link.
- **INFERENCE:** reasoned from facts.
- **HYPOTHESIS:** plausible but untested.
- **KNOWN:** a widely known product or practice that was not re-verified in this session.

**Method.** WebSearch and WebFetch only, run on 9 Oct 2026.

**What I could not verify.** Live API probes from the shell (curl to OpenAQ v3, WAQI and Open-Meteo) were blocked by the sandbox proxy (HTTP 403). WebFetch on the Open-Meteo API endpoint was blocked by robots.txt. The API capabilities below therefore come from documentation pages, not live responses. **Before committing, the team must make one live call to each API it will use.**

---

## Q1. Where do Indian individuals and households fail to turn environmental data into good decisions?

### Takeaway

The biggest household environmental lever is **cooling electricity**. Fans, ACs and coolers make up 40% of household use. The sharpest personal signal is the **rupee cliff** in free-electricity schemes: in Delhi alone, about 25 lakh households lose their zero bill every summer. The biggest personal-exposure lever is **commute mode and timing**: in Delhi, rickshaw or walking exposure is about 3.6–3.7× the metro's. Two-wheelers carry 52% of urban work trips.

In each of these cases the data exists (meter readings, weather, AQ forecasts, label values, mode-exposure studies). What is missing is a **forward projection tied to the household's own threshold**, and a way to **verify, net of weather, that an action worked**.

### Cited Findings

**A. Household electricity and cooling**
- **40%:** fans, ACs and air coolers' share of household electricity in surveyed homes. Average use is about 1,805 kWh/yr per household (urban 1,937; hot-dry urban 2,090). FACT: CLASP–BEE 2024 survey (4,321 households, 20 states), via [Down To Earth, 12 May 2026](https://www.downtoearth.org.in/amp/story/energy/cooling-appliances-now-drive-indias-household-electricity-use)
- **AC ownership is 13.3% of surveyed households** (17% urban, 4% rural). Of owned ACs, 40% are 3-star and 33% are 5-star. Nearly half of respondents cite appliance cost as a key purchase factor. FACT: [DTE, same survey](https://www.downtoearth.org.in/amp/story/energy/cooling-appliances-now-drive-indias-household-electricity-use)
- **Residential demand context.** FACT: [DTE](https://www.downtoearth.org.in/amp/story/energy/cooling-appliances-now-drive-indias-household-electricity-use)
  - Residential use was 25% of national electricity in FY25, growing about 6% a year.
  - Peak demand rose from 136 GW to 243 GW over 2013-14 to 2023-24.
  - The India Cooling Action Plan projects an eightfold rise in cooling demand by 2037-38.
- **NSS 2020:** about 5% of households owned an AC and 14% an air cooler; about 30% now own one or the other. Ownership is concentrated among the rich (ACs) and in arid central states (coolers). FACT: [Data For India, 4 Mar 2026](https://www.dataforindia.com/cold-comforts/)
- **Coolers and fans: Prayas survey** (UP and Maharashtra, Feb–Mar 2019). FACT: [Prayas Energy Group](https://energy.prayaspune.org/space-conditioning-focus-on-fans-and-air-coolers-for-efficiency)
  - Coolers are owned by about 40% of UP households and 23% of Maharashtra households.
  - BEE has **no star-labelling programme for air coolers**.
  - About 8 million coolers are bought each year (a national estimate, not from the survey).
  - More than 95% of fans produced are not star-rated.
- **BEE on AC setpoints.** FACT: [Business Standard, 10 Jun 2025](https://www.business-standard.com/india-news/india-standardise-air-conditioner-temperature-20-28-degree-celsius-125061001221_1.html)
  - Most ACs are set at 20–21 °C, though the comfort range is 24–25 °C.
  - Each +1 °C saves about 6%; 20→24 °C saves about 24%.
  - If half of AC users shifted, India would save about 10 BU/yr (BEE's estimate).
  - The 24 °C default has been mandated since 2020.
  - A 20–28 °C setting range was announced.
- **The 20–28 °C range was not to be implemented immediately.** FACT (headline only; body not read): [ETV Bharat, 27 Jun 2025](https://www.etvbharat.com/en/!bharat/govt-unlikely-to-implement-20-to-28-deg-c-ac-temp-range-immediately-union-environment-minister-enn25062705276). Its status in Oct 2026 was not established (see Gaps).
- **India Model for Adaptive Comfort (IMAC).** FACT: [Manu et al., Building and Environment (CEPT/UTS)](https://opus.cloud1.lib.uts.edu.au/bitstream/10453/41878/1/Manu%20et%20al%20Thomas%20-%20Adaptive%20Model%20India%201-s2.0-S0360132315302171-main.pdf)
  - Neutral temperature, naturally ventilated buildings: 0.54 × T_out(30-day running mean) + 12.83, ±2.4 °C at 90% acceptability.
  - Mixed-mode buildings: 0.28 × T_out + 17.87, ±3.5 °C.
  - Observed neutral temperature in AC buildings was 23.5–25.5 °C, against a common design practice of 22.5 ± 1 °C.
  - Fans are a major adaptation; air speed plateaus near 0.6 m/s at 30–36 °C.
- **ISEER (the AC star metric)** is computed on one national profile: 1,600 operating hours spread over 20 one-degree bins from 24 °C to 43 °C, drawn from 54 cities' weather data. It is not computed per city. FACT: [CAG (Citizen consumer and civic Action Group)](https://www.cag.org.in/newsletters/public-newsense/indian-seasonal-energy-efficiency-ratio-iseer-overview)

**B. Free-unit schemes and slab cliffs (unusually strong household signal)**
- **Delhi** (200 units free; 50% subsidy for 201–400). FACT: [Daily Pioneer, 8 Nov 2025](https://www.dailypioneer.com/2025/state-editions/zero-power-bills-surge-under-8monthold-bjp-government.html)
  - Zero-bill households: **43.87 lakh (Feb 2025) → 18.26 lakh (Jul 2025)**, out of about 60 lakh domestic consumers.
- **Telangana Gruha Jyothi** (200 units). FACT: [Deccan Chronicle, 21 Jun 2024](https://deccanchronicle.com/news/excess-use-of-power-affects-gruha-jyothi-beneficiaries-900090)
  - A household that uses **201 units "should pay the entire bill of 201 units"**.
  - "Numerous customers turned ineligible during the summer season."
- **Telangana beneficiaries:** 42.25 lakh received free electricity in July 2024. FACT: [Siasat, 16 Aug 2024](https://www.siasat.com/telangana-free-electricity-scheme-beneficiaries-struggle-to-receive-zero-bill-3079517/amp/)
- **Karnataka Gruha Jyothi.** FACT: [The News Minute, 5 Jun 2023](https://www.thenewsminute.com/article/explained-how-karnataka-free-electricity-scheme-will-work-178121)
  - Entitlement = the household's average monthly use + a 10% buffer, capped at 200 units.
  - Units above the entitlement are billed at ₹7.
  - Using **more than 200 units in a month means paying the full bill**.
- **Bihar:** 125 units free from 1 Aug 2025 for about 1.67 crore families; budget ₹3,797 cr for FY26. FACT: [ETV Bharat, Jul 2025](https://www.etvbharat.com/en/!state/bihar-cabinet-approves-free-electricity-scheme-enn25071805576)
- **Punjab:** 300 units/month (600 per two-month cycle) free; about 90% of households got zero bills (Jan 2023). Billing above the limit was not stated in the source. FACT: [Daily Pioneer, Jan 2023](https://www.dailypioneer.com/2023/state-editions/punjab---s-90--households-getting-zero-electricity-bill.html)

**C. Smart meters, time-of-day (ToD) tariffs and billing trust**
- **Smart meters:** 3.90 crore installed under the Revamped Distribution Sector Scheme (RDSS), and 5.28 crore across all schemes, by 31 Dec 2025. FACT: [SolarQuarter, 3 Feb 2026](https://solarquarter.com/2026/02/03/india-installs-over-5-28-crore-smart-meters-under-rdss-to-boost-power-sector-efficiency/)
  - The apps offer near-real-time consumption, history, recharge and low-balance alerts.
  - In an REC/PFC survey of 1.24 lakh app users, about 54,000 knew about real-time tracking.
- **Uttar Pradesh scrapped prepaid smart metering on 8 May 2026** after protests over "alleged excess billing and irregularities". FACT: [Outlook Business](https://www.outlookbusiness.com/economy-and-policy/up-govt-scraps-smart-prepaid-meter-system-shifts-all-consumers-to-postpaid-mode)
  - About 83 lakh of 85 lakh smart meters were prepaid and were moved to postpaid.
  - Some consumers dumped meters at collectorates.
- **ToD tariffs:** implemented in 23 states and 5 UTs "across consumer categories". FACT: [CEEW, Dec 2025](https://www.ceew.in/blogs/how-can-electricity-tariff-reforms-empower-indian-households)
  - Maharashtra domestic consumers get ₹0.80/unit off between 9 AM and 5 PM.
  - A 2018 BSES Rajdhani pilot sent home energy reports to about 2 lakh customers.
- **Goa:** "No ToD tariff for domestic consumers for three years". FACT (headline only): [Herald Goa](https://www.heraldgoa.in/?p=450926)
- **Daytime EV charging:** avoids nearly 10% more CO₂ than evening charging, about 10 kg/yr for an e-scooter. FACT: [CSEP, Nov 2024](https://csep.org/working-paper/demystifying-the-climate-benefit-of-ev-transition-in-india/)

**D. Water at home**
- **Desert or room coolers use 1.5–5 L of water per hour** (a retailer explainer; low-quality source). FACT: [Croma Unboxed](https://www.croma.com/unboxed/how-much-water-cooler-uses-8-hours)
- **Evaporative cooling is limited by the wet-bulb temperature.** A not-for-profit calculator assumes about 85% effectiveness. It takes manual temperature and humidity, uses no forecast, gives no hourly plan and tracks no water. FACT: [Studio Matrx evaporative cooler calculator](https://www.studiomatrx.org/utilities/evaporative-cooler-calculator)
- **RO purifiers waste about 3 L for every 1 L purified** (best case about 2:1). DTE recommends reusing reject water. FACT: [Down To Earth, 18 Mar 2024](https://www.downtoearth.org.in/water/bengaluru-water-crisis-how-use-of-ro-purifiers-is-reversing-efforts-to-save-water-95079)
- **NGT (19 May 2019)** directed MoEF to notify a ban on RO where water TDS is below 500 mg/L. The notification had not been issued as of Nov 2019. FACT: [India Water Portal](https://www.indiawaterportal.org/drinking-water/ngt-pushes-ban-ro-purifiers-water-tds-below-500-mgl)

**E. Personal exposure and mobility**
- **MoSPI National Household Travel Survey** (Jul 2025–Jun 2026, 4.92 lakh households). FACT: [The Policy Edge, 5 Oct 2026](https://www.policyedge.in/p/two-wheelers-lead-work-trips-while-buses-carry-most-overnight-travel-mospi-survey-finds)
  - **Two-wheelers carry 42.6% of work trips nationally and 52.3% in cities.** Walking carries 28.3%.
  - Students: walking 37.0%, bus 29.5%, cycling 15.8%.
  - Average commuting spend is ₹785/month (₹1,044 urban).
- **Delhi PM2.5 by mode (Feb 2018), mean µg/m³.** FACT: [Maji et al. 2021, Atmospheric Pollution Research](https://uwe-repository.worktribe.com/output/6946307)
  - Rickshaw 266; walking 259; non-AC car 149; bus 113; AC car 89; metro 72.
  - Walking dose was the highest per km (84.7 µg/km).
- **Delhi, Feb 2023, IIT Roorkee** (405 trips). FACT (vendor blog summarising a ScienceDirect paper): [Prana Air blog](https://www.pranaair.com/blog/prana-air-partnered-with-iit-roorkees-civil-engineering-dept-to-track-transport-pollution-in-delhi/)
  - Mean PM2.5: bicycle 59.8, metro 55.8, AC bus 40.8, AC car 40.2.
  - Per minute, cyclists inhale about 4.68× the PM2.5 of AC-bus riders.
  - Short metro trips gave a low total dose.
- **Vellore** (312 trips). FACT: [Manojkumar et al. 2021](https://research.vit.ac.in/pdf/postprint-commuter-exposure-concentrations-and-inhalation-doses-in-traffic)
  - Active commuters' dose per km is about 4–8× that of motorised commuters.
  - Morning traffic trips reach up to 1.8× the afternoon exposure.
  - Inhalation rates used: 0.01 m³/min (motorised), 0.015 (walking), 0.035 (cycling).
- **Delhi winter diurnal swing:** the overnight-to-10 AM mean is about 302 µg/m³ against about 169 at 4–5 PM. FACT: [r.i.c.e.](https://riceinstitute.org/maps/hourly-variation-in-pm-2-5-in-delhi-december-2015-january-2016/) (via 03)
- **Academic personal-dose apps exist abroad:** HazeDose and HKUST's PRAISE-HK. FACT (existence only): [HazeDose paper mirror](https://fugumt.com/fugumt/paper_check/2005.13745v1_enmode), [HKUST PRAISE-HK](https://hkust.edu.hk/news/personalized-real-time-air-quality-informatics-system-exposure-hong-kong-praise-hk)
- **Google Maps Timeline is now stored on the device.** FACT: [Android Authority](https://www.androidauthority.com/android-google-maps-location-history-3491255/)
  - Export: Settings → Location → Location services → Timeline → **Export**, giving one JSON file.
  - The menu is rolling out gradually.
  - Users report export failures. FACT (thread title): [Google Maps Community, Mar 2025](https://support.google.com/maps/thread/334584618/exporting-local-google-maps-timeline-fails?hl=en)
- **End-of-life vehicles (ELVs).** FACT: [Down To Earth, 5 Jul 2025](https://www.downtoearth.org.in/air/blanket-age-based-ban-on-vehicles-is-not-sustainable-need-a-combination-of-measures)
  - Delhi's "no fuel" rule for 15-year petrol and 10-year diesel vehicles started on 1 Jul 2025. The Delhi government sought a hold within two days.
  - About 6.2 million vehicles have been deregistered as ELVs.
  - Delhi's Oct 2024 tax concession on scrapping is capped at 50% of scrap value.
- **Scrappage policy.** FACT: [Autocar Pro, 27 Aug 2024](https://autocarpro.in/news/automakers-to-give-discounts-on-new-vehicles-against-scrapping-old-ones-gadkari-122235)
  - Up to 25% road-tax concession for non-transport vehicles, offered by about 21 states/UTs.
  - Manufacturer discounts of 1.5–3%.
  - More than 60 Registered Vehicle Scrapping Facilities (RVSFs).
  - About 96,980 vehicles scrapped by Aug 2024.

**F. Heat at home**
- **Wardha, Maharashtra (2025, 700 households).** FACT: [Mongabay India, 23 Jun 2025](https://india.mongabay.com/2025/06/too-hot-to-handle-as-rural-houses-turn-heat-traps/)
  - Tin-roof homes peaked at up to 40 °C indoors; RCC homes averaged 38.5 °C.
  - **RCC roofs release heat overnight**, which disrupts sleep.
  - 82% of residents reported at least one heat symptom.
- **Kolkata slum homes reached the elderly heat-tolerance (wet-bulb) threshold for 3–4 hours a day** (2019 study). FACT: [same source](https://india.mongabay.com/2025/06/too-hot-to-handle-as-rural-houses-turn-heat-traps/)
- **Elderly heat risk.** FACT (secondary citations): [Down To Earth, 30 Mar 2026](https://www.downtoearth.org.in/amp/story/climate-change/indias-elderly-face-deadly-toll-as-heatwaves-intensify)
  - The 2010 Ahmedabad heatwave caused 1,344 excess deaths, mostly among people over 65.
  - Elderly daily mortality is 14.7% higher after two consecutive days at the 97th-percentile temperature.
- **About 5.7% of Indians aged 60+ live alone** (LASI 2017-18). FACT: [DTE, Mar 2022](https://www.downtoearth.org.in/health/how-is-india-s-population-ageing-evidence-from-lasi-81770)

**G. Household waste**
- **Household food waste in India is about 55 kg per person per year** (UNEP Food Waste Index 2024). FACT (secondary): [Drishti IAS, 16 Apr 2026](https://www.drishtiias.com/daily-updates/daily-news-analysis/indias-food-waste-conundrum/print_manually)
- **Quick commerce** (Blinkit, Zepto, Instamart) is valued at US$3.65 bn. ORF gives **no India-specific per-order packaging figure**. FACT: [ORF, 30 Mar 2026](https://www.orfonline.org/expert-speak/delivered-in-minutes-hyperconsumerism-and-the-pollution-behind-convenience)

**H. Data sources checked (access status)**

| Source | What it provides | Access status |
|---|---|---|
| **Open-Meteo Air Quality API** | Hourly pm2_5, pm10, NO₂, O₃, us_aqi, uv_index | Global CAMS at 0.4° (~45 km), 3-hourly; history from Aug 2022; past_days ≤ 92; forecast up to 7 days. Free for non-commercial use; a key is needed for commercial use. FACT: [docs](https://open-meteo.com/en/docs/air-quality-api) |
| **Open-Meteo Historical Weather API** | Hourly temperature, humidity, dew point, **wet-bulb temperature**, vapour-pressure deficit (VPD) | ERA5 (0.25°, from 1940, 5-day delay) or IFS (9 km, from 2017, no delay). FACT: [docs](https://open-meteo.com/en/docs/historical-weather-api). The forecast API has hourly wet-bulb per 03, but a live call was blocked this session |
| **World Air Quality Index (WAQI) API** | Real-time station AQI and pollutants, plus a 3–8 day forecast | Free token. **No historical data in the API.** No paid apps or redistribution; attribution required. FACT: [aqicn.org/api](https://aqicn.org/api/). The page does not confirm India Central Pollution Control Board (CPCB) station coverage (Gap) |
| **CPCB** | Station data | **No real-time API** on data.gov.in. FACT: [data.gov.in](https://www.data.gov.in/resource/real-time-air-quality-index-various-locations) (via 03) |
| **OpenAQ** | Station archive | On AWS (`s3://openaq-data-archive`). FACT: [registry](https://registry.opendata.aws/openaq/). India station coverage for 2025–26 was **not verified** (Gap) |
| **Electricity Maps** | Grid carbon intensity | Free tier for individuals, "over 200 regions"; **India coverage not confirmed** on the page. FACT: [free tier](https://electricitymaps.com/free-tier) |
| **CEA grid emission factor** | Grid CO₂ intensity | 0.710 tCO₂/MWh (FY24-25), 0.675 (FY25-26). FACT: [CEA v22](https://cea.nic.in/wp-content/uploads/baseline/2026/09/User_Guide__Version_22.0.pdf) (via 03) |

**I. Existing alternatives checked**
- **VoltWise AI** (AMD Developer Hackathon, 10 May 2026). FACT: [lablab.ai](https://lablab.ai/ai-hackathons/amd-developer/spandan/voltwise-ai)
  - Parses bill PDFs (including Marathi MSEDCL bills) with Optical Character Recognition (OCR).
  - Shows slab impact, reconciles bills against a tariff engine, and runs what-if simulations.
  - **No weather normalisation or forward projection is mentioned.**
- **Bijli Bachao:** an online bill calculator for all states. FACT (title): [bijlibachao.com](https://www.bijlibachao.com/?p=71)
- **Bijli Book:** Android bill tracking with history and bill previews; no projection or slab alerts described. FACT: [Product Hunt](https://www.producthunt.com/products/bijli-book)
- **Studio Matrx AC star-rating savings calculator:** inputs are hours/day and months; **no city climate**. FACT: [Studio Matrx](https://www.studiomatrx.org/utilities/ac-star-rating-savings-calculator)
- **Cooler "smart humidity control"** appears in retail listings, e.g. Voltas Jetmax. FACT (listing title): [Croma](https://croma.com/voltas-jetmax-90-litres-desert-air-cooler-with-smart-humidity-control-dust-filter-white-/p/313545)
- **Car scrap services** such as Spinny. FACT (page exists): [Spinny](https://www.spinny.com/scrap-car/)

### Inferences

**Problem map: personal and household decisions**

| # | Decision | Decider | How often | Data that exists | Why the decision fails today | Is there a feedback loop? | Concept |
|---|---|---|---|---|---|---|---|
| 1 | How many AC or cooler hours fit this billing cycle | Bill-payer in a free-units state | Daily, Apr–Sep | Meter register, weather forecast, scheme rules (FACT) | The cliff is learned only from the bill. No projection exists (INFERENCE) | No | P-01 |
| 2 | Did my saving action work, or was it the weather? Is this bill plausible? | Any household | Monthly | Bill history, ERA5 weather (FACT) | Weather swamps behaviour. Smart-meter trust is low (FACT: UP) | No | P-02 |
| 3 | Which AC to buy, what size, how many stars | AC buyer | Once in 8–10 years | ISEER label; national bin hours (FACT) | Label efficiency assumes a national climate; buyers decide on price (FACT) | No | P-03 |
| 4 | What temperature to set the AC to | AC household | Nightly | IMAC; BEE 6%/°C (FACT) | People set 20–21 °C (FACT) and don't know their own comfort point | No | P-04 |
| 5 | Cooler, fan, or close the room up, hour by hour | Cooler household (14% nationally, 40% in UP) | Hourly, Apr–Sep | Hourly wet-bulb forecasts (FACT) | Humidity silently cancels evaporative cooling; no plan exists (INFERENCE) | No | P-05 |
| 6 | Which mode, when to leave, which route | Commuter, parent | Daily | Mode-exposure studies, AQ data (FACT) | Apps show ambient AQI, not personal dose; the biggest lever is invisible (INFERENCE) | No | P-06, P-10 |
| 7 | When to open windows at night | Non-AC household (about 83% of urban homes, INFERENCE from FACT) | Daily | Temperature and PM forecasts | Cool air and dirty air coincide overnight in north India (FACT diurnal; INFERENCE overlap) | No | P-07 |
| 8 | When to check on an elderly parent in heat | Remote adult child | Heatwave days | Forecasts; roof-type evidence (FACT) | District alerts don't translate to a specific home (INFERENCE) | No | P-08 |
| 9 | When to run shiftable loads | ToD/EV household | Daily | Tariff orders (FACT) | Small stakes; ToD for domestic users is patchy (FACT) | Partial (smart meter app) | P-09 |
| 10 | Keep, sell or scrap an old vehicle | Owner of a 10–15-year-old vehicle | Once | Rules and incentives (FACT) | Rules are fragmented by state and keep changing (FACT: Delhi pause) | No | P-11 |
| 11 | RO water: is it needed, and what to do with the reject | Urban RO household | Daily | 3:1 waste ratio (FACT) | Source TDS is unknown; reject water is invisible | No | P-12 |
| 12 | Which flat to rent | Renter or student | Every 1–2 years | Raster data (LST, DEM), AQ stations | Exposure is invisible at signing (INFERENCE) | No | P-13 |
| 13 | How much rice or dal to cook | Home cook | Per meal | User logs only | Over-cooking habit (HYPOTHESIS) | No | P-14 |
| 14 | Whether today's air is bad *for me* | People with asthma or allergies | Daily | AQ forecasts | Generic bands → alert fatigue (INFERENCE) | No | P-15 |

**Cross-cutting patterns**
1. **Discontinuities make environmental quantities salient.** About 25 lakh Delhi households fall off the 200-unit zero bill between spring and summer: 43.87 → 18.26 lakh (FACT). INFERENCE: a sizeable fraction sit within ±10% of the cliff, so they have both a strong rupee motive and a feasible kWh change. HYPOTHESIS: the shape of the distribution near the cliff is not public.
2. **Weather is the confounder households can't remove.** The same family's bill swings with the weather, so actions look as if they "didn't work", and smart-meter bills look suspicious (FACT: UP protests). Weather normalisation is a standard measurement-and-verification (M&V) practice (KNOWN: ASHRAE Guideline 14 / PRISM-style regression), but no Indian consumer packaging of it was found (INFERENCE; not exhaustive).
3. **National averages hide personal reality.** ISEER uses one national bin profile (FACT). IMAC gives a comfort band, not *your* setpoint (FACT). Mode-exposure ratios vary 3–4× between modes (FACT), yet AQI apps show one ambient number. INFERENCE: personalising a national parameter is a defensible, non-"AI wrapper" mechanism.
4. **Season matters for the video.** On 9 Oct, north India is entering smog season and leaving cooling season. South India and coastal cities are still warm. Heat and cooling concepts need either a live southern city or a **labelled replay** of May–June 2026 weather (ERA5) (INFERENCE).
5. **Cooking-fuel switching is not obviously "greener" on today's grid.** Rough calculation (INFERENCE, with stated assumptions):
   - Boiling 1 L of water from 25 °C takes 0.087 kWh of heat.
   - Induction at ~85% efficiency → 0.103 kWh × 0.71 kg/kWh ≈ **0.073 kg CO₂**.
   - LPG at an assumed ~55% stove efficiency → 0.0124 kg LPG × ~3.0 kg CO₂/kg ≈ **0.037 kg CO₂**.
   - The indoor-air benefits of induction are real (KNOWN), but the CO₂ case is weak, so no cooking-fuel concept is proposed.

### Gaps
- **Distribution of households near each scheme's cliff** (how many are at 180–220 units): not public in what I found.
- **Punjab's billing above the free limit** was not confirmed.
- **Telangana and Delhi tariff orders were not fetched.** Rules come from news reports and must be checked against the tariff orders and DISCOM pages before building.
- **Status of the AC 20–28 °C rule** in Oct 2026 is not established.
- **Smart-meter apps:** whether DISCOM apps (BESCOM, TGSPDCL, BSES, MSEDCL) already offer a cycle-end projection was not checked app by app. Treat "nobody projects the cliff" as INFERENCE.
- **OpenAQ India coverage** for 2025–26 and **WAQI India coverage** were not confirmed. Live API calls were blocked in this session.
- **Carpooling** (Quick Ride, sRide) and the post-2025 ride-hailing market were not researched. The mode-shift evidence base is thin.
- **No Indian study found on staple over-cooking** or on quick-commerce packaging per order.
- **Elderly people living with a spouse only** (as opposed to alone) were not found. The 5.7% living-alone figure is from 2017-18.
- **Building infiltration factors** (indoor/outdoor PM with windows open or closed) for Indian homes were not researched.

---

## Q2. Concept cards (P-01 … P-15)

### Takeaway

There are 15 concepts across Air (P-06, P-07, P-15), Heat & Water (P-05, P-08, P-12, P-13) and Waste & Energy (P-01, P-02, P-03, P-04, P-09, P-10, P-11, P-14). Most are cross-track.

The strongest are:
- **P-01 Cliff Guard + P-02 Bill X-ray.** They can merge into one plan → act → verify loop on the household electricity bill.
- **P-05 CoolerCheck:** wet-bulb-driven hourly cooler plan with a water ledger.
- **P-06 Dose Ledger:** personal inhaled dose with counterfactual mode/time swaps.

These have a specific mechanism, real public data plus user-owned inputs, and a result that is visible on screen.

### Cited Findings

Facts used in the cards are cited in Q1 or inline in each card. Field 9 of each card lists the data source and its access status.

### Inferences (concept cards; every claim tagged)

---

#### P-01 · Cliff Guard: "Will this month's bill fall off the free-units cliff, and how many AC hours can I still afford?"
**Track:** Waste & Energy (cross: Heat & Water)

1. **Problem:** In free-unit states, one unit over the line can turn a ₹0 bill into a full bill (Telangana: 201 units → pay all 201, FACT; Karnataka: >200 → full bill, FACT) or halve the subsidy (Delhi, 201–400 units, FACT). Households learn they crossed the line only when the bill arrives (INFERENCE).
2. **Primary user:** the bill-payer in a scheme household with a fan, cooler or AC in Delhi, Telangana, Karnataka, Punjab or Bihar. The same engine serves anyone near a telescopic slab boundary.
3. **Why it matters:**
   - Delhi zero-bill households fall by about 25.6 lakh from Feb to Jul 2025 (FACT, [Pioneer](https://www.dailypioneer.com/2025/state-editions/zero-power-bills-surge-under-8monthold-bjp-government.html)).
   - In Telangana, "numerous customers turned ineligible during the summer" (FACT, [DC](https://deccanchronicle.com/news/excess-use-of-power-affects-gruha-jyothi-beneficiaries-900090)); 42.25 lakh beneficiaries (FACT, [Siasat](https://www.siasat.com/telangana-free-electricity-scheme-beneficiaries-struggle-to-receive-zero-bill-3079517/amp/)).
   - Bihar has 1.67 crore families on 125 units (FACT); Punjab has about 90% zero bills (FACT).
   - Cooling is 40% of household kWh (FACT).
4. **Workarounds and alternatives:**
   - Waiting for the bill.
   - DISCOM apps showing past bills (KNOWN).
   - Smart-meter apps showing consumption to date (FACT: [SolarQuarter](https://solarquarter.com/2026/02/03/india-installs-over-5-28-crore-smart-meters-under-rdss-to-boost-power-sector-efficiency/)), but no weather-aware cycle-end projection against a scheme threshold was found (INFERENCE).
   - Bill calculators (Bijli Bachao, Bajaj Finserv) turn known units into rupees; they don't forecast (FACT exists, INFERENCE on function).
   - VoltWise AI parses past bills and runs what-ifs, with no forward weather projection mentioned (FACT, [lablab](https://lablab.ai/ai-hackathons/amd-developer/spandan/voltwise-ai)).
   - Some households read the meter by hand (HYPOTHESIS).
5. **Underlying insight:** The threshold is fixed and known, and cooling load is predictable from the weather. The real decision is a **budget of cooling hours for the rest of the cycle**, not a tip (INFERENCE).
6. **Mechanism:**
   1. The user photographs the meter at any point in the cycle; Bedrock vision reads the kWh register, and the user confirms.
   2. With 2+ readings (or the last bill's units plus its dates), fit daily kWh = base + β·CDH, where CDH = cooling degree-hours from the Open-Meteo history for the elapsed days.
   3. Project to the cycle end using the 16-day forecast.
   4. Apply the scheme rule engine (threshold, cliff type, slab rates) → **cliff margin** in units and ₹.
   5. Solve for an **appliance-hour budget**, e.g. "AC 1.5 t: ≤ 3.2 h/night for 11 nights, or 5 h at 27 °C", using the user's appliance wattages and BEE 6%/°C (FACT).
   6. EventBridge reminders prompt re-reads, which update the projection.
   7. At cycle end, log the outcome: kWh vs projection, ₹ kept.
7. **What is distinctive:** a **scheme-specific discontinuity** combined with a **weather-driven projection**, converted into an **hours budget** the household can follow.
8. **Why it isn't a new UI on an existing feature:** existing tools are retrospective (bill parsing, calculators) or show the meter's present state. The forecast-plus-cliff-plus-budget combination was not found (INFERENCE; DISCOM apps not exhaustively checked).
9. **Data and sources:**
   - Meter photos (user-provided).
   - Scheme and tariff rules: news sources above (FACT); **must be verified against current tariff orders** (Gap).
   - Open-Meteo forecast and historical data: free non-commercial (FACT).
   - Appliance wattage: user input or BEE label.
   - CEA emission factor for CO₂ (FACT).
10. **Architecture:**
    - Amplify-hosted mobile PWA (Hindi/English).
    - API Gateway → Lambda (`ingest`, `project`, `budget`).
    - Bedrock (vision) for meter OCR with a confidence score and a user-confirm step.
    - DynamoDB (households, readings, outcomes); S3 for photos.
    - EventBridge Scheduler for re-read nudges; SES email or web push (SMS in India needs DLT registration, KNOWN).
    - CloudWatch.
11. **Meaningful AWS use:** Bedrock vision does a job a human otherwise does (reading LCD registers that cycle through kWh, kVAh and MD). The Scheduler drives the loop. DynamoDB holds the time series. A Step Functions graph (read → validate → project → notify) can be shown on screen.
12. **Smallest useful MVP:** Telangana and Delhi rules; photo → reading → projection → budget slider; one re-read updates the forecast.
13. **Reproducible demo plan:**
    - A teammate photographs their own home meter (real).
    - The baseline comes from their last bill's units and dates (real).
    - A live October forecast plus a **labelled replay** of May 2026 (ERA5) shows the cliff in season.
    - No outside cooperation is needed.
14. **Strongest video moment:** a meter photo becomes "You'll reach **214 units on 28 May** → ₹0 becomes ₹1,0xx". Drag the AC-hours slider and the projection turns green at 196.
15. **Expected impact (evidence):**
    - The rupee stakes are FACT-based (full-bill rules).
    - kWh avoided per household is a HYPOTHESIS. International home-energy-report programmes show low single-digit % savings (KNOWN, not verified this session).
    - Risk: households far *below* the cliff may use their "headroom" (HYPOTHESIS, a rebound). Show the rebound honestly.
16. **Risks:**
    - *Technical:* meter OCR on varied LCDs; a noisy β with few readings; tariff-rule errors.
    - *Product:* useful mainly near the cliff; the October demo season.
    - *Competition:* DISCOM apps could add projections; bill analysers are a common LLM build (VoltWise exists).
17. **Why another team might build something similar:** "AI electricity bill analyser" is a stock prompt output, and slab calculators are easy.
18. **What would distinguish ours:** a forward, weather-aware **cliff-margin and hours budget**, rule packs for 5 states, and a verified end-of-cycle outcome. Nobody else's demo would say "you'll cross on 28 May".

---

#### P-02 · Bill X-ray: "Did my saving work, or was it just a cooler month? Is this bill plausible?"
**Track:** Waste & Energy

1. **Problem:** Households can't separate weather from behaviour or faults in their bills. A real saving can look like failure in a hotter month, and a faulty or disputed meter can't be challenged with evidence (INFERENCE; UP prepaid protests over "alleged excess billing", FACT).
2. **Primary user:** any household with 12+ months of bill history. Especially new AC buyers, people who changed setpoints or appliances, and smart-meter disputants.
3. **Why it matters:**
   - Cooling is 40% of household kWh (FACT).
   - In UP, 83 lakh prepaid meters were switched to postpaid after billing protests (FACT, [Outlook Business](https://www.outlookbusiness.com/economy-and-policy/up-govt-scraps-smart-prepaid-meter-system-shifts-all-consumers-to-postpaid-mode)).
   - A DISCOM home-energy-report pilot reached about 2 lakh BSES customers (FACT, [CEEW](https://www.ceew.in/blogs/how-can-electricity-tariff-reforms-empower-indian-households)).
4. **Workarounds and alternatives:**
   - DISCOM bill-history graphs (KNOWN).
   - VoltWise AI: bill parsing, slab impact, what-if; weather normalisation not mentioned (FACT).
   - Calculators (FACT).
   - Professional M&V (IPMVP Option C, ASHRAE Guideline 14) exists for buildings, not homes (KNOWN).
5. **Underlying insight:** 12–24 billing periods plus daily temperature are enough to fit a **change-point model** (baseload + cooling slope above a balance temperature). That model yields a **weather-adjusted counterfactual** for any later period, with an uncertainty band (KNOWN M&V method; INFERENCE on fit at household scale).
6. **Mechanism:**
   1. Upload bill photos or PDFs, or a screenshot of the DISCOM history table.
   2. Textract (AnalyzeExpense or Queries) or Bedrock vision extracts units and period dates.
   3. Fetch daily mean temperature for each period (Open-Meteo ERA5 or IFS).
   4. Grid-search the balance temperature Tb, then fit kWh/day = a + b·CDD(Tb).
   5. Outputs: baseload kWh/day (fridge, standby), cooling kWh by season, and implied AC-hours.
   6. **Verify an action:** the user marks "changed X on date D". The next bill is compared with the counterfactual ± the prediction interval → "saved 48 ± 15 kWh (₹, kg CO₂)", or "**can't tell yet**".
   7. **Plausibility check:** "this bill is 38% above the weather-expected value; check the meter or appliances."
7. **What is distinctive:** an honest counterfactual with an uncertainty band, and an explicit "can't tell" state, instead of a tip list.
8. **Why it isn't a new UI on an existing feature:** no Indian consumer tool found does weather-normalised verification (INFERENCE; not exhaustive).
9. **Data and sources:**
   - Bills (user).
   - Open-Meteo Historical (FACT: ERA5 from 1940, 5-day delay; IFS without delay).
   - CEA emission factor (FACT).
   - Tariff engine (shared with P-01).
10. **Architecture:**
    - Amplify PWA → S3 upload.
    - Step Functions: Textract → Lambda normaliser → Lambda fit (numpy/scipy layer) → DynamoDB.
    - Bedrock writes a plain-language explanation bound to computed numbers (no free-form numbers).
    - CloudWatch.
11. **Meaningful AWS use:** Textract is load-bearing (messy bills). The Step Functions graph is visible on screen. Bedrock is constrained to explanation only.
12. **Smallest useful MVP:** manual or table-screenshot entry; fit; decomposition chart; verify one marked action.
13. **Reproducible demo plan:**
    - Use 3–4 teammates' real bill histories from different cities and DISCOMs.
    - Show one plausibility flag.
    - Verification: use a real past change if a teammate had one; otherwise a **labelled** synthetic shift.
14. **Strongest video moment:** actual bars against the weather-expected line. The month after "raised AC to 26 °C" sits below the shaded band: "61 units saved, and not because of the weather".
15. **Expected impact (evidence):**
    - That verification improves the persistence of savings is a HYPOTHESIS.
    - The size of the saving depends on the actions taken (BEE 6%/°C, FACT).
16. **Risks:**
    - Few data points (bimonthly billing gives 6 a year) → wide bands.
    - Net-metered solar homes break the model.
    - Varied bill formats.
    - It can feel academic. Mitigation: pair it with P-01's forward budget.
17. **Why another team might build something similar:** "upload bill → AI insights" is generic.
18. **What would distinguish ours:** weather-normalised counterfactual with uncertainty, plus a "can't tell" state and a dispute-evidence PDF. **Recommended merge with P-01** as one product: **forward** (cliff budget) + **backward** (verified saving).

---

#### P-03 · AC Fit: "Which AC (stars, inverter, tonnage) is cheapest over 10 years *in my city, at my hours*?"
**Track:** Waste & Energy (cross: Heat & Water)

1. **Problem:** Star ratings come from ISEER, computed on **one national 1,600-hour temperature profile** (FACT, [CAG](https://www.cag.org.in/newsletters/public-newsense/indian-seasonal-energy-efficiency-ratio-iseer-overview)). A Chennai night-user and a Delhi afternoon-user face very different hours, so the 3-star vs 5-star and tonnage trade-off is mis-priced (INFERENCE).
2. **Primary user:** first-time AC buyers (13.3% ownership and growing; 40% of owned ACs are 3-star, FACT).
3. **Why it matters:**
   - Cost is a key purchase factor for nearly half of buyers (FACT).
   - The purchase locks in about 10 years of consumption (INFERENCE).
   - Peak demand has risen to 243 GW (FACT).
   - IndiaSpend headline: buyers are "choosing brands & features over energy efficiency" (FACT, headline only).
4. **Workarounds and alternatives:**
   - Studio Matrx calculator: hours × months, **no city climate** (FACT).
   - Retailer and fintech star guides (FACT exist).
   - BEE label annual-energy figure at the national profile (KNOWN).
5. **Underlying insight:** label values (ISEER, rated capacity, rated power) can be rescaled with **the user's city bin-hours in their usage window**. Room load sets tonnage.
6. **Mechanism:**
   1. Snap 2–3 BEE labels (store or Amazon screenshot); Bedrock vision extracts ISEER, capacity and power.
   2. Build a city bin profile: hourly temperature from Open-Meteo ERA5 for the last 5 years, restricted to the user's hours and months.
   3. Estimate seasonal load from a simple room load line (area, floor, orientation, roof exposure).
   4. Scale the label's seasonal consumption by the ratio of city to national bin load. Flag where part-load data is missing.
   5. Output 10-year kWh, ₹ (using the slab engine from P-01), CO₂ and a tonnage check.
7. **What is distinctive:** a city- and usage-specific recomputation of a national label.
8. **Why it isn't a new UI on an existing feature:** the existing calculator ignores climate (FACT).
9. **Data and sources:**
   - Label (user photo).
   - ISEER bins (FACT).
   - Open-Meteo ERA5 (FACT), or NASA POWER on AWS (FACT via 03, [registry](https://registry.opendata.aws/nasa-power/)).
   - BEE star-label product database: a web search portal, no API verified (Gap).
10. **Architecture:** PWA → Lambda; Bedrock vision; a precomputed city-bins table in DynamoDB, built by a Lambda batch from NASA POWER Zarr on S3; Amplify.
11. **Meaningful AWS use:** Bedrock vision, plus AWS Open Data (NASA POWER on S3) as the climate source. That is a visible "AWS data" story.
12. **Smallest useful MVP:** 3 cities, 2 labels, a 10-year cost card.
13. **Reproducible demo plan:** real Amazon listing screenshots of two models; compare Chennai, Delhi and Bengaluru.
14. **Strongest video moment:** the same two ACs: "5-star pays back in 2.8 years in Delhi and never in Bengaluru. The label can't tell you that."
15. **Expected impact (evidence):** better purchases reduce lifetime kWh (INFERENCE). Magnitude is a HYPOTHESIS that depends on physics simplifications.
16. **Risks:**
    - Part-load (inverter) behaviour isn't on the label → approximation credibility.
    - Low frequency (one-off decision).
    - October is outside the buying season (KNOWN: AC sales peak Mar–May).
    - Easily seen as "a calculator".
17. **Why another team might build something similar:** AC and solar calculators are common (05: calculators at 4/100).
18. **What would distinguish ours:** city bin-hour recomputation from the label photo; works as a module inside P-01/P-02.

---

#### P-04 · Setpoint Coach: "Find *your* comfortable AC setpoint in a week"
**Track:** Waste & Energy (alt: Heat & Water)

1. **Problem:** Most ACs run at 20–21 °C (FACT, BEE via [Business Standard](https://www.business-standard.com/india-news/india-standardise-air-conditioner-temperature-20-28-degree-celsius-125061001221_1.html)). Indians in AC buildings are neutral at 23.5–25.5 °C, and higher with fans (FACT, IMAC). Households don't know their own comfort point and fear trying (INFERENCE).
2. **Primary user:** urban AC households (17% of urban homes, FACT).
3. **Why it matters:** about 6% saving per +1 °C; 20→24 °C saves about 24%; 10 BU/yr nationally if half of users shift (FACT: BEE claim).
4. **Workarounds and alternatives:**
   - The 24 °C default (FACT).
   - Eco modes and brand apps with schedules (KNOWN).
   - Smart AC controllers such as Sensibo (KNOWN; hardware).
   - Awareness campaigns (KNOWN).
5. **Underlying insight:** comfort is adaptive and personal. The field-study method behind IMAC (thermal sensation votes against conditions) can be run as an **n-of-1 study** inside one household.
6. **Mechanism:**
   1. Prior: IMAC mixed-mode neutral temperature from the 30-day running-mean outdoor temperature (Open-Meteo).
   2. A nightly protocol steps the setpoint +0.5 °C every 2 nights and pairs it with fan speed.
   3. Each morning, a one-tap 7-point sensation vote plus sleep quality.
   4. A Bayesian update gives a personal neutral temperature and band.
   5. Output: a recommended schedule, including a pre-dawn raise as the outdoor temperature falls.
   6. Savings are estimated with 6%/°C and later verified with P-02.
   7. A smartwatch sleep score is an optional, unprioritised input.
7. **What is distinctive:** personal calibration of a published Indian comfort model.
8. **Why it isn't a new UI on an existing feature:** no consumer comfort-vote calibrator was found in India (INFERENCE).
9. **Data and sources:** Open-Meteo (FACT), IMAC equations (FACT), user votes.
10. **Architecture:** PWA; Lambda; DynamoDB; EventBridge Scheduler (nightly prompt, morning vote); Bedrock optional.
11. **Meaningful AWS use:** moderate. The Scheduler drives the protocol. AWS is not otherwise load-bearing (G partial).
12. **Smallest useful MVP:** a 7-night protocol, vote UI, and posterior chart.
13. **Reproducible demo plan:** only about 2 real nights are possible before submission. The rest must be a **labelled** simulated household, so the result can't truly be shown (F partial).
14. **Strongest video moment:** the posterior curve shifts: "Your family is comfortable at 26 °C with fan 3 → about 12% less AC energy (est.)".
15. **Expected impact (evidence):** 6%/°C (FACT: BEE claim). Whether households keep the setting is a HYPOTHESIS.
16. **Risks:**
    - The demo can't prove calibration in 48 h.
    - Off-season in the north.
    - Health caution for vulnerable people.
    - Noisy votes.
17. **Why another team might build something similar:** "AC tips chatbot".
18. **What would distinguish ours:** a calibrated personal neutral temperature with uncertainty. Best as a **feature of P-01** (the "how to stay under budget" lever) rather than a standalone entry.

---

#### P-05 · CoolerCheck: "Your cooler works till 6 PM today. After that it's just adding humidity."
**Track:** Heat & Water (cross: Energy)

1. **Problem:** Evaporative (desert or room) coolers cool only when the air is dry. The outlet temperature is bounded by the wet-bulb temperature (FACT, Studio Matrx). In humid hours (pre-monsoon evenings, monsoon, coastal cities), coolers keep using water and power while raising indoor humidity and heat stress. Users can't tell when to switch to fan-only, ventilate, or close up (INFERENCE).
2. **Primary user:** lower-middle-income households with coolers: 14% of households nationally (NSS 2020, FACT) and about 40% in UP (Prayas, FACT). Also hostels and PGs.
3. **Why it matters:**
   - About 8 million coolers are sold a year, with **no BEE label** (FACT, [Prayas](https://energy.prayaspune.org/space-conditioning-focus-on-fans-and-air-coolers-for-efficiency)).
   - Water use is 1.5–5 L/hour (FACT, weak source).
   - Humid-heat danger: Kolkata slum homes reach the elderly wet-bulb threshold for 3–4 hours a day (FACT, [Mongabay](https://india.mongabay.com/2025/06/too-hot-to-handle-as-rural-houses-turn-heat-traps/)).
4. **Workarounds and alternatives:**
   - Feel and habit.
   - Cooler "humidity control" knobs on some models (FACT, listing).
   - The Studio Matrx static calculator: manual inputs, no forecast, no hourly plan, no water accounting (FACT).
   - Weather apps show humidity but not cooler effectiveness (INFERENCE).
5. **Underlying insight:** Outlet T = T_db − ε (T_db − T_wb). With **hourly wet-bulb forecasts** this becomes a schedule. The physics is textbook; the hourly plan and water ledger are not offered to households (INFERENCE).
6. **Mechanism:**
   1. Fetch hourly T_db, RH and T_wb for the user's location (Open-Meteo).
   2. For each hour, compute cooler outlet temperature and the resulting indoor apparent temperature (heat index, with and without cross-ventilation), against fan-only (air-movement credit) and an AC option.
   3. Output a 24 h colour strip: **Cooler ON / Fan + windows / Close up, AC or rest**.
   4. Totals: **litres of water and kWh** for the plan against "cooler all day".
   5. An evening one-tap "was it comfortable?" learns the user's cooler ε (per-device calibration).
   6. A Scheduler notification fires when the cooler window closes.
7. **What is distinctive:** a forecast-driven psychrometric plan, a water and energy ledger, and per-cooler effectiveness learning.
8. **Why it isn't a new UI on an existing feature:** the only Indian calculator found is static, single-point and water-blind (FACT).
9. **Data and sources:** Open-Meteo forecast with hourly wet-bulb (FACT per 03 and the historical API docs; **live call not verified this session**); ERA5 for replay (FACT); cooler tank size and pump rating (user or sticker).
10. **Architecture:**
    - Amplify PWA in Hindi/English → API Gateway → Lambda planner.
    - DynamoDB (users, ε calibration).
    - EventBridge Scheduler for "switch now" pushes; optionally Bedrock vision to read the cooler sticker.
    - CloudWatch.
11. **Meaningful AWS use:** modest. Lambda, the Scheduler and DynamoDB carry the loop; Bedrock is optional (G partial). A Step Functions daily-plan pipeline can make it visible.
12. **Smallest useful MVP:** location → 24 h plan → water and kWh totals → one notification.
13. **Reproducible demo plan:**
    - Live October forecast for Jaipur (dry) against Kolkata or Chennai (humid).
    - A **labelled** replay of a June 2026 Delhi pre-monsoon day (ERA5) showing the mid-evening switch.
    - No hardware.
14. **Strongest video moment:** the same cooler on the same afternoon. Jaipur: outlet 27 °C, "Cooler ON". Kolkata: 33 °C and humidity rising, "Pump off, fan only: save 18 L today".
15. **Expected impact (evidence):**
    - Water saved = humid hours × 1.5–5 L (INFERENCE from FACT).
    - Heat-stress reduction is a HYPOTHESIS.
    - No field validation exists. State the ε assumption on screen.
16. **Risks:**
    - Room-level physics simplified.
    - Comfort is subjective.
    - October is off-season in the north.
    - Thin AWS story.
    - Judges may need the physics explained in 10 seconds (use the outlet-temperature gauge).
17. **Why another team might build something similar:** unlikely; "heat index app" is the nearest common build (05: heat alerts at 6/100).
18. **What would distinguish ours:** an hour-level *cooler* schedule from wet-bulb forecasts with a litres ledger. A distinct, India-specific, low-crowding Heat & Water entry.

---

#### P-06 · Dose Ledger: "Which of your trips gave you most of this week's PM2.5, and what single swap cuts it most?"
**Track:** Air (cross: mobility, Waste & Energy via transit)

1. **Problem:** Commuters see one ambient AQI number. Their inhaled dose depends far more on **mode, timing and duration**: in Delhi, rickshaw and walking exposure is about 3.6–3.7× the metro's (FACT), and cycling dose per minute is about 4.7× AC bus (FACT). They can't see which change matters most (INFERENCE).
2. **Primary user:** urban commuters, especially two-wheeler riders (52.3% of urban work trips, FACT, [NHTS](https://www.policyedge.in/p/two-wheelers-lead-work-trips-while-buses-carry-most-overnight-travel-mospi-survey-finds)), walkers, students (37% walk, FACT), and school-run parents.
3. **Why it matters:**
   - Mode exposure ratios (FACT: [Maji 2021](https://uwe-repository.worktribe.com/output/6946307); [IIT Roorkee 2023](https://www.pranaair.com/blog/prana-air-partnered-with-iit-roorkees-civil-engineering-dept-to-track-transport-pollution-in-delhi/)).
   - Active-mode dose per km is 4–8× that of motorised modes (FACT, [Vellore](https://research.vit.ac.in/pdf/postprint-commuter-exposure-concentrations-and-inhalation-doses-in-traffic)).
   - Delhi's diurnal swing is 1.8× (FACT).
4. **Workarounds and alternatives:**
   - AQI apps (IQAir, SAMEER, Google Maps AQI) show ambient levels (KNOWN).
   - Clean-route navigation projects are common (05: 5/100).
   - Academic dose tools abroad: HazeDose, PRAISE-HK (FACT exist).
   - Wearable monitors (KNOWN; hardware).
   - No Indian consumer dose ledger was found (INFERENCE).
5. **Underlying insight:** dose ≈ ambient × microenvironment factor(mode) × inhalation rate(activity) × minutes. The mode and time terms dominate and are documented by Indian studies, so a ledger plus a counterfactual can rank levers without a sensor.
6. **Mechanism:**
   1. Import 7 days of trips: Google Timeline on-device JSON (FACT); or quick manual entry; or live PWA GPS logging.
   2. Confirm the mode for each segment.
   3. Attach hourly ambient PM2.5: WAQI station data live; CAMS via Open-Meteo for the retrospective (coarse).
   4. Apply a **cited mode-factor table with ranges** and inhalation rates (FACT values).
   5. Per-trip dose (µg) → weekly ledger.
   6. A counterfactual engine enumerates feasible swaps (leave 45 min later, metro instead of auto, AC bus, different route segment) and ranks them by **dose avoided per extra minute**.
   7. The user commits to one swap; next week's ledger verifies it.
   8. Optional: smartwatch heart rate scales inhalation rate (no priority).
7. **What is distinctive:** **dose** (not concentration), a ranked **counterfactual** swap, and **next-week verification**.
8. **Why it isn't a new UI on an existing feature:** AQI apps and route apps don't compute personal dose or rank swaps (INFERENCE).
9. **Data and sources:**
   - Timeline export (FACT; gradual rollout and reported failures → manual fallback).
   - Open-Meteo AQ (FACT: 45 km, 3-hourly, from Aug 2022).
   - WAQI (FACT: real-time only, no history, no paid apps; India coverage unconfirmed).
   - OpenAQ on AWS (FACT; India coverage unverified).
   - Mode factors from 3 cited studies (FACT).
10. **Architecture:**
    - PWA → S3 (JSON) → Step Functions: parse → enrich AQ per trip-hour → dose → counterfactuals.
    - Amazon Location Service for alternative routes and times; DynamoDB.
    - Bedrock for a short narrative only.
    - Amplify; CloudWatch.
11. **Meaningful AWS use:** Step Functions pipeline, Location Service (routing and alternatives), and OpenAQ on AWS Open Data if India data is present. Strong and visible.
12. **Smallest useful MVP:** manual or Timeline import; ledger; top-3 swaps; one-week comparison (replayed).
13. **Reproducible demo plan:**
    - A teammate's own Timeline export or today's logged commute (real).
    - Ambient data is real.
    - Factors are cited on screen.
    - The "next week" verification is a **labelled** replay.
14. **Strongest video moment:** a ledger bar: "Your 8:40 auto ride = 41% of your week's dose. The 9:30 metro cuts it 63% for +6 min."
15. **Expected impact (evidence):**
    - Exposure reduction is plausible from the measured mode ratios (INFERENCE).
    - The health benefit is a HYPOTHESIS.
    - The emissions co-benefit exists only if the swap is to transit (INFERENCE).
16. **Risks:**
    - Ambient data is coarse (45 km), and WAQI has no history → retrospective precision is weak.
    - Mode factors are city- and season-specific.
    - Timeline export is flaky.
    - The Air track is the most crowded (05).
17. **Why another team might build something similar:** "pollution-aware route" is a classic maps + AQI combo.
18. **What would distinguish ours:** dose accounting with **cited Indian microenvironment factors**, re-time over re-route, and a verified week-over-week change.

---

#### P-07 · Window Planner: "Open the windows 11 PM–1 AM, not at dawn": trading night cooling against smog
**Track:** Air (cross: Heat & Water)

1. **Problem:** Non-AC homes cool down by opening windows at night. In north India's shoulder seasons, the coolest hours often coincide with the PM peak (overnight to 10 AM, FACT diurnal). RCC roofs keep releasing heat overnight (FACT). Families can't see the trade-off (INFERENCE).
2. **Primary user:** non-AC households in Indo-Gangetic plain cities (about 83% of urban homes lack an AC, INFERENCE from 17%); households with asthmatic children.
3. **Why it matters:** diurnal PM2.5 swings of about 1.8× (FACT); indoor heat in RCC homes (FACT); AC ownership is low (FACT).
4. **Workarounds and alternatives:** AQI apps (now); weather apps (temperature); purifier makers' "keep windows closed" advice (KNOWN). No planner was found (INFERENCE).
5. **Underlying insight:** ventilation is a scheduling problem over two forecast signals. Choose the hours that capture the most cooling per unit of PM let in.
6. **Mechanism:**
   1. A single-zone indoor model: indoor temperature relaxes towards outdoor with a time constant set by building type; indoor/outdoor PM factor for open vs closed windows (literature, Gap).
   2. Dynamic programming over 24 hours finds the open/close schedule that minimises a weighted heat + PM-dose cost.
   3. Weights come from household flags (asthma, elderly).
   4. Output: a schedule plus "price tags", e.g. "Open 23–01: bedtime 2.1 °C cooler, +18% indoor PM".
7. **What is distinctive:** a joint heat–air optimisation.
8. **Why it isn't a new UI on an existing feature:** none was found (INFERENCE).
9. **Data and sources:** Open-Meteo forecast and AQ (FACT; AQ is coarse); infiltration factors (Gap); user building inputs.
10. **Architecture:** PWA; Lambda optimiser; Scheduler reminders; DynamoDB.
11. **Meaningful AWS use:** modest (G partial).
12. **Smallest useful MVP:** a 24 h plan with a household-flag toggle.
13. **Reproducible demo plan:** live Delhi October forecast (warm days, smog onset). This is *timely* this week.
14. **Strongest video moment:** toggling "asthmatic child" flips the plan from dawn ventilation to late-evening only.
15. **Expected impact (evidence):** a HYPOTHESIS. **Without an indoor sensor there is no verification** (F partial).
16. **Risks:** unverifiable; model credibility; coarse AQ data.
17. **Why another team might build something similar:** rare.
18. **What would distinguish ours:** the explicit trade-off visual. Better as a **feature** inside P-05 or P-06 than as a standalone entry.

---

#### P-08 · Heat Buddy: "Call Amma at 2 PM, and ask these three questions"
**Track:** Heat & Water

1. **Problem:** Heat deaths concentrate among the elderly, often indoors in hot homes. Relatives elsewhere don't know when a parent's home becomes dangerous, and district alerts don't account for roof type or floor (INFERENCE from FACT).
2. **Primary user:** remote adult children and caregivers of elders. 5.7% of people aged 60+ live alone (FACT, LASI); more live with a spouse only (Gap).
3. **Why it matters:**
   - Ahmedabad 2010: 1,344 excess deaths, mostly over 65 (FACT, secondary).
   - +14.7% elderly mortality at the 97th-percentile temperature (FACT, secondary).
   - Indoor temperatures of 38.5–40 °C (FACT); 82% report symptoms (FACT).
   - Surveillance undercounts (FACT via 03).
4. **Workarounds and alternatives:** IMD and SACHET district alerts; HAP outreach via ASHAs (KNOWN); WhatsApp family groups (INFERENCE); medical-alert devices (KNOWN; hardware).
5. **Underlying insight:** indoor risk is predictable from the forecast plus roof, floor, ventilation, cooling assets and the person's risk factors. Caregivers need *when to call and what to ask*, not a map.
6. **Mechanism:**
   1. Home and person profile: roof type, top floor, cross-ventilation, cooling, age, medications such as diuretics.
   2. Indoor heat estimate using empirical roof offsets (labelled assumptions).
   3. Hourly indoor heat index for 3 days → risk tiers.
   4. Caregiver plan: call time plus a 3-question script (water intake, urine colour, dizziness).
   5. One-tap check-in log, with an escalation ladder (neighbour, move to a cooler room, nearest cooling centre).
7. **What is distinctive:** home-specific indoor risk translated into a caregiver protocol.
8. **Why it isn't a new UI on an existing feature:** no such tool was found (Gap: Indian elder-care apps were not searched).
9. **Data and sources:** Open-Meteo (FACT); roof evidence (FACT, limited); user inputs.
10. **Architecture:** Amplify; Lambda; DynamoDB; EventBridge Scheduler for check-ins; SNS or SES; Bedrock for the Hindi or regional script (bounded).
11. **Meaningful AWS use:** the Scheduler, SNS and Lambda form the loop (pass).
12. **Smallest useful MVP:** profile → 3-day risk → schedule → check-in log.
13. **Reproducible demo plan:** a teammate's grandparent profile, entered by us; a **labelled** May 2026 heatwave replay plus a live hot southern city.
14. **Strongest video moment:** the same forecast for two homes (ground-floor RCC vs top-floor tin) gives different plans, and a check-in ping arrives on the phone.
15. **Expected impact (evidence):** a HYPOTHESIS; elderly vulnerability is FACT.
16. **Risks:** medical-liability tone; a weak indoor model; season; it sits close to the crowded heat-alert cluster (05: 6/100).
17. **Why another team might build something similar:** heatwave alert bots are the default.
18. **What would distinguish ours:** indoor risk per home plus a call protocol, not a broadcast alert.

---

#### P-09 · Green Hours: shift washing, pumping, water heating and e-scooter charging into cheap, cleaner hours
**Track:** Waste & Energy

1. **Problem:** Time-of-day (ToD) tariffs exist in 23 states and 5 UTs across categories (FACT). Households don't know which loads can shift or what that saves.
2. **Primary user:** smart-metered ToD households (e.g. Maharashtra domestic: −₹0.80/unit, 9–5, FACT) and e-two-wheeler owners.
3. **Why it matters:** the stakes are small. Daytime charging avoids only about 10% CO₂, about 10 kg/yr per e-scooter (FACT, [CSEP](https://csep.org/working-paper/demystifying-the-climate-benefit-of-ev-transition-in-india/)). Goa deferred domestic ToD (FACT, headline).
4. **Workarounds and alternatives:** appliance timers; DISCOM notices (KNOWN).
5. **Underlying insight:** only a handful of household loads are shiftable.
6. **Mechanism:** appliance inventory → schedule against the ToD table and a solar-hour proxy → savings; verification via smart-meter app screenshots read by Bedrock.
7. **What is distinctive:** low.
8. **Why it isn't a new UI on an existing feature:** weakly; it is close to tariff explainers.
9. **Data and sources:** tariff orders (to verify); Electricity Maps India coverage unverified (FACT: free tier exists).
10. **Architecture:** PWA; Lambda; DynamoDB; Bedrock vision.
11. **Meaningful AWS use:** adequate.
12. **Smallest useful MVP:** inventory → schedule.
13. **Reproducible demo plan:** easy.
14. **Strongest video moment:** a weak "₹/month saved" card.
15. **Expected impact (evidence):** small (FACT-based).
16. **Risks:** low impact; patchy domestic ToD; I-13 ToD Shift was already evaluated earlier.
17. **Why another team might build something similar:** EV nudges are on the track page.
18. **What would distinguish ours:** little. **Fold into P-01** as a tip only.

---

#### P-10 · Mode Switch Trial: a 10-day randomised self-experiment on your own commute
**Track:** Waste & Energy (public transport; cross: Air)

1. **Problem:** Two-wheeler and car commuters assume transit is slower, costlier and worse. One-off calculators don't convince them, and they never test their own route (INFERENCE).
2. **Primary user:** urban two-wheeler or car commuters with a metro or bus option (two-wheelers carry 52.3% of urban work trips, FACT).
3. **Why it matters:** average commute cost is ₹785/month (FACT); exposure differs 1.6–3.7× by mode (FACT); emissions differ by mode (KNOWN; factors not verified).
4. **Workarounds and alternatives:** Google Maps, Chalo and transit apps give time estimates (KNOWN); commute-carbon calculators and gamified apps (05: 2/100).
5. **Underlying insight:** a short **ABAB self-trial** gives a believable *personal* answer with confidence intervals, and also works as a commitment device.
6. **Mechanism:**
   1. Baseline setup → a randomised 10-day schedule.
   2. One-tap start and stop GPS logging (PWA).
   3. Door-to-door time, cost, CO₂ (factors) and dose (P-06 engine).
   4. Paired comparison with a 90% CI → verdict card, e.g. "Metro: +7 ± 4 min, −₹38/day, −1.3 kg CO₂, −58% PM dose".
7. **What is distinctive:** experimental design and personal CIs.
8. **Why it isn't a new UI on an existing feature:** none was found (INFERENCE).
9. **Data and sources:** user GPS; fuel price (public but not verified); Open-Meteo AQ (FACT); CEA factor (FACT); vehicle emission factors (Gap).
10. **Architecture:** PWA plus Location Service; Lambda; DynamoDB; Step Functions nightly analysis; Bedrock summary.
11. **Meaningful AWS use:** good.
12. **Smallest useful MVP:** 2+2 logged trips, then analysis.
13. **Reproducible demo plan:** teammates can log 2–4 real trips between Fri and Sun (feasible), plus a **labelled** 10-day simulated set.
14. **Strongest video moment:** the result card with confidence intervals.
15. **Expected impact (evidence):** mode-shift persistence is a HYPOTHESIS.
16. **Risks:** small n; needs transit access; uses build time; may read as "carbon tracker".
17. **Why another team might build something similar:** commute-carbon apps.
18. **What would distinguish ours:** a randomised personal trial with CIs. **Pairs naturally with P-06.**

---

#### P-11 · Old Vehicle Exit Planner: keep, sell outside NCR, or scrap with a Certificate of Deposit?
**Track:** Waste & Energy (cross: Air)

1. **Problem:** Owners of ageing vehicles face shifting rules. Delhi's no-fuel rule was paused (FACT); scrappage concessions vary by state (FACT). They can't compute the best exit (INFERENCE).
2. **Primary user:** owners of 10–15-year-old vehicles, mostly in NCR.
3. **Why it matters:** about 6.2 million vehicles deregistered as ELVs (FACT); up to a 25% tax concession in about 21 states/UTs; more than 60 RVSFs; about 97k vehicles scrapped by Aug 2024 (FACT).
4. **Workarounds and alternatives:** scrap services (Spinny, FACT); RTO blogs; dealers' exchange offers (KNOWN).
5. **Underlying insight:** net present cost across options, combined with the legal clock and emissions.
6. **Mechanism:** RC photo → Bedrock extracts registration date and fuel → state rule engine → option table with NPV and emissions.
7. **What is distinctive:** moderate.
8. **Why it isn't a new UI on an existing feature:** partly; dealer tools cover a slice of it.
9. **Data and sources:** rules (curated, volatile); resale values (no API, Gap); RVSF list (not verified).
10. **Architecture:** PWA; Lambda; Bedrock vision; DynamoDB.
11. **Meaningful AWS use:** adequate.
12. **Smallest useful MVP:** Delhi plus one other state.
13. **Reproducible demo plan:** a family car's RC.
14. **Strongest video moment:** "Scrap now: +₹41k vs keep".
15. **Expected impact (evidence):** replacing old vehicles cuts per-km emissions (INFERENCE). The embodied emissions of the replacement are a confounder.
16. **Risks:** legal churn; resale data; NCR-heavy (D partial).
17. **Why another team might build something similar:** rare.
18. **What would distinguish ours:** a state rule engine with CoD maths. **Not recommended.**

---

#### P-12 · RO Reject Planner: "Your purifier throws away 14 L a day"
**Track:** Heat & Water

1. **Problem:** RO purifiers waste about 3 L per litre purified (FACT, [DTE](https://www.downtoearth.org.in/water/bengaluru-water-crisis-how-use-of-ro-purifiers-is-reversing-efforts-to-save-water-95079)). Many households may not need RO (NGT on TDS < 500, FACT). The reject water goes unused.
2. **Primary user:** urban RO households in water-stressed cities.
3. **Why it matters:** the 3:1 ratio (FACT); Bengaluru's supply gap (FACT).
4. **Workarounds and alternatives:** "zero-wastage" RO models (FACT claim); TDS controllers (KNOWN); DTE's reuse advice (FACT).
5. **Underlying insight:** drinking volume × recovery ratio is an invisible daily water budget.
6. **Mechanism:**
   1. Litres per day plus the RO spec (sticker → Bedrock) give the reject volume.
   2. A source-water TDS estimate (city or municipal report; an optional TDS pen the household already owns, given no priority) gives a keep-RO or alternative recommendation.
   3. A reuse plan plus a weekly bucket-count log.
7. **What is distinctive:** low to moderate.
8. **Why it isn't a new UI on an existing feature:** partially.
9. **Data and sources:** CGWB and municipal water quality (access not verified, Gap).
10. **Architecture:** PWA; Lambda; DynamoDB.
11. **Meaningful AWS use:** thin.
12. **Smallest useful MVP:** reject calculator plus reuse log.
13. **Reproducible demo plan:** a teammate's RO.
14. **Strongest video moment:** "5,100 L a year down the drain".
15. **Expected impact (evidence):** litres per household come from FACT ratios; behaviour change is a HYPOTHESIS.
16. **Risks:** health-advice liability; data weakness; self-reported verification.
17. **Why another team might build something similar:** water trackers (05: 4/100).
18. **What would distinguish ours:** little. **Not recommended.**

---

#### P-13 · Rent Check: a pre-lease heat, flood and air card for any flat
**Track:** Heat & Water (cross: Air)

1. **Problem:** Renters and students choose flats or PGs on rent and commute. Heat island, top-floor heat, waterlogging and nearby pollution are invisible until they are locked into an 11-month lease (INFERENCE).
2. **Primary user:** renters, students and migrant workers in metros.
3. **Why it matters:** urban flooding and heat (FACT via 03); RCC top-floor heat (FACT); monitor sparsity (FACT via 03). Rental market size not found (Gap).
4. **Workarounds and alternatives:** property portals' locality ratings (KNOWN; whether they show AQI or heat was not verified); Google Maps AQI layer (KNOWN).
5. **Underlying insight:** a flat-level comparison card built from open rasters plus building factors, with questions to ask the landlord.
6. **Mechanism:** address → geocode (Amazon Location) → summer Landsat surface temperature (30 m), relative elevation from the Copernicus DEM, distance to and annual PM of the nearest station, plus top-floor and orientation modifiers → a card comparing 2–3 flats.
7. **What is distinctive:** hyperlocal open-data exposure at the moment of the decision.
8. **Why it isn't a new UI on an existing feature:** portals don't show this (INFERENCE).
9. **Data and sources:** Landsat Collection 2 on AWS (KNOWN; requester-pays); Copernicus DEM on AWS Open Data (KNOWN); OpenAQ (FACT; India Gap). Not verified this session.
10. **Architecture:** batch pre-processing for 1–2 cities (Lambda or EC2) → cloud-optimised GeoTIFFs (COGs) in S3 → Lambda point query → Location Service → Amplify.
11. **Meaningful AWS use:** strong (Open Data, S3 and Location Service).
12. **Smallest useful MVP:** one city, two addresses.
13. **Reproducible demo plan:** two real Bengaluru addresses.
14. **Strongest video moment:** a side-by-side card: "Flat B: 4.1 °C hotter surface, low-lying".
15. **Expected impact (evidence):** reduced exposure for renters is a HYPOTHESIS; there is no emissions change.
16. **Risks:** GIS preparation time; surface temperature ≠ indoor temperature; per-city prep (D partial); no action loop after signing.
17. **Why another team might build something similar:** "climate risk map" builds.
18. **What would distinguish ours:** flat-level comparison at the moment of decision. Heavy for 48 h.

---

#### P-14 · Cook-Right: learn how much rice and dal *your* family actually eats
**Track:** Waste & Energy

1. **Problem:** Households over-cook staples and throw away leftovers. Existing trackers log waste but don't change the quantity cooked (HYPOTHESIS: no Indian study was found).
2. **Primary user:** home cooks in families.
3. **Why it matters:** household food waste is about 55 kg per person per year (FACT, secondary).
4. **Workarounds and alternatives:** food-waste trackers (04: at least 4 at First Commit, FACT); Too Good To Go and pantry apps (KNOWN).
5. **Underlying insight:** quantity cooked is a small forecasting problem (headcount, day of week, dish), learnable from a two-tap leftover log.
6. **Mechanism:** per meal, log planned quantity plus headcount; log leftover in katoris; a Bayesian per-dish, per-head model suggests "1.75 cups rice for 4 tonight", and tracks grams avoided.
7. **What is distinctive:** moderate.
8. **Why it isn't a new UI on an existing feature:** partially.
9. **Data and sources:** user logs only; food emission factors (Gap).
10. **Architecture:** PWA; Lambda; DynamoDB.
11. **Meaningful AWS use:** thin.
12. **Smallest useful MVP:** log plus suggestion.
13. **Reproducible demo plan:** a **labelled** seeded week plus a live log.
14. **Strongest video moment:** the suggestion adapts after the leftover log.
15. **Expected impact (evidence):** a HYPOTHESIS.
16. **Risks:** crowded space; logging burden.
17. **Why another team might build something similar:** food-waste apps are a staple build.
18. **What would distinguish ours:** cooking-quantity forecasting. **Not recommended.**

---

#### P-15 · Trigger Diary: learn the pollution level that sets off *your* asthma
**Track:** Air

1. **Problem:** Generic AQI bands cause alert fatigue (INFERENCE via 03). Sensitive people react at personal thresholds and combinations (PM with cold or humidity) that they can't learn by themselves.
2. **Primary user:** people with asthma or allergic rhinitis, and parents of asthmatic children.
3. **Why it matters:** Delhi's diurnal and seasonal exposure (FACT). Indian asthma prevalence was not researched (Gap).
4. **Workarounds and alternatives:** AQI apps' advice for sensitive groups; generic symptom diaries (KNOWN).
5. **Underlying insight:** an n-of-1 exposure–response curve from daily logs plus exposure gives a personal threshold, so the app alerts only on days predicted to exceed it.
6. **Mechanism:** daily one-tap symptom score plus reliever puffs; lagged PM, temperature and humidity features (Open-Meteo); a shrinkage logistic model gives a personal threshold → a forecast-based "your risk tomorrow" plus a monthly doctor summary.
7. **What is distinctive:** moderate to high.
8. **Why it isn't a new UI on an existing feature:** the diary is linked to local exposure (INFERENCE).
9. **Data and sources:** Open-Meteo (FACT); user logs.
10. **Architecture:** PWA; Lambda; DynamoDB; Scheduler; Bedrock for the doctor summary.
11. **Meaningful AWS use:** adequate.
12. **Smallest useful MVP:** log → threshold → alert.
13. **Reproducible demo plan:** needs weeks of logs, so a **simulated** dataset is unavoidable (F weak).
14. **Strongest video moment:** "Your threshold: about 140 µg/m³ when the night is below 14 °C".
15. **Expected impact (evidence):** a HYPOTHESIS; medical.
16. **Risks:** medical-claims risk; no real learning can be shown in 48 h.
17. **Why another team might build something similar:** AQI health bots (05: 10/100).
18. **What would distinguish ours:** a personal threshold. **Not recommended for this weekend.**

---

### Gaps (Q2)
- **No live API test was possible** (proxy and robots blocks). Wet-bulb in the Open-Meteo *forecast* endpoint, WAQI India coverage and OpenAQ India coverage must be confirmed with one call each before choosing P-05 or P-06.
- **Mode-specific microenvironment factors** come from 3 studies: two in Delhi in February and one in Vellore. Factors for other cities and seasons are not established.
- **BEE label fields** (whether annual consumption at 1,600 h is printed on current labels) were not verified for P-03.
- **Textract language support** for Indian bills (Hindi, Telugu, Kannada) was not verified (KNOWN: Textract targets Latin-script languages). Bedrock vision is the likely fallback.
- **SMS delivery in India** via SNS requires DLT registration (KNOWN, not verified). Plan for email or web push.

---

## Q3. Summary table and triage

### Takeaway

Three concepts clearly pass every constraint:
- **P-01 Cliff Guard + P-02 Bill X-ray** (merge as one Waste & Energy product).
- **P-05 CoolerCheck** (Heat & Water).

**P-06 Dose Ledger** is the best Air option but carries data-resolution risk.

Each has an India-specific mechanism a generic prompt wouldn't produce:
- scheme-cliff projection;
- weather-normalised verification;
- wet-bulb cooler scheduling;
- dose with cited mode factors.

Each can be demoed with teammates' own bills, meters, locations or commutes, plus labelled replays.

### Cited Findings
- The **crowded clusters** to avoid: AQI dashboards (10/100), flood alerts (9/100), waste classifiers (8/100), heat-alert bots (6/100); calculators and carbon trackers are moderate. FACT/INFERENCE: internal 05 overlap map.
- **A bill-analyser student project already exists** (VoltWise AI, May 2026, AMD hackathon). FACT: [lablab.ai](https://lablab.ai/ai-hackathons/amd-developer/spandan/voltwise-ai). P-01/P-02 must lead with *projection* and *verification*, not parsing.
- **The only evaporative-cooler and AC-star calculators found are static and climate-blind.** FACT: [Studio Matrx cooler](https://www.studiomatrx.org/utilities/evaporative-cooler-calculator), [Studio Matrx AC](https://www.studiomatrx.org/utilities/ac-star-rating-savings-calculator)

### Inferences

**Summary table.** Constraint key: A software-only · B 48 h · C data · D broad · E differentiation · F observable · G AWS. Ratings are preliminary, 1–10.

| ID | Name | Track | One-line mechanism | A | B | C | D | E | F | G | Distinct | Build 48h | Demo | Data | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-01 | Cliff Guard | W&E (×H&W) | Meter photo + weather-driven projection against the state's free-unit cliff → AC/cooler hours budget | pass | pass | pass | pass | pass | pass | pass | 7 | 8 | 8 | 8 | **Top pick**; rupee hook, millions of households; verify tariff rules; replay for season |
| P-02 | Bill X-ray | W&E | Change-point regression of bill history on cooling degree-days → weather-adjusted counterfactual: "saved X ± Y kWh" or "can't tell"; bill plausibility | pass | pass | pass | pass | pass | pass | pass | 7 | 7 | 7 | 8 | **Top pick as the verifier half of P-01** |
| P-03 | AC Fit | W&E (×H&W) | Label photo + city bin-hours replace the national ISEER profile → 10-year cost and tonnage | pass | pass | partial | pass | partial | pass | partial | 6 | 7 | 6 | 7 | Module inside P-01/P-02, not standalone |
| P-04 | Setpoint Coach | W&E (alt H&W) | IMAC prior + nightly setpoint steps + comfort votes → personal neutral setpoint | pass | partial | pass | pass | pass | partial | partial | 7 | 7 | 5 | 8 | Good lever; can't show calibration in 48 h; fold into P-01 |
| P-05 | CoolerCheck | H&W (×Energy) | Hourly wet-bulb forecast → cooler outlet temp → Cooler / Fan / Close-up schedule + litres and kWh ledger; per-cooler ε learning | pass | pass | pass | pass | pass | pass | partial | 8 | 9 | 7 | 9 | **Top Heat & Water pick**; thin AWS (add Step Functions/Scheduler); off-season in north |
| P-06 | Dose Ledger | Air (×mobility) | Trips × ambient PM × cited mode factor × inhalation rate → weekly dose; ranked swaps by dose avoided per minute; next-week verification | pass | partial | partial | pass | pass | pass | pass | 7 | 6 | 8 | 6 | **Best Air pick**; confirm AQ data with a live call; Air is crowded |
| P-07 | Window Planner | Air (×H&W) | 24 h optimisation of window opening, trading cooling degree-hours against PM let in | pass | pass | partial | pass | pass | partial | partial | 8 | 8 | 6 | 6 | Novel but unverifiable; feature of P-05/P-06 |
| P-08 | Heat Buddy | H&W | Home-specific indoor heat estimate → caregiver call schedule + check-in log + escalation | pass | pass | partial | pass | partial | pass | pass | 6 | 8 | 6 | 7 | Humane; near the crowded heat-alert cluster; weak indoor model |
| P-09 | Green Hours | W&E | Shiftable-load schedule against ToD table / solar hours | pass | pass | partial | partial | fail | partial | pass | 4 | 8 | 5 | 5 | Drop; small stakes (about 10 kg CO₂/yr per e-scooter) |
| P-10 | Mode Switch Trial | W&E (×Air) | Randomised ABAB commute self-trial → personal CIs on time, ₹, CO₂ and dose | pass | partial | pass | pass | pass | partial | pass | 7 | 6 | 6 | 7 | Interesting; small n; pair with P-06 |
| P-11 | Old Vehicle Exit | W&E (×Air) | RC photo + state rule engine → keep / sell / scrap NPV + emissions | pass | partial | partial | partial | partial | pass | partial | 5 | 6 | 5 | 5 | Drop; legal churn, NCR-heavy |
| P-12 | RO Reject Planner | H&W | Litres × recovery ratio → reject volume, need-for-RO check, reuse log | pass | pass | partial | pass | partial | partial | partial | 5 | 8 | 5 | 4 | Drop; source TDS unknowable without a meter |
| P-13 | Rent Check | H&W (×Air) | Address → 30 m surface temperature, DEM low-lying score, nearest-station PM → flat comparison card | pass | partial | partial | partial | pass | pass | pass | 7 | 5 | 7 | 6 | Strong AWS Open Data story, but GIS-heavy for 48 h |
| P-14 | Cook-Right | W&E | Leftover log → per-dish, per-head quantity forecast | pass | pass | pass | pass | partial | partial | partial | 5 | 9 | 5 | 9 | Drop; crowded food-waste space |
| P-15 | Trigger Diary | Air | Symptom log × lagged exposure → personal threshold → alerts only above it | pass | pass | pass | pass | pass | partial | partial | 6 | 7 | 4 | 8 | Drop for this weekend; needs weeks of logs; medical risk |

**Recommended triage (INFERENCE)**
1. **Bijli Budget: P-01 + P-02 (+ P-04 as a lever, P-03 as a module).** Track: Waste & Energy.
   - **Strongest overall.** Real rupee stakes backed by FACT scheme rules, and the Delhi summer drop of about 25 lakh zero-bill households.
   - Teammates' own meters and bills make the demo real.
   - AWS is load-bearing: Bedrock vision, Textract, Step Functions and the Scheduler.
   - It completes a plan → act → verify loop that 05 says almost nobody shows.
   - Main risks: rule accuracy, and October off-season (use a labelled summer replay).
2. **CoolerCheck (P-05).** Track: Heat & Water.
   - The most novel and cheapest build, in a low-crowding area.
   - Its weaknesses are a thin AWS story and the season (a live Jaipur vs Kolkata/Chennai comparison works today).
   - P-07's window logic could be added as a second screen.
3. **Dose Ledger (P-06, + P-10 as the "try it" mode).** Track: Air.
   - The best demo moment ("41% of your week's dose").
   - Proceed only if a live call confirms usable station-level history for India (OpenAQ) or the team accepts CAMS at 45 km with clear labelling.

### Gaps
- All ratings are preliminary and desk-based. No user interviews were run.
- The rupee and kWh impacts of every concept are HYPOTHESES until a field test is done.
- Whether judges, as technically strong generalists (INFERENCE per 00), will value the M&V/psychrometric mechanism without a 10-second explainer is untested. Script the explainer.
