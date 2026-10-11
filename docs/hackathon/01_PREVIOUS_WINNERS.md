# 01 — Previous Winner Deconstruction

> **Round-2 update (9 Oct 2026):** the seven demo videos have now been watched (transcripts + 30–40 frames each). See [`round2/01_WINNER_VIDEO_ANALYSIS.md`](round2/01_WINNER_VIDEO_ANALYSIS.md). It **corrects** several script-based readings below:
> - Suraksha's video demos the earlier "Rakshak" build: a real watch drop leads to a real phone call. The Cedar/Rahul→Priya climax is not shown.
> - Beacon's demo runs in labelled local mode (moto, scripted model).
> - FreshTrace is an IoT food-spoilage sensor.
> - Four placed videos ran past 3:00.
>
> Where this file and round 2 disagree, round 2 is based on observation.

## What was analysed, and how

- **Source event:** *First Commit*, Bharat Builds Tour Event 01 (17–20 Sep 2026).
  - Same organisers, rulebook, submission format (repo + under-3-min video + writeup) and five judging criteria as Environmental Hacks.
  - The theme was open: any real problem.
- **Field size:** **1,180 projects** were filed.
- **Prize board:**

| Prize | Award |
|---|---|
| Ship It (1st) | ₹2L + $3k |
| Build It (2nd) | ₹1.5L + $2k |
| Best UI (3rd) | ₹1L + $1k |
| Four runners-up | $1k credits each |

- **No winners were provided by you yet.** These seven are the officially announced winners and runners-up. Add any others to this file in the same format.

### Evidence actually reviewed

| Evidence | Projects | Notes |
|---|---|---|
| README, repo structure, commit counts | All 7 | — |
| Team-authored demo scripts and runbooks | Beacon (`docs/demo-script.md`, a shot-by-shot 3:00 script); Suraksha (`DEMO.md`, a click-path runbook) | — |
| Landing-page source code | Suraksha | Its live site now returns **HTTP 401** in a real browser, so it is password-protected after the event. The page structure and copy were read from `web/src/app/page.tsx` and `components/landing/*` in the public repo |
| Screenshots described in README | CampusEvac, Beacon | — |
| Live site title | FreshTrace | Its README isn't on the default branch |
| Full title list | All 1,180 projects | Scraped from the official gallery for the field statistics in §8 |

### Not reviewed

**The YouTube demo videos.** YouTube refuses automated access, so the video analysis below is reconstructed from each team's own demo script where one exists.

- Those parts are marked **(from script)**.
- Everything else about the videos is **INFERENCE**.
- A 25-minute watch checklist is in §9 so the team can confirm or correct these readings.

### Tags used

- **FACT:** directly from the repo, README or official page.
- **INFERENCE:** reasoned from the evidence.
- **HYPOTHESIS:** plausible, unverified.

---

## 1. Suraksha — an agentic companion for an aging parent

