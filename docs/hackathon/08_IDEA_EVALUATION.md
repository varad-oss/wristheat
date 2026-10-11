# 08 — Differentiation Test & Evaluation

Every idea from 07 is put through the ten required questions.

**Scoring:**
- **Q1–Q5** are "bad if yes". A pass (✓) means the answer is **No**.
- **Q6–Q10** are "good if yes". A pass (✓) means the answer is **Yes**.
- **~** = partial pass, worth 0.5.
- An idea needs **≥ 8.0** to proceed, *and* must survive the feasibility screen (no hardware dependency, real users reachable, real data this weekend).

**The ten questions:**

| # | Question |
|---|---|
| Q1 | Could a generic AI prompt produce it? |
| Q2 | Does it resemble a common hackathon project? |
| Q3 | Is the novelty only "we added AI"? |
| Q4 | Is the novelty only "we added a dashboard"? |
| Q5 | Is the novelty only "we used AWS"? |
| Q6 | Is the differentiator demonstrable in under 3 minutes? |
| Q7 | Is the differentiator useful? |
| Q8 | Does it change what the user *does*? |
| Q9 | Is there a measurable outcome? |
| Q10 | Is it narrower and deeper than competitors? |

---

## 1. The grid

| # | Idea | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Score | Feasible this weekend? | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|
| I-01 | SunCheck (solar check-up) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **10.0** | Yes (software + photos + open data) | **Advance** |
| I-02 | HeatShift (WBGT work-rest) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | **9.5** | Yes (historical replay) | **Advance** |
| I-03 | Clean-Air Windows (+ I-07) | ~ | ✗ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **8.0** | Yes | **Advance** (crowding flag) |
| I-04 | BinScore 2026 (SWM compliance) | ~ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **9.0** | Yes (campus photos) | **Advance** |
| I-05 | TankerTruth | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **10.0** | Partly (needs a society with a readable sump gauge) | **Advance** (environment-link flag) |
| I-06 | NightFlow (tank leak) | ~ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **9.0** | **No** (hardware procurement and install by Saturday) | **Advance to red team only to test the hardware call** |
| I-07 | Walk-Shift | ~ | ~ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | 8.0 | Yes | **Merge → I-03** (same engine, second user) |
| I-08 | GRAP-Ready | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | ✓ | ~ | ✓ | **8.5** | Partly (GRAP-stage forecast skill unproven) | **Advance** |
| I-09 | Straw Link | ~ | ~ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ~ | ✓ | 8.0 | **No** (users unreachable; fully simulated) | Reject |
| I-10 | Vendor Heat Card | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ~ | ~ | ✓ | 8.5 | **No** (Indian IVR numbers on Amazon Connect, reach, October) | Reject |
| I-11 | Kabadi Ledger | ✓ | ~ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | 9.0 | **No** (no real pickers this weekend; simulated) | Reject (keep for later) |
| I-12 | E-Drive | ~ | ✗ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ~ | 7.5 | Yes | Reject (below bar) |
| I-13 | ToD Shift | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ~ | **9.0** | Partly (meter-data access) | **Advance** (likely merge → I-01) |
| I-14 | Basement Watch | ✗ | ✗ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | 6.5 | Yes (seasonal) | Reject (flood space crowded) |
| I-15 | Cool Roof Planner | ✓ | ✓ | ~ | ✓ | ✓ | ~ | ✓ | ✓ | ✗ | ✓ | 8.0 | Partly (no outcome verification) | Reject (unverifiable outcome) |
| I-16 | Classroom Air Balancer | ~ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 9.0 | **No** (sensor hardware) | Reject (hardware) |
| I-17 | Shuttle Pool | ✗ | ✗ | ✓ | ✓ | ✓ | ~ | ~ | ✓ | ✓ | ~ | 6.5 | Partly (needs a fleet) | Reject |
| I-18 | Borewell Commons | ~ | ~ | ✓ | ~ | ✓ | ✗ | ✓ | ~ | ~ | ✓ | 6.5 | Yes, but feedback takes months | Reject |
| I-19 | Dumpsite Fire Watch | ✓ | ~ | ✓ | ~ | ✓ | ✓ | ~ | ✗ | ~ | ✓ | 7.0 | Partly (no reachable officer; 375 m pixels) | Reject |
| I-20 | Ward Heat Atlas | ~ | ~ | ~ | ✗ | ✓ | ~ | ~ | ✗ | ✗ | ✗ | 4.0 | GIS-heavy | Reject ("big problem solved vaguely") |
| I-21 | Mess Loop | ✗ | ✗ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | 7.0 | Yes | Reject (≥4 near-identical entries last event) |
| I-22 | Rider Shield | ~ | ~ | ✓ | ~ | ✓ | ~ | ~ | ✗ | ~ | ~ | 5.5 | Platforms unreachable | Reject (fold into I-02 as future variant) |
| I-23 | Purifier Reality Check | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | ✗ | ✗ | 7.0 | Yes | Reject (small; fold into I-03 indoor fallback) |

