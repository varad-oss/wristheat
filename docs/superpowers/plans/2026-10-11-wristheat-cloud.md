# WristHeat Cloud + Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (native, recommended for this deadline) or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy the AWS backend, risk engine, escalation workflow, simulator and supervisor dashboard for WristHeat. The Galaxy Watch app (built separately) streams heart rate to this backend.

**Architecture:**
- A pure-Python risk engine (ECTemp → PSI → levels → state machine) runs inside an ingest Lambda behind an API Gateway HTTP API, with state in DynamoDB.
- A Step Functions workflow runs the escalation with task tokens. A scheduled Lambda computes Liljegren WBGT from Open-Meteo.
- A React dashboard on S3 + CloudFront, behind Cognito, polls the API.
- Everything is one CDK (TypeScript) stack in `ap-south-1`.

**Tech Stack:** Python 3.12 (Lambda arm64), pytest, Powertools for AWS Lambda, thermofeel 2.3.0 + numpy; AWS CDK v2 (TypeScript, Node ≥ 20); React 18 + Vite + TypeScript + Recharts + aws-amplify v6.

**Spec:** `docs/superpowers/specs/2026-10-11-wristheat-design.md` (read it fully before Task 1; section numbers below refer to it).

## Global Constraints

- Region `ap-south-1` for every resource. Lambda runtime `python3.12`, architecture `ARM_64`.
- No Docker. Lambda dependencies are installed with `pip --platform manylinux2014_aarch64 --implementation cp --python-version 3.12 --only-binary=:all:`.
- Engine constants exactly as spec §7.2: `b0=-7887.1, b1=384.4286, b2=-4.5714, gamma2=0.000484, sigma2=356.5654, CT0=37.1, v0=0.02`.
- Thresholds exactly as spec §7.3–7.4. Comparisons use **unrounded** PSI and CT.
- WBGT via `thermofeel==2.3.0` `calculate_wbgt_liljegren` only. The simple formula is forbidden (spec §8).
- Copy text verbatim from the spec:
  - advice strings: §7.7
  - Polly text and the Bedrock system prompt: §9
  - footer: §11
  - honesty rules: §14
- Contract: responses must validate against `contracts/ingest_response.schema.json`.
- Labelling: every simulated or replayed trainee shows a `SIMULATED` or `REPLAY` badge everywhere it appears.
- **Commit after every task**, with small commits and `feat:` / `test:` / `chore:` prefixes. The repo history must show continuous work on 11 Oct (event rule).
- Never commit secrets, `local.properties`, `.env*`, `cdk.out/`, `node_modules/`, `dist/`, `build/`, `simulator/.state.json`, `infra/outputs.json`.
- Every API response: `Content-Type: application/json; charset=utf-8`, body from `json.dumps(obj, ensure_ascii=False)` (Hindi text must arrive intact on the watch and the dashboard).
- Deadline Sun 11 Oct 20:00 IST. If a task overruns, follow the cut order in spec §17.

## Review Focus

1. **Watch retries a batch** (same samples twice) → minutes must not double-count. *Test:* `test_duplicate_samples_ignored` (Task 4).
2. **Watch reconnects after 10 min offline and flushes 600 samples** → many minutes close in one call. Events fire in order, and the one-shot alert is the last transition. *Test:* `test_flush_closes_many_minutes_and_keeps_last_alert` (Task 4).
3. **Two overlapping requests for one session** → a version conflict must retry, not lose state. *Test:* `test_ingest_retries_on_version_conflict` (Task 6).
4. **Two supervisors press Acknowledge** → the second gets 409 and Step Functions is signalled only once. *Test:* `test_ack_twice_returns_409_and_signals_once` (Task 9).
5. **Open-Meteo is down or returns an unexpected shape** → keep the last env, mark it stale after 45 min, and the engine runs body-only. *Test:* `test_context_failure_keeps_previous_env` (Task 8) and `test_stale_env_treated_as_none` (Task 3).

---

## File map

```
backend/
  pyproject.toml                    pytest config (pythonpath = src)
  requirements-core.txt             aws-lambda-powertools[tracer]
  requirements-sci.txt              numpy>=2,<3 ; thermofeel==2.3.0
  requirements-dev.txt              pytest jsonschema boto3 numpy thermofeel==2.3.0
  src/wristheat/
    ectemp.py        Kalman step/run
    strain.py        psi, flags, candidate level, projection
    engine.py        EngineState, minute aggregation, calibration, state machine
    advice.py        EN/HI advice strings
    contract.py      request validation, response building
    envctx.py        cossza, Liljegren WBGT, Open-Meteo parsing, coolest hour, Env dataclass
    repo.py          DynamoRepo + FakeRepo (same interface)
    incidents.py     incident ids, facts, metrics, template report
    clients.py       thin wrappers: SFN, SNS, Polly, Bedrock, S3, Secrets (injectable)
    handlers/
      ingest.py  api.py  context.py
      esc_notify.py  esc_register.py  esc_escalate.py  esc_close.py
  tests/  test_contracts.py test_ectemp.py test_strain.py test_engine.py test_contract.py
          test_ingest.py test_envctx.py test_context_handler.py test_api.py test_incidents.py test_escalation.py
infra/
  bin/wristheat.ts
  lib/wristheat-stack.ts            composes the constructs below
  lib/data.ts  lib/layers.ts  lib/ingest-api.ts  lib/context.ts  lib/auth.ts
  lib/escalation.ts  lib/web.ts  lib/observability.ts
  test/wristheat.test.ts            aws-cdk-lib/assertions
simulator/  common.py simulate.py export_session.py replay.py  tests/test_simulator.py
scripts/    build_lambdas.sh deploy.sh seed.py smoke.py
dashboard/  (Vite React TS app; see Tasks 12–13)
```

---

### Task 1: Repository scaffold and contract tests

**Files:**
- Create: `README.md` (stub), `LICENSE` (MIT), `CREDITS.md` (copy spec §18), `.gitignore` (spec §4 list), `Makefile`
- Create: `docs/` — copy the spec, this plan, `docs/superpowers/plans/2026-10-11-wristheat-wear.md` and the hackathon research folder if provided
- Create: `contracts/` — copy the provided schemas and examples unchanged
- Create: `backend/pyproject.toml`, `backend/requirements-*.txt`, `backend/src/wristheat/__init__.py`
- Test: `backend/tests/test_contracts.py`

