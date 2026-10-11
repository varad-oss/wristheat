# 03 — Environmental Problem Landscape (India, Oct 2026)

**Tags:**
- **FACT:** sourced; the link is in Sources.
- **INFERENCE:** reasoned from facts.
- **HYPOTHESIS:** plausible, needs validation.

**Lens:** we are looking for *problems*, not products. For each track we ask:
- Who hurts?
- What do they do today?
- What data exists, and how fresh is it?
- Where does behaviour fail to change?

---

## TRACK 1 — AIR

### Pain points

| Pain point | Tag | Detail |
|---|---|---|
| Chronic exposure in the Indo-Gangetic plain | FACT | 2025 annual PM2.5: Byrnihat 100 µg/m³, **Delhi 96**, Ghaziabad 93. 103 of 231 cities with adequate data exceeded the PM2.5 standard; 190 of 229 exceeded PM10 |
| National Clean Air Programme (NCAP) under-delivery | FACT | Of 100 NCAP cities with enough PM10 data, 51 met the initial 20–30% target, 23 met the revised 40% target, and **23 got worse**. ~74% of released funds were used (₹9,929 cr of ₹13,415 cr) |
| Monitoring gaps | FACT | **565 continuous stations** and 1,035 manual stations across 584 cities. **28 of 130 NCAP cities have no continuous monitor**. Manual stations are 465 short of target. Siting and maintenance problems are documented |
| Episodic emergency days | FACT | Delhi-NCR's Graded Response Action Plan (GRAP) escalates restrictions by AQI. In Dec 2024 the Commission for Air Quality Management (CAQM) moved **hybrid schooling up to Class V** into the "Severe" band. On 11 Nov 2025, GRAP Stage III triggered hybrid classes up to Class V in Delhi (per headlines) |
| Stubble burning, falling but persistent | FACT | Fire counts, 15 Sep–3 Nov: **Punjab 2,518 (2025) vs 4,132 (2024)**; Haryana 145 vs 857. Enforcement: 946 FIRs and ₹52.75 lakh in environmental compensation in Punjab |
| Time-of-day blindness | FACT | Delhi winter PM2.5 (US Embassy monitor, Dec 2015–Jan 2016): **overnight to 10 AM mean ~302 µg/m³**, falling to a **~169 µg/m³ low around 4–5 PM**, about 1.8× different within one day |
| Same-day exposure is mostly a timing problem | INFERENCE | Morning walks, school assemblies, PE periods and dawn commutes fall in the worst window of a winter day. AQI apps show "the AQI now", not *when today is least bad*. |

### Underserved users (INFERENCE unless tagged)

- **School heads and PE coordinators** in NCR, who decide daily about assemblies, sports and outdoor breaks.
  - GRAP gives them binary directives (hybrid or not), not hour-by-hour guidance.
- **Elderly morning walkers**, whose habit coincides with the worst hours.
- **Outdoor workers** (traffic police, vendors, construction), who can't avoid exposure but could re-time tasks.
- **Small towns without monitors** (FACT: 28 NCAP cities lack continuous monitors).
- **Asthmatic children and their parents.**

### Existing workflows

- CAQM declares a GRAP stage, the state education department issues a circular, and schools comply.
- Citizens check AQI apps (SAMEER, IQAir, Google). Some buy purifiers and masks.
- City agencies sprinkle water, deploy anti-smog guns and penalise dust (INFERENCE from GRAP measures).

### Data

| Source | What | Freshness and limits | Tag |
|---|---|---|---|
| CPCB continuous stations (CAAQMS) | Hourly pollutants | Real-time on CPCB portals. The data.gov.in "Real-time AQI" resource page states **no API exists** for it (checked 8 Oct) | FACT |
| **OpenAQ on AWS** (`s3://openaq-data-archive`, us-east-1) | Aggregated global measurements | Daily gz-CSV archive plus API; licence varies by provider; no AWS account needed | FACT |
| CAMS forecast via Open-Meteo Air Quality API | PM2.5, PM10, dust, AQI, up to 7 days | For India: **global domain, ~45 km, 3-hourly**. Too coarse for street- or school-level decisions; useful for trend | FACT |
| NASA FIRMS (VIIRS/MODIS fires) | Active fire detections | Near-real-time | Not verified this session |
| Sentinel-5P (NO₂ etc.) on AWS Open Data | Satellite columns | Daily, coarse; column ≠ surface | Not verified this session |

