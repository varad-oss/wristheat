# R2-05 — Top-10 Feasibility Report and Top-5 Shortlist

**What was audited:**
- Nine concepts from the longlist (03), selected for constraint fit, with at least one per cluster.
- The round-1 favourite, SunCheck, re-tested as the tenth.

**How:**
- Live keyless technical spikes on 9 Oct, 21:50–22:30 IST, mostly through the Claude app's built-in browser.
- AWS calls were **not** made: no credentials exist in this workspace. All AWS capability claims are from documentation.

**Full evidence:** [`evidence/B_audit_*.md`](evidence/) and [`evidence/A_data_access.md`](evidence/A_data_access.md).

**Capability labels:**

| Label | Meaning |
|---|---|
| ✅ **VERIFIED** | Tested live, or the method is fully published and reproduced |
| 🟨 **VERIFIED-BUT-CONSTRAINED** | Works, with a stated limit |
| ⬜ **PLAUSIBLE-UNTESTED** | Should work; not tried |
| ❌ **UNSUPPORTED** | Evidence says no, or nothing found |

---

## 1. Capabilities that underpin several concepts (verified once)

| Capability | Status | Detail |
|---|---|---|
| Open-Meteo forecast and archive (temperature, RH, wet-bulb, radiation, rain) for Indian cities, keyless | ✅ | Archive to 9 Oct 2026 via the best-match blend; ERA5-only lags ~6 days; 16-day forecast. 9 cities, 0 nulls in wet-bulb |
| Air quality, live, keyless, India | 🟨 | CAMS via Open-Meteo is 0.4° (~45 km), 3-hourly. It returned **one identical value for three Delhi points**, and its 5 Oct daily mean was 96.6 µg/m³ vs station means of 50–62 (hourly shape correlates r = 0.52–0.87). Stations: OpenAQ v3 needs a free key; the keyless S3 archive is ~4.5 days stale. Google AQ API needs billing |
| Wearable cloud APIs (Fitbit, Garmin, Strava) | ❌ | Fitbit Web API turned off 30 Oct 2026, successor not onboarding; Garmin business-only; Strava bans AI use |
| Web Bluetooth Heart Rate Service in Chrome (Android, Windows, macOS, ChromeOS) | 🟨 | Documented and supported. **Not iOS or Safari.** Works only if the watch broadcasts standard HRS (see §2.1). A one-click test page exists: <https://webbluetoothcg.github.io/demos/heart-rate-sensor/> (loaded 9 Oct) |
| Overture buildings on AWS (`s3://overturemaps-us-west-2/release/2026-09-23.1/`) | ✅ | Keyless DuckDB queries returned 950–2,600 buildings per ~1.2 km² in Bengaluru, Pune, Chennai and Delhi. Heights essentially absent (0–6 per box) |
| Meta/WRI canopy height CHMv2 on AWS | ✅ | Bengaluru tile read keyless; MAE 3.0 m; imagery ~2018–20; 8.7 m geolocation error |
| Vision LLM reading real meter displays | 🟨 | Published benchmark: best models 53–80% on real digital displays. A confirm step and a "reading must increase" check are required |
| Bedrock (Claude/Nova), Polly Hindi (Kajal), Transcribe hi-IN, IoT Core, Step Functions, EventBridge Scheduler, Amazon Location in ap-south-1 | ⬜ | Docs only; untested without an account |
| SMS to Indian numbers | ❌ for the MVP | Needs DLT registration. Use web push, email (SES) or Telegram |

---

## 2. Concept feasibility

### 2.1 WristHeat: body-aware heat strain from your own watch

