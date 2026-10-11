# R2-07 — Final Top-3 Comparison

**The three concepts:** the post-red-team survivors from 06.

**Timeline assumptions** (all IST):

| Milestone | Time | Source |
|---|---|---|
| Now | Fri 9 Oct, ~22:45 | — |
| Submission form opens | **Sun 08:00** | WeMakeDevs API |
| Hard close | **Sun 20:00** | WeMakeDevs API |
| Internal "everything filmed" | **Sun 16:00** | Our own buffer |
| Submit by | Sun 18:00 | Our own buffer |

**Scope note:** the 48-hour plans below are **milestone plans**. Architecture and a coding plan come only after approval.

Tags: FACT · INFERENCE · HYPOTHESIS.

---

## A. WristHeat: body-aware heat-strain warning (Heat & Water)

| | |
|---|---|
| **Precise problem** | Heat warnings give everyone in a place the same number. People who exert themselves in heat (runners, outdoor workers, recruitment-test candidates, students in afternoon PE) can't tell when *their own* body is reaching its limit, so they stop too late. |
| **Target user** | **Primary:** the person who supervises exertion in heat (PE teacher, coach, run or test organiser, site supervisor), watching a group. **Secondary:** an individual exerting outdoors with a compatible watch. First journey: one runner plus one coach view. |
| **Why it deserves solving** | **India, 2024:** ~48,000 suspected heatstroke cases and 159 deaths, under-counted (FACT, round-1 sources). **Jharkhand, Aug–Sep 2024:** 12 candidates died during a 10 km / 60-min excise-constable recruitment run; humidity and no health screening were cited (FACT, [Deccan Herald](https://www.deccanherald.com/amp/story/india%2Fjharkhand%2Fhumidity-lack-of-health-screening-change-in-rules-some-reasons-behind-12-deaths-at-jharkhand-recruitment-drive-report-3181567)). **Gap:** five live heat entries plan from weather only (FACT). |
| **Distinctive mechanism** | 1. **Body:** a Kalman filter turns live heart rate into an estimated core temperature (ECTemp, USARIEM; public parameters). 2. **Environment:** WBGT for the exact spot from forecast data. 3. **Fused:** "time to limit at this effort", plus a pre-session "best hour to start". 4. **Loop:** alert → rest → **verified recovery** (estimate and HR both confirm) → cleared. |
| **Competitors** | **In the event:** 0 body-signal entries (FACT). **Outside:** the GarminLabs body-temperature field (2021, Garmin-only, no environment, group or recovery logic); Kenzen and SlateSafety (proprietary hardware); Equivital/Zephyr (pro chest straps). |
| **Technical approach** | Chrome Web Bluetooth reads the standard Heart Rate Service. The stream goes to the cloud, where the filter, WBGT and state logic run. Dashboards subscribe live. Every raw stream is stored, so any session can be replayed deterministically. |
| **Data and models** | ✅ Live HR from the team's watch: **gate**. ✅ Open-Meteo inputs for WBGT. ✅ ECTemp equations. ❌ Wrist-sensor validation (stated on screen). ⬜ Bedrock for the debrief. |
| **Core AWS** (each with a job) | **IoT Core:** ingest live HR over MQTT/WSS. **Lambda:** run the filter, PSI and time-to-limit. **DynamoDB:** session state. **IoT topics** (or AppSync Events): fan out to the coach view. **Step Functions:** alert → rest timer → recovery check → escalate to coach. **Polly:** Hindi/English spoken alerts. **EventBridge Scheduler:** pre-session WBGT plan. **Bedrock:** post-session debrief. **S3:** raw streams for replay. **Amplify + Cognito:** app and identity. **CloudWatch:** visible in the video. |
| **Weather on demo day** | Delhi, Sat 10 Oct, 13:00–15:00: 31.8–32.2 °C, RH 45–48%, wet-bulb ~23.4 °C, sun 600–700 W/m² (FACT, Open-Meteo forecast pulled 9 Oct). In sun this is roughly WBGT ~29 °C (INFERENCE, rough estimate), which is in the moderate-to-high band for hard exertion. Sunday is a little cooler (~29.8 °C). |

**48-hour milestone plan (3–4 people):**

| When | Milestone | Gate / output |
|---|---|---|
| **Fri 22:45–01:00** | **Watch test** on <https://webbluetoothcg.github.io/demos/heart-rate-sensor/> with broadcast mode on. Create the AWS account and request Bedrock access. Create the repo (fresh history). | **GO / NO-GO tonight** |
| Fri late (optional) | Record one 15-min indoor HR session as a replay fixture | Fixture file |
| Sat 08:00–12:00 | Filter + PSI + time-to-limit engine with unit tests against the published equations. WBGT pipeline. Browser capture page streaming to AWS | First live number in the cloud |
| Sat 12:00–14:00 | Live runner view + coach view. Step Functions alert → recovery loop. Polly voice | End-to-end loop indoors |
| **Sat 14:00–16:00** | **Hero take #1 outdoors** (30–40 min hard effort). Record the raw stream and phone video | Real session in the bag |
| Sat 17:00–23:00 | Fix what broke. Pre-session best-hour planner. Coach view with labelled replays of real recorded sessions. Bedrock debrief. Deploy | Deployed URL |
| Sun 08:00–11:00 | Polish. Honesty card. **Backup take** if Saturday's failed (~29–30 °C) | — |
| Sun 11:00–16:00 | Video edit, README, writeup (list AI tools), Builder Center blog | Video ≤ 2:55 |
| Sun 16:00–18:00 | Signed-out link check; submit | Submitted |

**Exact demo sequence (≤ 2:55):**

| Time | Beat |
|---|---|
| 0:00–0:12 | Headline frame: 12 recruitment-run deaths, Jharkhand 2024. Line: "Heat warnings tell everyone the same thing. Your body doesn't." |
| 0:12–0:30 | Pre-session card: "This park, now: WBGT high; best start 07:00." Runner goes anyway (it's a demo). Architecture with each service labelled by its verb |
| 0:30–1:20 | **Split screen:** runner (phone footage) on one side; coach view on the other (live HR, estimated core temperature with band, PSI, "~9 min to limit"). IoT message counter inset |
| 1:20–1:45 | Threshold approaches → Hindi voice alert → Step Functions graph enters *Rest*. Runner stops in shade |
| 1:45–2:10 | Estimate falls; HR recovers → Step Functions **Cleared** (green). "Alert came N min before the limit" |
| 2:10–2:30 | Coach view with 4 people (1 live, 3 **labelled replays**); one goes red; Bedrock debrief |
| 2:30–2:45 | Honesty card: USARIEM ECTemp, chest-strap validation ±0.6 °C, **wrist not validated**, wellness not medical, watches that work |
| 2:45–2:55 | Tally card + URL |

**Biggest remaining uncertainty:** whether the team's watch broadcasts standard BLE heart rate, and whether optical HR stays clean during a hard run.

**Strongest reason it might not win:**
1. Judges may read it as a *fitness* gadget rather than *environmental*, or doubt the estimate's validity.
2. It sits in the **most crowded track** (Heat & Water, 48% of visible entries).

---

## B. Bijli Budget: "Was it you or the weather?" plus the free-unit cliff (Waste & Energy)

| | |
|---|---|
| **Precise problem** | Households in free-unit states can't tell whether a bill rise came from their behaviour or the weather. They discover the cliff only when the bill arrives. |
| **Target user** | A bill-payer in a true-cliff state (Telangana, Karnataka, Punjab, Tamil Nadu, Kerala, MP) or Delhi. First journey: one teammate's household in a city with cooling signal. |
| **Why it deserves solving** | ~5 crore households are on threshold schemes, ~3.5 crore in true-cliff states (FACT, partly sourced). Delhi's zero-bill households fell from 43.9 lakh (Feb 2025) to 18.3 lakh (Jul 2025) (FACT). Fans, ACs and coolers are 40% of household electricity (FACT, CLASP–BEE 2024). |
| **Distinctive mechanism** | 1. A household-run **weather-normalised counterfactual** (base + CDD slope) separates behaviour from weather. 2. **P(crossing the pro-rated cliff)** before cycle end, as a daily budget. 3. Verification from meter photos days apart, normalised by cooling degree-hours, with an honest "can't tell yet". |
| **Competitors** | SmartBill (BESCOM: OCR + cliff + temperature-aware next bill); TPDDL self-read; 21 "bijli" repos; Opower (US); CalTRACK. **No Indian consumer tool found** doing the counterfactual or the crossing probability (21 Play listings). |
| **Technical approach** | Upload bill-history screenshots and meter photos → extract and confirm → fit the regression → project with the 16-day forecast → apply the rule pack → budget → schedule re-reads → verify. |
| **Data and models** | ✅ Weather. 🟨 Bill and meter extraction (53–80% vision accuracy, so a confirm step). 🟨 Rule pack (Delhi at 201 units unresolved). ⬜ Projection accuracy (±13–24%). |
| **Core AWS** | **S3:** uploads. **Textract / Bedrock vision:** read bills and meters. **Lambda:** regression and projection. **DynamoDB:** ledger. **Step Functions:** read → validate → project → wait for the next reading → verify. **EventBridge Scheduler:** re-read nudges and cycle-end. **SES / web push:** notifications. **Bedrock:** Hindi/English explanation. **Amplify + Cognito.** |

**48-hour milestone plan:**

| When | Milestone |
|---|---|
| Fri tonight | **Gate:** a teammate in Delhi, Hyderabad, Chennai or Punjab exports 12–13 months of bill history and photographs their meter |
| Sat 08:00–14:00 | Extraction + confirm UI; rule pack with citations; CDD regression |
| Sat 14:00–20:00 | Projection and crossing probability; budget; Step Functions verify loop |
| Sat night | Meter photo #2; deploy |
| Sun 08:00 | Meter photo #3; verification run; video; submit |

**Exact demo sequence:**

| Time | Beat |
|---|---|
| 0:00 | "My bill went up 18% *(illustrative)*. Was it me?" |
| 0:15 | **Side by side:** a naive analyser says "you used more"; ours says "Oct 2026 had ~95 CDD by the 24th vs 66 in all of Oct 2025 (FACT, Delhi); weather explains most of it" |
| 0:45 | Meter photo → units so far → "P(stay under 200) = X% at ≤ Y units/day" |
| 1:30 | Step Functions waiting → photo #2 → verified or "can't tell yet", with the band |
| 2:10 | Rule pack across states |
| 2:30 | Honesty card |
| 2:45 | Tally |

**Biggest remaining uncertainty:** whether a teammate's real history in a cooling-signal city exists and gives a clean fit.

**Strongest reason it might not win:** judges see "another bill app". The differentiator is analytical, not visual.

---

## C. Monsoon Replay: RWH sizing from real roofs and real monsoons (Heat & Water)

| | |
|---|---|
| **Precise problem** | Housing societies size RWH tanks and pits with annual-average calculators that imply 100% capture. They over-build tanks, under-build recharge, and can't price the tanker savings. |
| **Target user** | An RWA or campus committee in Bengaluru or Chennai. |
| **Why it deserves solving** | Bengaluru charges a 25–50% water-bill penalty, and only ~18% of connections have RWH (FACT). Delhi Jal Board withdrew rebates from 119 societies with non-working systems (FACT). The 2026 south-west monsoon was 87% of normal (FACT). |
| **Distinctive mechanism** | A daily replay of real monsoons over **many real roofs from AWS Open Data**, with recharge-pit routing, tanker ₹ and a rainfall uncertainty band. |
| **Competitors** | SimTanka; a JNTU Jal Shakti 2025 winner; KSCST advisor; 14 RWH student repos (SIH PS 53 genre). |
| **Technical approach** | Athena on Overture → roofs → three-model rainfall → water balance → committee pack. |
| **Data** | ✅ Roofs. 🟨 Rain (−48% to +33% vs IMD). ❌ Measured validation. |
| **Core AWS** | **Athena + S3 (Overture Open Data):** roofs. **Lambda:** replay. **DynamoDB.** **Amazon Location:** map. **Bedrock:** committee pack. **Amplify.** |
| **48-hour plan** | Sat: data plus replay. Sat night: UI plus pack. Sun: video. Lowest build risk of the three, ~25–30 h. |
| **Demo** | Real complex on a map → Athena in the console → roofs → animated 2024 monsoon fill and overflow, with the band → tank-size curve → tankers saved → pack. |
| **Biggest uncertainty** | Whether judges trust model rainfall that is known to miss cloudbursts. |
| **Strongest reason it might not win** | Prior art plus a familiar SIH genre, and there is no live or physical moment. |

---

## Side-by-side

| Dimension | A. WristHeat | B. Bijli Budget | C. Monsoon Replay |
|---|---|---|---|
| Score (05) | 71.0 (62 if the watch gate fails) | 65.0 | 61.5 |
| Mechanism novelty in the field | **High** (0 entries) | Medium-low (bill-app genre) | Low (SIH genre) |
| Visual proof | **Physical, in one take** | Numbers / side-by-side | Animation |
| Data you can produce yourselves | Own HR, live | Own bills and meter | Public only |
| Build risk | Medium-high (device-gated) | Medium | **Low** |
| Breadth | Medium (device-limited) | **High** | Medium |
| Track crowding | Most crowded track | **Least crowded track** | Most crowded track |
| AWS depth on screen | **High** (streaming + state machine live) | High | Medium-high (Athena + Open Data) |
| Fatal-if-wrong | Watch can't broadcast | No teammate history | None (but low ceiling) |