**Interfaces:**
- Produces: `make test` (runs `cd backend && python -m pytest -q`), `make synth`, `make deploy`. Path constant `CONTRACTS_DIR` in tests = `<repo>/contracts`.

- [ ] **Step 1: Write the test.** `test_examples_match_schemas`: every `contracts/examples/ingest_request.*.json` validates against `ingest_request.schema.json`, and every `ingest_response.*.json` validates against `ingest_response.schema.json` (use `jsonschema.validate`).
- [ ] **Step 2:** Create a venv (`python3.12 -m venv .venv`), install dev requirements, run `make test`. Expected: PASS (6 example files).
- [ ] **Step 3: Commit.** `chore: scaffold repo, contracts and docs`

### Task 2: ECTemp filter

**Files:** Create `backend/src/wristheat/ectemp.py`; Test `backend/tests/test_ectemp.py`

**Interfaces:**
- Produces:
  - `B0, B1, B2, GAMMA2, SIGMA2, CT0, V0` (floats, spec §7.2)
  - `step(ct: float, v: float, hr: float) -> tuple[float, float]`
  - `run(hrs: Sequence[float], ct: float = CT0, v: float = V0) -> list[tuple[float, float]]`

- [ ] **Step 1: Failing tests** (tolerance: `ct` ±0.0005, `v` ±0.00001):
  - `test_step_golden_165`: `step(37.1, 0.02, 165) == (37.290475, 0.018330)`
  - `test_step_golden_80_zero_var`: `step(37.1, 0.0, 80) == (37.099811, 0.000483)`
  - `test_run_sequence_A`: `run([75]*2+[165]*20+[100]*10)`; ct at minutes 2, 12, 22, 32 equals `37.0656, 38.0408, 38.4650, 38.1118`
  - `test_run_published_params_crosses_38_at_34`: with `v=0.0`, `[80]*10+[150]*30+[100]*20`: the first 1-based index with ct ≥ 38.0 is 34; peak `38.1827`
- [ ] **Step 2:** Run `pytest tests/test_ectemp.py -v`. Expected: FAIL (module missing).
- [ ] **Step 3:** Implement exactly the update in spec §7.2.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(engine): ECTemp Kalman filter with golden tests`

### Task 3: Strain index, heat flags, candidate level, projection

**Files:** Create `backend/src/wristheat/strain.py`; Test `backend/tests/test_strain.py`

**Interfaces:**
- Consumes: `ectemp.step`
- Produces:
  - `FLAG_ORDER = ("NONE","WHITE","GREEN","YELLOW","RED","BLACK")`
  - `psi(ct: float, hr: float, hr0: int) -> float` — unrounded, clamped `[0, 10]`
  - `flag_for_wbgt(wbgt_c: float | None) -> str` — `None` → `"NONE"`; compare `round(wbgt_c, 1)` against spec §7.4
  - `effective_flag(env: "Env | None", now_ms: int) -> str` — `"NONE"` if env is None, stale (`now_ms - env.updated_at > 45*60*1000`), or `wbgt_c` is None
  - `candidate_level(psi_value: float, ct: float, flag: str) -> Literal["GREEN","AMBER","RED"]`
  - `project_minutes_to_red(ct: float, v: float, hr_mean: float, hr0: int, flag: str, limit: int = 90) -> int | None`

- [ ] **Step 1: Failing tests:**
  - `test_psi_formula`: `psi(38.3, 150, 75)` ≈ `5*(1.2/2.4) + 5*(75/105)` = `6.0714` (±1e-4)
  - `test_psi_clamped`: `psi(36.0, 60, 75) == 0.0`; `psi(41.0, 200, 75) == 10.0`
  - `test_flag_boundaries`: 25.5→NONE, 25.6→WHITE, 27.7→WHITE, 27.8→GREEN, 29.4→GREEN, 29.5→YELLOW, 31.0→YELLOW, 31.1→RED, 32.1→RED, 32.2→BLACK, `None`→NONE; 31.04→YELLOW (rounds to 31.0)
  - `test_candidate_levels`:
    - `(7.0, 38.0, "NONE")`→RED
    - `(3.0, 39.0, "NONE")`→RED
    - `(6.0, 38.0, "RED")`→RED
    - `(6.0, 38.0, "YELLOW")`→AMBER
    - `(5.0, 37.5, "NONE")`→AMBER
    - `(4.0, 37.5, "YELLOW")`→AMBER
    - `(4.0, 37.5, "GREEN")`→GREEN
    - `(4.99, 37.5, "NONE")`→GREEN
  - `test_projection_vectors`: run `ectemp.run([75,75,165])` to get (ct, v) after minute 3. Then `project_minutes_to_red(ct, v, 165, 75, "RED") == 8` and with `"YELLOW"` `== 18`.
  - `test_stale_env_treated_as_none`: an Env with `updated_at = now - 46 min` → `effective_flag == "NONE"`; at 44 min it returns its own flag.
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3:** Implement. The projection copies (ct, v) and loops `ectemp.step` up to `limit` times, returning the first n where `candidate_level(psi(ct, hr_mean, hr0), ct, flag) == "RED"`. Define `Env` in `envctx.py` now as a dataclass `Env(wbgt_c: float|None, flag: str, pm25: float|None, us_aqi: int|None, updated_at: int, temp_c: float|None = None, rh: float|None = None, wind_ms: float|None = None)`, which Task 8 extends.
- [ ] **Step 4:** Run. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(engine): PSI, TB MED 507 flags, levels, projection`

### Task 4: Engine — minutes, calibration, state machine

**Files:** Create `backend/src/wristheat/engine.py`; Test `backend/tests/test_engine.py`