| Step of the main journey | Status | Basis |
|---|---|---|
| Live HR from the team's watch into a Chrome page | 🟨 **GATE** | Broadcasts standard HRS: Garmin (many), COROS, Polar Ignite 2/3 and Unite, Amazfit on Zepp OS 3+, some Huawei, probably Xiaomi Band 10. **Galaxy Watch: no built-in broadcast. Apple: only via the HeartCast app relaying through an iPhone. Noise, boAt and Fire-Boltt (50.4% of India's 2025 shipments, per IDC): undocumented** |
| Fallback: exported workout file → HR series | ⬜ | Samsung Health, Health Connect and Apple Health exports exist; HR density unverified |
| ECTemp estimate from HR | ✅ | Parameters are public: US patent US10702165B2 and USARIEM T17-08. HR = −4.5714·CT² + 384.4286·CT − 7887.1; process variance 0.000484; measurement variance 356.57; start 37.1 °C. The audit implemented and simulated it |
| Accuracy on wrist optical HR | ❌ | No validation found. Chest-strap validations: bias −0.03 °C, LoA ±0.63 °C (military); ±1.2 °C (Marines field); ±0.76 °C (farmworkers); <50% sensitivity above 39 °C (elite athletes) |
| WBGT for the location from forecast | ✅ | Open-Meteo inputs + Liljegren method (already used by competitors) |
| Heat-strain state (PSI band) + rest/hydration advice | 🟨 | Published formula; must be framed as wellness. CDSCO's final software guidance excludes general-wellness apps (secondary source) |
| October demonstrability | 🟨 | Simulation: 60 min at 105 bpm peaks at 37.6 °C; **≥30 min at 150–165 bpm reaches 38–38.8 °C**. Afternoon highs are 33–38 °C in several cities. **There is no ground truth on camera** |

**Minimum working demonstration** (no outside person or bought hardware):
1. A teammate wears **their own broadcasting watch** and runs or cycles 30–40 min in the afternoon.
2. A Chrome page shows live HR → core-temperature estimate with an uncertainty band → PSI state, alongside the WBGT for that spot.
3. An alert fires at the threshold.
4. The rest period shows the estimate falling, and the system marks the person "recovered".
5. An implementation cross-check shows the same HR series run through the published equations.
6. **If the watch can't broadcast:** a labelled replay from their own exported workout. This is weaker.

**Other constraints:**
- **Patent:** US10702165B2 is active (Google estimates expiry 16 Dec 2033), and USARIEM says commercial use needs a licence. INFERENCE, not legal advice: a non-commercial hackathon prototype in India carries low practical risk, but say "research prototype" and credit USARIEM.
- **Build estimate:** ~30–36 h for 3 people, *if* the watch passes.

### 2.2 Bijli Budget: "Was it you or the weather?" plus the free-unit cliff

| Step | Status | Basis |
|---|---|---|
| Bill history (12+ months) from DISCOM-app screenshots or bill photos | 🟨 | Apps expose history. That paper bills print 12 months is unverified. Two-month billing (Punjab, Tamil Nadu) gives 6 points a year |
| Meter-photo kWh reading | 🟨 | Precedents exist (TPDDL self-read, SmartBill). 53–80% model accuracy, so confirm and monotonic checks are needed |
| Daily temperature → cooling degree-days (CDD), history + forecast | ✅ | Delhi: 466 days to 9 Oct. **Oct 2026 ≈ 95 CDD by the 24th vs 66 in all of Oct 2025** |
| State rule engine | 🟨 | **True cliffs:** Telangana (201 → full bill), Karnataka (>200 → full bill), Punjab (300/600), Tamil Nadu (from 10 May 2026: crossing 500 units bimonthly costs ~₹478 for one unit), Kerala (>250 → ~₹237), Madhya Pradesh (>150). **Delhi's amount payable at 201 units is unresolved.** Pro-rating is documented by TPDDL |
| Projection + P(crossing the threshold) | ⬜ | Standard method (CalTRACK). On 12 monthly points: ±13% (summer), ±24% (October) |
| Daily budget + biggest single action | ⬜ | The budget is arithmetic. Ranking actions without sub-metering is HYPOTHESIS-grade |
| Verify savings from the next bill | 🟨 | Method is real (IPMVP C). It cannot be shown with a real post-bill inside 46 h, and "can't tell yet" will be common |
| Verify from meter photos hours apart | ⬜ | Feasible with the team's own meter. October nights in Delhi are mild, so the signal is small |

**Minimum working demonstration:**
- One teammate's real 12–13-month history and 3–4 meter photos taken Fri–Sun.
- Live Open-Meteo data and a cited rule pack.
- Any synthetic "after" change is labelled.
- Prefer a household in Delhi, Hyderabad, Chennai or Punjab, **not Bengaluru** (≈0 CDD in October).