### Measurement limitations

- **Spatial:** sparse monitors; one station often stands for a whole neighbourhood (FACT, siting issues documented).
- **Temporal:** forecasts are coarse for India (FACT, 45 km / 3-hourly).
- **Low-cost sensors** need calibration, and humidity biases PM readings (INFERENCE).

### Behavioural barriers (INFERENCE)

- **Alert fatigue:** in Nov–Jan, "Very Poor" is the default, so daily alerts are ignored.
- **No actionable alternative:** "stay indoors" isn't a plan for a school or a worker.
- **Habit:** morning walks and assemblies are fixed rituals.

### Infrastructure limitations

- No open real-time CPCB API (FACT).
- School buildings are not sealed; purifiers are scarce in government schools (HYPOTHESIS).

### Campus, city and rural angles

| Setting | Angle | Tag |
|---|---|---|
| Campus | Outdoor sports schedules, hostel ventilation, and events in Oct–Jan smog | INFERENCE |
| City | NCR's GRAP machinery is a ready-made institutional trigger | FACT |
| Rural | Stubble fires (FACT); household solid-fuel smoke | HYPOTHESIS: not researched in depth |

---

## TRACK 2 — HEAT & WATER

### Heat: pain points

| Pain point | Tag | Detail |
|---|---|---|
| Heat illness at scale, badly counted | FACT | 2024: ~48,000 suspected heatstroke cases and 159 deaths in Integrated Disease Surveillance Programme (IDSP) data. 2025 (1 Mar–24 Jun): **7,192 suspected cases, 14 confirmed deaths**; Andhra Pradesh had 4,055 of those cases. Experts say surveillance captures only a fraction. For 2015–22, NCDC counted 3,812 deaths and NCRB counted 8,171 |
| Labour productivity | FACT | ILO projects India will lose **5.8% of working hours in 2030**, equivalent to ~34 million full-time jobs. *The Lancet* estimated **181 billion potential labour hours** lost in 2023 (~₹13 lakh crore income) |
| No national worker heat standard | FACT | Only Tamil Nadu's factory rules set temperature limits. Heatstroke is not an occupational disease under ESI. Most heat action plans say little about outdoor workers |
| Heat action plans are weak | FACT | The Centre for Policy Research (CPR) reviewed **37 HAPs** in 2023 (9 city, 13 district, 15 state). Most were not localised, poorly targeted vulnerable groups, were underfunded, and had weak legal backing |
| Informal workers have no buffers | FACT | Of 519 street vendors surveyed by WIEGO, **89% had no free drinking water** and 90% cut working hours. 87% of 115 garment workers reported heat symptoms |
| Existing financial instrument | FACT | SEWA's parametric heat insurance covered ~50,000 women in 2024 and paid nearly ₹5 cr |

### Heat: underserved users

- **Construction site supervisors and contractors**, who decide shift timing and breaks, with no tool or standard (INFERENCE from the FACT gap).
- **Gig and delivery riders** (HYPOTHESIS).
- Street vendors (FACT, survey).
- Elderly people living alone (INFERENCE).

### Water: pain points

| Pain point | Tag | Detail |
|---|---|---|
| Groundwater depletion | FACT | Central Ground Water Board (CGWB) 2025 assessment: 6,762 units, of which **730 over-exploited (10.8%)**, 201 critical, and 758 semi-critical. National extraction stage is **60.63%** |
| Tanker dependence and price shocks | FACT | In the Bengaluru 2024 crisis, prices hit ₹1,800–2,000 per 12,000 L. The district capped them at **₹600 / 6,000 L within 5 km** (₹1,000 / 12,000 L), for four months |
| Network losses (non-revenue water, NRW) | FACT | Urban India loses ~**38% of potable water** to NRW against a 15–20% global benchmark: **Delhi ~58%**, Mumbai ~30%. Only ~50% of urban households have functional meters. Losses push households to tankers and groundwater |
| Urban flooding | FACT | Bengaluru had severe 2025 pre-monsoon waterlogging. Chennai's 2015 floods caused >₹15,000 cr in damage. Mumbai's drains were designed for 25 mm/hr. Bengaluru has lost or degraded ~80% of its historic lakes (as cited) |