**Interfaces:**
- Consumes: `ectemp`, `strain`, `envctx.Env`
- Produces:
  ```python
  @dataclass
  class EngineState:
      started_at: int; first_minute: int | None; last_t: int | None
      ct: float; v: float
      open_minute: int | None; open_sum: float; open_n: int
      calib_means: list[float]; hr0: int | None; rest_hr_override: int | None
      state: str; state_since: int
      history: list[dict]          # last 4 non-gap evaluated minutes: {minute, level, hr, psi, ct}
      pending_alert: str           # "NONE" | "AMBER" | "RED" | "RECOVERED"
      hr_now: int | None; psi: float | None; minutes_to_red: int | None
      def to_dict(self) -> dict    # floats as str-safe numbers for DynamoDB (repo converts to Decimal)
      @classmethod
      def from_dict(cls, d: dict) -> "EngineState"

  @dataclass
  class MinuteRow:
      minute: int; hr: float | None; n: int; core_est_c: float; core_var: float
      psi: float | None; level: str | None; state: str
      wbgt_c: float | None; flag: str; pm25: float | None

  @dataclass
  class EngineResult:
      state: EngineState; minutes: list[MinuteRow]; events: list[tuple[int, str]]  # (minute, event)

  def new_state(started_at_ms: int, rest_hr_override: int | None) -> EngineState
  def apply_samples(state: EngineState, samples: list[tuple[int, int]], env: Env | None, now_ms: int) -> EngineResult
  def calibration_remaining_s(state: EngineState, now_ms: int) -> int
  ```
  - Event names: `CALIBRATED`, `AMBER_ENTERED`, `RED_ENTERED`, `RECOVERING_ENTERED`, `RECOVERY_CONFIRMED`.
  - `new_state` with an override sets `hr0 = override` and `state = "GREEN"`; otherwise `state = "CALIBRATING"`.
  - `hr_now` = rounded mean of this call's newly accepted samples (unchanged if none).

- [ ] **Step 1: Failing tests.** Use helper `minutes_to_samples(minute_hrs, start_ms)`: 60 samples at 1 Hz per minute; `None` → 5 samples (a gap); plus one sample at the start of the following minute so the last minute closes. Use a fixed env with the given flag and `updated_at = now`.
  - `test_D1_red_flag`, `test_D2_yellow_flag`, `test_D3_no_flag`, `test_D4_realistic_decay`, `test_D5_gaps`: feed each vector from spec §7.4 in **one** call and in **5-sample batches** (two parametrised variants). Assert that the list of `(minute, event)` pairs, **excluding `CALIBRATED`**, equals the spec table's list (also excluding CALIBRATED). Separately assert `CALIBRATED` at minute 2 for D1 and minute 3 for D5. Minute indexes are 1-based from the session's first minute, and gap minutes count.
  - `test_calibration_clamp`: means `[110,120]` → `hr0 == 100`; `[40,42]` → `hr0 == 45`.
  - `test_override_skips_calibration`: `new_state(t0, 80)` → state GREEN, `hr0 == 80`, no CALIBRATED event.
  - `test_duplicate_samples_ignored`: apply the same 60-sample batch twice → the second call closes nothing, `open_n` unchanged, `last_t` unchanged.
  - `test_flush_closes_many_minutes_and_keeps_last_alert`: after calibration at 75, one call with 600 samples at 165 bpm (10 min) under a RED flag → events include AMBER_ENTERED, and `pending_alert == "AMBER"` (RED needs more minutes). A further 300 samples → `RED_ENTERED` and `pending_alert == "RED"`.
  - `test_calibration_remaining`: `first_minute = m`; at `now = m*60000 + 30000` → `90`; after `hr0` is set → `0`.
  - `test_gap_minute_does_not_update_filter`: ct and v are unchanged across a gap minute.
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement `apply_samples`.**
  1. Drop samples with `t <= last_t`.
  2. Bucket the rest by `t // 60000`.
  3. Close the open minute whenever a later minute index appears.
  4. For each closed minute: if it is a gap (`n < 10`), record a MinuteRow with `hr=None` (ct/v unchanged). Otherwise step the filter, then calibrate or evaluate the state machine per spec §7.1 and §7.4 (escalation before de-escalation before recovery).
  5. Every transition sets `pending_alert` (RECOVERING_ENTERED does not) and `state_since = (minute+1)*60000`.
  6. After processing, compute `minutes_to_red` per spec §7.5 using the mean HR of the last 3 history entries.
- [ ] **Step 4:** Run. Expected: PASS (all D-vectors in both batchings).
- [ ] **Step 5: Commit.** `feat(engine): minute aggregation, calibration and risk state machine`

### Task 5: Advice text and the ingest contract

**Files:** Create `backend/src/wristheat/advice.py`, `backend/src/wristheat/contract.py`; Test `backend/tests/test_contract.py`

**Interfaces:**
- Produces:
  - `advice_for(state: str, pm25: float | None, alert: str) -> dict[str, str]` — keys `en`, `hi`; text verbatim from spec §7.7. `alert == "RECOVERED"` wins; indoors when `pm25 > 60`; `{pm25}` rounded to int.
  - `class RequestError(Exception)` with `.status: int`, `.code: str`
  - `validate_request(body: dict, now_ms: int) -> tuple[dict, list[tuple[int, int]], int]` returns `(meta, accepted_samples, dropped)`. Raises `RequestError(400, "bad_request" | "source_mismatch" ...)`. Validates per spec §5.1. The trainee-kind check happens in the handler.
  - `build_response(trainee_id: str, session_id: str, accepted: int, dropped: int, st: EngineState, env: Env | None, incident_id: str | None, now_ms: int) -> dict` — consumes `st.pending_alert` into the `alert` field (the handler then resets it to `"NONE"`).