---

## 2. Notes on the hard calls

- **I-03 fails Q2.** "School safety on bad days" is printed on the organisers' track page. Our timing lever and measured counterfactual are real differentiators, but the *topic* will be crowded and judges will see many similar thumbnails. It advances so the red team can test whether the twist survives.

- **I-05 passes all ten but carries a framing risk** the questions don't capture. Judging criterion #1 asks whether it "fixes a real environmental problem". Short-delivery is a fairness problem first. It advances to see whether the red team can strengthen the environmental link.

- **I-06 and I-16 are strong ideas killed by hardware.**
  - We are entering at ~23:00 on Day 1.
  - Ordering and installing sensors, and collecting meaningful night-flow or classroom data by Sunday, is not credible.
  - The rules also strongly favour a *working* demo over an ambitious one.

- **I-11 and I-09 are socially compelling but un-demoable with real users this weekend.**
  - Demoing them would mean simulating the core, against our own rule of real data in the final demo.

- **I-13 scores well but is thin alone.**
  - Time-of-day tariff rollout is uneven, and meter data is hard to get.
  - It naturally extends I-01: same household, same inverter data, "use your solar when it's cheapest".

- **Novelty-only-AI check (Q3).** No advancing idea relies on "we added AI".
  - In every advancing idea, the AI's job is narrow: read messy real-world input (photos, screenshots), draft language, or explain.
  - The core value comes from a deterministic engine: PV model, WBGT, diurnal profile, geometry.

---

## 3. Advancing to red team (top 8)

| Rank | Idea | Track | Score | Why it advances |
|---|---|---|---:|---|
| 1 | I-01 SunCheck | Waste & Energy | 10.0 | Full pass; strongest whitespace (06 W1); real data; verify loop |
| 2 | I-05 TankerTruth | Heat & Water | 10.0 | Full pass; unusual mechanism; environment-link question |
| 3 | I-02 HeatShift | Heat & Water | 9.5 | Planning-not-alerting; strong science; seasonal risk |
| 4 | I-04 BinScore 2026 | Waste & Energy | 9.0 | Regulatory hook; campus-native |
| 5 | I-06 NightFlow | Heat & Water | 9.0 | Tests whether hardware risk can be designed out |
| 6 | I-13 ToD Shift | Waste & Energy | 9.0 | Tests standalone vs merge |
| 7 | I-08 GRAP-Ready | Air | 8.5 | Air track's least-crowded angle |
| 8 | I-03 Clean-Air Windows | Air | 8.0 | Air track's most usable angle; crowding test |

**Rejected: 15 ideas** (I-07 merged into I-03; I-22 and I-23 folded into others).

Each rejection is recorded above with its reason, so we don't relitigate them at 3 AM.