### Water and floods: existing workflows

- Tankers are booked by phone or WhatsApp through society managers (INFERENCE).
- Flood alerts come from IMD/state agencies and Google Flood Hub (riverine) (INFERENCE/known).
- City helplines handle waterlogging complaints.

### Data

| Source | What | Freshness and limits | Tag |
|---|---|---|---|
| **Open-Meteo forecast API** | Hourly temperature, humidity, dew point, **wet-bulb temperature**, wind, shortwave/direct/diffuse radiation, global tilted irradiance (GTI), precipitation and probability | Up to 16 days; free for non-commercial use; no key | FACT |
| ECMWF **thermofeel** (Apache-2.0) | Wet-bulb globe temperature (WBGT, incl. Liljegren physical method), UTCI, heat index | Python library | FACT |
| **NASA POWER on AWS** (`s3://nasa-power` Zarr, us-west-2, CC BY 4.0) | Meteorology and solar; hourly solar from 2001 | Updated nightly; solar latency ~5–7 days | FACT |
| CGWB / India-WRIS | Groundwater levels and assessments | Periodic | Access not verified |
| IMD | Warnings, gridded data | Limited open APIs | INFERENCE |

### Measurement limitations

- **WBGT is rarely measured on Indian sites.** It must be *estimated* from forecasts, with error. INFERENCE: acceptable for planning, not for compliance.
- **Heat deaths are under-counted** (FACT).
- **Tanker volumes are unverified** at delivery (HYPOTHESIS, consistent with the price-gouging FACT).

### Behavioural barriers (INFERENCE)

- Workers skip breaks for fear of missing targets (FACT for garment workers).
- Supervisors optimise output, not exposure.
- Water is invisible until the tap runs dry.

### Campus, city and rural angles

| Setting | Angle | Tag |
|---|---|---|
| Campus | Construction on campuses; sports in heat | INFERENCE |
| City | Waterlogging hotspots; NRW is a city-utility problem | INFERENCE / FACT |
| Rural | Groundwater over-exploitation is concentrated in agricultural blocks; drought | INFERENCE |

---

## TRACK 3 — WASTE & ENERGY

### Waste: pain points

| Pain point | Tag | Detail |
|---|---|---|
| Volume | FACT | ~1.85 lakh tonnes of municipal solid waste per day (CPCB 2023–24) |
| New legal regime from 1 Apr 2026 | FACT | The Solid Waste Management (SWM) Rules 2026 mandate **four-stream source segregation**: wet, dry, sanitary, special-care |
| Bulk waste generators | FACT | Under SWM 2026: ≥20,000 m² floor area, or ≥40,000 L/day water use, or ≥100 kg/day waste. **This includes residential societies and universities**, about 30% of waste. They must process wet waste on site or obtain a responsibility certificate (EBWGR). A **central online portal** replaces paper reporting, and environmental compensation applies for non-compliance |
| Informal recyclers carry the system | FACT | An estimated **1.5–4 million waste pickers** manage **60–70% of urban recyclables**; ~70% of plastic recycling depends on them. Most earn under ₹10,000/month, and EPR largely bypasses them. SWaCH (Pune) has 4,000+ pickers serving ~1M households |
| E-waste | FACT | **13.97 lakh tonnes** generated in 2024–25, up from 12.54 |

### Energy: pain points (rooftop solar emerged as unusually under-served)