- [ ] **Step 1: Failing tests:**
  - `test_advice_red_indoors`: `advice_for("RED", 72.4, "NONE")["en"] == "Stop now. Rest indoors — outdoor air is poor (PM2.5 72 µg/m³)."`
  - `test_advice_recovered_overrides`: `advice_for("GREEN", 10, "RECOVERED")["en"]` is the recovery-confirmed line.
  - `test_validate_drops_out_of_range_and_future`: bpm 25 and 240 dropped; t = now+61 s dropped; live t = now−7 h dropped; `dropped == 4`.
  - `test_validate_rejects_bad_schema`: missing `samples` → 400; 601 samples → 400; `source: "replay"` without `replay_of` → 400.
  - `test_response_matches_schema`: build responses for CALIBRATING, AMBER-with-alert, env None; each validates against `contracts/ingest_response.schema.json`, and `core_band_c == 0.6`.
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3:** Implement. Round `core_est_c` to 2 dp and `psi` to 1 dp in the response only. Hand-written validation; no jsonschema at runtime.
- [ ] **Step 4:** Run. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(api): ingest contract validation, advice text, response builder`

### Task 6: Repository layer and ingest handler

**Files:** Create `backend/src/wristheat/repo.py`, `backend/src/wristheat/clients.py`, `backend/src/wristheat/handlers/ingest.py`; Test `backend/tests/test_ingest.py`

**Interfaces:**
- Produces (`repo.py`): `class Repo(Protocol)` with:
  - `get_trainee(tid) -> dict | None`
  - `get_session(sid) -> dict | None`
  - `create_session(item: dict) -> None`
  - `save_session(item: dict, expected_version: int) -> None` — raises `VersionConflict`
  - `set_current_session(tid, sid) -> None`
  - `put_readings(sid, samples: list[tuple[int,int]]) -> None`
  - `put_minutes(sid, rows: list[MinuteRow]) -> None`
  - `get_site(site_id) -> dict | None`
  - `put_incident(item) -> None`, `get_incident(iid) -> dict | None`, `update_incident(iid, **fields) -> None`, `append_incident_event(iid, event: dict) -> None`

  `DynamoRepo(table_names: dict[str, str])` uses boto3 and converts floats ↔ `Decimal`. `FakeRepo()` is in-memory, with `fail_next_save_with_conflict: int` for tests.
- Produces (`clients.py`): `Clients` dataclass `(sfn, sns, polly, bedrock, s3, secrets)` plus `get_device_token() -> str` (cached 300 s). The `FakeClients` in tests records calls.
- Produces (`handlers/ingest.py`):
  - `handler(event, context)` (API Gateway v2 proxy event), dispatching on `routeKey` between `POST /v1/ingest` and `POST /v1/sessions/{session_id}/end`
  - `process_ingest(body: dict, headers: dict, deps: Deps, now_ms: int) -> tuple[int, dict]`
  - `process_end(session_id: str, headers: dict, deps: Deps, now_ms: int) -> tuple[int, dict]` → `200 {"ended": true}`, sets status `ENDED`; unknown session → `404 unknown_session`
  - `Deps(repo, clients, state_machine_arn, site_env_loader)`
  - Environment variables: `TABLE_SITES, TABLE_TRAINEES, TABLE_SESSIONS, TABLE_READINGS, TABLE_MINUTES, TABLE_INCIDENTS, DEVICE_TOKEN_SECRET_ARN, STATE_MACHINE_ARN, SITE_ID`.
  - Incident hooks: on `RED_ENTERED` call `incidents.open_incident(...)` and `clients.sfn.start_execution(stateMachineArn, name=incident_id, input=json)`. On `RECOVERY_CONFIRMED` with an open incident, set `recovered_at` and send task success if a `recovery_token` exists. **In this task `open_incident` is a stub** that creates `{incident_id, status: "NOTIFIED", opened_at, trainee_id, session_id, trigger}`; Task 11 fills it in. If `STATE_MACHINE_ARN` is empty, skip `start_execution`.

- [ ] **Step 1: Failing tests** (FakeRepo, FakeClients):
  - `test_unauthorized`: wrong token → 401 `{"error":"unauthorized",…}`
  - `test_unknown_trainee_404`
  - `test_simulated_trainee_cannot_send_live`: → 400 `source_mismatch`
  - `test_first_batch_creates_session_and_sets_current`: the session exists, the trainee's `current_session_id` is set, state is CALIBRATING, and the response validates against the schema.
  - `test_red_entered_opens_incident_and_starts_execution`: drive vector D1 in 5-sample batches → exactly one `start_execution` with `name == incident_id`; the response with that transition has `alert == "RED"`; the next response has `alert == "NONE"`.
  - `test_recovery_sends_task_success_when_token_present`: preset `recovery_token` on the incident → on RECOVERY_CONFIRMED, `send_task_success` is called once with that token.
  - `test_ingest_retries_on_version_conflict`: `fail_next_save_with_conflict = 1` → the handler reloads, reapplies, and the final state is identical to a no-conflict run.
  - `test_end_session_marks_ended` and `test_end_unknown_session_404` (both need the device token; a wrong token → 401).
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement.** Constant-time token compare (`hmac.compare_digest`). Writes use the Sessions `version` attribute (conditional expression `version = :v`). Add Powertools Logger/Metrics/Tracer decorators. Emit metrics `SamplesIngested`, `IngestLatencyMs`, and `StateTransitions` per event with dimension `to`.
- [ ] **Step 4:** Run. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(ingest): DynamoDB repo and ingest Lambda with incident hooks`

### Task 7: CDK stack M1 (data, secret, layers, ingest API) + scripts → **first deploy**

**Files:**
- Create: `infra/` (via `npx cdk init app --language typescript`), `infra/lib/data.ts`, `infra/lib/layers.ts`, `infra/lib/ingest-api.ts`, `infra/lib/wristheat-stack.ts`, `infra/test/wristheat.test.ts`
- Create: `scripts/build_lambdas.sh`, `scripts/deploy.sh`, `scripts/seed.py`, `scripts/smoke.py`

**Interfaces:**
- Produces stack outputs (`cdk deploy --outputs-file infra/outputs.json`): `ApiUrl`, `DeviceTokenSecretArn`, `TableSites`, `TableTrainees`, `TableSessions`, `TableReadings`, `TableMinutes`, `TableIncidents`, `AudioBucketName`.
- Produces `scripts/build_lambdas.sh`, which creates:
  - `build/layer-core/python` from `requirements-core.txt`
  - `build/layer-sci/python` from `requirements-sci.txt` (both with the pip `--platform` flags in Global Constraints)
  - `build/app` as a copy of `backend/src`
- Produces `scripts/seed.py --name <wearer> --age <n>`, which upserts:
  - Site `kgp` = {"IIT Kharagpur campus", 22.3149, 87.3105} (edit if filming elsewhere)
  - `T1` (real), `R1` ("<name> — earlier run", real)
  - `S1–S4` (simulated): ages 22/24/21/23, `rest_hr_override` 72/68/76/70, names "Arjun", "Meera", "Kabir", "Ishaan"
  - `S0` (simulated, `hidden: true`, `rest_hr_override` 70)
