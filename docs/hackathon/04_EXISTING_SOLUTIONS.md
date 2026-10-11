# 04 — Existing Solutions & Competition

**Scope:** solutions that a judge, or our user, would compare us to.

- **FACT:** verified this session (link in Sources).
- **KNOWN:** widely known product or programme, not re-verified this session.
- **INFERENCE:** our reading.

**Column guide for every table below:**
- **Does / users:** what it does and who uses it.
- **Strengths / weaknesses:** what it does well and where it falls short.
- **Doesn't solve → why the problem persists:** the gap left open, and why users still have the problem.
- **Hard to copy:** what a hackathon team couldn't easily rebuild.

---

## A. AIR

| Solution | Does / users | Strengths | Weaknesses | Doesn't solve → why the problem persists | Hard to copy |
|---|---|---|---|---|---|
| **CPCB station network and AQI portals, incl. SAMEER app** (KNOWN; network FACT) | Hourly pollutant readings and AQI for ~565 continuous stations; used by citizens, media, agencies | Official, near-real-time | Sparse in small cities (28 NCAP cities have none); **no open real-time API on data.gov.in** (FACT) | "What should *I* do *today*?" — habituation and no actionable alternative | Regulatory network |
| **SAFAR / IITM Decision Support System** (KNOWN) | City-scale forecasts and source contributions for Delhi and select cities; policymakers, CAQM | Scientific forecasting, source apportionment | Policy-facing, coarse for individuals and institutions | Institution-level scheduling | Models and emission inventories |
| **GRAP** (FACT) | Staged restrictions by AQI band, incl. hybrid schooling up to Class V in Severe | Ready-made trigger with legal force | Binary, day-level, reactive | Hour-level decisions inside the school day; anything outside NCR | Legal authority |
| **Consumer AQI apps** (IQAir, Google Maps AQI, AQI.in; KNOWN) | Current AQI, maps, forecasts, health advice | Polished, ubiquitous | Generic advice ("limit outdoor activity"); one number per location | Turning a forecast into a schedule for a group | Brand and sensor networks |
| **OpenAQ** (FACT) | Open aggregation of global measurements; S3 archive on AWS | Free, programmatic | A data layer, not a decision tool; licence varies by provider | — (it's an input for us) | — |
| **Purifiers and indoor monitors** (KNOWN) | Household and office indoor PM reduction | Real exposure reduction indoors | Cost; wrong sizing; run with windows open (INFERENCE) | Outdoor exposure; schools | Hardware |
| **Hackathon AQI projects** (FACT: e.g. a HackQuest "real-time AQI indicator"; First Commit "Vayu AI-satellite-ground fusion") | AQI dashboards, predictions, alerts | Fast to build | Indistinguishable from each other and from IQAir | Same as consumer apps | Nothing |

**International analogues (KNOWN):** EPA AirNow, PurpleAir (low-cost sensor network), Plume Labs (exposure tracking), BreezoMeter (acquired by Google). All are *information* layers.

---

## B. HEAT

| Solution | Does / users | Strengths | Weaknesses | Doesn't solve → why the problem persists | Hard to copy |
|---|---|---|---|---|---|
| **IMD warnings, Mausam app, NDMA SACHET alerts** (KNOWN) | Heatwave warnings by district; citizens, administrators | Official, colour-coded | District-level; temperature-centric; no task guidance | What a site supervisor should change in tomorrow's shift plan | Authority |
| **Heat Action Plans** (FACT: 37 reviewed by CPR) | City, district and state preparedness and response | Institutional framework (Ahmedabad pioneer, KNOWN) | Not localised; vulnerable groups poorly targeted; underfunded; weak legal basis (FACT) | Workplace execution | — |
| **OSHA-NIOSH Heat Safety Tool** (FACT: exists; features KNOWN) | US app computing a heat index and risk level with protective measures for workers | The international precedent for a worker-facing heat tool | Heat index ignores solar load (WBGT is better outdoors); US-centric; no shift planning | Indian sites, languages, contractors | Agency credibility |
| **SEWA parametric heat insurance** (FACT) | Pays informal women workers when heat thresholds hit; ~50,000 covered in 2024 | Money reaches workers fast | Compensates after exposure rather than preventing it | Daily exposure planning | Insurance partners |
| **Tamil Nadu factory temperature thresholds** (FACT) | Legal max temperatures in factory units | Binding | One state, factories only | Construction and outdoor work everywhere else | Law |

**INFERENCE:** no Indian tool turns an hourly forecast into a *work-rest schedule* that a supervisor signs off on.

---

## C. WATER & FLOODS

| Solution | Does / users | Strengths | Weaknesses | Doesn't solve → why the problem persists | Hard to copy |
|---|---|---|---|---|---|
| **Google Flood Hub** (KNOWN) | Riverine flood forecasts, incl. India | Global ML model, free | Riverine, not street waterlogging (INFERENCE) | Underpass and basement flooding | Models and data |
| **City control rooms and complaint apps** (KNOWN) | Waterlogging complaints, pump dispatch | Official | Reactive | Prevention | — |
| **Tanker rate caps** (FACT: Bengaluru 2024) | Regulates price per load by distance | Clear published rates | **No delivery-volume verification** (INFERENCE); temporary | Short delivery; continued groundwater mining | — |
| **Smart building water meters** (KNOWN, e.g. Indian apartment metering startups; US analogues Flume, Phyn) | Per-flat metering, leak alerts | Measured data | Hardware and installation cost; apartments only | Tanker verification; city-level non-revenue water | Hardware |
| **First Commit flood entries** (FACT: FloodRoute, FloodSense ×2, ResQNet) | Risk-aware navigation (Bedrock + NASA data), alerts, coordination | Shows the topic is popular | None placed | — | — |

---

## D. WASTE

| Solution | Does / users | Strengths | Weaknesses | Doesn't solve → why the problem persists | Hard to copy |
|---|---|---|---|---|---|
| **SWM Rules 2026 central portal** (FACT) | Digital tracking of generation, collection and disposal; bulk waste generator (BWG) compliance | Legal mandate from Apr 2026 | A reporting channel, not a behaviour tool (INFERENCE) | Daily segregation quality inside a hostel or society | Mandate |
| **Scrap-pickup marketplaces** (KNOWN: Recykal, ScrapUncle, The Kabadiwala, Kabadiwalla Connect) | Doorstep pickup of dry recyclables at listed prices | Convenient | Urban, app-literate users; can bypass waste pickers (INFERENCE) | Wet waste; segregation compliance | Logistics networks |
| **Waste-picker organisations** (FACT: SWaCH, Hasiru Dala) | Door-to-door collection; integration of informal workers | Social impact, proven scale (SWaCH ~1M households) | Depend on municipal contracts | Digital price transparency for pickers (INFERENCE) | Trust networks |
| **CPCB EPR portals** (KNOWN) | Producer obligations for plastic and e-waste | Legal teeth | Producers can comply via formal recyclers that bypass pickers (FACT) | Household behaviour | — |
| **Hackathon staples** (FACT: First Commit had ≥4 food-waste apps, ≥4 waste platforms) | Image classifiers, smart bins, food-waste trackers | Easy demos | Near-identical; classification ≠ behaviour change | — | Nothing |

**International analogues (KNOWN):** Recycle Coach, Too Good To Go (food surplus), TOMRA reverse vending.

---

## E. ENERGY — rooftop solar (the least-served area we found)

| Solution | Does / users | Strengths | Weaknesses | Doesn't solve → why the problem persists | Hard to copy |
|---|---|---|---|---|---|
| **PM Surya Ghar national portal** (FACT) | Application, subsidy, loans, net-metering, vendor ratings, ~23,000 third-party inspections, complaints (GMS) | End-to-end for *installation* | **Tracks installs, not generation** (FACT); post-install support is reactive | Whether a system is performing; when to clean; when to claim | National mandate |
| **MNRE M2M remote-monitoring mandate** (FACT: Dec 2025) | SIM-based monitoring of new PM Surya Ghar systems, sent to central servers | Will create a national generation dataset | New installs only; ~23 GW legacy unmonitored; protocols not yet implemented (FACT); **government-facing, not owner-facing** (INFERENCE) | Owner-level diagnosis and action | Regulation |
| **Inverter maker apps and clouds** (KNOWN / INFERENCE) | Live and daily kWh, fault codes, per brand | Real data | No weather-normalised *expected* value (INFERENCE); fault codes are cryptic; brand silos; owners stop opening them (FACT: "~99% stop monitoring") | "Is this number good for *today's* sunshine?" | Device integration |
| **Qbits WhatsApp alerts** (FACT) | Pushes generation and fault alerts to WhatsApp | Meets owners where they are | Expected generation **set manually** from installer estimate or history; **no irradiance**; e.g. alerts below 40% for two days (FACT) | Soiling-level losses (10–25%) stay invisible under a 40% threshold (INFERENCE) | — |
| **Installer-side performance guarantees** (KNOWN, e.g. installer blogs on generation guarantees) | Some vendors guarantee yields for their customers | Accountability | Only for that vendor's customers; the vendor marks its own homework | Independent evidence for the owner | — |
| **Utility-scale SCADA and performance-ratio monitoring** (KNOWN) | Plants track performance ratio against irradiance sensors | Exactly the right science | Built for MW plants with pyranometers, not homes | Household scale, no sensors | Expertise |
| **SolarLens** (FACT: First Commit entry) | *Pre-purchase* independent quote checker | Consumer advocacy | Before installation only | After-install performance | — |
| **Complaint and warranty SOPs** (FACT: MNRE Jun and May 2026) | Vendor response timelines, deactivation; module warranty process with lab testing | Formal leverage | Owners need *evidence* and must know the process (INFERENCE) | Building the evidence pack | Policy |

**International analogues (KNOWN):** Enphase Enlighten and SolarEdge monitoring (module- or inverter-level, OEM-specific), PVWatts-style expected-yield calculators (NREL), and pvlib, the open-source PV modelling library. **INFERENCE:** the science is mature. Nobody has packaged it for India's 50 lakh new, non-technical, subsidy-era owners, connected to their 5-year maintenance right.

---

## F. What a generic AI prompt produces

We asked ourselves what "build an environmental hackathon project for India on AWS" returns from a typical LLM. The answer is the crowded set, and this is our **anti-target list**:

1. An AQI dashboard plus a Bedrock chatbot for health advice.
2. Waste image classification with Rekognition or a vision LLM.
3. A flood alert system with SNS notifications and a map.
4. A carbon-footprint tracker with gamification.
5. A solar ROI calculator or rooftop-potential estimator from satellite images.
6. An EV charging-station finder.
7. A water-usage tracker with IoT.
8. A crop or drought advisory chatbot.

---

## G. What is difficult to copy quickly (our moat candidates)

| Moat | Why a weekend team won't arrive at it |
|---|---|
| **Domain mechanics a prompt won't produce:** treating natural rain events as free panel cleanings to self-calibrate a household PV baseline (see 06) | Comes from combining domain science, not from a prompt |
| **Institutional hooks** | Knowing the 5-year free-maintenance condition, MNRE's 8+7+15-day complaint ladder, SWM 2026 bulk-generator thresholds, and GRAP's school provisions |
| **Data plumbing** | Satellite irradiance at the rooftop's coordinates and tilt, or WBGT via thermofeel, joined with user-generated readings (photos) |
| **A verification loop** | Proving the intervention worked with the next data |

---

## Sources

- [OpenAQ on AWS Open Data](https://registry.opendata.aws/openaq/)
- [data.gov.in real-time AQI resource (no API)](https://www.data.gov.in/resource/real-time-air-quality-index-various-locations)
- [CREA NCAP 2026 report](https://energyandcleanair.org/publication/2026-progress-report-on-national-clean-air-programme/)
- [GRAP revision, The Tribune](https://www.tribuneindia.com/news/delhi/grap-rules-revised-nod-to-hybrid-learning-till-class-v-in-severe-aqi/amp)
- [HackQuest: BreatheEasy real-time AQI project](https://hackquest.io/projects/BreatheEasy)
- [CPR heat action plan assessment](https://cprindia.org/briefsreports/how-is-india-adapting-to-heatwaves-an-assessment-of-heat-action-plans-with-insights-for-transformative-climate-action/)
- [OSHA-NIOSH Heat Safety Tool (Heat Health info page)](https://heathealth.info/resources/osha-niosh-heat-safety-tool-app)
- [Newslaundry/IndiaSpend on worker heat protection and SEWA insurance](https://www.newslaundry.com/amp/story/2026%2F04%2F13%2Fas-india-braces-for-summer-informal-workers-have-little-heat-protection)
- [Bengaluru tanker rates](https://businesstoday.in/india/story/bengaluru-water-crisis-district-administration-fixes-rates-for-water-tanker-services-420502-2024-03-07)
- [ORF on non-revenue water](https://www.orfonline.org/expert-speak/the-cost-of-leakage-how-water-losses-fuel-unsustainable-choices)
- [First Commit all projects](https://www.wemakedevs.org/aws/first-commit/projects/all)
- [SWM Rules 2026](https://www.drishtiias.com/daily-updates/daily-news-analysis/solid-waste-management-swm-rules-2026/print_manually)
- [DTE on waste pickers](https://www.downtoearth.org.in/amp/story/waste/indias-waste-economy-runs-on-invisible-workers-climate-policy-keeps-forgetting-them)
- [PM Surya Ghar 50 lakh](https://solarquarter.com/2026/08/07/pm-surya-ghar-scheme-crosses-50-lakh-rooftop-solar-installations-adds-record-5-06-lakh-homes-in-july-2026/)
- [DTE generation blind spot](https://www.downtoearth.org.in/amp/story/energy/as-rooftop-solar-scales-up-india-confronts-a-generation-blind-spot)
- [ETV Bharat on rooftop solar maintenance](https://etvbharat.com/en/bharat/rooftop-solar-push-under-pm-surya-ghar-yojana-crossed-37-lakh-but-maintenance-a-challenge-enn26070705272)
- [Qbits WhatsApp solar monitoring](https://qbitsenergy.com/blog/whatsapp-solar-monitoring/)
- [SolarSquare: does your solar guarantee production? (title)](https://www.solarsquare.in/blog/does-your-solar-guarantee-power-production-and-savings)
- [MNRE complaint SOP](https://solarquarter.com/2026/06/25/mnre-introduces-strict-sop-to-address-consumer-complaints-against-solar-vendors-under-pm-surya-ghar-scheme/)
- [MNRE warranty SOP (JSA)](https://www.jsalaw.com/wp-content/uploads/2026/05/JSA-Prism-Energy-May-2026-SOP-on-warranty-claims.Final_.pdf)
