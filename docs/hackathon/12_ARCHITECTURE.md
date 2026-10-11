# WristHeat — Design Spec

**Status:** Approved by the team, Sun 11 Oct 2026, 00:32 IST. This is the single source of truth for both builds.
**Event:** AWS Environmental Hacks (WeMakeDevs × AWS Builder Center). Track: **Heat & Water**.
**Hard deadline:** **Sun 11 Oct 2026, 20:00 IST.** Internal submit target: 19:00 IST.
**Builds:** (1) the Wear OS watch app, built by the Android agent; (2) the AWS cloud plus the supervisor dashboard, simulator and tooling, built by Claude Code.

Tags used: **FACT** (sourced), **INFERENCE** (reasoned), **HYPOTHESIS** (untested).

---

## 1. Problem, user, success

**Problem.** A heat warning gives everyone in a place the same number. Someone exerting themselves in heat (a trainee on a recruitment run, an NCC cadet, a student athlete, a site worker) cannot tell when *their own* body is reaching its limit. The person supervising them cannot see it either. People stop too late.

- FACT: In Jharkhand, Aug–Sep 2024, 12 candidates died during a 10 km excise-constable recruitment run. Humidity and the absence of health screening were cited ([Deccan Herald](https://www.deccanherald.com/amp/story/india%2Fjharkhand%2Fhumidity-lack-of-health-screening-change-in-rules-some-reasons-behind-12-deaths-at-jharkhand-recruitment-drive-report-3181567)).
- FACT: None of the 111 live Environmental Hacks projects we scanned uses a body signal. The five worker-heat entries all plan from weather alone (our scan, 9–10 Oct).

**Primary user:** the **supervisor** of a group exerting in heat (coach, NCC instructor, test organiser, site supervisor).
**Secondary user:** the **wearer**, who gets a vibration and an instruction on their own wrist.

**Mechanism.** The product fuses three things:

1. **Body.** Live heart rate from the wearer's own smartwatch feeds a Kalman filter (ECTemp, USARIEM). The filter gives an *estimated* core-temperature trend with an uncertainty band, and from that a Physiological Strain Index (PSI).
2. **Environment.** WBGT for the exact site, computed with the physically based Liljegren method from Open-Meteo inputs, plus PM2.5 / AQI.
3. **Closed loop.** A risk state on the wrist and on the supervisor dashboard, then escalation (supervisor → backup contact), then **recovery confirmed from the data** before the incident closes.

**Success (for the submission):**
- A ≤ 2:55 video showing real heart rate from the team's Galaxy Watch5 Pro flowing through AWS to a supervisor dashboard, with the wearer's watch vibrating on a state change.
- A full escalation incident visible in the Step Functions graph, closed by a data-confirmed recovery.
- A public repo with continuous commit history from today, a deployed URL, and a write-up listing AWS services and AI tools used.

---

## 2. Scope

**In scope**

| Area | Included |
|---|---|
| Watch app | Live HR via Health Services, 5-second uploads, on-wrist state, vibration, calibration, offline buffering |
| Cloud | Ingest, risk engine, environment context, escalation workflow, Polly voice alerts, email alerts, Bedrock incident report, metrics and tracing |
| Dashboard | Group view, trainee detail chart, alert banner + acknowledge, incident report, method/honesty page, EN/HI alert text |
| Tools | Simulator for labelled simulated trainees, recorder/replayer for real sessions, seed and smoke scripts |

**Out of scope (YAGNI, do not build):** phone companion app; Health Connect; SMS; IoT Core/MQTT; GPS on the watch; multi-site admin UI; user self-sign-up; editing trainees in the UI; push notifications; offline dashboard; any claim of clinical accuracy.

---

## 3. System overview

```
[Galaxy Watch5 Pro · Wear OS app]  HR ~1 Hz (Health Services ExerciseClient, foreground service)
        │ every 5 s  POST /v1/ingest  (x-device-token)
        ▼
[API Gateway HTTP API] ──► [Lambda ingest] ── risk engine (ECTemp → PSI → level → state machine)
        ▲                       │  writes: Readings, Minutes, Sessions        reply: state + alert → watch vibrates
        │                       │  on → RED: open Incident + StartExecution
[simulator.py / replay.py]      ▼
 (same endpoint,        [Step Functions: wristheat-escalation]
  source=simulated|replay)   Notify (SNS email + Polly EN/HI → S3)
                             → WaitForAck (task token, ACK timeout) ──timeout──► Escalate (SNS backup) → WaitForAck
                             → WaitForRecovery (task token, released by ingest on "recovery confirmed")
                             → Close (metrics + Bedrock report, template fallback)

[EventBridge Scheduler, every 10 min] → [Lambda context] → Open-Meteo forecast + air quality
                                           → Liljegren WBGT (thermofeel 2.3.0) → Sites table

[Dashboard: React SPA on S3 + CloudFront] ── Cognito login ──► API (JWT authorizer)
        polls GET /v1/roster every 3 s · GET series · incidents · POST ack
```

### AWS services and the job each one does

| Service | Job (say this verb in the video) |
|---|---|
| API Gateway (HTTP API) | Receives the watch stream; JWT-protects supervisor routes |
| Lambda (Python 3.12, arm64) | Runs the risk engine, context fetch, workflow steps, supervisor API |
| DynamoDB (on-demand, TTL) | Stores readings, per-minute estimates, session state, incidents, sites |
| Step Functions (Standard) | Runs the escalation: notify → wait for acknowledgement → escalate → wait for confirmed recovery → close |
| EventBridge Scheduler | Refreshes site heat and air every 10 min |
| Amazon Polly (neural, Kajal, en-IN + hi-IN) | Spoken alert in English and Hindi |
| Amazon SNS (email) | Alerts the supervisor, then the backup contact |
| Amazon Bedrock (Converse, Nova Lite via the APAC inference profile) | Writes the incident report from logged facts only |
| Amazon S3 | Alert audio and dashboard assets |
| Amazon CloudFront | Serves the dashboard over HTTPS |
| Amazon Cognito | Supervisor sign-in |
| AWS Secrets Manager | Holds the device token |
| CloudWatch + X-Ray (via Powertools for AWS Lambda) | Logs, custom metrics, a WristHeat dashboard, traces |
| AWS CDK (TypeScript) / CloudFormation | Entire stack as code, one deploy command |

**Region:** `ap-south-1` (Mumbai) for everything. Bedrock is called in `ap-south-1` through a geo (APAC) cross-region inference profile.

---

## 4. Repository layout

```
wristheat/
  README.md  CREDITS.md  LICENSE (MIT)  .gitignore  Makefile
  docs/                      spec, plans, hackathon research, architecture diagram
  contracts/                 JSON Schemas + example payloads shared by watch and cloud
  backend/                   Python package `wristheat` + Lambda handlers + pytest tests
  infra/                     AWS CDK app (TypeScript)
  dashboard/                 React + Vite + TypeScript SPA
  simulator/                 simulate.py, replay.py, export_session.py
  scripts/                   build_lambdas.sh, deploy.sh, seed.py, smoke.py
  fixtures/                  exported real sessions (JSON) for replay
  wear/                      Android Studio project (Wear OS app)
```

`.gitignore` must include: `local.properties`, `.env*`, `cdk.out/`, `build/`, `node_modules/`, `dist/`, `*.keystore`, `__pycache__/`, `.venv/`, `scripts/.seed-output.json`, `simulator/.state.json`, `infra/outputs.json`, `.gradle/`, `.idea/`, `wear/app/build/`.

---

## 5. API contract (shared by the watch and the cloud)

Base URL: the HTTP API default endpoint, e.g. `https://abc123.execute-api.ap-south-1.amazonaws.com`. All paths are prefixed `/v1`. JSON in and out, UTF-8. All timestamps are **epoch milliseconds, UTC**. Errors use `{"error": "<code>", "message": "<human text>"}`.

### 5.1 Device routes (header `x-device-token: <token>`)

Wrong or missing token → `401 {"error":"unauthorized"}`.

**`POST /v1/ingest`**

Request:
```json
{
  "schema": 1,
  "trainee_id": "T1",
  "session_id": "3f6c1e9a-0b7d-4a51-9a52-0c3c0d2f8e11",
  "source": "live",
  "device": "SM-R920",
  "samples": [
    {"t": 1791700000000, "bpm": 92},
    {"t": 1791700001000, "bpm": 93}
  ]
}
```

| Field | Rule |
|---|---|
| `schema` | must be `1` |
| `trainee_id` | must exist in Trainees, else `404 unknown_trainee` |
| `session_id` | 8–64 chars, `[A-Za-z0-9-]`; created by the client at session start |
| `source` | `live` \| `simulated` \| `replay`. Trainees of kind `simulated` may only send `simulated`; kind `real` may send `live` or `replay`. Mismatch → `400 source_mismatch` |
| `device` | free text ≤ 40 chars |
| `replay_of` | optional; required when `source` is `replay` (the original session id). Stored on the session |
| `samples` | 0–600 items, ascending by `t`. An empty list is a valid poll that returns current state |
| `samples[].bpm` | integer. Values outside 30–230 are dropped and counted in `dropped` |
| `samples[].t` | not more than 60 s in the future. For `live`, not older than 6 h. Violations are dropped |

Response `200`:
```json
{
  "schema": 1,
  "trainee_id": "T1",
  "session_id": "3f6c1e9a-0b7d-4a51-9a52-0c3c0d2f8e11",
  "accepted": 5,
  "dropped": 0,
  "state": "AMBER",
  "state_since": 1791700060000,
  "calibration_remaining_s": 0,
  "hr_now": 158,
  "hr0": 74,
  "core_est_c": 37.92,
  "core_band_c": 0.6,
  "psi": 5.9,
  "minutes_to_red": 6,
  "env": {
    "wbgt_c": 31.4, "flag": "RED", "pm25": 72.0, "us_aqi": 158,
    "updated_at": 1791699600000, "stale": false
  },
  "advice": {"en": "Strain rising. Slow down and drink water.", "hi": "तनाव बढ़ रहा है। गति धीमी करें और पानी पिएँ।"},
  "alert": "NONE",
  "incident_id": null,
  "server_time": 1791700065000
}
```

| Field | Meaning |
|---|---|
| `state` | `CALIBRATING` \| `GREEN` \| `AMBER` \| `RED` \| `RECOVERING` |
| `calibration_remaining_s` | seconds left in calibration, `0` once done |
| `hr_now` | rounded mean of this batch's accepted samples; if the batch is empty, the last known value; `null` if none yet |
| `hr0`, `core_est_c`, `psi` | `null` while calibrating; `psi` rounded to 1 dp, `core_est_c` to 2 dp |
| `core_band_c` | always `0.6` (see §7.6) |
| `minutes_to_red` | integer projection (§7.5) or `null` |
| `env` | latest site context; `null` if none fetched yet. `stale` = older than 45 min |
| `alert` | **one-shot**: `AMBER`, `RED` or `RECOVERED` appears in exactly one response, the first one after that transition. Otherwise `NONE`. The watch vibrates only on this field |

**`POST /v1/sessions/{session_id}/end`** → `200 {"ended": true}`. Marks the session `ENDED`. Unknown session → `404 unknown_session`.

### 5.2 Supervisor routes (Cognito JWT, `Authorization: Bearer <id or access token>`)

**`GET /v1/roster`**
```json
{
  "site": {
    "site_id": "kgp", "name": "IIT Kharagpur campus", "lat": 22.3149, "lon": 87.3105,
    "env": {"wbgt_c": 31.4, "flag": "RED", "temp_c": 31.2, "rh": 71, "wind_ms": 2.1,
            "pm25": 72.0, "us_aqi": 158, "updated_at": 1791699600000, "stale": false,
            "coolest_hour": {"local": "06:00", "wbgt_c": 26.9}}
  },
  "trainees": [
    {"trainee_id": "T1", "name": "Varad", "kind": "real", "source": "live", "session_id": "…",
     "state": "AMBER", "state_since": 1791700060000, "hr_now": 158, "hr0": 74,
     "core_est_c": 37.92, "core_band_c": 0.6, "psi": 5.9, "minutes_to_red": 6,
     "last_seen": 1791700065000, "stale": false, "incident_id": null, "replay_of": null}
  ],
  "open_incidents": [{"incident_id": "inc-…", "trainee_id": "S3", "status": "NOTIFIED", "opened_at": 1791700100000}],
  "server_time": 1791700066000
}
```
- One site per deployment.
- A trainee with no session appears with `state: null` and `session_id: null`.
- `stale` = no ingest for that session in the last 30 s.
- `replay_of` is the original session id when `source` is `replay`.

**`GET /v1/sessions/{session_id}/series?since_minute=<epoch_minute>`** returns closed minutes only, ascending:
```json
{"session_id": "…", "points": [
  {"minute": 29861666, "hr": 151.2, "n": 60, "core_est_c": 37.81, "core_var": 0.0123,
   "psi": 5.1, "state": "AMBER", "wbgt_c": 31.0, "flag": "YELLOW"}]}
```

**`GET /v1/incidents?status=open|all`** → `{"incidents": [ {incident summary} ]}`, newest first, max 50.

**`GET /v1/incidents/{incident_id}`** → the full incident (§6) plus `audio: {"en": "<presigned url, 15 min>", "hi": "<…>"}` and `console_url` (the Step Functions execution in the AWS console).

**`POST /v1/incidents/{incident_id}/ack`** body `{"note": "cooling started"}` → `200 {"status": "ACKNOWLEDGED"}`; `409 already_acknowledged` if acknowledged or closed. `acked_by` is the Cognito username from the token.

**`POST /v1/context/refresh`** → runs the context update for the site now and returns `{"env": {…}}`. Used before filming.

**CORS:** allow the CloudFront domain and `http://localhost:5173`. Methods `GET, POST, OPTIONS`; headers `authorization, content-type`.
**Throttling:** default route 20 rps, burst 40.

`contracts/` holds `ingest_request.schema.json`, `ingest_response.schema.json` and `examples/*.json`. Both builds test against them.

---

## 6. Data model (DynamoDB, on-demand)

| Table | Keys | Main attributes | TTL |
|---|---|---|---|
| `Sites` | PK `site_id` | name, lat, lon, env (map), env_updated_at, forecast (list of {t, wbgt_c, flag}, next 24 h), coolest_hour | — |
| `Trainees` | PK `trainee_id` | name, kind (`real`\|`simulated`), age, site_id, rest_hr_override (optional), current_session_id, hidden (bool; `true` only for the smoke-test trainee `S0`, which the roster omits) | — |
| `Sessions` | PK `session_id` | trainee_id, source, device, replay_of, started_at, last_seen, status (`ACTIVE`\|`ENDED`), engine (map: see §7), state, state_since, pending_alert, incident_id, hr_now, version | 30 d |
| `Readings` | PK `session_id`, SK `t` | bpm | 30 d |
| `Minutes` | PK `session_id`, SK `minute` | hr, n, core_est_c, core_var, psi, level, state, wbgt_c, flag, pm25 | 30 d |
| `Incidents` | PK `incident_id` | trainee_id, session_id, status, opened_at, trigger (map), events (list of {t, type, detail}), ack_token, ack_pending, acked_at, acked_by, recovery_token, recovered_at, closed_at, outcome, audio (map of S3 keys), report (map: text, source, model, generated_at), metrics (map), execution_arn | 90 d |

**Incident status:** `NOTIFIED → (ESCALATED) → ACKNOWLEDGED → CLOSED`, or `… → CLOSED` with outcome `recovered_unacknowledged` / `not_confirmed`.

**Event types:** `OPENED, NOTIFIED, AUDIO_READY, ESCALATED, ACKNOWLEDGED, RECOVERY_CONFIRMED, REPORT_READY, CLOSED`.

**Concurrency:** Sessions writes use a conditional update on `version`. On a conflict, reload and retry up to 3 times. Each client sends one batch at a time per session, so conflicts are rare.

**Scale note:** the incident list uses Scan with a filter. That is acceptable at demo scale (< 1,000 items) and should be documented as a known limit.

---

## 7. Risk engine (pure Python, no AWS imports)

### 7.1 Minute aggregation and calibration

- **Minute index:** `m = t // 60000`.
- **Partial minute:** the engine keeps one open minute `{m, sum, n}`. A minute is **closed** when an accepted sample arrives with a later minute index. Samples older than the last closed minute are stored in Readings but ignored by the engine.
- **Duplicates and retries:** the engine keeps `last_t`, the newest sample time it has accepted. A sample with `t ≤ last_t` is ignored by the engine and is not counted as dropped, so a watch retry never double-counts. Readings writes are idempotent on (`session_id`, `t`).
- **Big flushes:** one batch may close many minutes (up to 600 samples after an outage). Minutes are processed in order. `pending_alert` holds the alert of the **last** transition in the batch.
- **Gap minute:** a closed minute with `n < 10` (live, simulated or replay). The filter is not updated and the minute is recorded with `hr = null`. A gap never changes state.
- **Calibration:** the first **2 non-gap closed minutes** of the session.
  - `hr0 = min(mean_1, mean_2)`, clamped to `[45, 100]` and rounded.
  - If the trainee has `rest_hr_override`, it is used and calibration is skipped (simulated trainees).
  - The filter runs during calibration; levels are not evaluated.
  - `calibration_remaining_s = max(0, ceil(((first_minute + 2)·60000 − now_ms) / 1000))`, where `first_minute` is the minute index of the session's first accepted sample. It is `0` once `hr0` is set. If calibration is still incomplete when this reaches 0 (gap minutes), report `0` and keep `CALIBRATING` until two non-gap minutes exist.

### 7.2 ECTemp core-temperature filter

Published sources: Buller et al. 2013; US patent US10702165B2; USARIEM T17-08. Initial variance follows de Korte et al. 2022.

```
b0 = -7887.1, b1 = 384.4286, b2 = -4.5714       # HR = b2·CT² + b1·CT + b0
gamma2 = 0.000484                                # process variance per minute (0.022²)
sigma2 = 356.5654                                # measurement variance (18.88²)
CT0 = 37.1, v0 = 0.02

step(ct, v, hr):
    v_p = v + gamma2
    c   = 2·b2·ct + b1
    k   = v_p·c / (c²·v_p + sigma2)
    ct' = ct + k·(hr − (b2·ct² + b1·ct + b0))
    v'  = (1 − k·c)·v_p
```

Golden values (computed 11 Oct; tests must match to ±0.0005 for `ct` and ±0.00001 for `v`):

| Case | Expected |
|---|---|
| `step(37.1, 0.02, 165)` | `ct = 37.290475`, `v = 0.018330` |
| `step(37.1, 0.0, 80)` | `ct = 37.099811`, `v = 0.000483` |
| Sequence `[75]*2 + [165]*20 + [100]*10` from (37.1, 0.02) | after min 2: `37.0656`; min 12: `38.0408`; min 22: `38.4650`; min 32: `38.1118` |
| Sequence `[80]*10 + [150]*30 + [100]*20` from (37.1, **0.0**) | first minute with `ct ≥ 38.0` is **34**; peak `38.1827` (matches the published-parameter simulation in our audit within 1 min) |

### 7.3 Physiological Strain Index

Moran et al. 1998:

```
PSI = 5·(CT − 37.1)/(39.5 − 37.1) + 5·(HR − HR0)/(180 − HR0)
```
- `CT` is this minute's filter output; `HR` is the minute mean.
- Clamp to `[0, 10]`. Round to 1 dp **for display only**. All threshold comparisons in §7.4–7.5 use the unrounded PSI and CT.
- Published bands (Buller): < 5 low, 5–6 moderate, 7–8 high, 9–10 very high.

### 7.4 Levels and state machine

**Heat flag from WBGT** (US Army TB MED 507 categories, °C, compare after rounding to 1 dp):

| WBGT (°C) | Flag |
|---|---|
| ≥ 32.2 | `BLACK` |
| ≥ 31.1 | `RED` |
| ≥ 29.5 | `YELLOW` |
| ≥ 27.8 | `GREEN` |
| ≥ 25.6 | `WHITE` |
| otherwise | `NONE` |

If env is missing or stale, use `NONE` (body-only).

**Candidate level `L` for each closed, non-gap minute after calibration:**

| L | Condition |
|---|---|
| `RED` | `PSI ≥ 7.0` **or** `CT ≥ 39.0` **or** (`PSI ≥ 6.0` **and** flag ∈ {RED, BLACK}) |
| `AMBER` | `PSI ≥ 5.0` **or** (`PSI ≥ 4.0` **and** flag ∈ {YELLOW, RED, BLACK}) |
| `GREEN` | otherwise |

The PSI cut-offs at 5 and 7 are the published bands. The flag-adjusted rules are **our heuristic** and are labelled as such on the method page.

**State machine.** Ranks: GREEN 0, AMBER 1, RED 2; RECOVERING counts as rank 1 for escalation.

1. **After calibration:** state becomes `GREEN`.
2. **Escalate:** if the last 2 non-gap minutes both have `L ≥ X` and `rank(state) < X`, go to `X`. Check RED before AMBER. Set `pending_alert = X`.
3. **De-escalate:** if state is AMBER or RED and the last 2 non-gap minutes both have `L < state`, go to `RECOVERING` (no alert).
4. **Confirm recovery:** if state is `RECOVERING` and the last **3** non-gap minutes **each** have
   - `L = GREEN`,
   - `HR ≤ HR0 + 30`,
   - `PSI < 4.0`,
   - and the current minute's `CT ≤` the `CT` three non-gap minutes earlier,

   then go to `GREEN` and set `pending_alert = RECOVERED`. Emit event `RECOVERY_CONFIRMED`.
5. Rule 2 takes priority over rules 3 and 4 in the same minute.
6. **Entering RED** emits `RED_ENTERED`. The ingest handler opens an incident if the session has none open.

**Reference vectors** (per-minute mean HR, minute 1 = first closed minute, HR0 from calibration = 75; verified with a reference implementation on 11 Oct):

| Id | Minute HRs | Flag | Events (minute: event) |
|---|---|---|---|
| D1 | `[75,75] + [165]*20 + [100]*10` | RED | 2: CALIBRATED, 4: AMBER_ENTERED, 12: RED_ENTERED, 24: RECOVERING_ENTERED, 25: RECOVERY_CONFIRMED |
| D2 | same as D1 | YELLOW | 4: AMBER_ENTERED, 22: RED_ENTERED, 24: RECOVERING_ENTERED, 25: RECOVERY_CONFIRMED |
| D3 | same as D1 | NONE | 6: AMBER_ENTERED, 22: RED_ENTERED, 24: RECOVERING_ENTERED, 25: RECOVERY_CONFIRMED |
| D4 | `[75,75] + [165]*14 + [140,120,110,104,100,98,96,95,94,93]` | RED | 4: AMBER_ENTERED, 12: RED_ENTERED, 18: RECOVERING_ENTERED, 22: RECOVERY_CONFIRMED |
| D5 | `[75,gap,75] + [165,gap,165,165] + [165]*8` | RED | 3: CALIBRATED, 6: AMBER_ENTERED, 14: RED_ENTERED |

Also: `minutes_to_red` after minute 3 is **8** in D1 and **18** in D2. Calibration means `[110,120]` → HR0 = **100**; `[40,42]` → HR0 = **45**.

### 7.5 Minutes to RED (projection)

- **When:** state ∈ {GREEN, AMBER, RECOVERING} and the mean HR of the last 3 non-gap minutes is `≥ HR0 + 20`.
- **How:** copy `(ct, v)` and step the filter forward with that mean HR, up to 90 times. At each step evaluate the RED condition (§7.4) with the current flag.
- **Result:** return the first step count `n` (1–90) at which it holds; otherwise `null`. When state is RED, return `null`.
- **Label everywhere:** "~n min to RED at this effort (model projection)".

### 7.6 Uncertainty band

Show `core_est_c ± 0.6 °C`.

- **Why 0.6 (FACT):** the published 95% limits of agreement on chest-strap HR are ±0.45–0.63 °C in the lab, and up to ±1.2 °C in the field.
- **Wrist sensors (FACT):** ECTemp has **never been validated** on wrist optical HR. Sensitivity for CT > 39 °C was < 50% in elite athletes (de Korte 2022).
- **Required copy:** the dashboard and the method page say "estimated trend, not a thermometer".

### 7.7 Advice text

Chosen by state, plus `indoors = env.pm25 > 60` (India's 24-h PM2.5 standard, 60 µg/m³). A native Hindi speaker should proofread before filming.

| Situation | en | hi |
|---|---|---|
| CALIBRATING | Sit still — measuring your resting heart rate. | स्थिर बैठें — आपकी आराम की हृदय गति मापी जा रही है। |
| GREEN | Strain low. Keep drinking water. | तनाव कम है। पानी पीते रहें। |
| AMBER | Strain rising. Slow down and drink water. | तनाव बढ़ रहा है। गति धीमी करें और पानी पिएँ। |
| RED, outdoors | Stop now. Rest in shade and cool down with water. | अभी रुकें। छाँव में आराम करें और पानी से शरीर ठंडा करें। |
| RED, indoors | Stop now. Rest indoors — outdoor air is poor (PM2.5 {pm25} µg/m³). | अभी रुकें। अंदर आराम करें — बाहर की हवा खराब है (PM2.5 {pm25} µg/m³)। |
| RECOVERING, outdoors | Recovering. Stay in shade until cleared. | रिकवरी जारी है। साफ़ संकेत मिलने तक छाँव में रहें। |
| RECOVERING, indoors | Recovering. Stay indoors until cleared. | रिकवरी जारी है। साफ़ संकेत मिलने तक अंदर रहें। |
| Response carrying `alert = RECOVERED` | Recovery confirmed. Resume only at an easier pace. | रिकवरी की पुष्टि हुई। अब केवल धीमी गति से दोबारा शुरू करें। |

`{pm25}` is rounded to an integer.

---

## 8. Environmental context

**Fetch:** every 10 min (EventBridge Scheduler), and on `POST /v1/context/refresh`.

**Weather (Open-Meteo forecast, keyless)** — `latitude`, `longitude`:
- `current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,shortwave_radiation,direct_radiation`
- `hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,shortwave_radiation_instant,direct_radiation_instant`
- `wind_speed_unit=ms`, `timezone=auto`, `forecast_days=2`
- **The builder must make one live call first and confirm each variable name.** If a name is rejected, use the closest documented variable and record the substitution in the README. Never invent values.

**Air (Open-Meteo air quality, CAMS):** `https://air-quality-api.open-meteo.com/v1/air-quality` with `current=pm2_5,pm10,us_aqi`, `timezone=auto`.

**WBGT:** `thermofeel==2.3.0` (ECMWF, Apache-2.0), function `calculate_wbgt_liljegren(t2_k, rh, pressure_hPa, va_10m_ms, ssrd_Wm2, fdir, cossza)`. Result in kelvin; convert to °C.
- `fdir = direct / shortwave` when `shortwave ≥ 1`, else `0`, clamped to `[0, 1]`.
- `cossza` comes from the NOAA solar-position approximation for the site's lat/lon at the observation time (UTC).
- Golden values:

| Inputs (°C, %, hPa, m/s, W/m², fdir, cossza) | WBGT (±0.05 °C) |
|---|---|
| (31, 70, 1005, 2.0, 700, 0.7, 0.8) | 31.99 |
| (31, 70, 1005, 2.0, 0, 0, −0.1) | 27.65 |

- Golden `cossza` for lat 22.3149, lon 87.3105 on 2026-10-11 (±0.002):

| UTC | cossza |
|---|---|
| 00:30 | 0.0870 |
| 06:30 | 0.8658 |
| 12:30 | −0.1751 |

- **Why not the simple formula (FACT, our check):** the simple ACSM/BoM approximation overstates humid Indian heat by 2–3 °C. It gives 33.8 °C for 31 °C/70% RH and would show a black flag nearly all day. Do not use it.
- **Label on screen:** "Open-field WBGT (sun), Liljegren method".

**Derived values:**
- `coolest_hour`: the minimum hourly WBGT between 05:00 and 19:00 local over the next 24 h.
- `forecast`: the next 24 hourly `{t, wbgt_c, flag}`.

**Failure:** keep the previous env, log the error, emit metric `ContextFetchErrors`. Env older than 45 min is `stale` and the engine treats the flag as `NONE`.

**Attribution (required, dashboard footer and README):**
- "Weather data by Open-Meteo.com (CC BY 4.0)"
- "Air quality: Copernicus Atmosphere Monitoring Service via Open-Meteo"

---

## 9. Escalation workflow (Step Functions Standard: `wristheat-escalation`)

Execution name = `incident_id` (`inc-<session8>-<epochms>`).

| State | Type | Behaviour |
|---|---|---|
| `Notify` | Lambda `esc_notify` | Status `NOTIFIED`; synthesise Polly mp3 EN + HI to `s3://…/audio/{incident_id}/{en,hi}.mp3`; publish to SNS `wristheat-supervisor`; events `NOTIFIED`, `AUDIO_READY` |
| `WaitForAck` | Lambda `esc_register` with `.waitForTaskToken`, payload `{incident_id, kind: "ack", token}` | Stores `ack_token`. If `ack_pending` is already true, it calls `SendTaskSuccess` itself. `TimeoutSeconds = ACK_TIMEOUT_SECONDS` (default **90**) |
| on `States.Timeout` → `Escalate` | Lambda `esc_escalate` | Status `ESCALATED`; publish to SNS `wristheat-backup`; event `ESCALATED` |
| `WaitForAckAfterEscalation` | as WaitForAck | `TimeoutSeconds = 600`. On timeout → `MarkUnacknowledged` (Pass) → `WaitForRecovery` |
| `WaitForRecovery` | Lambda `esc_register` with `kind: "recovery"` | Stores `recovery_token`. If `recovered_at` is already set, it calls `SendTaskSuccess` itself. `TimeoutSeconds = 3600`. On timeout → `Close` with outcome `not_confirmed` |
| `Close` | Lambda `esc_close` | Computes metrics; writes the report (Bedrock, else template); status `CLOSED`; SNS "resolved" message to supervisor; events `REPORT_READY`, `CLOSED` |

**Other rules**

- **Ack API:** if status ∈ {NOTIFIED, ESCALATED}, call `SendTaskSuccess(ack_token)` when the token exists, otherwise set `ack_pending = true`. Then set `acked_at` and `acked_by`, status `ACKNOWLEDGED`, event `ACKNOWLEDGED`.
- **Recovery:** when ingest emits `RECOVERY_CONFIRMED` for a session with an open incident, it sets `recovered_at`, adds event `RECOVERY_CONFIRMED`, and calls `SendTaskSuccess(recovery_token)` if the token exists.
- **Token errors:** `TaskTimedOut` or `InvalidToken` from SendTaskSuccess are logged and ignored.

**Outcomes:**

| Outcome | Meaning |
|---|---|
| `recovered` | acknowledged, then recovery confirmed |
| `recovered_unacknowledged` | recovery confirmed without any acknowledgement |
| `not_confirmed` | recovery-wait timeout |

**Metrics in `incident.metrics`:** `time_to_ack_s`, `time_to_recovery_s` (opened → recovered), `minutes_in_red`, `peak_psi`, `peak_core_c`, `escalated` (bool).

**Polly text:**
- EN, voice Kajal, neural, en-IN: "Heat alert. {name} needs to stop now. Strain index {psi}. Open-field W B G T {wbgt} degrees. Move them to {shade|indoors} and cool them with water."
- HI, Kajal, neural, hi-IN: "गर्मी की चेतावनी। {name} को अभी रुकना होगा। उन्हें {छाँव में|अंदर} ले जाएँ और पानी से ठंडा करें।"
- If neural hi-IN is unavailable, fall back to voice Aditi (standard).

**Bedrock report**
- Converse API.
- `modelId` from env `BEDROCK_MODEL_ID`. Default `apac.amazon.nova-lite-v1:0`; the builder confirms it with `aws bedrock list-inference-profiles --region ap-south-1` and uses what is listed.
- `maxTokens 400`, `temperature 0.2`.
- System prompt (verbatim):

  > You write short factual incident summaries for a heat-strain monitoring prototype. Use only the facts in the JSON you are given. Do not diagnose, do not speculate about medical causes, and do not invent any number. Write at most 120 words in plain English: what triggered the alert, the response timeline with times, whether recovery was confirmed by the data, and one practical suggestion for the next session that follows from the facts (for example the coolest hour). End with: "Estimated values; not a medical assessment."

- Any error → deterministic template report built from the same facts; `report.source = "template"`. Emit metric `BedrockFallbacks`.

**SNS email body:** plain text with trainee name, trigger numbers, advice EN, and the dashboard incident link `https://<cloudfront>/incidents/{id}`.

**Email recipients:** supervisor and backup emails come from CDK context `supervisorEmail` and `backupEmail`. Each subscription must be confirmed from the inbox once.

---

## 10. Watch app (summary; full detail in the Android prompt)

- **Platform:** Wear OS app, package `com.wristheat.watch`; min SDK 30, target/compile SDK 36. Device: Galaxy Watch5 Pro SM-R920 on Wear OS 6 / Android 16.
- **Permissions:** `android.permission.health.READ_HEART_RATE` on API 36+; `BODY_SENSORS` with `maxSdkVersion="35"`.
- **Heart rate:** Health Services `ExerciseClient` with `DataType.HEART_RATE_BPM`, inside a foreground service of type `health`. `MeasureClient` is the fallback; a fake source is used for the emulator.
- **Upload:** every 5 s via `POST /v1/ingest`. Queue up to 900 samples; retry with backoff 2 → 30 s.
- **Screens:** Start → Calibrating (2:00) → Live (state ring, BPM, est. core ± band, WBGT/flag, minutes to RED, sync dot) → Alert overlays → Stop.
- **Vibration on the one-shot `alert`:**

| Alert | Pattern |
|---|---|
| AMBER | 2 × 200 ms |
| RED | 3 × 600 ms, repeated every 10 s until tapped |
| RECOVERED | 1 × 800 ms |

- **Config:** `local.properties` → BuildConfig: `wristheat.apiBaseUrl`, `wristheat.deviceToken`, `wristheat.traineeId`. Never committed.

---

## 11. Supervisor dashboard

- **Stack:** React 18 + Vite + TypeScript, Recharts, `aws-amplify` v6 (Auth only), and `@aws-amplify/ui-react` Authenticator for the login screen.
- **Hosting:** S3 + CloudFront. The SPA loads `/config.json` (`apiUrl`, `region`, `userPoolId`, `userPoolClientId`), written at deploy time from stack outputs.
- **Polling:** `GET /v1/roster` every 3 s; paused while the tab is hidden.

**Pages**

1. **`/` Live group view**
   - **Site strip:** open-field WBGT with flag chip, air temp, RH, wind, PM2.5 µg/m³ + US AQI, coolest hour today, "Updated hh:mm · Open-Meteo".
   - **Trainee cards**, sorted RED → AMBER → RECOVERING → GREEN → CALIBRATING → none. Each card shows: name; source badge **LIVE / SIMULATED / REPLAY**; state chip (text + colour); HR; est. core ± 0.6 °C; PSI bar 0–10; "~n min to RED"; last-seen or "Signal lost 45 s"; a 30-min core sparkline.
2. **Alert banner** (on every page), for each open incident:
   - "{name}: STOP — heat strain RED", the trigger numbers, and the advice with an EN/हिंदी toggle.
   - Buttons: "▶ Play alert (EN)", "▶ हिंदी", "Acknowledge — cooling started".
   - Shows "Escalated to backup contact at hh:mm" when escalated.
   - Audio autoplays when the browser allows.
3. **`/trainee/:id`** chart:
   - HR line (left axis);
   - core estimate line with a ±0.6 band (right axis, 36.5–40 °C);
   - background bands by state;
   - WBGT flag strip;
   - incident markers.
4. **`/incidents`** and **`/incidents/:id`:**
   - timeline;
   - metrics tiles (time to acknowledge, time to confirmed recovery, minutes in RED, peak PSI, peak est. core);
   - report labelled either "Summary generated by Amazon Bedrock from the logged events below" or "Template summary (Bedrock unavailable)";
   - "Open in Step Functions console" link.
5. **`/method`:** the honesty copy (§14) plus credits.

**Rules**
- Colour is never the only signal; every state has text.
- It must look right at 1280×720 (screen recording) and at phone width.
- Every action has loading, success and error states.
- **Footer attribution (verbatim):** "Weather: Open-Meteo.com (CC BY 4.0) · Air quality: CAMS via Open-Meteo · Core-temperature estimate: ECTemp (USARIEM, US patent 10702165), used in a non-commercial research prototype".

**Visual direction:** a calm field-operations console, not a fitness app. Light theme by default for video legibility. Large numerals. Risk colours with text labels: GREEN `#1f7a4d`, AMBER `#b26a00`, RED `#b42318`, RECOVERING `#1d5fa8`. Use the `frontend-design` skill for typography and layout.

---

## 12. Simulator, replay, fixtures

- **`simulator/simulate.py`**
  - Streams simulated trainees S1–S4 at 1 Hz, one batch every 5 s, `source: "simulated"`.
  - Profiles:

| Trainee | Profile |
|---|---|
| S1 | steady ~138 ± 4 bpm |
| S2 | ~124 ± 4 bpm |
| S3 | at-risk: 150 rising to 182 after `--surge-after` seconds |
| S4 | ~96 ± 3 bpm |

  - `--backfill-minutes N` first sends N minutes of history quickly, with past timestamps, so charts and the filter start realistic.
  - Simulated trainees have `rest_hr_override` set, so there is no calibration.
- **`simulator/export_session.py --session <id>`** writes `fixtures/<date>-<trainee>-<id8>.json` (Readings plus metadata). Commit it.
- **`simulator/replay.py --fixture <file> --as R1 [--speed 1]`** re-streams a recorded **real** session. R1 is a separate trainee of kind `real` (seeded as "{name} — earlier run"), so a replay never replaces the live T1 card.
  - New `session_id`, `source: "replay"`, `replay_of` = the original id.
  - Timestamps are shifted to now.
  - The dashboard badge reads "REPLAY · recorded {date time} on SM-R920".
- **Nothing simulated or replayed is ever shown without its badge.**

---

## 13. Security, privacy, operations

- **Device token:** a Secrets Manager secret (`wristheat/device-token`, 32 random chars). Lambdas read it and cache it for 5 min; comparison is constant-time.
- **Cognito:** self sign-up disabled. `scripts/seed.py` creates the supervisor user and prints the temporary password once.
- **Data minimisation:** trainee ids and display names only. No GPS from the watch; location is the site only.
- **Retention:** Readings, Minutes and Sessions expire after 30 days; Incidents after 90.
- **Least privilege:** every Lambda gets only the table and service permissions it uses (CDK grants).
- **Powertools for AWS Lambda (Python):** Logger (JSON), Tracer (X-Ray), Metrics (EMF) in every handler.
  - Metrics: `SamplesIngested`, `IngestLatencyMs`, `StateTransitions` (dimension `to`), `IncidentsOpened`, `ContextFetchErrors`, `BedrockFallbacks`.
  - CloudWatch dashboard `WristHeat` showing those, Lambda errors, and Step Functions executions.
- **Packaging (no Docker needed):** Lambda dependencies are installed with `pip --platform manylinux2014_aarch64 --only-binary=:all: --python-version 3.12` into layers:
  - `core` layer: `aws-lambda-powertools`;
  - `sci` layer: `numpy`, `thermofeel==2.3.0`, used by the context Lambda only.
- **Repository hygiene:** commit early and in small steps. Never commit `local.properties`, tokens or `.env`.

---

## 14. Honesty rules (on-screen copy, verbatim on `/method` and in the README)

1. "WristHeat estimates a core-temperature *trend* from heart rate using ECTemp (US Army Research Institute of Environmental Medicine). It is not a thermometer and not a medical device."
2. "ECTemp was validated with chest-strap heart rate (about ±0.6 °C). It has not been validated on wrist optical sensors like the one in this watch, and studies found it misses many cases above 39 °C. Treat it as an early indicator, never as clearance to continue."
3. "WBGT is computed for open ground in sun from Open-Meteo forecast data (Liljegren method). Shade, indoor and local conditions differ."
4. "The rules that combine strain with the heat flag are our own heuristic, not a published standard."
5. "Trainees marked SIMULATED are generated by our simulator. REPLAY shows a real session recorded earlier. LIVE is a real person wearing the watch now."
6. "ECTemp is patented (US 10702165). This is a non-commercial research prototype."

Never claim a prevented illness, clinical accuracy, or measured impact.

---

## 15. Testing strategy

| Layer | What proves it |
|---|---|
| Engine | pytest with the golden values in §7.2 and §8, plus state-machine cases (escalation persistence, de-escalation, recovery confirmation, gap minutes, calibration clamp) |
| Contract | Handler responses validated against `contracts/*.schema.json`; the watch parses `contracts/examples/ingest_response.*.json` in a unit test |
| Infra | `cdk synth` passes; `scripts/smoke.py` posts a batch and reads the roster on the deployed stack |
| Workflow | Simulator surge with `ACK_TIMEOUT_SECONDS=90` produces NOTIFIED → ESCALATED → ACKNOWLEDGED → CLOSED, seen in the console |
| End to end | Watch on wrist indoors: calibration → GREEN → stair climbing → AMBER vibration → rest → RECOVERED vibration; dashboard mirrors it within 10 s |

---

## 16. Demo story (video ≤ 2:55, maps every beat to a built component)

| Time | Beat | Component |
|---|---|---|
| 0:00–0:12 | "12 candidates died in a recruitment run in Jharkhand. Heat warnings tell everyone the same thing. Your body doesn't." | Title card |
| 0:12–0:30 | Supervisor dashboard: site strip shows open-field WBGT with flag, PM2.5, coolest hour. Architecture card, each service with its verb | Dashboard, diagram |
| 0:30–1:15 | Split screen: wearer runs outdoors (phone footage); watch shows live BPM and state; dashboard card shows LIVE HR, core estimate with band, PSI, "~n min to RED" | Watch, ingest, engine |
| 1:15–1:35 | State changes; **the watch vibrates on camera**; supervisor sees it | One-shot alert |
| 1:35–2:05 | Simulated trainee S3 goes RED → Hindi voice alert plays → Step Functions graph in the console → supervisor misses it → escalated to backup → acknowledge | Escalation workflow |
| 2:05–2:25 | Wearer rests in shade; estimate falls; **"Recovery confirmed" vibration**; incident closes; Bedrock report with metrics | Recovery loop, report |
| 2:25–2:45 | Method/honesty card | `/method` |
| 2:45–2:55 | Closing: the services used, repo URL, live URL | — |

**Safety rule for filming:** the wearer stops at RED or at any symptom, with a spotter and water present, and the run lasts no more than 20 min. Whether the real wearer reaches RED depends on the day's WBGT. **INFERENCE** from §7.2: about 10–12 min at ~165 bpm reaches PSI ≈ 6, so RED needs a RED/BLACK flag. The escalation beat is therefore always shown with simulated S3, which is labelled.

---

## 17. Risks and fallbacks

| Risk | Fallback |
|---|---|
| Health Services exercise blocked (e.g. Samsung Health workout running) | Stop the Samsung workout; else switch the watch build to `MeasureClient` with the screen kept on |
| Watch Wi-Fi drops outdoors | Phone Bluetooth proxy; watch buffers 15 min; replay the recorded session if filming fails |
| Bedrock model not enabled | Template report; badge says so |
| Polly neural Hindi unavailable | Aditi standard voice |
| Open-Meteo outage | Last good env; `stale` shown; engine runs body-only |
| Real wearer does not reach RED | Expected and acceptable; real AMBER plus real recovery, with escalation shown on labelled S3 |
| Time runs short | Cut in this order: coolest-hour strip, trainee detail chart (keep the sparkline), Hindi audio (keep the text), Bedrock (keep the template) |

---

## 18. Credits and licences (`CREDITS.md`)

- **ECTemp:** Buller MJ et al. 2013, *Physiol Meas* 34:781–798; US patent 10702165B2 (US Army); USARIEM T17-08 (Looney 2017).
- **Initial variance:** de Korte et al. 2022, *Front Sports Act Living*.
- **PSI:** Moran DS et al. 1998, *Am J Physiol*.
- **Heat categories:** US Army TB MED 507.
- **thermofeel** (ECMWF, Apache-2.0); **Open-Meteo** (CC BY 4.0); **CAMS** air quality.
- **Powertools for AWS Lambda** (MIT-0); **Recharts** (MIT); **AWS Amplify JS** (Apache-2.0).
- **AI tools used:** Claude (Claude Code) for research, design and code; the Android agent tool used by the team — name it in the write-up.