**Build estimate:** ~28–34 h.

### 2.3 Monsoon Replay: RWH sizing by replaying real monsoons over real roofs

| Step | Status | Basis |
|---|---|---|
| Buildings from Overture on AWS | ✅ keyless DuckDB / ⬜ Athena in the team's account | — |
| Roof areas | ✅ | — |
| Daily past rainfall | 🟨 | **−48% to +33% vs IMD**; record bursts ~4× under-stated; models disagree by 53% |
| Daily tank and overflow balance | ✅ | 10 kL tank on a 1,000 m² roof: 73% capture (Bengaluru 2024) / 52% (Chennai) vs 100% implied by calculators |
| Recharge-pit routing; tanker ₹; mandate check | ⬜ / 🟨 | Bengaluru 2024 tanker rates cited |
| Proof the replay matches reality | ❌ | Rainfall-total cross-check only |

**Minimum working demonstration:** a real Bengaluru or Chennai complex, three rainfall models shown as a band, replay animation, and a committee pack.

**Build estimate:** ~25–30 h.

### 2.4 CoolerCheck

| Step | Status | Basis |
|---|---|---|
| Wet-bulb → outlet temperature by hour | ✅ | — |
| Litres | 🟨 | — |
| Learn each cooler's ε | ❌ | — |
| Verify benefit | ❌ (measured) | Hindcast only |

**Physics corrections:**
- "Wastes water in humid hours" is **unsupported**: evaporation is proportional to the cooling delivered.
- "Only adds humidity" is **unsupported**: in a ventilated room the cooler doesn't make heat stress worse.

**Prior art:** Evaporative Cooler Forecaster (2025). **Build estimate:** ~15 h.

### 2.5 Heat Roll-Call

| Step | Status | Basis |
|---|---|---|
| Registry, forecast trigger, Step Functions ladder | ✅ / ⬜ | — |
| October trigger | 🟨 | No city > 38.1 °C over 10–16 Oct, so a labelled replay is needed |
| Real responders | ❌ | Teammates role-play |

**Build estimate:** ~20 h. **Novelty risk:** Suraksha déjà vu.

### 2.6 Dose Ledger

| Step | Status | Basis |
|---|---|---|
| Hourly PM | 🟨 | CAMS supports time and mode swaps, **not route swaps** |
| Mode factors | 🟨 | Indian studies conflict, e.g. metro 0.8× ambient vs 1.4× an AC car |
| Indoor factor (largest share of dose) | ❌ | Unreliable |
| Timeline export | 🟨 | Off by default; only teammates who already had it on |
| Next-week verification | ❌ in 46 h | — |

**Live field:** 6+ entries already do this.

### 2.7 Window Planner

| Step | Status | Basis |
|---|---|---|
| Trade-off computable | ✅ | Delhi tonight: coolest hours carry the highest modelled PM |
| Indoor benefit | ❌ | Contradictory Indian studies |
| Verification | ❌ | No sensor |

### 2.8 ShadeSite

| Step | Status | Basis |
|---|---|---|
| Canopy and footprints | ✅ | — |
| Building heights | ❌ (Overture) / ⬜ (Google 2.5D, unvalidated in India) | — |
| Footpaths | 🟨 | Campuses only |
| Shadow casting | ⬜ | Custom ray-march |
| Benefit timing | HYPOTHESIS | Saplings take 5–10 years to shade |

**Build estimate:** 32–40 h, with GIS risk.

### 2.9 ReCheck

| Step | Status | Basis |
|---|---|---|
| Public complaint data with closure timestamps | ❌ | The ICMyC CSV has no resolution timestamps |
| Demo re-checks | 🟨 | Team re-photographs 3–5 campus spots over ~36 h. This gives **counts, not a half-life** |

### 2.10 SunCheck (round-1 favourite, re-tested)

| Step | Status | Basis |
|---|---|---|
| Satellite expected generation | ✅ | — |
| **Real system history** | ❌ | The team has no access to a system. **Fails constraint C**, as you flagged |

---

## 3. Phase 7 scoring

**Weights:**

