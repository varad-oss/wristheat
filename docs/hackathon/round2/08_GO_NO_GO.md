# R2-08 — Go / No-Go Recommendation

> **Decision recorded (Sun 11 Oct, 00:02 IST): GO WristHeat, with a native Wear OS app.**
> - W1 failed on the direct path. Brave blocks Web Bluetooth; in Chrome, the Galaxy Watch5 Pro (SM-R920) does not advertise the standard BLE Heart Rate Service.
> - The Health Connect relay was also empty (Samsung Health → Health Connect showed no heart-rate records).
> - B1 (Bijli Budget) failed: the team has no electricity-bill history.
> - The team chose WristHeat anyway, getting heart rate from **an app on the watch itself** (Health Services ExerciseClient → HTTPS → AWS). This keeps the live demo and removes the broadcast dependency.
> - Spec: `docs/superpowers/specs/2026-10-11-wristheat-design.md`. Runbook: `docs/hackathon/13_EXECUTION_PLAN.md`.


**Status:** decision document. **No architecture or implementation planning has started.** It waits for your explicit approval.

---

## Bottom line

**No concept clearly survives unconditionally.**

After the audits, every candidate either:
- is already done by an existing product or by entries in this event (CoolerCheck, Dose Ledger, Window Planner, Heat Roll-Call), or
- lives in a crowded student genre with a narrow differentiator (Bijli Budget, Monsoon Replay), or
- depends on a single device check that hasn't been run yet (WristHeat).

The honest recommendation is therefore a **gated decision**, which can be made **tonight in about 15 minutes**:

| Step | Gate | If it passes | If it fails |
|---|---|---|---|
| 1 | **W1, watch test** (by 01:00 IST). In Chrome on an Android phone or laptop, open <https://webbluetoothcg.github.io/demos/heart-rate-sensor/>, turn on the watch's heart-rate broadcast, click, and see live BPM | **GO WristHeat** (if W2 also passes) | Go to step 2 |
| 1b | **W2, stability.** Jog 10 min with the watch broadcasting. No gap over ~20 s, and HR looks plausible | Confirms GO WristHeat | Step 2 |
| 2 | **B1, bill history.** A teammate in Delhi, Hyderabad, Chennai, Punjab, Tamil Nadu or Telangana (not Bengaluru) can export 12–13 months of bill history tonight or by Sat 09:00 | **GO Bijli Budget** (verification-led version, 06 §3) | Step 3 |
| 3 | No further gate | **GO Monsoon Replay** (lowest risk, lowest ceiling) | — |

**Watch-specific notes for W1** (from the audit):

| Watch | What to do |
|---|---|
| **Garmin** (most models), **COROS**, **Polar** Ignite 2/3 / Unite, **Amazfit** on Zepp OS 3+, some **Huawei** | Enable heart-rate broadcast; should pass |
| **Galaxy Watch** | No built-in broadcast; expect fail. A Wear OS BLE heart-rate broadcaster app is unverified. Try for ≤30 min, otherwise treat as fail |
| **Apple Watch** | Only through the HeartCast app relaying via an iPhone. **Web Bluetooth doesn't work on iOS**, so the page must run on an Android phone or a laptop |
| **Noise / boAt / Fire-Boltt** | Undocumented; likely fail |
| **Chest strap** (any BLE) | If anyone on the team already owns one, it passes and is the more accurate source. It counts as "existing device", not a purchase |

---

## Why WristHeat is first, if the gate passes

1. **The only mechanism in the shortlist with zero lookalikes in the field.**
   - 0 of 111 visible entries and 0 student repos since September use body signals (FACT).
   - The five heat entries all plan from weather only.
2. **It reproduces the winning video pattern honestly.** A real physical event leads to a visible consequence and a **verified** recovery, in one take, on the team's own devices. That is the trait the top two First Commit winners shared (01).
3. **AWS is load-bearing and shows on screen.**
   - Live streaming ingest, and a state machine that waits for the body to recover.
   - Spoken alerts, scheduled planning and an LLM debrief.
4. **It uses the smartwatch you have.** That was your stated preference, but it was not given priority in the scoring: WristHeat ranked first on evidence (05).
5. **Demo weather is suitable.** Delhi on Saturday afternoon is forecast at ~32 °C with strong sun (FACT, forecast), roughly WBGT ~29 °C in sun (INFERENCE).

**What you are accepting with WristHeat:**
- Its core estimate is **not validated on wrist sensors**. It must be presented as a heat-strain *indicator* with an uncertainty band and the published chest-strap accuracy, never as a thermometer or a medical device.
- It works with **some watch brands only** (honest breadth).
- It competes in the **most crowded track**, though not against anything like it.
- ECTemp is a **US patent** (US10702165B2, active), and USARIEM says commercial use needs a licence. Present it as a non-commercial research prototype and credit USARIEM. *(INFERENCE; not legal advice.)*

## Why Bijli Budget is the fallback rather than the lead

**For it:**
- The broadest reach: ~5 crore households.
- The least crowded track.
- Real data the team owns.
- An unusually good live hook: Delhi's October 2026 was much hotter than October 2025 (~95 vs 66 cooling degree-days, FACT). A naive bill comparison blames the household; the weather-adjusted one doesn't.

**Against it:**
- The genre is crowded: 21 "bijli" repos since 25 Sep, and SmartBill already does OCR, the cliff and a temperature-aware prediction.
- Its true differentiator, weather-normalised verification, is analytical rather than visual.

**Expect:** a solid, working submission with a lower ceiling.

