# WristHeat v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn WristHeat from a live monitor into a whole-session tool (plan → command → record) with a public demo, and make the repo presentable.

**Architecture:** Small backend additions to the existing ingest/API Lambdas (event log on sessions, roster activity, session summary, public roster); everything else is dashboard (pure guidance functions + new components/pages). CDK only gains two routes. Engine, contract and escalation are untouched.

**Tech Stack:** Python 3.12 + pytest; React 18 + Vite + vitest; AWS CDK v2 (TypeScript).

**Spec:** `docs/superpowers/specs/2026-10-11-wristheat-v2-design.md` (v1 spec stays authoritative for the engine/contract/escalation).

## Global Constraints

- Contract in `contracts/` unchanged; engine thresholds unchanged.
- Every state shown with its word, never colour alone; every SIMULATED/REPLAY trainee shows its badge wherever it appears (feed, actions, demo).
- TB MED 507 table values exactly as spec §2.2; source line on screen: "Work/rest and water: US Army TB MED 507 (acclimatized adults). Published guidance, not individualised."
- Public endpoint exposes **only** `kind == "simulated"` trainees.
- Deploy after each phase; live site must never break (run `make test`, `cd infra && npm test`, `cd dashboard && npm test && npm run build` before each deploy).
- Commit after every task; message prefixes `feat:`/`fix:`/`docs:`; attribution line per session reminder.
- Phase 1 (Tasks 1–3) deployed by 16:45 IST.

## Review Focus

1. A trainee with no current session or a hidden trainee must never appear in the activity feed or needs-action list → covered in Task 1 (`test_roster_activity_excludes_hidden`) and Task 2 (`needsAction` ignores `session_id: null`).
2. Forecast missing or shorter than 24 h (context never ran) → Today panel shows "Heat forecast not available yet" instead of crashing → Task 3 test.
3. A RED trainee whose signal is also lost must appear once, as RED (highest priority wins) → Task 2 test.
4. Public roster must not leak a real trainee via `open_incidents` or `activity` → Task 6 test.
5. A session with zero closed minutes (just started) → summary returns zeros, report renders "No completed minutes yet" → Task 4/5 tests.

---

## Phase 1 — before filming

### Task 1: Session event log and roster activity (backend)

**Files:** Modify `backend/src/wristheat/handlers/ingest.py`, `backend/src/wristheat/handlers/api.py`; Test `backend/tests/test_ingest.py`, `backend/tests/test_api.py`

**Interfaces:**
- Produces: session item field `recent_events: list[{t: int, event: str, state: str}]` (newest last, cap 20, `t = (minute+1)*60000`, `state` = engine state after the event).
- Produces: roster field `activity: list[{t, trainee_id, name, kind, source, event, state}]`, newest first, cap 20, hidden trainees and trainees without a current session excluded.

- [ ] **Step 1: Failing tests**
  - `test_ingest.py::test_events_logged_on_session`: drive `D_BASE[:14]` (flag RED) → `repo.sessions[SID]["recent_events"]` event names (in order) contain `CALIBRATED, AMBER_ENTERED, RED_ENTERED`; every entry has `t`, `event`, `state`; `state` of the RED_ENTERED entry is `"RED"`.
  - `test_ingest.py::test_event_log_capped_at_20`: preset `recent_events` with 25 entries on an existing session, ingest one event-producing batch → length 20 and the newest event is last.
  - `test_api.py::test_roster_activity_sorted_and_excludes_hidden`: sessions for T1, S3 and hidden S0 each carry `recent_events` → `activity` newest first, contains T1 and S3 items with `name`, `kind`, `source`, no S0 items, ≤ 20.
- [ ] **Step 2:** `cd backend && ../.venv/bin/python -m pytest -q tests/test_ingest.py tests/test_api.py` → FAIL.
- [ ] **Step 3:** In ingest, after `apply_samples`, append `{t: (m+1)*60000, event, state: st.state}` for each `(m, event)` in `res.events` to `session["recent_events"]` (keep last 20). In api, build `activity` from each listed trainee's current session.
- [ ] **Step 4:** Same command → PASS (full suite too).
- [ ] **Step 5:** Commit `feat(api): session event log and roster activity feed`.

### Task 2: Guidance logic (dashboard, pure functions)

