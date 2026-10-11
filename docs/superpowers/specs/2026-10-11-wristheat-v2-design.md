# WristHeat v2 — Session lifecycle, command view, public demo

**Status:** approved in chat, Sun 11 Oct 2026 ~14:55 IST. Builds on `2026-10-11-wristheat-design.md` (v1), which stays authoritative for the engine, contract and escalation.
**Deadline:** submission by Mon 12 Oct 00:00 IST. Outdoor filming ~17:00 IST (Phase 1 must be deployed by 16:45).

## 1. Intent

Judges see only the video, repo and write-up (no live demo). v1 reads as a monitor you could do without. v2 makes WristHeat cover the **whole session**, so a supervisor needs it even when nobody gets hurt:

| Moment | Supervisor question | v2 answer |
|---|---|---|
| Before | Should we train now, and how hard? | **Today panel**: 24-h heat-flag timeline, best window, published work/rest + water for the current flag |
| During | Who needs me right now? | **Command view**: status counts, "Needs action now" list, activity feed |
| After | What happened, and can I show I responded? | **Session report**: printable duty-of-care record |
| Anyone with the URL | What is this? | **Landing page + read-only public demo** (simulated trainees only) |

Unchanged: risk engine, watch contract (`contracts/`), escalation workflow, honesty rules (v1 §14).

## 2. Phase 1 — before filming (deploy by 16:45)

### 2.1 Command view (Live page)

- **Status bar** at the top of the group view: counts per state in fixed order RED, AMBER, RECOVERING, GREEN, CALIBRATING, plus "signal lost" (session exists, not ENDED, `stale`). Each count shows the state word, never colour alone. Zero counts are shown muted.
- **Needs action now** list, derived client-side from the roster, highest priority first:

  | Condition | Line |
  |---|---|
  | state RED | "Stop {name} now — rest in shade, cool with water." (indoors variant when site PM2.5 > 60) |
  | stale and session active | "Check on {name} — no data for {elapsed}." |
  | state AMBER | "Slow {name} down and give water." |
  | state GREEN/RECOVERING/AMBER and `minutes_to_red` ≤ 10 | "{name}: ~{n} min to RED at this effort (model projection)." |
  | state RECOVERING | "Keep {name} resting until cleared." |

  Empty list → "No action needed. Next check: {coolest/next window hint}" is out of scope; show "No action needed right now."
- **Activity feed**: the last 20 state changes across the group, newest first, `hh:mm {name} → {STATE}` with SIMULATED/REPLAY badge where relevant.
  - Backend: ingest appends each engine event to `session.recent_events` (cap 20; `{t, event, state}`, `t = state_since`). Roster returns `activity` = merged, sorted, capped at 20, each item `{t, trainee_id, name, kind, source, event, state}`. Hidden trainees excluded.
- Cards keep v1 content; visual hierarchy tightened (see §4).

### 2.2 Today panel

- **Timeline**: next 24 hourly blocks from `site.forecast` (`{t, wbgt_c, flag}`), coloured by flag with the flag word in the tooltip/label; current hour marked; night hours (19:00–05:00 local) dimmed.
- **Best window**: the earliest longest run of consecutive daytime hours (05:00–19:00 local) whose flag is NONE, WHITE or GREEN; shown as "Best window: 05:00–08:00 (GREEN or cooler)". If none, "No GREEN-or-cooler daytime hour in the next 24 h — coolest hour {hh:00}, WBGT {x} °C."
- **Work/rest and water for the current flag** — US Army TB MED 507 table (acclimatized adults, 2022 revision). Source cited on screen. Water converted 1 US quart = 0.95 L:

  | Flag (WBGT °C) | Easy work | Moderate work | Hard work |
  |---|---|---|---|
  | WHITE (25.6–27.7) | no limit · 0.5 L/h | no limit · 0.7 L/h | 40 min work / 20 min rest · 0.7 L/h |
  | GREEN (27.8–29.4) | no limit · 0.5 L/h | 50/10 · 0.7 L/h | 30/30 · 0.95 L/h |
  | YELLOW (29.5–31.0) | no limit · 0.7 L/h | 40/20 · 0.7 L/h | 30/30 · 0.95 L/h |
  | RED (31.1–32.1) | no limit · 0.7 L/h | 30/30 · 0.7 L/h | 20/40 · 0.95 L/h |
  | BLACK (≥ 32.2) | 50/10 · 0.95 L/h | 20/40 · 0.95 L/h | 10/50 · 0.95 L/h |

  Footnote (verbatim intent): "Hourly fluid intake should not exceed 1.4 L; daily intake should not exceed 11 L. Published guidance for acclimatized adults; WristHeat does not individualise it." NONE flag → "Below heat category 1: normal precautions."