**🥇 First prize, Ship It** · team StarBugs (3) · [code](https://github.com/harshendram/firstcommit-hack) · [video](https://youtu.be/XVr34XeXvlE) · live site now login-protected

**1. Problem (FACT).**
- Adult children in another city cannot tell whether a parent living alone is okay.
- The existing options all fail:
  - Cameras and always-on dashboards take away independence.
  - Silence leaves families guessing.
  - Panic buttons only work if the parent can, and wants to, press them.

**2. Target user (FACT).** A dual user:
- "Amma", 72, in Bengaluru, speaking Hindi/Hinglish and wearing a Galaxy Watch.
- Her children, Rahul and Priya, in other cities.
- An optional neighbour.

**3. Core insight (INFERENCE from the copy).** The real conflict is dignity versus reassurance, and the landing page says plainly that both sides are right. The resolution is ordering:
- Learn the parent's normal.
- Talk to *her* first.
- Involve family only when something is actually off, and then only the person who can show up.

**4. Exact mechanism (FACT).**
1. A routine baseline: 13 days of *labelled-simulated* history plus live today.
2. Deviation detection: missed wake window, missed call, flat or short answers. One strong or two moderate signals trigger it.
3. Tier 1: the companion checks in with Amma by voice.
4. Tier 2: an escalation chain run by **Step Functions `waitForTaskToken` callbacks**: Rahul, then on timeout Priya, then the neighbour only if allowed.
5. Tier 3: a failsafe.
6. Consent: Amma's spoken privacy rules become **Cedar** `forbid` policies, checked before every tool call and written to an audit log she can read.

**5. Genuinely novel.**
- Consent-as-policy: a spoken preference becomes a Cedar rule that blocks tools.
- An "ask her first" escalation order.
- Evidence-only family Q&A: answers come only from tool-returned records.
- A success metric of silence: most days the product says nothing.

**6. Standard hackathon implementation.**
- An LLM voice companion (Transcribe → Bedrock → Polly).
- A DynamoDB store, a Next.js dashboard, and Cognito login.

**7. UX and journey (FACT).** Separate surfaces per role:

| Route | Surface |
|---|---|
| `/` | Landing |
| `/parent` | Tablet voice companion |
| `/parent/privacy` | What was shared, and audit |
| `/home` | Calm family view |
| `/command` | Timeline |
| `/family/respond/[id]` | Push accept/decline |
| `/guard` | Neighbour handset |
| `/explore` | 3D storytelling world |

**8. Architecture (FACT).**
- Amplify (Next.js) and Cognito JWT, fronting API Gateway HTTP API.
- Lambda container images from ECR: API, proactive worker, escalation.
- EventBridge sweep every minute.
- Step Functions Standard for the family chain.
- Bedrock Nova 2 Lite for agents and the judge.
- Transcribe (STT) and Polly (TTS).
- DynamoDB single table with a GSI, PITR and TTL.
- Cedar ConsentGuard.
- Secrets Manager/KMS, CloudWatch/CloudTrail.
- CDK for infrastructure, plus a Wear OS app (Kotlin).

**9. AI use (FACT).**
- An orchestrator plus five specialist agents (Strands-style tools).
- Stated rule: the model decides language and judgement; **code decides actions**.
- No silent LLM fallback. If Bedrock fails, the UI shows `llm_unavailable`.

**10. AWS use (FACT/INFERENCE).**
- About 15 services, each with a job.
- **Step Functions is the "coordinate the right person" mechanism.**
- **EventBridge is the proactive heartbeat.**
- The AWS diagram *is* the product logic, not a hosting footnote.

**11. Website (FACT, from source).** Editorial, story-led, in this order:
1. **Eyebrow:** positions it as non-surveillance support for aging at home.
2. **Hero:** "helps families care without watching", with a *Talk to Amma* CTA and service tags (Strands, Bedrock, Cedar, Wear OS).
3. **Tier strip:** T1 check in, T2 ask the right person, T3 only if needed.
4. **"The gap":** a three-line statement of the worry-versus-dignity tension.
5. **Six-step "How it works".**
6. **"The spine":** one orchestrator, five specialists.
7. **Watch scene.**
8. **Closing:** three short lines (remembers, asks her first, stays quiet).

**12. Screenshots and UI (FACT, from source).**
- Warm paper-and-ink palette using OKLCH tokens, display type, and framer-motion reveals.
- The hero "product seal" shows a live hi-IN call transcript with a "Day 14 · live" status and a line saying the panel usually stays empty.

**13. Demo video.** Not watched. `DEMO.md` **(from script)** is a 3–5 minute click path for an earlier variant called *Rakshak*, aimed at post-discharge readmission:
1. Landing.
2. Hinglish check-in, using chips for reliability and the mic for the wow.
3. Patient status card.
4. Doctor dashboard with AI summary and "why this risk".
5. Fall-detection replay.
6. Close.

It also has:
- A pre-demo smoke test of every AWS dependency.
- A fallback for every risk (chips if the mic fails, replay if the watch fails).
- A rehearsed answer to "what if Bedrock goes down?": show `/health/deep` breaker states and cross-region failover.

**INFERENCE:** the team pivoted mid-event from Rakshak to the sharper Suraksha story (the `backend/` folder is "legacy Rakshak plumbing"), and the final video centres on Amma's day.

**14. Story presentation (INFERENCE).** A named person, city, age, family and language. The problem is framed as an emotional tension, not a technology gap.

**15. Strongest demo moment (HYPOTHESIS).** The missed wake window:
1. Suraksha asks Amma first.
2. No reply, so Rahul is asked.
3. He can't come, so Priya is asked.
4. The neighbour is reached only because Amma's Cedar policy allows it.

This is judgement and consent made visible in one sequence.

**16. What made it memorable.**
- "Without watching."
- Silence as success.
- Consent spoken by voice and enforced as policy.

**17. What another team could easily copy.** An elderly voice companion with reminders and family alerts. This is very common.

**18. Likely reason judges preferred it (INFERENCE).** It scored on all five criteria at once:
- A universal problem with a specific ethical stance.
- A mechanism you can *see* (the escalation ladder and consent block).
- Deep, purposeful AWS, plus hardware and Hinglish voice.
- The Ship It prize explicitly scored architecture, and this architecture *is* the product.

**19. Weaknesses to avoid.**
- Scope sprawl: Wear OS, a 3D world, legacy backend, eight routes.
- The core baseline is simulated, though labelled.
- The live site is now locked, so it can't be verified after the event.
- Dependence on a physical watch.

**20. Transferable principles.**
- Frame the problem as a conflict between two legitimate needs, and make the mechanism the resolution.
- Make "fewer, better interventions" the outcome metric.
- AI judges; code acts.
- Turn consent and policy into a visible artifact.
- Escalate in a ladder that starts with the affected person.
- Label simulated data.

---

## 2. Beacon Night Shift — the on-call agent that fixes the 3 AM page by voice

**🥈 Second prize, Build It** · solo (CoffeAndCode) · [code](https://github.com/Prashant-thakur77/Beacon) · [video](https://youtu.be/a3SxZHvIkCo) · 87 commits · 244 tests (FACT)

**1. Problem (FACT).** At 3 AM, payments are failing and the on-call engineer is alone and half-asleep. They need four answers:
- Is it real?
- What changed?
- What do I do?
- Can I go back to sleep?

**2. Target user.** A solo on-call engineer running an AWS workload.

**3. Core insight.**
- A repeat of the same incident should not wake a human.
- Consent for automation should be scoped, expiring, and grounded in the human's own words.
- "Recovered" must be proven against telemetry, not asserted.

**4. Exact mechanism (FACT).**
1. A CloudWatch alarm fires and a triage Lambda runs:
   - Cordon log reduction using Nova multimodal embeddings.
   - Root-cause analysis by Nova 2 Lite.
   - A CloudTrail change ledger fed by EventBridge.
   - Security-group drift checked against a golden snapshot.
2. A Strands voice agent (Transcribe streaming plus Polly) proposes **one allowlisted fix**, with a dry run under the executing role and a stated blast radius.
3. The human says "approve fix one". This is checked against the **raw transcript**, not the model's claim.
4. A Step Functions loop runs DryRun → Approve → Execute → Wait → Verify ×6.
5. The incident resolves only if three checks pass:
   - The alarm returned to OK *after* the execute.
   - The error metric is zero.
   - The post-condition holds.
6. A **Sleep Contract** grants a scoped, expiring standing approval by voice.
7. The next identical incident is fixed unattended, and a morning email says "you were not woken".

**5. Genuinely novel.**
- The Sleep Contract.
- The transcript as the safety artifact.
- Verification-gated recovery.
- A two-role IAM design, asserted by tests that parse the real CloudFormation.

**6. Standard.** An alarm → LLM summary → chat UI. Many teams build this.

**7. UX and journey (FACT).**
- **Night Board:** the incident card, timeline, and evidence chips that tie each claim to evidence.
- **Talk** panel.
- **Contracts** page.
- **Safety** page with a kill switch.
- **Analytics:** recovery, sleep, cost.
- **"▶ Run the night":** replays the whole story locally in about 90 seconds.

**8. Architecture (FACT).**
- Five Lambdas.
- Step Functions.
- DynamoDB: incidents, approvals, contracts with TTL, change ledger, idempotency.
- SNS for pages and emails.
- S3 + CloudFront, or a Function URL proxy while a new account is under verification.
- CloudTrail → EventBridge.
- Transcribe and Polly.
- Bedrock Nova 2 Lite and Nova embeddings.
- A real ECS Fargate + RDS "patient" app to break.
- SAM templates, GitHub Actions CI, and a local mode with moto.

**9. AI use.**
- The LLM does root cause and dialogue only.
- Actions are bounded by a code allowlist, IAM, and transcript-checked consent.
- Every sentence cites its evidence.

**10. AWS use.** AWS is both the **platform and the subject**: it fixes AWS outages, giving the strongest possible "Built on AWS" signal. It also uses AWS open source (Strands, Powertools) to qualify for Build It while also being deployed.

**11. Website.**
- The live console runs on a Lambda Function URL.
- The README has a landing GIF, an architecture GIF/SVG, and screenshots.

**12. Screenshots and UI.**
- Night Board and Analytics screenshots.
- The final tally card reads "0 humans woken".

**13. Demo video (from script, `docs/demo-script.md`).** The team's own 3:00 shot list.

| Time | On screen | Analysis |
|---|---|---|
| 0:00–0:12 | A phone lights up on a bedside table with the SNS alarm email; the title appears; the four questions are spoken | **Problem clear in ~10 s** |
| 0:12–0:30 | Animated architecture naming each service by its verb (detects, reasons, says what changed, talks, fixes and proves) | **AWS visible by 0:30** |
| 0:30–0:50 | A real break: an RDS security-group rule is revoked on a live Fargate app; logs go red; the alarm flips; the Bedrock model ID is visible in logs | Product failure *happens for real* |
| 0:50–1:30 | Incident card; voice "what changed?" cites CloudTrail evidence; "can you fix it?" shows a fix card with dry run passed and blast radius | **Product visible by ~0:50** |
| 1:30–1:50 | "Approve fix one"; Step Functions graph turns green; EC2 rule back; alarm OK; "verified 3/3" | The climax |
| 1:50–2:15 | Sleep Contract granted by voice; a second outage is fixed with nobody woken; "not woken" email | **Payoff** |
| 2:15–2:42 | Safety montage, ~4 s each: allowlist, IAM JSON, approval record with transcript quote, idempotent replay, kill switch, tests green | Rigour |
| 2:42–3:00 | Tally: 2 incidents · 2.2 min median recovery · 0 humans woken; links | Final impression |

**Craft notes (from script):**
- 1080p, captions on every spoken line so it works muted.
- The real on-screen clock, with no edited timestamps.
- Rehearsed exact phrases.
- Retake reset commands.
- A fallback table for each failure.
- A local-mode take if AWS is unusable on recording day.

**14. Story presentation.**
- Three acts: pain, mechanism, payoff.
- A **second incident** acts as the before/after inside one video.

**15. Strongest moment.** The second outage is fixed under the contract and the tally reads "0 humans woken".

**16. Memorable.**
- A nameable concept: "Sleep Contract".
- A quotable command: "approve fix one".

**17. Easy to copy.** An LLM incident summariser or chat-ops bot.

**18. Likely reason judges preferred it (INFERENCE).**
- The judges are engineers and devrel people who *live* this pain.
- The safety engineering is credible, and a real outage is fixed on camera.
- A solo builder with 244 tests signals exceptional execution.

**19. Weaknesses to avoid.**
- The audience is narrow, and its societal impact is smaller.
- A long setup.
- The demo depends on exact scripted phrases.
- A non-devops judge needs the 0:00–0:12 framing to keep up.

**20. Transferable principles.**
- Make the failure happen for real on camera.
- Verify outcomes rather than claim them.
- Show human-in-the-loop first, then earned autonomy.
- End with a quantified tally.
- Captions, exact phrases, and a reset script.
- A local replay mode so anyone can run it.

---

## 3. CampusEvac — "Two views. One safe exit."

**🥉 Third prize, Best UI** · team 3 BUILDS (3) · [code](https://github.com/AfreenInnovates/campus) · [video](https://youtu.be/FhgTfCz0ou8) · 49 commits

**1. Problem (FACT).**
- Fire drills are expensive, disruptive and rare, so no muscle memory forms.
- Drills train evacuees but almost never the coordinator (warden).

**2. Target user.** Schools, colleges and offices, covering two roles: evacuee and warden or safety officer.

**3. Core insight.** Evacuation is a *two-person coordination problem* under time pressure. Training should rehearse that coordination cheaply and repeatedly.

**4. Exact mechanism (FACT).**
- An asymmetric two-player browser drill:
  - A first-person evacuee in a smoke-filled 3D building.
  - An overhead warden who verifies progress, sends route guidance, and can trigger ventilation.
- Neither can finish alone.
- Realtime sync uses AppSync Events on two channels:
  - Position broadcast at ~10 Hz, never stored.
  - Game and command events, persisted to DynamoDB.
- The end-of-run replay checks physical plausibility (advisory only).
- Polly narration with cached lines.
- An SES report email, scored server-side rather than trusting the client.

**5. Novel.** Training the warden role, an asymmetric co-op drill, and server-side recomputation of scores.

**6. Standard.** A 3D web game (React Three Fiber, Rapier) and realtime multiplayer.

**7. UX and journey.** Lobby → paired views → objectives → outcome → emailed report.

**8. Architecture.** Next.js on Amplify, AppSync Events, DynamoDB, Polly, SES v2, and CDK.

**9. AI use.** Essentially none: Polly TTS only. **It won without an LLM.**

**10. AWS use.** AppSync Events is an unusual, well-fitted choice. Every service maps to a game function.

**11. Website.** A live Amplify site. The README has 8 screenshots.

**12. Screenshots and UI.** The README's screenshots cover:
- Narration overlay.
- Moving to the classroom.
- Next-objective HUD.
- The "got out safely" state.
- Report cards.
- The evacuee and warden views.

**13. Demo video.** Not watched. **HYPOTHESIS:** a split-screen of both players coordinating, built around the tagline.

**14. Story.**
- A two-part tagline ("Two views. One safe exit.").
- A cost and disruption problem.
- The "forgotten role" insight.

**15. Strongest moment (HYPOTHESIS).** The warden's ventilation intervention clears the smoke for the evacuee, seen in split screen.

**16. Memorable.** The asymmetric two-view mechanic.

**17. Easy to copy.** A generic 3D evacuation simulator.

**18. Why judges preferred it.** It won **Best UI**: visual polish plus a novel interaction. That category is judged on design and usability.

**19. Weaknesses.**
- No evidence of training outcomes.
- Needs two players.
- Little intelligence in the loop.

**20. Principles.**
- A striking visual metaphor sells on video.
- A project without an LLM can win on design.
- Find **the role nobody serves**.
- Recomputing results server-side signals rigour.

---

## 4. Magpie — AI-native finance workspace

**Runner-up ($1k)** · VOXTON (4) · [code](https://github.com/akkki007/magpie) · [video](https://youtu.be/VAFMQW4o7iE) · 12 commits

1. **Problem:** finance teams spend time repairing spreadsheets instead of planning, and reconciliation is manual.
2. **User:** finance teams at companies.
3. **Insight:** a model is a graph, not a grid. Formulas stored as ASTs with ID references survive renames, and one command bus can serve humans and agents (undo, audit, AI edits).
4. **Mechanism:**
   - A modelling grid on Postgres.
   - A reconciliation engine run against an **11,258-record synthetic batch with a labelled answer key**: 100% precision, 0% false matches, 98.6% match rate.
   - AI output is a *proposed* ChangeSet that a human accepts.
5. **Novel:** a ground-truth evaluation harness (`recon:eval`) and an ablation script.
6. **Standard:** a landing page, auth, and a dashboard.
7. **UX:** a dense, editorial finance UI ("black, white, and one flash of blue"), with a scripted 10-step product tour (driver.js) built for recording.
8. **Architecture:** Next.js 16 and Prisma. Deployed on ECS Fargate behind an ALB, with RDS Postgres and Secrets Manager.
9. **AI:** an adjudication tier, which the README admits has never run against a live model.
10. **AWS:** conventional hosting.
11. **Website:** magpie.akkki.tech, a full marketing surface.
12. **UI:** prototype screens in `designs/` are the target.
13. **Video:** not watched. The tour script exists for a stable take.
14. **Story (INFERENCE):** "less repair, more planning".
15. **Strongest moment (HYPOTHESIS):** the reconciliation scoreboard with 0% false matches.
16. **Memorable:** honesty. The README opens with a "what is actually built" status table.
17. **Easy to copy:** an AI spreadsheet.
18. **Why placed (INFERENCE):** measured accuracy against ground truth, plus taste.
19. **Weaknesses:** broad product, synthetic data, an AI tier not live, and plain AWS hosting.
20. **Principles:**
    - Publish a metric with ground truth.
    - AI proposes, a human approves.
    - Write an honest status table.

---

## 5. FreshTrace — real-time food freshness intelligence

**Runner-up ($1k)** · Powerpuff Girls (4) · [code](https://github.com/RakshitChaturvedi/FreshTrace) · [video](https://youtu.be/2fs2fxV5wJw) · 31 commits · **low-confidence analysis**

- **Facts available:**
  - The live site is an S3 static website in ap-south-1, titled "Real-time Food Freshness Intelligence".
  - The repo has `FreshTrace_Sensor/` (hardware firmware), `config/food_types/`, `frontend/`, `src/` and `data/`.
  - No README is visible on the default branch.
- **INFERENCE:** a sensor (likely gas, temperature or humidity) streams readings, which are scored against per-food-type spoilage profiles to predict remaining shelf life.
- **HYPOTHESIS:** aimed at households or small vendors to reduce food waste.
- **Transferable principles:**
  - Physical hardware makes a demo tangible.
  - Per-category domain configuration (food types) signals depth.
  - Food waste sits next to our Waste & Energy track.
- **Weakness to avoid:** a repo whose README doesn't explain itself. Judges read repos.

---

## 6. Expressive Captions — captions that hear how you said it

**Runner-up ($1k)** · Need sleep (3) · [code](https://github.com/sept1st2c/Daks-caption_VoiceAgent-video-editing) · [video](https://youtu.be/D836OKdoY2g) · 150 commits

1. **Problem:** Hinglish auto-captions are inaccurate and flat, so creators style emphasis by hand.
2. **User:** Reels and Shorts creators, editors, and small brands working in Hinglish or English.
3. **Insight:** style should come from **measured prosody** (loudness, pitch, duration), not guesswork. No single speech engine gets both Hinglish text and word timings right.
4. **Mechanism:**
   - Sarvam produces the Hinglish text, and AWS Transcribe (hi-IN) produces word timings. The two are aligned phonetically.
   - librosa measures prosody, and percentile-ranked emphasis drives styling.
   - Tone is decided per line by Bedrock, because per-word tone detection was tested and failed.
   - A voice agent edits by command ("make that line angry") through a Bedrock Converse tool loop, returning schema-validated JSON patches.
   - Rekognition places captions relative to objects ("where my hand is").
5. **Novel:**
   - Engine reconciliation.
   - Measured styling.
   - Published negative results.
   - "Preview equals export" via shared Remotion code.
6. **Standard:** an auto-caption editor.
7. **UX:** a browser editor with a demo project. Playback commands bypass the model so they stay instant.
8. **Architecture:** React/Vite and FastAPI; S3 and DynamoDB; Bedrock, Transcribe and Rekognition; LiveKit; Terraform; Lambda Function URL in ap-south-1.
9. **AI:** a typed tool surface with validation before applying, and one undo per agent turn.
10. **AWS:** speech, vision and LLM services are core to the value.
11. **Website:** a live editor.
12. **UI:** the README poster shows a side-by-side of their captions, a voice-edited version, and **another tool's output on the same footage**.
13. **Video:** not watched. **INFERENCE:** a head-to-head comparison against the status quo.
14. **Story:** "your captions sound flat; ours sound like you".
15. **Strongest moment (HYPOTHESIS):** the side-by-side comparison, then the voice edit.
16. **Memorable:** a visible before/after on the same input.
17. **Easy to copy:** auto-captions with styling.
18. **Why placed (INFERENCE):** a sharply Indian problem (Hinglish), measurable craft, and an honest engineering log.
19. **Weaknesses:**
    - No auth.
    - Borrowed credentials on the deployed stack, per its own README.
    - Voice tested mainly with synthesised speech.
20. **Principles:**
    - Show a head-to-head against what users use today.
    - Measure instead of guessing.
    - Publish what didn't work.

---

## 7. Factcade — AI operations copilot for small factories

**Runner-up ($1k)** · solo · [code](https://github.com/Alikhan207/Factcade) · [video](https://youtu.be/dzFcAaL3DCM) · **1 commit (FACT)**

1. **Problem:** when one machine stops, a small factory owner can't see what the whole line is about to lose.
2. **User:** small factory owners in India.
3. **Insight:** owners act on **rupees per hour**, not uptime percentages.
4. **Mechanism:**
   1. Simulated machine failure.
   2. A deterministic cascade model computes loss per hour in ₹ (plain Python, no AI).
   3. A Strands agent on Bedrock Nova Pro uses read-only tools to propose a plan.
   4. The plan is validated against the real machines and orders.
   5. The owner approves.
   6. EventBridge events record recovery.
   7. A rule-based fallback runs if AI times out, and the UI says so.
5. **Novel:** "the AI never computes money".
6. **Standard:** a simulation dashboard.
7. **UX:** live factory line, loss counter, plan, and approve.
8. **Architecture:** Amplify, API Gateway, Lambda, Bedrock (Strands), DynamoDB, EventBridge, and a notifier that logs.
9. **AI:** planning only, with outputs validated.
10. **AWS:** serverless, with Strands as the AWS open-source tool.
11. **Website:** an Amplify site; it also runs offline on sample data with a banner.
12. **UI:** a ticking rupee loss counter.
13. **Video:** not watched. The README says to show the notifier's CloudWatch log group on a second screen for the "where AWS fits" part.
14. **Story:** machine fails, ₹ bleeds, AI plan, approve, recovery.
15. **Strongest moment (HYPOTHESIS):** the loss counter slowing after approval.
16. **Memorable:** money on screen.
17. **Easy to copy:** factory dashboards.
18. **Why placed (INFERENCE):** a clear owner-level metric (₹/hour) and a clean separation between AI and maths.
19. **Weaknesses:**
    - A modelled factory with assumed numbers. The README admits the 60% recovery figure is an assumption.
    - Alerts only go to logs.
    - **A single-commit repository: under this tour's rules, a history that doesn't match the event dates can disqualify. Never copy this.**
20. **Principles:**
    - Put the user's own currency on screen.
    - Deterministic core, AI planner.
    - Label sample-data mode visibly.

---

## 8. The field: what the other 1,173 entries tell us

These titles were scraped from the official "All projects" gallery, **1,180 entries** in total, and matched by keyword. They are approximate counts, since a title can match more than one pattern.

| Pattern in the title | Count | Share |
|---|---:|---:|
| Guard / Shield / Sentinel / Kavach / Raksha | 99 | 8.4% |
| "AI-powered" / "AI-driven" | 65 | 5.5% |
| Assistant / Copilot / Companion / Buddy / Mitra / Sahayak | 65 | 5.5% |
| Indic-word naming (Setu, Kavach, Mitra, Vayu, Seva…) | 64 | 5.4% |
| "Platform" | 60 | 5.1% |
| "Intelligence" | 46 | 3.9% |
| Civic / complaint / road | 37 | 3.1% |
| Emergency / SOS / disaster | 27 | 2.3% |

**Environmental entries already appeared at First Commit**, even though its theme was open:
- Floods: FloodRoute, FloodSense ×2, ResQNet.
- Landslide: NER Landslide Guard.
- Cyclones from satellite: VayuDrishti.
- Satellite-ground air quality fusion: Vayu AI.
- Food-waste apps: ≥4.
- Waste management platforms: Chokho AI, Waste2Value, TrashTag, Sustainify.
- Solar: SolarLens, a quote checker.
- EV: SmartCharge.
- Electricity theft: Tripwire.

**None of them placed.**

**INFERENCE:** an environmental topic earns nothing by itself; the winners won on mechanism, specificity and execution. Expect these same ideas, many by the same students, to return in volume for Environmental Hacks.

---

## 9. Video watch checklist for the team (~25 minutes)

Watch in this order and note answers in this file:
1. [Suraksha](https://youtu.be/XVr34XeXvlE)
2. [Beacon](https://youtu.be/a3SxZHvIkCo)
3. [CampusEvac](https://youtu.be/FhgTfCz0ou8)
4. [Factcade](https://youtu.be/dzFcAaL3DCM)
5. [Expressive Captions](https://youtu.be/D836OKdoY2g)
6. [Magpie](https://youtu.be/VAFMQW4o7iE)
7. [FreshTrace](https://youtu.be/2fs2fxV5wJw)

For each video:
- [ ] Seconds until the problem is clear.
- [ ] Seconds until the product appears.
- [ ] Seconds until AWS appears, and *how* (diagram, console, logs).
- [ ] Is the voiceover a human or TTS? Are there captions?
- [ ] Is real data or a real-world event shown?
- [ ] The single strongest moment, with its timestamp.
- [ ] The last 10 seconds: what is the final image?
- [ ] Anything confusing or slow.

---

## Sources

- [First Commit winners page](https://www.wemakedevs.org/aws/first-commit/projects) · [all 1,180 projects](https://www.wemakedevs.org/aws/first-commit/projects/all) · [top blogs](https://www.wemakedevs.org/aws/first-commit/projects/blogs) · [event overview and judging criteria](https://www.wemakedevs.org/aws/first-commit) · [judges](https://www.wemakedevs.org/aws/first-commit/judges)
- Repos:
  - [Suraksha](https://github.com/harshendram/firstcommit-hack) (incl. [DEMO.md](https://github.com/harshendram/firstcommit-hack/blob/main/DEMO.md) and landing source under `web/src/`)
  - [Beacon](https://github.com/Prashant-thakur77/Beacon) (incl. [demo-script.md](https://github.com/Prashant-thakur77/Beacon/blob/main/docs/demo-script.md))
  - [CampusEvac](https://github.com/AfreenInnovates/campus)
  - [Magpie](https://github.com/akkki007/magpie)
  - [FreshTrace](https://github.com/RakshitChaturvedi/FreshTrace)
  - [Expressive Captions](https://github.com/sept1st2c/Daks-caption_VoiceAgent-video-editing)
  - [Factcade](https://github.com/Alikhan207/Factcade)
- [FreshTrace live site (title only)](http://freshtrace.s3-website.ap-south-1.amazonaws.com/)