**Files:** Create `dashboard/src/guidance.ts`; Test `dashboard/src/__tests__/guidance.test.ts`; Modify `dashboard/src/types.ts` (add `ActivityItem`, `Roster.activity`)

**Interfaces:**
- Produces (`guidance.ts`):
  - `WORK_REST: Record<'WHITE'|'GREEN'|'YELLOW'|'RED'|'BLACK', {easy: Rule, moderate: Rule, hard: Rule}>` where `Rule = {work: string, waterLph: number}`; `work` is `"No limit"` or `"{w} min work / {r} min rest"`; values = spec §2.2.
  - `statusCounts(trainees: TraineeRow[]): {RED, AMBER, RECOVERING, GREEN, CALIBRATING, signalLost: number}` — signalLost counts `session_id && stale`.
  - `needsAction(trainees: TraineeRow[], sitePm25: number | null, serverTime: number): Action[]` with `Action = {trainee: TraineeRow, priority: number, text: string}`; one action per trainee (highest priority), sorted by priority then name; texts exactly as spec §2.1 table; skip trainees with `session_id === null`.
  - `bestWindow(forecast: {t, wbgt_c, flag}[], tz = 'Asia/Kolkata'): {start: number, end: number, label: string} | null` — earliest longest run of consecutive hourly points with local hour 05–18 and flag ∈ {NONE, WHITE, GREEN}; `end` = last point t + 1 h.
- [ ] **Step 1: Failing tests** (`guidance.test.ts`):
  - `WORK_REST.YELLOW.hard` → `{work: '30 min work / 30 min rest', waterLph: 0.95}`; `WORK_REST.BLACK.easy` → `{work: '50 min work / 10 min rest', waterLph: 0.95}`; `WORK_REST.WHITE.moderate.work === 'No limit'`.
  - `statusCounts` on RED, AMBER, GREEN, GREEN(stale with session), none(no session) → `{RED:1, AMBER:1, GREEN:2, RECOVERING:0, CALIBRATING:0, signalLost:1}`.
  - `needsAction` ordering: RED+stale trainee appears once as "Stop Kabir now — rest in shade, cool with water."; then stale GREEN "Check on Meera — no data for 2 min."; then AMBER "Slow Arjun down and give water."; then GREEN with `minutes_to_red: 6` "Varad: ~6 min to RED at this effort (model projection)."; RECOVERING "Keep Ishaan resting until cleared."; PM2.5 72 → RED text uses "rest indoors" variant "Stop Kabir now — rest indoors, cool with water."
  - `bestWindow`: hours 03–10 local with flags [GREEN×3 (03–05), YELLOW (06), GREEN×4 (07–10)] → window 07:00–11:00; all YELLOW → `null`.
- [ ] **Step 2:** `cd dashboard && npx vitest run src/__tests__/guidance.test.ts` → FAIL.
- [ ] **Step 3:** Implement; reuse `elapsed()` from `format.ts` for "no data for …".
- [ ] **Step 4:** Same → PASS.
- [ ] **Step 5:** Commit `feat(dashboard): heat guidance, status counts and action list logic`.

### Task 3: Command view and Today panel (dashboard UI) → deploy

**Files:** Create `dashboard/src/components/{CommandBar,NeedsAction,ActivityFeed,TodayPanel}.tsx`; Modify `dashboard/src/pages/Live.tsx`, `dashboard/src/styles.css`, `dashboard/src/preview.tsx`; Test `dashboard/src/__tests__/command.test.tsx`

**Interfaces:** Consumes Task 2 functions and `Roster.activity`.

- [ ] **Step 0:** Invoke `frontend-design` and `web-design-guidelines` for the layout pass (spec §4: status bar, two-column ≥ 1200 px with cards left and Needs action + Activity right; phones: Needs action first).
- [ ] **Step 1: Failing tests** (`command.test.tsx`, render `Live` with fixtures):
  - status bar shows "1 RED" and "2 GREEN" as text.
  - Needs action list's first item text is the RED line; empty roster → "No action needed right now."
  - Activity feed shows "Kabir → RED" with a SIMULATED badge.
  - Today panel: YELLOW site → "30 min work / 30 min rest" and "0.95 L/h" in the hard-work row, source line present; forecast `[]` → "Heat forecast not available yet".