| Criterion | Weight |
|---|---:|
| Severity and relevance (Sev) | 15% |
| **Distinctiveness of mechanism** (Dist) | **20%** |
| Usefulness to the user (Use) | 15% |
| **Ability to build and demonstrate the complete mechanism** (Build) | **20%** |
| Data quality and access (Data) | 10% |
| Demo strength (Demo) | 10% |
| AWS (AWS) | 5% |
| Breadth (Br) | 5% |

**Rules applied:**
- No novelty points for "added AI" or "used AWS".
- Novelty risk is assessed separately and qualitatively.
- These are decision aids from desk evidence, **not predictions of winning**.

| Rank | Concept | Sev | Dist | Use | Build | Data | Demo | AWS | Br | **Score /100** | Novelty risk |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | **WristHeat** | 8 | 8 | 6 | 6 | 6 | 9 | 9 | 5 | **71.0** | Medium |
| 2 | Heat Roll-Call | 8 | 3 | 7 | 8 | 7 | 7 | 9 | 7 | **66.5** | **Very high** |
| 3 | **Bijli Budget** | 6 | 5 | 7 | 7 | 7 | 6 | 8 | 9 | **65.0** | High |
| 4 | **Monsoon Replay** | 6 | 4 | 6 | 8 | 5 | 7 | 8 | 7 | **61.5** | High |
| 5 | CoolerCheck | 5 | 3 | 6 | 9 | 9 | 5 | 4 | 8 | **60.5** | **Very high** |
| 6 | ReCheck | 6 | 7 | 6 | 6 | 3 | 5 | 7 | 7 | 59.0 | Low |
| 7 | Dose Ledger | 8 | 3 | 6 | 6 | 4 | 7 | 7 | 8 | 57.5 | High |
| 8 | ShadeSite | 7 | 6 | 5 | 3 | 5 | 8 | 7 | 5 | 55.0 | Medium |
| 9 | SunCheck | 7 | 8 | 7 | 2 | 1 | 3 | 8 | 6 | 52.0 | Low |
| 10 | Window Planner | 6 | 2 | 4 | 7 | 5 | 5 | 5 | 8 | 49.5 | Very high |

### Why each score

**WristHeat**

| Criterion | Score | Reason |
|---|---:|---|
| Sev | 8 | Heat illness is real and under-counted: ~48,000 suspected heatstroke cases and 159 deaths in 2024 (round-1 sources). 12 candidates died in Jharkhand's 10 km recruitment run in Aug–Sep 2024 |
| Dist | 8 | 0 of 111 live entries and 0 student repos use body signals. GarminLabs' field is Garmin-only and obscure, so it stays below 9 |
| Use | 6 | Only for compatible watches, and the estimate is unvalidated on wrist sensors |
| Build | 6 | Small code (a Kalman step, BLE, streaming), but **gated on the watch** |
| Data | 6 | Own HR is real, but accuracy is ❌ |
| Demo | 9 | A physical event → consequence in one take (01, principle 2) |
| AWS | 9 | Streaming, state machine, scheduler, voice and LLM are all natural |
| Br | 5 | Device-limited |

**Sensitivity:** if the watch gate fails, Build 4, Data 4 and Demo 6 drop the score to **62**, below Bijli Budget.

**Heat Roll-Call:** scores well on build and AWS. Novelty risk is very high because it repeats the previous winner's pattern on screen.

**Bijli Budget**

| Criterion | Score | Reason |
|---|---:|---|
| Br | 9 | ~5 crore households are on threshold schemes |
| Dist | 5 | The genre is crowded (21 "bijli" repos, SmartBill). Only verification and probability are new |
| Demo | 6 | Numbers on screen, with no physical moment. October weakens the cooling signal |

**Monsoon Replay:** Build 8 (simple maths, verified data access). Dist 4 (SimTanka, Jal Shakti winner, an SIH genre). Data 5 (rainfall error up to −48%).

**CoolerCheck:** easiest to build, but an equivalent app already ships.

### Top 5 (by score)

WristHeat · Heat Roll-Call · Bijli Budget · Monsoon Replay · CoolerCheck. These go to the red team (06).

**Not shortlisted:**
- **ReCheck** (59.0) was the closest miss. Its mechanism is genuinely new, but its data can't show a half-life within 46 h.