- Produces `scripts/smoke.py`: posts 3 batches for `S0` (source simulated), expects 200, a schema-valid response and `state == "GREEN"`.

- [ ] **Step 1: CDK assertion test** (`infra/test/wristheat.test.ts`): the template has 6 DynamoDB tables with `BillingMode: PAY_PER_REQUEST`; the Lambda runtime is `python3.12` and architecture `arm64`; the HTTP API has the routes `POST /v1/ingest` and `POST /v1/sessions/{session_id}/end`; there is a Secrets Manager secret with `GenerateSecretString.PasswordLength: 32` and `ExcludePunctuation: true`.
- [ ] **Step 2:** `cd infra && npm test`. Expected: FAIL.
- [ ] **Step 3: Implement the constructs.**
  - Tables per spec §6, with TTL attribute `ttl` on Sessions, Readings, Minutes and Incidents.
  - Audio bucket: private, `BlockPublicAccess.BLOCK_ALL`, auto-delete.
  - Secret `wristheat/device-token`.
  - Two `LayerVersion`s from `build/layer-*`.
  - Ingest function: handler `wristheat.handlers.ingest.handler`, memory 512 MB, timeout 15 s, `tracing: ACTIVE`, env vars from Task 6.
  - HTTP API with a CORS preflight placeholder and default throttling 20/40.
  - **Use `RemovalPolicy.DESTROY` everywhere** (hackathon stack).
- [ ] **Step 4:** `npm test`. Expected: PASS. Then `bash scripts/deploy.sh` (it runs build_lambdas then `cdk deploy --require-approval never --outputs-file outputs.json`), then `python scripts/seed.py --name "<wearer name>" --age <age>`, then `python scripts/smoke.py`. Expected: smoke prints `OK GREEN`.
- [ ] **Step 5: Commit.** `feat(infra): data, ingest API, layers, seed and smoke scripts`
- [ ] **Step 6: MILESTONE M1 — tell the human.** Print `ApiUrl` and the command to read the token: `aws secretsmanager get-secret-value --secret-id wristheat/device-token --query SecretString --output text --region ap-south-1`. The watch developer puts both in `wear/local.properties`.

### Task 8: Environment context (Liljegren WBGT) and scheduler

**Files:**
- Modify: `backend/src/wristheat/envctx.py`
- Create: `backend/src/wristheat/handlers/context.py`, `infra/lib/context.ts`
- Test: `backend/tests/test_envctx.py`, `backend/tests/test_context_handler.py`

**Interfaces:**
- Produces:
  - `cossza(lat: float, lon: float, when_utc: datetime) -> float` (NOAA approximation; code below)
  - `wbgt_liljegren_c(t_c: float, rh: float, p_hpa: float, wind10_ms: float, ssrd: float, direct: float, cz: float) -> float | None`
  - `build_env(forecast_json: dict, air_json: dict, lat: float, lon: float, now_ms: int) -> tuple[Env, list[dict], dict]` returns `(env, forecast_24h, coolest_hour)`
  - `load_site_env(repo, site_id, now_ms) -> Env | None`
  - Context handler `handler(event, context)` refreshes site `SITE_ID`; it is also called by the API refresh route (Task 9).

  ```python
  def cossza(lat, lon, when_utc):
      doy = when_utc.timetuple().tm_yday
      hour = when_utc.hour + when_utc.minute / 60 + when_utc.second / 3600
      g = 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)
      eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                      - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
      decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
              + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
      ha = math.radians((hour * 60 + eqt + 4 * lon) / 4 - 180)
      la = math.radians(lat)
      return math.sin(la) * math.sin(decl) + math.cos(la) * math.cos(decl) * math.cos(ha)
  ```

- [ ] **Step 0: Live check (no code).** Call the two Open-Meteo URLs from spec §8 for the site with `curl`, save the JSON to `backend/tests/fixtures/openmeteo_forecast.json` and `openmeteo_air.json`, and confirm every variable name is present. If a name is rejected, use the closest documented variable and note it in the README.
- [ ] **Step 1: Failing tests:**
  - `test_cossza_golden`: lat 22.3149, lon 87.3105, 2026-10-11 at 00:30 / 06:30 / 12:30 UTC → `0.0870 / 0.8658 / -0.1751` (±0.002)
  - `test_wbgt_golden_sun`: `(31,70,1005,2.0,700,direct=490,cz=0.8)` → `31.99` ±0.05. Here direct = 0.7 × 700, so fdir = 0.7.
  - `test_wbgt_golden_night`: `(31,70,1005,2.0,0,0,-0.1)` → `27.65` ±0.05
  - `test_build_env_from_fixture`: build_env on the saved fixtures returns flag ∈ FLAG_ORDER, a `coolest_hour.local` matching `^\d\d:00$`, and `len(forecast_24h) == 24`
  - `test_context_failure_keeps_previous_env`: when the HTTP fetch raises, the Sites item still holds the previous env and metric `ContextFetchErrors` is emitted
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement.**
  - Convert to the units thermofeel expects (K, %, hPa, m/s, W/m²); `fdir = clamp(direct/ssrd, 0, 1)` when `ssrd ≥ 1`, else 0.
  - Use urllib (no requests dependency), timeout 10 s.
  - The context Lambda uses both layers (core + sci), memory 1024 MB, timeout 60 s.
  - EventBridge Scheduler: `rate(10 minutes)` → context Lambda (use the `aws-cdk-lib/aws-scheduler` L2 if your CDK version has it, else `CfnSchedule` with a role).
- [ ] **Step 4:** Run pytest. Expected: PASS. Deploy, then `aws lambda invoke --function-name <ContextFn> /dev/stdout --region ap-south-1` and check the Sites item has `env.wbgt_c` set.
- [ ] **Step 5: Commit.** `feat(context): Liljegren WBGT from Open-Meteo every 10 min`

### Task 9: Cognito and the supervisor API

