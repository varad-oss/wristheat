# 13 — Execution Plan (team runbook, Sun 11 Oct 2026)

**Concept:** WristHeat, approved 00:02 IST. **Hard close: 20:00 IST today.** Our submit target: **19:00**.

**Documents**
- Spec: `docs/superpowers/specs/2026-10-11-wristheat-design.md` (also serves as `12_ARCHITECTURE.md`)
- Cloud plan: `docs/superpowers/plans/2026-10-11-wristheat-cloud.md`
- Watch plan: `docs/superpowers/plans/2026-10-11-wristheat-wear.md`
- Prompts to paste: `PROMPT_CLAUDE_CODE_CLOUD.md`, `PROMPT_ANDROID_AGENT.md`

---

## 1. Who does what

| Who | Owns |
|---|---|
| **You (Varad)** | Run Claude Code (cloud); give it the inputs; relay M1 (API URL + token) to the Android dev; wearer in the video; video edit and submission |
| **Android dev** | Runs the Android agent; installs on the watch; integration tests; records the watch screen during filming |
| **Claude Code (cloud)** | Tasks 1–14 of the cloud plan, reporting at M1–M5 |
| **Android agent** | Tasks W1–W8 of the watch plan |
| **Anyone free** | Write-up, CREDITS, README review, optional Builder Center blog, a spotter during filming |

---

## 2. Timeline (IST)

| Time | Cloud (Claude Code + you) | Watch (Android dev + agent) | Gate / decision |
|---|---|---|---|
| 00:45–01:00 | Repo created; paste the cloud prompt with names and emails | Paste the Android prompt; W1 | Both agents running |
| 01:00–03:00 | Tasks 1–7 → **M1 ingest live** | W2–W3 (models, uploader), then W4 **device HR spike** | **03:00:** M1 URL + token sent to the Android dev. **If the HR spike fails** → `hrSource=measure` |
| 03:00–05:00 | Tasks 8–10 (WBGT context, supervisor API, simulator) → M2 | W5–W6 with `fakeApi=true`; then W7 against the real API | **05:00:** watch shows a real state from AWS |
| 05:00–06:30 | Task 11 escalation → M3 | Android dev sleeps after W7 passes | **06:30:** one execution reaches `Close` |
| 06:30–09:00 | Tasks 12–13 dashboard → M4 (Claude Code autonomous; you sleep 06:45–08:45) | Sleep | — |
| 09:00–09:30 | Task 14 | W8 steps 1–3 | — |
| **09:30–10:30** | **Indoor rehearsal of the full loop** (checklist §3) | | **Go / fix** |
| 10:30–11:30 | Fix only what the rehearsal broke. **Feature freeze 11:30** | W8 steps 4–6 | — |
| **11:45–13:30** | **Outdoor hero take** (§4), live dashboard screen recording on the laptop | Watch screen recording | Raw session exported as a fixture |
| 13:30–15:00 | Escalation take with simulated S3; Step Functions graph; CloudWatch; Bedrock report; Hindi audio | Backup outdoor take if needed (15:00–16:00, lower heat) | — |
| 15:00–17:30 | **Video edit** (≤ 2:50), captions; write-up; README final | Help with the write-up | — |
| 17:30–18:30 | YouTube upload (**Public**); check signed out; final push; repo public check | — | — |
| **18:30–19:00** | **Submit the form** | | Submitted ✅ |
| 19:00–20:00 | Buffer only | | — |

**Fallback triggers**

| Condition | Action |
|---|---|
| M1 not live by 03:30 | The watch continues on `fakeApi`; Claude Code drops everything else until ingest works |
| Watch install or HR fails by 06:00 | Film with the simulator plus any short real session recorded, labelled honestly. The concept still stands, but the "watch buzz" beat is lost; avoid this |
| Rehearsal fails at 10:30 | Cut per spec §17; never cut the honesty card or the labels |
| Outdoor take fails | Backup take at 15:00, or use REPLAY of the best real session (badge visible) |

---

## 3. Indoor rehearsal checklist (09:30)

- [ ] Dashboard URL opens; supervisor login works; site strip shows WBGT/flag/PM2.5 with "Updated hh:mm".
- [ ] Watch: Start → Calibrating 2:00 → GREEN; the dashboard shows T1 **LIVE** within 10 s.
- [ ] Hard effort → AMBER → **watch vibrates**; the dashboard card turns AMBER.
- [ ] Rest → RECOVERING → "Recovery confirmed" vibration.
- [ ] Simulator S3 surge → RED incident → banner + Hindi audio → wait 90 s → "Escalated to backup" → both emails received → Acknowledge → S3 recovers → incident closes → report shows.
- [ ] Step Functions console shows the executed path; the CloudWatch `WristHeat` dashboard has data.
- [ ] Airplane-mode the watch for 60 s → "Offline · buffering" → turn it back on → the backlog uploads.
- [ ] `/method` page reads correctly; footer attribution is present.