## Why Monsoon Replay is third

- Lowest build risk, with verified AWS Open Data in place (Overture via Athena).
- But real prior art (SimTanka, a 2025 Jal Shakti winner), an SIH lookalike genre, rainfall data that misses cloudbursts, and no physical or live moment.

## Rejected after evidence

| Concept | Why rejected |
|---|---|
| Heat Roll-Call | Previous winner's pattern on screen |
| CoolerCheck | An equivalent app already ships |
| Dose Ledger | 6+ live entries already do it |
| Window Planner | Existing apps; indoor benefit unverifiable |
| ShadeSite | WRI already maps shade; GIS risk; benefit deferred 5–10 years |
| ReCheck | New metric, but no data to show it within 46 h |
| SunCheck | No accessible system data, as you flagged |

---

## What I need from you

1. **Your smartwatch model**, and whether any teammate owns a Garmin, COROS, Polar, Amazfit or a BLE chest strap.
2. **The W1 result tonight.** Ideally a screenshot of the test page showing live BPM.
3. **Which city** the team and the household for a possible Bijli fallback are in.
4. **Explicit approval of one concept.** Then I'll start Phase 12: architecture and execution plan, using Superpowers + feature-dev, with one vertical slice first.

---

## Key sources

- **Deadline:** WeMakeDevs API [`/hackathons/env`](https://wemakedevs-server.onrender.com/hackathons/env). `end_date` 2026-10-11T14:30Z (20:00 IST); `submissions_open_at` 02:30Z (08:00 IST); 8,653 registrations (checked 9 Oct 22:20 IST).
- **Heat illness:**
  - [Jharkhand recruitment-run deaths (Deccan Herald, 8 Sep 2024)](https://www.deccanherald.com/amp/story/india%2Fjharkhand%2Fhumidity-lack-of-health-screening-change-in-rules-some-reasons-behind-12-deaths-at-jharkhand-recruitment-drive-report-3181567)
  - [NCDC heatstroke data via RTI (The Week)](https://www.theweek.in/wire-updates/national/2025/07/27/del4-climate-heat-rti.html)
- **ECTemp:**
  - [US10702165B2](https://patents.google.com/patent/US10702165)
  - [USARIEM T17-08 (DTIC)](https://apps.dtic.mil/sti/pdfs/AD1031877.pdf)
  - [USARIEM CBT algorithm page](https://usariem.health.mil/index.cfm/research/products/cbt_algorithm)
  - [de Korte et al. 2022 (athlete validation)](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.882254/full)
- **Prior art:** [GarminLabs body-temperature field (Garmin blog)](https://www.garmin.com/it-IT/blog/running/lapp-connect-iq-stima-temperatura-corporea/)
- **Watches and Web Bluetooth:**
  - [Web Bluetooth (Chrome for Developers)](https://developer.chrome.com/docs/capabilities/bluetooth)
  - [Garmin broadcast (DC Rainmaker)](https://dcrainmaker.com/2020/04/garmin-wearable-broadcasting.html)
  - [COROS broadcast](https://support.coros.com/hc/en-us/articles/360040256991-Broadcast-heart-rate)
  - [Polar HR sensor mode](https://support.polar.com/en/troubleshooting-ignite-2-hr-sensor-mode)
  - [Amazfit Zepp OS HR push](https://blog.hyperate.io/post/amazfit-heart-rate-push-live-bluetooth-heart-rate-streaming-with-zepp-os-hyperate-compatible/)
  - [Indian wearable shipments 2025 (IDC via FoneArena)](https://www.fonearena.com/blog/476987/indian-wearable-shipments-2025.html)
  - [W3C Web Bluetooth CG heart-rate demo](https://webbluetoothcg.github.io/demos/heart-rate-sensor/)
- **Regulation:** [CDSCO software guidance (Emergo by UL)](https://www.emergobyul.com/news/india-cdsco-finalizes-guidance-medical-device-software)
- **Bijli Budget:**
  - [SmartBill (BESCOM bill chatbot)](https://github.com/SudeepSBingolli/BESCOM-Bill-Chatbot)
  - [Tamil Nadu 500-unit expansion (SolarQuarter)](https://solarquarter.com/2026/05/29/tnerc-approves-%e2%82%b91545-14-crore-subsidy-as-tamil-nadu-expands-free-electricity-benefit-up-to-500-units/)
  - [TPDDL billing FAQ (pro-rating)](https://www.tatapower-ddl.com/Editor_UploadedDocuments/Content/FAQs_BIlling_Jan'24.pdf)
  - [BRPL Opower trial (IEA)](https://www.iea.org/policies/17804-opower-home-energy-reports-in-india)
- **Monsoon Replay:**
  - [Overture on AWS](https://registry.opendata.aws/overture/)
  - [SimTanka](https://apps.apple.com/ke/app/simtanka/id6446281690)
  - [JNTU RWH project (ETV Bharat)](https://www.etvbharat.com/en/technology/rainwater-harvesting-system-with-a-jntu-student-develops-hydro-harvesting-ai-enn26032405752)
  - [IMD OND 2026 outlook](https://mausam.imd.gov.in/Forecast/marquee_data/Press_Release%20OND_30-09-2026.pdf)
- **Rejected concepts:**
  - [Evaporative Cooler Forecaster (Google Play)](https://play.google.com/store/apps/details?id=com.tenthlight.evaporative_cooler&hl=en_IN)
  - [WRI Cool Cities shade](https://coolcities.wri.org/data-and-methods/shade)

All other sources are in [`evidence/`](evidence/).
