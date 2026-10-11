# 05 — Submission Overlap Map

This is a prediction of what competent competing teams will submit.

## Basis

| Input | Tag | Detail |
|---|---|---|
| Field size at the previous event | FACT | First Commit, same tour and audience, drew **1,180** projects with an open theme |
| Environmental entries in an open theme | FACT | Even there, students built floods (4), waste and food-waste (≥8), satellite air quality, solar quotes and EV charging |
| Expected Environmental Hacks field | INFERENCE | **600–1,200** projects. Assumed split: Air ~35%, Heat & Water ~35%, Waste & Energy ~30%. That is roughly **200–420 per track** |
| Why Air may be over-represented | INFERENCE | The Delhi build day falls in smog season, and the track page explicitly suggests "school safety on bad days" |
| Generic-prompt baseline | INFERENCE | What an LLM produces from a generic prompt (see 04 §F) is assumed to be over-represented |

**How to read the numbers:** "per 100" means out of 100 competent teams across all tracks. Multiply by the field size ÷ 100 for absolute counts (e.g. 6/100 ≈ 36–72 near-duplicates).

**Ratings:** H = high · M = medium · L = low.

---

## 1. Matrix

### Air

| Idea | Per 100 | User value | Tech difficulty | Demo power | Differentiation | Why it gets copied | How we could deviate |
|---|---:|---|---|---|---|---|---|
| AQI dashboard/map + LLM health advice | **10** | L–M | L | M | **L** | Top result of any generic prompt; free APIs | Replace "what is the AQI" with "**when** today is least bad, for **this** group" |
| School AQI alert / closure notifier | **6** | M | L | M | L | Organisers list "school safety on bad days" verbatim | Hour-level timetable re-planning + parent notice + GRAP compliance log |
| Clean-route / exposure-aware navigation | 5 | M | M | M | L | Classic "maps + AQI" combo | Re-time, don't re-route: the diurnal swing (~1.8×) beats route choice within a city (HYPOTHESIS) |
| AQI forecasting ML (LSTM/Prophet) | 4 | L | M | L | L | Standard ML assignment | Don't compete on forecasting; use forecasts as an input |
| Stubble-fire satellite detection | 4 | M | M | M | M | FIRMS data is famous; topical in October | Target the *decision-maker* (field officer or baler operator), not a fire map |
| Indoor air IoT + purifier control | 4 | M | M (hardware) | H | M | Hardware looks impressive | — (hardware time risk) |
| Pollution-source complaint reporting (burning, dust) | 2 | M | L | L | L | Civic-app template | — |

### Heat & Water

| Idea | Per 100 | User value | Tech difficulty | Demo power | Differentiation | Why it gets copied | How we could deviate |
|---|---:|---|---|---|---|---|---|
| Flood/waterlogging alerts + crowd map + safe route | **9** | M | M | M | **L** | Visual, topical; 4 such entries already at First Commit | Only with a very specific user (e.g. basement parking managers) |
| Heatwave alert app/chatbot (Hindi) | **6** | M | L | L | L | Generic prompt + IMD-style thresholds | Turn the forecast into a **work-rest schedule** a supervisor signs |
| Water-usage tracker / smart meter dashboard | 4 | L–M | M | L | L | "Track your usage" template | — |
| Flood prediction ML | 3 | L | M | L | L | Kaggle-style dataset projects | — |
| Leak detection IoT | 3 | M | M (hardware) | M | M | Hardware demo appeal | Software-only leak inference (night flow) |
| Groundwater dashboard/prediction | 3 | L | M | L | M | CGWB data exists | Decision for one borewell owner or society |
| Drought/crop advisory chatbot | 3 | M | L | L | L | Agritech default | — |
| Cooling-centre / shade-finder map | 2 | M | L | M | L | Maps template | — |
| Tanker booking marketplace | 2 | M | M | M | M | Topical after the 2024 Bengaluru crisis | Verify delivery volume and fair price instead of booking |

### Waste & Energy

| Idea | Per 100 | User value | Tech difficulty | Demo power | Differentiation | Why it gets copied | How we could deviate |
|---|---:|---|---|---|---|---|---|
| Waste image classifier ("which bin?") | **8** | L | L | M | **L** | Vision-LLM demo in five minutes | Contamination *audit* for bulk generators with SWM 2026 compliance output |
| Smart bin / collection-route optimisation | 4 | M | M | M | L | IoT + maps classic | — |
| Carbon footprint tracker, gamified | 4 | L | L | L | L | Generic sustainability app | — |
| Rooftop solar potential/ROI calculator or PM Surya Ghar subsidy chatbot | 4 | M | L–M | M | L | Topical (50 lakh homes); calculators are easy | **After-install** performance: expected vs actual, diagnose, act, verify |
| Scrap/kabadiwala marketplace | 3 | M | M | M | L | Uber-for-X template | Price transparency and receipts *for pickers* |
| E-waste pickup/locator | 3 | M | L | L | L | Directory template | Campus drive with authorised-recycler routing and certificates |
| EV charging finder / EV vs ICE calculator | 3 | L | L | L | L | Maps template | — |
| Public-transport / commute-carbon nudge | 2 | M | M | L | M | Gamification | — |

**Total ≈ 100.** The four rows marked **bold** in the "Per 100" column (AQI dashboards, flood alerts, waste classifiers, school AQI alerts and heat alerts) are ~40% of the expected field.

---

## 2. Crowding tiers

| Tier | Definition | Ideas |
|---|---|---|
| **Heavily crowded** | ≥ 6 per 100 | AQI dashboards with LLM advice; flood/waterlogging alerts and maps; waste image classifiers; school AQI alerts; heatwave alert bots |
| **Moderate** | 2–5 per 100 | Clean-route navigation; AQI forecasting; stubble-fire maps; indoor-air IoT; water trackers; leak IoT; groundwater dashboards; drought chatbots; smart bins; carbon trackers; **solar ROI/subsidy tools**; scrap marketplaces; e-waste locators; EV finders; tanker booking |
| **Unusual whitespace** | ≤ 1 per 100 (INFERENCE) | Rooftop solar *post-install* performance + maintenance-right enforcement; WBGT-based work-rest scheduling for site supervisors; hour-level clean-air windows for institutions; SWM 2026 bulk-generator compliance loop for campuses/RWAs; tanker delivery and price verification; time-of-day tariff load shifting; heat-day planning for street vendors |

---

## 3. Patterns behind the crowding

| # | Pattern | Detail |
|---|---|---|
| 1 | Information beats intervention | Most entries end at "show the number" or "send an alert". Very few change a schedule, a contract or a maintenance visit. |
| 2 | The user is "citizens" | Few target the decider: supervisor, principal, owner, facility manager. |
| 3 | AI as a chat skin | Bedrock answers questions about the data. Very few use AI to *read* messy real-world input (photos, bills, displays) and feed a deterministic engine. |
| 4 | No verification | Almost nobody proves the intervention worked. |
| 5 | Naming convergence | Expect a wave of Vayu-, Jal-, Prithvi-, Green-, Eco-, -Guard and -Sense names. The previous field had 99 Guard/Shield/Kavach-style titles (FACT, see 01). |

---

## 4. What this means for us

- **Avoid the bold-numbered rows** unless we have a structural twist that a judge sees in the first 15 seconds.
- **Prefer ideas where the decider, the intervention and the verification are all specific.**
- **Do not let our track choice be driven by salience.** Air is the most salient track in Delhi in October and therefore the most crowded. A whitespace idea in Waste & Energy competes against a far weaker median field.