| Pain point | Tag | Detail |
|---|---|---|
| Scale | FACT | PM Surya Ghar reached **50.06 lakh households and ~14.8 GW** by July 2026. It added **5.06 lakh homes in July alone** (~1 lakh every six days). ₹28,024 cr of subsidy has been paid; the target is 75 lakh by Dec 2026 |
| **Generation blind spot** | FACT | The government tracks *installations*, not *generation*. Data sits fragmented in consumer and DISCOM systems. MNRE mandated SIM-based M2M monitoring for PM Surya Ghar systems (Dec 2025), but **only for new installs**. Vendor-neutral protocol testing began Sept 2025 with no implementation date. The existing ~23 GW is unmonitored |
| Owners stop watching | FACT | An industry MD estimates ~99% of consumers stop monitoring after installation. Owners contact vendors only after a fault |
| A maintenance right owners don't know about | FACT | Empanelled vendors must provide **free maintenance for five years** as a subsidy condition. **Many consumers don't know** this |
| Soiling silently eats output | FACT | IIT Bombay simulation (Mumbai): soiling accumulates **~0.4% per day** in the dry season. Uncleaned panels could fall to ~50% of nameplate in ~120 days. Monthly cleaning costs ~4% a year. Dust and droppings cut output 5–30%. Dust-heavy states (Rajasthan, Gujarat, Haryana) need more frequent cleaning |
| Complaint and warranty machinery now exists | FACT | MNRE's SOP of 22 Jun 2026: vendors get 8 + 7 days to respond, then a show-cause notice, then **portal deactivation**. Listed violations include **failure to provide promised maintenance**. The module warranty SOP of 6 May 2026 sets 10-year product and **25-year power output** warranties, NABL testing, and 30-day repair or replacement |
| Disputes reach courts | FACT | A consumer court ordered a firm to pay ₹25,265 when rooftop solar failed promised savings (Jul 2026 headline) |
| Generation rule of thumb | FACT | 1 kW yields ~4–5.5 units/day on a clear day (press summary) |
| Grid emission factor | FACT | CEA database v22 (Aug 2026): **0.710 tCO₂/MWh (FY24-25), 0.675 (FY25-26)**. Every lost solar kWh is largely replaced by this grid mix |
| Time-of-day tariffs | FACT | Since 1 Apr 2025, smart-metered consumers other than agricultural ones fall under time-of-day tariffs: solar hours 10–20% cheaper, peak 10–20% costlier. INFERENCE: rollout depends on state regulators and smart-meter coverage |

### Impact arithmetic (INFERENCE)

1. 14.8 GW × ~1,400 kWh/kW/year ≈ **20.7 TWh/year** expected from PM Surya Ghar rooftops.
2. If the average realised loss from soiling and faults is 10%, that is ≈ 2.1 TWh/year of clean power lost.
3. At ~0.68–0.71 t/MWh, that is ≈ **1.4–1.5 million tCO₂/year** extra.

The 10% figure is a HYPOTHESIS, consistent with the 5–30% FACT range. State it as an assumption on screen.

### Underserved users

- **First-time rooftop solar owners** with no technical background and a vendor that has moved on (INFERENCE from FACTs).
- **Campus and RWA facility managers** facing new SWM 2026 obligations (INFERENCE).
- **Waste pickers** (FACT, excluded from EPR).

### Existing workflows

| User | Today | Tag |
|---|---|---|
| Solar owner | Glances at the inverter app or display, sees a number with no benchmark, calls the vendor only if it hits zero | INFERENCE, consistent with the FACT quote |
| BWG (society or campus) | Hires a composting vendor or ignores it; paper registers (pre-2026) | INFERENCE |
| Household waste | Mixed bins collected by municipal or contractor trucks; kabadiwala buys dry recyclables | INFERENCE |

### Data

| Source | What | Freshness and limits | Tag |
|---|---|---|---|
| **Open-Meteo Satellite Radiation API** | **Himawari and EUMETSAT IODC cover India**; ~5 km; hourly or native 10–15 min; GHI, DNI, DHI; **GTI with panel tilt and azimuth** | Latency ~30 min (Himawari) to ~2 h | FACT |
| **NASA POWER on AWS** | Long-term solar climatology and hourly irradiance for baselines | Latency 5–7 days for solar | FACT |
| Inverter displays and apps | Daily and lifetime kWh. Brand-specific clouds; screens visible to the owner | — | INFERENCE |
| CEA CO₂ baseline v22 | Emission factor | Annual | FACT |
| PM Surya Ghar portal | Installs, vendors, complaints (GMS) | **Not generation** | FACT |

### Measurement limitations

- Satellite irradiance carries ~5–10% daily error (INFERENCE from typical satellite products). This is fine for detecting 15–30% shortfalls, but not 2% ones.
- Net-metering bills show import and export, not gross generation. Self-consumption never crosses the meter (INFERENCE from how net metering works). **The inverter is the honest source.**