- [ ] **Step 2:** `npx vitest run` → new tests FAIL.
- [ ] **Step 3:** Implement components; update preview fixtures; visual check at 1280×720 and 375 px (no horizontal scroll).
- [ ] **Step 4:** `npm test && npm run build` → PASS; `make test` and `cd infra && npm test` → PASS.
- [ ] **Step 5:** Commit `feat(dashboard): command view and Today panel`; `bash scripts/deploy.sh`; verify the live bundle contains "Needs action".

## Phase 2 — after filming

### Task 4: Session summary endpoint

**Files:** Modify `backend/src/wristheat/handlers/api.py`, `infra/lib/ingest-api.ts`; Test `backend/tests/test_api.py`, `infra/test/wristheat.test.ts`

**Interfaces:** Produces `GET /v1/sessions/{session_id}/summary` (JWT) → spec §3.1 shape; `summarize_session(repo, session_id) -> tuple[int, dict]`.

- [ ] Tests: `test_summary_counts_minutes_by_state` (minutes GREEN×3, AMBER×2, gap×1 → `minutes_by_state` {GREEN:3, AMBER:2, gap:1}, peaks from max), `test_summary_includes_incidents` (incident on that session → listed with metrics/outcome), `test_summary_empty_session` (no minutes → zeros, peaks null), unknown session → 404; CDK test: route `GET /v1/sessions/{session_id}/summary` has `AuthorizationType: JWT`. FAIL → implement → PASS → commit `feat(api): session summary for duty-of-care report`.

### Task 5: Session report page

**Files:** Create `dashboard/src/pages/SessionReport.tsx`; Modify `api.ts` (`getSessionSummary`), `types.ts`, `TraineeCard.tsx`/`TraineeDetail.tsx` (link), `styles.css` (`@media print`); Test `dashboard/src/__tests__/report.test.tsx`

- [ ] Tests: renders trainee name + badge, "Time in state" bar labels with minutes, incident row with "Acknowledged after 1 min 47 s", empty summary → "No completed minutes yet", a "Print / save PDF" button calling `window.print`. FAIL → implement → PASS → commit `feat(dashboard): printable session report`.

### Task 6: Public roster endpoint

**Files:** Modify `backend/src/wristheat/handlers/api.py`, `infra/lib/ingest-api.ts`; Test `backend/tests/test_api.py`, `infra/test/wristheat.test.ts`

**Interfaces:** Produces `GET /v1/public/roster` (no authorizer) → roster shape filtered to simulated trainees; `public_roster(deps, now_ms)`.

- [ ] Tests: `test_public_roster_only_simulated` (T1/R1 absent from trainees, activity and open_incidents; S1/S3 present); CDK: route has `AuthorizationType: NONE`. FAIL → implement → PASS → commit `feat(api): public read-only demo roster (simulated only)`.

### Task 7: Landing page, public demo, console routes

**Files:** Create `dashboard/src/pages/{Landing,Demo}.tsx`; Modify `App.tsx`, `main.tsx` (Authenticator only under `/console`), `api.ts` (`getPublicRoster` without auth), `web.py` unchanged (SPA fallback already); Test `dashboard/src/__tests__/public.test.tsx`

- [ ] Tests: landing renders the Before/During/After sections and both CTAs ("See the live demo", "Supervisor sign-in"); demo page shows the fixed SIMULATED banner and no Acknowledge button; old path `/incidents` redirects to `/console/incidents`. FAIL → implement → PASS → deploy → commit `feat(dashboard): landing page, public demo, console routes`.

### Task 8: Repository presentation

**Files:** `wear/` (subtree), `README.md`, `docs/README.md`, `docs/images/*.png`

- [ ] `git subtree add --prefix=wear /Users/varad/Documents/aws-2/heatwristapp main`; confirm `git ls-files wear | grep -c local.properties` → 0.
- [ ] Screenshots of landing, console, Today panel, report, incident page into `docs/images/`; README rewritten per spec §3.3; `docs/README.md` index.
- [ ] Secret scan: `git log -p | grep -nEi '(device_?token|secret|password)\s*[:=]\s*["'\'']?[A-Za-z0-9]{16,}'` → no real values. Commit `docs: README, screenshots, docs index; import watch app`; push.