**Files:**
- Create: `backend/src/wristheat/handlers/api.py`, `infra/lib/auth.ts`
- Modify: `infra/lib/ingest-api.ts` (routes + JWT authorizer), `scripts/seed.py` (supervisor user)
- Test: `backend/tests/test_api.py`

**Interfaces:**
- Produces routes per spec §5.2 in one Lambda (`wristheat.handlers.api.handler`), dispatched on `event["routeKey"]`:
  - `GET /v1/roster`
  - `GET /v1/sessions/{session_id}/series`
  - `GET /v1/incidents`
  - `GET /v1/incidents/{incident_id}`
  - `POST /v1/incidents/{incident_id}/ack`
  - `POST /v1/context/refresh` (invokes the context Lambda synchronously via the `CONTEXT_FUNCTION_NAME` env var)
- Produces `ack_incident(repo, clients, incident_id: str, username: str, note: str, now_ms: int) -> tuple[int, dict]`.
- Produces outputs `UserPoolId`, `UserPoolClientId`. The Cognito pool has self sign-up off and email sign-in. `seed.py --supervisor-email <e>` creates user `supervisor` and prints the temporary password.

- [ ] **Step 1: Failing tests:**
  - `test_roster_shape_and_sorting`: RED before AMBER before GREEN; hidden S0 omitted; `stale` true when `last_seen` is older than 30 s; `source`/`replay_of` passed through
  - `test_series_since_minute`
  - `test_incident_get_has_presigned_audio_and_console_url`: `console_url` starts with `https://ap-south-1.console.aws.amazon.com/states/home?region=ap-south-1#/v2/executions/details/`
  - `test_ack_with_token_sends_success`
  - `test_ack_before_token_sets_pending`
  - `test_ack_twice_returns_409_and_signals_once`
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement.**
  - HTTP API JWT authorizer: issuer `https://cognito-idp.ap-south-1.amazonaws.com/<poolId>`, audience = client id. Attach it to every supervisor route, not to device routes.
  - `acked_by` comes from the `cognito:username` claim.
  - CORS allowed origins: `http://localhost:5173` now; the CloudFront domain is added in Task 12.
- [ ] **Step 4:** Run pytest and `npm test` (add assertions: the authorizer exists and the ingest route has no authorizer). Deploy; run `seed.py --supervisor-email ...`.
- [ ] **Step 5: Commit.** `feat(api): Cognito-protected supervisor API`

### Task 10: Simulator, session export and replay

**Files:** Create `simulator/common.py`, `simulator/simulate.py`, `simulator/export_session.py`, `simulator/replay.py`, `simulator/requirements.txt` (boto3); Test `simulator/tests/test_simulator.py`

**Interfaces:**
- Produces:
  - `common.post_batch(api_url, token, payload) -> dict`
  - `common.make_payload(trainee_id, session_id, source, samples, replay_of=None) -> dict`
  - `simulate.profile_hr(profile: str, t_s: float, surge_after_s: float | None, rng: random.Random) -> int`, with profiles `steady138`, `steady124`, `atrisk`, `easy96`
  - CLI `simulate.py --api URL --token TOKEN [--backfill-minutes 20] [--surge-after 120] [--only S3] [--profile atrisk|steady138|steady124|easy96] [--seed 7]`. `--profile` overrides the profile of the `--only` trainee, e.g. to let S3 recover. Default mapping: S1 steady138, S2 steady124, S3 atrisk, S4 easy96.
  - On start, a simulator session for a trainee continues the trainee's current session id if it was written in the last 10 min (kept in `simulator/.state.json`, git-ignored). Switching S3 to `easy96` therefore continues the same session, which is what lets the incident close with RECOVERY_CONFIRMED.
  - `export_session.py --session SID --outputs infra/outputs.json` → `fixtures/<YYYYMMDD-HHMM>-<trainee>-<sid8>.json` with `{meta:{session_id,trainee_id,device,started_at,source}, samples:[[t,bpm],…]}`
  - `replay.py --fixture FILE --as R1 --api URL --token TOKEN [--speed 1.0]` (new session id, `source: "replay"`, `replay_of` = original id, timestamps shifted so the last sample lands at now)
- Atrisk profile: 150 ± 4 bpm, ramping linearly to 182 over 6 min after `surge_after_s`. Others are as in spec §12.
- Backfill sends past minutes in 300-sample batches with `t` from `now - N min`, then streams live 5-sample batches every 5 s.

- [ ] **Step 1: Failing tests:**
  - `test_profile_ranges`: 1,000 draws of each profile stay inside ±12 bpm of the target
  - `test_atrisk_surge_reaches_180`: at `surge_after + 6 min` the mean of 60 draws is ≥ 178
  - `test_replay_shifts_timestamps`: the last shifted t equals `now`, spacing is preserved, the payload has `source == "replay"` and `replay_of` set
  - `test_payload_matches_contract`: `make_payload` output validates against `contracts/ingest_request.schema.json`
- [ ] **Step 2:** Run. Expected: FAIL. **Step 3:** Implement. **Step 4:** Run. Expected: PASS. Then live-run `simulate.py --backfill-minutes 15 --surge-after 60` for 3 min; the roster (via `curl` with a JWT, or a DynamoDB scan) shows S1–S4 sessions.
- [ ] **Step 5: Commit.** `feat(sim): labelled simulator, session export and replay`

### Task 11: Escalation workflow (Step Functions, SNS, Polly, Bedrock)

**Files:**
- Create: `backend/src/wristheat/incidents.py`, `backend/src/wristheat/handlers/esc_notify.py`, `esc_register.py`, `esc_escalate.py`, `esc_close.py`, `infra/lib/escalation.ts`
- Modify: `backend/src/wristheat/handlers/ingest.py` (replace the stub with `incidents.open_incident`), `infra/lib/wristheat-stack.ts`
- Test: `backend/tests/test_incidents.py`, `backend/tests/test_escalation.py`