### Behavioural barriers (INFERENCE)

- Solar is "installed and forgotten", and any shortfall is invisible because the bill still drops.
- Cleaning a roof is a chore without a trigger.
- Owners don't know their rights (FACT: they don't know about the 5-year maintenance).

### Campus, city and rural angles

| Setting | Angle | Tag |
|---|---|---|
| Campus | Universities are BWGs under SWM 2026 (FACT); campus rooftop solar; e-waste drives (INFERENCE) | FACT / INFERENCE |
| City | RWAs are BWGs (FACT); urban rooftop solar is concentrated in cities (INFERENCE) | FACT / INFERENCE |
| Rural | PM-KUSUM solar pumps; informal e-waste processing | HYPOTHESIS: not researched |

---

## Cross-track synthesis

1. **Measurement exists but action doesn't:**
   - Rooftop solar has inverter counters but no expected baseline or follow-through.
   - AQI has station data but no "when today" answer.
   - Heat has forecasts but no work-rest plan.
2. **New rules created new obligations** without tools:
   - SWM 2026 for bulk waste generators.
   - MNRE's complaint and warranty SOPs (2026).
   - Time-of-day tariffs (2025).
3. **The person who decides is rarely the person the apps target.** Supervisors, principals and owners decide; apps talk to "citizens".
4. **Data gaps judges won't know about** are a pitch asset:
   - No open CPCB real-time API.
   - Coarse CAMS data for India.
   - The national generation blind spot.

---

## Sources