---

## 4. Outdoor hero take (11:45–13:30)

**Safety (non-negotiable)**
- A spotter with water and shade nearby.
- The wearer stops **immediately** at RED or at any symptom (dizziness, nausea, headache, confusion).
- Maximum 20 min of hard effort. Don't run if unwell, dehydrated or after a heavy meal.
- If the flag is **BLACK**, keep the run to ≤ 10 min at moderate effort.

**Setup**
- Laptop in shade with the dashboard on Live view, recording the screen (QuickTime, 1280×720 window).
- One phone on a tripod filming the run wide; a second phone for watch close-ups.
- Android dev: `adb shell screenrecord` on the watch if Wi-Fi debugging reaches; else close-ups.
- Click **Refresh context** first so the site strip is fresh.

**Sequence**
1. Seated calibration, 2 min (film the watch countdown).
2. Run hard (HR ~160–170). Film the watch at AMBER (vibration: hand on the wrist, the watch overlay "SLOW DOWN") and the dashboard card.
3. If RED is reached (likely only with a RED/BLACK flag, after ~10–12 min), the wearer **stops at once**. Film the RED overlay and the dashboard banner.
4. Rest in shade. Film the recovery: the estimate falls, then the "Recovery confirmed" vibration (≈ 5–7 min after stopping).
5. Stop the session. Claude Code runs `simulator/export_session.py` → the fixture is committed (the REPLAY fallback).

---

## 5. Video script (≤ 2:50)

| Time | Picture | Voice-over (draft) |
|---|---|---|
| 0:00–0:12 | Black card with the news headline: 12 recruitment-run deaths, Jharkhand 2024 | "In 2024, twelve candidates died during a recruitment run in Jharkhand. Heat warnings tell everyone the same number. Your body doesn't." |
| 0:12–0:30 | Dashboard site strip (WBGT with flag, PM2.5), then the architecture card | "WristHeat turns the smartwatch people already wear into a heat-strain early warning. AWS fuses live heart rate with the site's heat and air." |
| 0:30–1:15 | Split screen: runner + watch close-up \| dashboard LIVE card (HR, core estimate ± band, PSI, "~n min to RED") | "Every five seconds the watch streams heart rate to API Gateway. A Lambda runs a Kalman filter developed by the US Army to estimate a core-temperature trend, computes physiological strain, and combines it with Liljegren WBGT from Open-Meteo." |
| 1:15–1:35 | **Watch vibrates**, AMBER overlay; dashboard turns AMBER | "When strain rises, the wearer feels it on their wrist, and the supervisor sees it." |
| 1:35–2:05 | Simulated S3 goes RED → Hindi voice → Step Functions graph → "Escalated to backup" → Acknowledge | "For a simulated trainee who goes red, Step Functions alerts the supervisor in English and Hindi with Amazon Polly, escalates to a backup contact if nobody responds, and waits." |
| 2:05–2:25 | Wearer in shade; "Recovery confirmed" vibration; incident page with metrics + Bedrock report | "The incident only closes when the data confirms recovery. Then Amazon Bedrock writes a factual report from the logged events." |
| 2:25–2:42 | `/method` honesty card | "This is an estimate, not a thermometer. It isn't validated on wrist sensors yet, and simulated trainees are labelled." |
| 2:42–2:50 | Services list + repo + URL | "WristHeat. Built on AWS." |

- Captions on throughout.
- Put AWS on screen early: console shots of API Gateway, Lambda, Step Functions and CloudWatch, not only a logo slide.

---

## 6. Write-up outline (submission form + README)

1. **Problem (2 lines):** the Jharkhand fact; weather-only warnings.
2. **What it does:** wearer and supervisor; the closed loop.
3. **How it works:** ECTemp → PSI → levels with the WBGT flag; Liljegren WBGT; escalation; recovery confirmation.
4. **AWS:** the services table (spec §3), each with its job.
5. **Honesty and limits:** spec §14.
6. **Data and credits:** Open-Meteo (CC BY 4.0), CAMS, thermofeel (Apache-2.0), ECTemp/USARIEM (patent noted), Moran PSI, TB MED 507.
7. **AI tools used:** Claude Code (Anthropic) for research, design and backend code; the Android agent (name it); any others.
8. **Links:** repo, live dashboard (demo login on request), video.

---

## 7. Submission checklist

- [ ] Repo **public**, many commits dated today, README complete, no secrets (`git log -p | grep -i token` is clean).
- [ ] Video **≤ 2:55**, on YouTube, **Public**; plays signed out.
- [ ] Write-up lists the AWS services **and** the AI tools.
- [ ] `CREDITS.md` present.
- [ ] Form submitted by **19:00**; screenshot of the confirmation saved.
- [ ] Every teammate's Builder Center profile verified (needed for prizes/fast-track).