**Interfaces:**
- Produces (`incidents.py`):
  - `incident_id_for(session_id: str, now_ms: int) -> str` → `f"inc-{session_id[:8]}-{now_ms}"`
  - `open_incident(trainee: dict, session_id: str, st: EngineState, env: Env | None, now_ms: int) -> dict` — trigger = `{psi, core_est_c, hr, wbgt_c, flag, pm25, rule}`, where `rule` names the matched RED clause (`"psi>=7"`, `"core>=39"`, `"psi>=6 & flag"`)
  - `polly_texts(name: str, psi: float, wbgt: float | None, indoors: bool) -> dict[str, str]` — verbatim spec §9
  - `compute_metrics(incident: dict, minutes: list[dict]) -> dict` — spec §9 metric names
  - `report_facts(incident: dict, metrics: dict, site: dict) -> dict`
  - `template_report(facts: dict) -> str` — ≤ 120 words, ends with "Estimated values; not a medical assessment."
  - `bedrock_report(clients, model_id: str, facts: dict) -> tuple[str, str]` → `(text, source)`, where source is `"bedrock"` or `"template"`
- Step Functions definition (CDK, Standard type, name `wristheat-escalation`, tracing on, logs to CloudWatch):
  - `Notify` = `LambdaInvoke(esc_notify)`, `payloadResponseOnly`, `resultPath: DISCARD`
  - `WaitForAck` = `LambdaInvoke(esc_register)` with `integrationPattern: WAIT_FOR_TASK_TOKEN`, payload `{incident_id.$: "$.incident_id", kind: "ack", token: JsonPath.taskToken}`, `taskTimeout: Timeout.duration(seconds(ackTimeoutSeconds))`, `resultPath: DISCARD`; `.addCatch(Escalate, errors: ["States.Timeout"], resultPath: "$.timeout")`
  - `Escalate` → `WaitForAckAfterEscalation` (same as WaitForAck, timeout 600, catch → `MarkUnacknowledged` Pass) → `WaitForRecovery` (kind `"recovery"`, timeout 3600, catch → `Close`) → `Close`
  - `ackTimeoutSeconds` comes from CDK context `ackTimeoutSeconds` (default 90)
- IAM:
  - `polly:SynthesizeSpeech`
  - `sns:Publish` on both topics
  - `bedrock:InvokeModel` on `arn:aws:bedrock:ap-south-1:<acct>:inference-profile/<profileId>` and `arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0`
  - `states:SendTaskSuccess` for the ingest and API Lambdas
  - `states:StartExecution` for ingest
- SNS topics `wristheat-supervisor` and `wristheat-backup` with email subscriptions from CDK context `supervisorEmail` and `backupEmail`.
- `BEDROCK_MODEL_ID`: first run `aws bedrock list-inference-profiles --region ap-south-1` and use the listed APAC Nova Lite profile id (expected `apac.amazon.nova-lite-v1:0`). If none is listed, use any listed APAC text model; else leave it empty (template only).

- [ ] **Step 1: Failing tests:**
  - `test_incident_id_format`
  - `test_open_incident_rule_names`: three cases, one per RED clause
  - `test_polly_texts_verbatim`: the EN string for `("Kabir", 7.2, 31.4, False)` equals spec §9 with substitutions
  - `test_metrics`: synthetic incident with opened, acked +40 s, recovered +300 s, and 5 RED minutes → `time_to_ack_s == 40`, `time_to_recovery_s == 300`, `minutes_in_red == 5`
  - `test_template_report_word_limit_and_suffix`
  - `test_bedrock_failure_falls_back`: a fake bedrock client raises → `source == "template"` and metric `BedrockFallbacks` is emitted
  - `test_register_ack_with_pending_immediately_succeeds`
  - `test_register_recovery_when_already_recovered_immediately_succeeds`
  - `test_close_sets_outcome`: three cases → `recovered`, `recovered_unacknowledged`, `not_confirmed`
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement.**
  - Polly: `OutputFormat mp3`, `Engine neural`, `VoiceId Kajal`, `LanguageCode en-IN` / `hi-IN`. On a `ValidationException` for hi-IN neural, retry with `Engine standard`, `VoiceId Aditi`.
  - Audio is saved to the audio bucket.
  - `esc_close` publishes a short "resolved" email to `wristheat-supervisor`: trainee, outcome, time to acknowledge, time to confirmed recovery, and the incident link.
  - Every handler appends the timeline events named in spec §6.
  - The SNS email link uses the env var `DASHBOARD_URL`, set in Task 12; until then use `"(dashboard pending)"`.
- [ ] **Step 4:** Run pytest and `npm test` (assert the state machine exists and contains `waitForTaskToken`). Deploy with `-c ackTimeoutSeconds=90 -c supervisorEmail=… -c backupEmail=…`; confirm both SNS subscription emails in the inbox.
  - **Live check:** `simulate.py --only S3 --backfill-minutes 18 --surge-after 30`. Within ~5 min an execution named `inc-…` appears; after 90 s it moves to `Escalate`; two emails arrive. Then run `curl -X POST …/ack` with a JWT (from `aws cognito-idp admin-initiate-auth`, or wait for the dashboard), stop the simulator surge (Ctrl-C), and run `simulate.py --only S3 --profile easy96` until RECOVERY_CONFIRMED. The execution then reaches `Close` and the incident has a report.
- [ ] **Step 5: Commit.** `feat(escalation): Step Functions escalation with Polly, SNS and Bedrock report`

### Task 12: Dashboard foundation (auth, config, live group view, hosting)

**Files:**
- Create: `dashboard/` (`npm create vite@latest dashboard -- --template react-ts`), `dashboard/src/api.ts`, `dashboard/src/auth.ts`, `dashboard/src/types.ts`, `dashboard/src/pages/Live.tsx`, `dashboard/src/components/{SiteStrip,TraineeCard,StateChip,SourceBadge,PsiBar,Sparkline,Footer}.tsx`
- Create: `infra/lib/web.ts`
- Modify: `scripts/deploy.sh` (build the dashboard before `cdk deploy`), `infra/lib/ingest-api.ts` (CORS + CloudFront origin)
- Test: `dashboard/src/__tests__/live.test.tsx` (vitest + @testing-library/react)

**Interfaces:**
- Consumes: `GET /v1/roster` (spec §5.2).
- Produces:
  - `types.ts` mirroring spec §5.2 shapes (`Roster`, `TraineeRow`, `SiteEnv`, `IncidentSummary`, `Incident`)
  - `api.ts`: `getRoster()`, `getSeries(sessionId, sinceMinute?)`, `getIncidents(status)`, `getIncident(id)`, `ackIncident(id, note)`, `refreshContext()` — each attaches `Authorization: Bearer <idToken>` from `fetchAuthSession()`
  - `/config.json` loaded before `Amplify.configure`