- **Air**
  - CREA, [Tracing the Hazy Air 2026, NCAP progress report (9 Jan 2026)](https://energyandcleanair.org/publication/2026-progress-report-on-national-clean-air-programme/)
  - The Tribune, [GRAP revised: hybrid learning till Class V in Severe AQI (Dec 2024)](https://www.tribuneindia.com/news/delhi/grap-rules-revised-nod-to-hybrid-learning-till-class-v-in-severe-aqi/amp)
  - Business Today, [GRAP-3: Delhi schools hybrid up to Class 5 (11 Nov 2025)](https://www.businesstoday.in/amp/india/story/grap-3-restrictions-in-delhi-schools-directed-to-hold-classes-in-hybrid-mode-for-children-upto-class-5-501666-2025-11-11)
  - r.i.c.e., [Hourly variation in PM2.5 in Delhi, Dec 2015–Jan 2016](https://riceinstitute.org/maps/hourly-variation-in-pm-2-5-in-delhi-december-2015-january-2016/)
  - The Tribune, [Sharp drop in stubble burning incidents, CAQM (4 Nov 2025)](https://www.tribuneindia.com/news/punjab/sharp-drop-in-stubble-burning-incidents-in-punjab-haryana-caqm)
  - Open Government Data, [Real-time AQI resource (no API)](https://www.data.gov.in/resource/real-time-air-quality-index-various-locations)
  - [OpenAQ on the AWS Registry of Open Data](https://registry.opendata.aws/openaq/)
  - [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)
- **Heat & water**
  - PTI via The Week, [7,192 suspected heatstroke cases, Mar–Jun 2025 (RTI)](https://www.theweek.in/wire-updates/national/2025/07/27/del4-climate-heat-rti.html)
  - Newslaundry/IndiaSpend, [Informal workers have little heat protection (13 Apr 2026)](https://www.newslaundry.com/amp/story/2026%2F04%2F13%2Fas-india-braces-for-summer-informal-workers-have-little-heat-protection)
  - CPR, [How is India adapting to heatwaves? (27 Mar 2023)](https://cprindia.org/briefsreports/how-is-india-adapting-to-heatwaves-an-assessment-of-heat-action-plans-with-insights-for-transformative-climate-action/)
  - ETV Bharat, [Nearly 11% of groundwater units over-exploited (21 Jul 2026)](https://www.etvbharat.com/en/bharat/nearly-11-per-cent-groundwater-assessment-units-over-exploited-govt-enn26072007475)
  - Business Today, [Bengaluru fixes water tanker rates (7 Mar 2024)](https://businesstoday.in/india/story/bengaluru-water-crisis-district-administration-fixes-rates-for-water-tanker-services-420502-2024-03-07)
  - ORF, [The cost of leakage (24 Aug 2025)](https://www.orfonline.org/expert-speak/the-cost-of-leakage-how-water-losses-fuel-unsustainable-choices)
  - Drishti IAS, [Urban flooding in India (29 May 2025)](https://www.drishtiias.com/daily-updates/daily-news-analysis/urban-flooding-in-india/print_manually)
  - [Open-Meteo forecast API](https://open-meteo.com/en/docs)
  - [ECMWF thermofeel](https://github.com/ecmwf/thermofeel)
  - [NASA POWER on the AWS Registry of Open Data](https://registry.opendata.aws/nasa-power/)
- **Waste & energy**
  - Drishti IAS, [SWM Rules 2026 (29 Jan 2026)](https://www.drishtiias.com/daily-updates/daily-news-analysis/solid-waste-management-swm-rules-2026/print_manually)
  - Down To Earth, [India's waste economy runs on invisible workers (15 May 2026)](https://www.downtoearth.org.in/amp/story/waste/indias-waste-economy-runs-on-invisible-workers-climate-policy-keeps-forgetting-them)
  - UNI, [13.97 lakh tonnes e-waste in 2024-25 (CPCB, Lok Sabha)](https://test.uniindia.com/over-13-97-lakh-tonnes-e-waste-generated-in-2024-25-cpcb-data/parliament/news/3542425.html)
  - SolarQuarter, [PM Surya Ghar crosses 50 lakh installations (7 Aug 2026)](https://solarquarter.com/2026/08/07/pm-surya-ghar-scheme-crosses-50-lakh-rooftop-solar-installations-adds-record-5-06-lakh-homes-in-july-2026/)
  - Energetica India, [75 lakh households targeted by Dec 2026 (headline)](https://www.energetica-india.net/news/75-lakh-households-targeted-for-rooftop-solar-installations-under-pm-surya-ghar-by-dec-2026-joshi)
  - Down To Earth, [Rooftop solar's generation blind spot (24 Dec 2025)](https://www.downtoearth.org.in/amp/story/energy/as-rooftop-solar-scales-up-india-confronts-a-generation-blind-spot)
  - ETV Bharat, [Rooftop solar maintenance a challenge (7 Jul 2026)](https://etvbharat.com/en/bharat/rooftop-solar-push-under-pm-surya-ghar-yojana-crossed-37-lakh-but-maintenance-a-challenge-enn26070705272)
  - SolarQuarter, [MNRE complaint SOP for PM Surya Ghar vendors (25 Jun 2026)](https://solarquarter.com/2026/06/25/mnre-introduces-strict-sop-to-address-consumer-complaints-against-solar-vendors-under-pm-surya-ghar-scheme/)
  - JSA, [MNRE SOP on module warranty claims (May 2026)](https://www.jsalaw.com/wp-content/uploads/2026/05/JSA-Prism-Energy-May-2026-SOP-on-warranty-claims.Final_.pdf)
  - pv magazine India, [The impact of dust on solar panels (Jul 2021)](https://www.pv-magazine-india.com/2021/07/10/the-long-read-the-impact-of-dust-on-solar-panels-matters)
  - Business Today, [Court orders firm to pay after rooftop solar fails promised savings (6 Jul 2026)](https://www.businesstoday.in/latest/trends/story/rooftop-solar-failed-to-deliver-promised-savings-court-orders-renewable-energy-firm-to-pay-rs25265-541205-2026-07-06)
  - Outlook Money, [PM Surya Ghar explainer (subsidy, 4–5.5 units/kW/day)](https://www.outlookmoney.com/personal-finance-news/pm-surya-ghar-muft-bijli-yojana-everything-you-need-to-know-and-amount-of-subsidy)
  - CEA, [CO₂ Baseline Database v22.0 user guide (Aug 2026)](https://cea.nic.in/wp-content/uploads/baseline/2026/09/User_Guide__Version_22.0.pdf)
  - EastMojo, [Time-of-day tariff rules (Jun 2023)](https://eastmojo.com/national/2023/06/23/new-power-tariff-rule-save-up-to-20-for-usage-during-solar-hours/)
  - [Open-Meteo Satellite Radiation API](https://open-meteo.com/en/docs/satellite-radiation-api)
