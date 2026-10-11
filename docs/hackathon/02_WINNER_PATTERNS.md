# 02 — Winner Patterns: transferable principles, not features

> **Round-2 update (9 Oct 2026):** these patterns are now re-derived from watching the actual videos, in [`round2/01_WINNER_VIDEO_ANALYSIS.md`](round2/01_WINNER_VIDEO_ANALYSIS.md).
> - The main addition: **the top three were separated by one memorable visual proof**, often physical and in one take (real phone call, second outage with nobody woken, split screen). It was not AI depth.
> - Labelled simulation appeared in four of seven placed videos. It was accepted when paired with some real proof.

These patterns are drawn from the seven First Commit winners (see 01) and the 1,180-entry field. Every pattern below is stated as **"X worked because it solved Y friction for Z user using mechanism A."** No pattern is "feature X wins."

---

## 1. Why each winner worked (causal statements)

| Winner | X worked… | …because it solved Y friction… | …for Z user… | …using mechanism A |
|---|---|---|---|---|
| Suraksha | Tiered "ask her first" escalation | Reassurance normally costs dignity; cameras and alerts feel like surveillance | Adult children and a parent aging alone | Routine baseline → deviation → check with the parent by voice → Step Functions callback ladder to the *one* relative who can show up → Cedar-enforced consent |
| Beacon | The Sleep Contract | The same incident wakes a human again and again; nobody trusts automation that can't prove itself | A solo on-call engineer | Allowlisted fix + dry run → transcript-checked approval → Step Functions verify loop → scoped, expiring standing approval for repeats |
| CampusEvac | The asymmetric two-view drill | Drills are rare, disruptive, and never train the coordinator | Wardens and evacuees in schools and offices | Realtime two-player sim (AppSync Events) where neither role can succeed alone, with server-side scoring |
| Magpie | A reconciliation scoreboard against ground truth | "AI is accurate" claims are unverifiable, and finance can't tolerate false matches | Finance teams | Synthetic batch with a labelled answer key → deterministic matcher → precision and false-match metrics |
| Expressive Captions | The side-by-side on the same footage | Auto-captions are flat and wrong for Hinglish, and hand-styling is slow | Hinglish short-video creators | Two STT engines reconciled + measured prosody → styling → voice-editable JSON patches |
| Factcade | A live ₹-per-hour loss counter | The cost of one machine stopping is invisible until the day is lost | Small factory owners | Deterministic cascade maths + an AI planner over read-only tools + owner approval |

---

## 2. The pattern catalogue

### P1. A narrow person, in a vivid moment

- Suraksha has "Amma, 72, Bengaluru".
- Beacon opens at "3 AM, payments failing".
- Factcade opens on "one machine stops".
- Every winner can be pictured as **a specific person, at a specific time, with a specific loss**.
- Generic entries describe a category ("citizens", "users", "farmers").

### P2. Close the loop: measure → decide → act → **verify**

- The two top prizes both *verify the outcome*:
  - Beacon refuses to say "recovered" until CloudWatch agrees.
  - Suraksha's chain waits for a real reply before escalating.
- Dashboards stop at "measure". Alert apps stop at "decide".
- **The verify step is the cheapest way to look ten times more real.**

### P3. Deterministic core, AI at the edges

- Each winner restricts AI to specific jobs:
  - Factcade: "the AI never computes money".
  - Suraksha: "the model decides language and judgement; code decides actions".
  - Beacon: code allowlists actions and IAM restricts them.
- AI does reading, language, judgement and planning. Code does maths, money, safety and actions.
- Judges trust what they can reason about.

### P4. Safety, consent and honesty as *visible artifacts*

- Examples: Cedar consent rules, transcript-checked approvals, "dry run passed", blast radius, kill switch, and labelled simulated history.
- Others: Magpie's "what is actually built" table, Expressive Captions' "rough edges" list, Factcade's "honest limits".
- **Honesty reads as competence.**

### P5. AWS as load-bearing structure, where each service is a verb in the story

| Service | Verb in the story |
|---|---|
| EventBridge | The proactive heartbeat |
| Step Functions | The escalation ladder or verification loop |
| Transcribe / Polly | The voice |
| Bedrock | The judgement |
| DynamoDB | The memory and audit |
| CloudTrail | "What changed" |

- Winners show AWS *doing things* on screen: a Step Functions graph turning green, log lines, a model ID.
- Losers show a logo slide.

### P6. Video craft

From Beacon's 3:00 script, the only fully documented one:

| Element | Target |
|---|---|
| Problem understood | **≤ 12 s** |
| AWS named with roles | **≤ 30 s** |
| Product on screen | **≤ 50 s** |
| Pacing | One beat every ~20 s |
| Climax | ~1:30 |
| Payoff | Twist/second run at ~2:00 |
| Rigour montage | ~2:15–2:40 |
| Close | A **tally card** with the numbers that changed |