- `web.ts`:
  - private S3 bucket + CloudFront distribution (OAC, default root `index.html`, SPA error responses 403/404 → `/index.html` with 200)
  - `BucketDeployment` of `../dashboard/dist`, plus `Source.jsonData('config.json', {apiUrl, region, userPoolId, userPoolClientId})`
  - output `DashboardUrl`; pass `DASHBOARD_URL` to the escalation Lambdas

- [ ] **Step 0:** Invoke the `frontend-design` skill for the visual direction in spec §11 (calm field-operations console, light theme, large numerals, risk colours with text).
- [ ] **Step 1: Failing tests** (render `Live` with a mocked `getRoster`):
  - `renders SIMULATED badge for kind simulated`
  - `orders RED card first`
  - `shows "Signal lost" when stale`
  - `shows "~6 min to RED (model projection)" when minutes_to_red = 6`
  - `footer contains the exact attribution string`
- [ ] **Step 2:** `npm test` (vitest). Expected: FAIL.
- [ ] **Step 3: Implement.**
  - Polling every 3 s with `document.visibilityState` pause.
  - The site strip has a small "Refresh heat data" button that calls `refreshContext()` and shows loading, success ("Updated hh:mm") and error states. It is used just before filming.
  - Authenticator (hideSignUp).
  - Responsive grid: 1 column on phones, 3 at ≥ 1200 px.
  - Est. core shown as `37.92 ± 0.6 °C` with the caption "estimated trend".
- [ ] **Step 4:** `npm test` → PASS; `npm run build` → PASS. Deploy; open `DashboardUrl`, sign in as supervisor, see the site strip and cards while the simulator runs.
- [ ] **Step 5: Commit.** `feat(dashboard): authenticated live group view on CloudFront`

### Task 13: Dashboard incident flow, charts and method page

**Files:**
- Create: `dashboard/src/components/AlertBanner.tsx`, `dashboard/src/pages/{TraineeDetail,Incidents,IncidentDetail,Method}.tsx`, `dashboard/src/i18n.ts`
- Test: `dashboard/src/__tests__/incident.test.tsx`

**Interfaces:**
- Consumes: Task 12 `api.ts`.
- Produces routes `/trainee/:id`, `/incidents`, `/incidents/:id`, `/method` (react-router).

- [ ] **Step 1: Failing tests:**
  - `banner appears for an open incident and Acknowledge calls ackIncident once`
  - `second click is disabled while pending and shows the 409 message "Already acknowledged"`
  - `banner shows "Escalated to backup contact at hh:mm" when status ESCALATED`
  - `incident page labels the report source` (bedrock vs template texts per spec §11)
  - `method page contains all six honesty statements verbatim`
- [ ] **Step 2:** Run. Expected: FAIL.
- [ ] **Step 3: Implement.**
  - **Banner:** EN/हिंदी toggle for advice; two audio buttons using `<audio>` with the presigned URLs; try `play()` on first appearance and ignore a rejection; buttons always visible.
  - **Trainee chart:** Recharts `ComposedChart` with HR line (left axis), core line plus band area `[core-0.6, core+0.6]` (right axis 36.5–40), `ReferenceArea` per state segment, and incident `ReferenceLine`s.
  - **Incident page:** metric tiles, timeline list, report, and an "Open in Step Functions console" link (`console_url`).
- [ ] **Step 4:** Run tests, build, deploy. Manual check with the simulator surge → banner → play Hindi audio → Acknowledge → the console shows the execution moving on.
- [ ] **Step 5: Commit.** `feat(dashboard): alert banner, acknowledgement, incident report, charts, method page`

### Task 14: Observability, docs, final verification

**Files:**
- Create: `infra/lib/observability.ts`, `docs/architecture.md` (Mermaid diagram of spec §3)
- Modify: `README.md`, `CREDITS.md`

**Interfaces:**
- Produces:
  - CloudWatch dashboard `WristHeat` with widgets: `SamplesIngested` (sum, 1 min), `IngestLatencyMs` (p95), `StateTransitions` by `to`, `IncidentsOpened`, Step Functions `ExecutionsStarted/Succeeded/Failed`, Lambda `Errors` for every function, `ContextFetchErrors`, `BedrockFallbacks`
  - Output `CloudWatchDashboardUrl`

- [ ] **Step 1:** CDK assertion test: `AWS::CloudWatch::Dashboard` exists with name `WristHeat`. Run → FAIL; implement → PASS.
- [ ] **Step 2: README.**
  - What it is (2 lines)
  - Live URL
  - Architecture diagram
  - The AWS services table from spec §3
  - Quick start (deploy, seed, watch config, simulator)
  - Honesty rules (spec §14, verbatim)
  - Data attribution
  - AI tools used
  - Known limits (Scan on incidents; WBGT open-field; wrist validity)
- [ ] **Step 3: Final verification** (use the superpowers:verification-before-completion skill):
  - `make test`, `cd infra && npm test`, `cd dashboard && npm test && npm run build` all pass
  - `scripts/smoke.py` → OK
  - Open the dashboard signed out → login screen; signed in → roster
  - Step Functions console shows at least one execution that reached `Close`
- [ ] **Step 4: Commit.** `docs: README, architecture, observability dashboard`. Then `git push`.

---

## Milestones and target times (IST, Sun 11 Oct)

| Milestone | Tasks | Target | Unblocks |
|---|---|---|---|
| **M1** ingest live | 1–7 | **03:00** | Watch app talks to the real backend |
| **M2** context + supervisor API + simulator | 8–10 | 05:00 | Dashboard data, escalation testing |
| **M3** escalation | 11 | 06:30 | The full loop |
| **M4** dashboard | 12–13 | 09:00 | Indoor end-to-end rehearsal at 09:30 |
| **M5** polish + docs | 14 | 10:30 | Feature freeze 11:00; filming 12:00 |

If M4 slips past 10:00, cut per spec §17 and keep the alert banner, acknowledgement and live cards.