- Frontend only; no backend change.

### 2.3 Phase 1 testing

- Backend: `test_ingest` — events appended to `recent_events`, capped at 20; `test_api` — roster `activity` merged, sorted, hidden excluded, capped.
- Dashboard (vitest): status counts; needs-action ordering (RED before stale before AMBER); best-window computation (incl. none case); work/rest row for each flag; activity feed rendering with badge.

## 3. Phase 2 — after filming

### 3.1 Session report (`/console/sessions/:id/report`)

- Backend `GET /v1/sessions/{session_id}/summary` (JWT): `{session, trainee, started_at, last_seen, duration_min, hr0, minutes_by_state {GREEN, AMBER, RED, RECOVERING, CALIBRATING, gap}, peak_psi, peak_core_c, peak_hr, flag_minutes {flag: n}, incidents: [summary + metrics + outcome], env_at_start}` computed from Minutes + Incidents.
- Page: header (trainee, badge, date, duration, site), state-time bar, peak tiles, incident list with response times, heat context, honesty footer; print stylesheet so "Print / save PDF" yields a clean A4 record. Linked from the trainee card and trainee page.

### 3.2 Public landing page and read-only demo

- Routes: `/` landing (public), `/demo` read-only group view (public), `/console/*` authenticated console (all existing pages move here; old paths redirect).
- `GET /v1/public/roster` (no auth): same shape as roster, **trainees with `kind == "simulated"` only**, `open_incidents` and `activity` filtered to simulated trainees, no audio/console links. Demo page shows a fixed banner: "Public demo — all trainees here are SIMULATED. Real wearers are visible only to signed-in supervisors."
- Landing: product story in the order Problem → Before/During/After → How it works (AWS services with their jobs) → Honesty → CTA buttons "See the live demo" and "Supervisor sign-in". No invented metrics or testimonials.

### 3.3 Repository

- Import the watch app into `wear/` with history (`git subtree add`); its `local.properties` stays ignored.
- README: hero screenshot, "What it does" (before/during/after), architecture diagram (Mermaid), services table, quick start, honesty, attribution, AI tools, limits; `docs/README.md` index; screenshots in `docs/images/`.
- Pre-publication secret scan (`git log -p` for token/secret/password patterns) before the repo is made public.

## 4. Visual direction (unchanged identity, tighter hierarchy)

Keep v1 tokens (sage ground, slate ink, Barlow / Barlow Condensed, risk colours with words, flag pennant as the one loud element). Command view adds a single status bar and a two-column layout at ≥ 1200 px (cards left, "Needs action" + activity right); one column on phones with "Needs action" first. No new colours except the TB MED 507 flag swatches already used by the pennant.

## 5. Out of scope

Editing trainees or sites in the UI; push notifications; per-person water tracking; any claim that work/rest guidance is individualised; Bedrock chat; changes to thresholds or the engine.

## 6. Risks

| Risk | Fallback |
|---|---|
| Phase 1 not deployed by 16:45 | Film on current UI; record dashboard screens again tonight |
| Public endpoint misuse | Only simulated data exposed; stage throttle 20/40 rps |
| Moving the console under `/console` breaks bookmarks | Redirect old paths |