Other craft rules:
- Captions on every line, so it works muted.
- A real on-screen clock.
- Rehearsed exact phrases.
- A reset script between takes.
- A fallback take.

### P7. Make the counterfactual visible inside the video

- Beacon's second incident (woken, then not woken).
- Expressive Captions' competitor output on the same footage.
- Factcade's loss counter before and after approval.
- **A before/after in the same three minutes is the strongest evidence of impact a judge can get without a live demo.**

### P8. Indian context is a feature, not a translation

- Four of seven winners built for an Indian specific:
  - Hindi/Hinglish voice (Suraksha, Expressive Captions).
  - A Hinglish contract phrase (Beacon).
  - Rupees as the unit (Factcade).
- Judges reward "built for where they are" (Environmental Hacks criterion #3).

### P9. Runnable by a stranger

- Local mode with mocked AWS (Beacon), sample-data banner mode (Factcade), and demo projects (Expressive Captions).
- Also "Reset demo" buttons and seeded data.
- A judge or reviewer who opens the repo can see it work.

### P10. The execution bar is very high

- 244 tests from a solo builder; IaC (CDK, SAM, Terraform) in 4 of 7 winners; CI; idempotency; retries.
- Most winners were clearly built with AI coding tools; two repos carry `CLAUDE.md` or agent files.
- **INFERENCE:** in this tour, "it works and it's robust" is table stakes for a top-3 finish.
- The differentiator must be the *idea and mechanism*. Raw effort alone won't be enough.

---

## 3. Anti-patterns observed in the 1,180-entry field

| Anti-pattern | Evidence | Why it loses (INFERENCE) |
|---|---|---|
| "Guard/Shield/Kavach/Sentinel" naming | 99 titles (8.4%) | Judges can't tell entries apart; the name says "protect" rather than *what changes* |
| "AI-powered ___ platform" | 65 "AI-powered", 60 "platform" | Signals breadth over depth; "platform" means many half-features |
| Assistant / copilot / companion | 65 titles | A chat surface without a mechanism behind it; easiest to produce from a generic prompt |
| Topic-only differentiation | Every environmental entry at First Commit (floods ×4, waste ×6+, solar, EV, air) placed nowhere | A good topic doesn't substitute for a mechanism |
| Single-commit repos | One runner-up had 1 commit | Violates the spirit of the repo-history rule. Unacceptable risk |
| Simulated core data, unlabelled | (Winners labelled theirs) | Erodes trust once a judge notices |

---

## 4. How the patterns map to the five Environmental Hacks criteria

| Criterion | Patterns that score it | What to show |
|---|---|---|
| Idea & Impact | P1, P2, P7 | A named user, a physical environmental quantity (kWh, µg/m³·h, litres, kg) changing on screen, and a before/after |
| Built on AWS | P5, P3 | 4–6 services that each do a job in the story, visible in the console, logs or graph; AWS open data where relevant |
| Design & usability | P8, P9 | Mobile-first, one primary action, local language, obvious next step; an outsider understands within 10 s |
| Execution | P2, P4, P10 | One complete, verified loop on real data; failure states shown; tests and IaC in the repo |
| Demo video | P6, P7 | The Beacon-style beat sheet, captions, and a tally card |

---

## 5. Our self-check rubric

Every concept from Phase 6 onward is scored 0–2 on each question.

1. Can the user be named in under 10 words (who, where, when)?
2. Is there a single moment of pain we can show in the first 12 seconds?
3. Does the loop include **verify**, with something proven after acting?
4. Is the AI's job narrow and checkable, with the maths and actions in code?
5. Does every AWS service map to a verb in the story?
6. Is there a before/after inside the video?
7. Is there an Indian-specific element (policy, language, currency, scheme)?
8. Can a stranger run it from the repo, or does a hosted URL work?
9. Is the environmental quantity physical and measured, not just "awareness"?
10. Would the name and pitch stand out in a list of 300 titles from our track?

**A concept scoring under 14 of 20 is not a winner candidate.**

---

## 6. The video template we will use

Adapted from P6. Total ≤ 2:55.

| Time | Beat |
|---|---|
| 0:00–0:12 | Real-world hook: the person, the moment, the loss |
| 0:12–0:30 | One sentence on the insight, plus the architecture with AWS services named by their verbs |
| 0:30–1:20 | The loop on real data, step by step, with AWS visible in-shot at least twice |
| 1:20–1:50 | Climax: the action taken, then **verified** |
| 1:50–2:20 | Counterfactual or second run: what happens next time, or without us |
| 2:20–2:40 | Rigour montage: data sources, labelled simulation, tests, guardrails |
| 2:40–2:55 | Tally card (the environmental and human numbers), repo and live URL |
