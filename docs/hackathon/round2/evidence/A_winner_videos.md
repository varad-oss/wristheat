# First Commit winners: evidence-based demo-video analysis (seven announced winners)

Scope: this file completes and corrects the script-based video readings in `/home/claude/docs/hackathon/01_PREVIOUS_WINNERS.md`. Every bullet is labelled **OBSERVED** (a frame seen at mm:ss, YouTube metadata, or a transcript quote of 15 words or fewer, with its timestamp) or **INFERENCE** (my reasoning from those observations). Source links point at the exact second (`&t=Ns`).

Short source keys used below:
- Suraksha (S): https://www.youtube.com/watch?v=XVr34XeXvlE
- Beacon Night Shift (B): https://www.youtube.com/watch?v=a3SxZHvIkCo
- CampusEvac (C): https://www.youtube.com/watch?v=FhgTfCz0ou8
- Magpie (M): https://www.youtube.com/watch?v=VAFMQW4o7iE
- FreshTrace (F): https://www.youtube.com/watch?v=2fs2fxV5wJw
- Expressive Captions (E): https://www.youtube.com/watch?v=D836OKdoY2g
- Factcade (X): https://www.youtube.com/watch?v=dzFcAaL3DCM

---

## Evidence base: what was actually watched, and how reliable is it?

### Takeaway
All seven videos were reached and examined in the Claude desktop app's built-in browser on 2026-10-09: full auto-generated transcripts for all seven, plus 30–40 sampled frames per video, with full-width frames wherever on-screen text mattered. Audio could not be heard, so voice type (human or TTS) and music are only partly determinable.

### Cited Findings
- OBSERVED: YouTube was reachable from the built-in browser; every video's `ytInitialPlayerResponse` exposed only one caption track, `en` auto-generated (ASR), with no manual track — [S](https://www.youtube.com/watch?v=XVr34XeXvlE), [B](https://www.youtube.com/watch?v=a3SxZHvIkCo), [C](https://www.youtube.com/watch?v=FhgTfCz0ou8), [M](https://www.youtube.com/watch?v=VAFMQW4o7iE), [F](https://www.youtube.com/watch?v=2fs2fxV5wJw), [E](https://www.youtube.com/watch?v=D836OKdoY2g), [X](https://www.youtube.com/watch?v=dzFcAaL3DCM)
- OBSERVED (method): the `timedtext` caption URL fetched from page context returned an empty body, so transcripts were read from YouTube's own "Transcript" panel (6 videos). For Magpie the panel never loaded and the direct transcript API returned "Precondition check failed". Its transcript was captured instead from the player's live auto-captions while the video played at 2x — [M](https://www.youtube.com/watch?v=VAFMQW4o7iE)
- OBSERVED (method): frames were drawn from the paused `<video>` element into a contact-sheet canvas at 0, 3, 8, 15, ~22, ~30 s and then about every 7–10 s, plus the final seconds. Any text visible in these frames is burned into the video; YouTube's caption overlay is not captured by this method — all seven URLs above
- OBSERVED: no ads blocked sampling. Only Beacon showed a pre-roll, which was skipped — [B](https://www.youtube.com/watch?v=a3SxZHvIkCo)

### Inferences
- INFERENCE: auto-captions mis-hear product names ("Suraka", "FactCAD", "Corton" for Cordon, "Mac by" for Magpie). Quotes below are corrected only where the on-screen text confirms the right word.
- INFERENCE: with sampling every 7–10 s, beats shorter than about 5 s (for example Beacon's 4-second "real account" terminal shots) could be under-described. Where a beat mattered, it was re-sampled at 1–2 s spacing.

### Gaps
- No audio was heard. Statements about human versus TTS voice rest on visual evidence (a speaker on camera) or ASR traits (fillers such as "uh", self-introductions). Background music is known only where ASR inserted "[music]" (CampusEvac).
- Judges' score sheets are not public, so links between video features and placement are INFERENCE.

---

## Cross-video summary table (timings and AWS presentation)

### Takeaway
Problems became clear fastest in Suraksha, Beacon, FreshTrace and Expressive Captions (15 s or less). Two runners-up (Magpie, Factcade) spent their first 17–24 s on team or builder intros. Four of the seven videos run longer than 3:00. AWS was shown in four different ways (static diagram, animated diagram, live console, CLI terminal), and one placed video (Factcade) showed no AWS visual at all.

### Cited Findings

| Video (place) | Length (lengthSeconds) | Problem clear | Working product first on screen | First AWS visual, and how | Voice / captions |
|---|---|---|---|---|---|
| Suraksha (1st) | 3:02 (182) | ~0:08 | 0:00 landing; 0:28 watch + dashboard | Landing service tags at 0:00; static architecture diagram 1:57–2:48; 3D-world service cards 2:54–3:00 | Narrator plus on-camera team member (1:35); explanatory burned-in captions |
| Beacon (2nd) | 3:23 (203) | ~0:13 | 1:07–1:10 Night Board | 0:45 animated 3D architecture; 2:43–2:47 AWS CLI on the real account | Off-camera narrator; kinetic type in the cold open only |
| CampusEvac (3rd) | 2:50 (170) | Never stated as a problem; tagline at 0:12 | 0:22 lobby; 0:30 split-screen play | 2:00–2:38 live AWS consoles (Amplify, AppSync, SES, CloudFormation) | Human; full burned-in auto-captions; music at the end |
| Magpie (RU) | 3:41 player / 222 s | ~0:35 | 0:30 animated inserts; 1:37 real app | 1:12–1:31 animated stack slide and App Runner vs Fargate race | Human, on camera; no captions |
| FreshTrace (RU) | 2:59 (179) | ~0:05 | 0:00 dashboard | 0:00 "AWS IoT Core Active" badge; 0:50 IoT console (phone-filmed); 1:58–2:59 console tour | Human, off camera; no captions |
| Expressive Captions (RU) | 2:59 (179) | ~0:15 | 0:22 editor | 2:24–2:59 animated architecture, Terraform terminal, live URL | Human, on camera; product-generated animated captions throughout |
| Factcade (RU) | 3:27 (207) | ~0:45 | 0:00 dashboard | None; AWS only narrated, 2:19–2:42 | Human, off camera; no captions |

Supporting evidence for the table:
- OBSERVED: lengths come from `videoDetails.lengthSeconds`. Suraksha 182, Beacon 203, CampusEvac 170, Magpie 222, FreshTrace 179, Expressive 179, Factcade 207 — [S](https://www.youtube.com/watch?v=XVr34XeXvlE), [B](https://www.youtube.com/watch?v=a3SxZHvIkCo), [C](https://www.youtube.com/watch?v=FhgTfCz0ou8), [M](https://www.youtube.com/watch?v=VAFMQW4o7iE), [F](https://www.youtube.com/watch?v=2fs2fxV5wJw), [E](https://www.youtube.com/watch?v=D836OKdoY2g), [X](https://www.youtube.com/watch?v=dzFcAaL3DCM)
- OBSERVED: view counts on 2026-10-09 were Beacon 283, Suraksha 249, CampusEvac 159, Magpie 149, FreshTrace 93, Expressive 91, Factcade 25 — same sources
- OBSERVED: upload timestamps (YouTube microformat, US Pacific) all fall on 2026-09-20: CampusEvac 06:02, Beacon 09:07, Factcade 10:32, Magpie 10:59, Suraksha 11:15, FreshTrace 11:22, Expressive 20:58 (that is 2026-09-21 09:28 IST) — same sources

### Inferences
- INFERENCE: four placed videos ran past 3:00: Suraksha by 2 s, Beacon by 23 s, Factcade by 27 s, Magpie by 41 s. Under the "under-3-min video" rule noted in 01_PREVIOUS_WINNERS.md, length was evidently not disqualifying, either through leniency or because judges watched only the first 3 minutes. Copying this is a risk, not a pattern.
- INFERENCE: how AWS was shown does not predict placement. Raw consoles (CampusEvac, FreshTrace), diagrams (Suraksha, Expressive, Magpie), diagram plus CLI (Beacon) and nothing at all (Factcade) all placed.

### Gaps
- The submission deadline time zone is unknown, so I cannot say whether Expressive's upload at 09:28 IST on 21 Sep was on time.

---

## 1. Suraksha (1st, Ship It): what does the video actually show?

### Takeaway
The video pitches "Suraksha" on its landing page, then demos the **earlier "Rakshak" build running on localhost**. A physical Galaxy Watch is dropped, the watch asks "are you okay?" in Hindi, an escalation dashboard notifies a neighbour and building security, and a real phone rings with an automated emergency call. AWS appears only as a static diagram and as narration. The previously hypothesised "missed wake window → Rahul → Priya → Cedar-gated neighbour" sequence is not shown.

### Cited Findings
**Metadata**
- OBSERVED: title "Suraksha - First Commit Hackathon Submission", 182 s, uploaded 2026-09-20 11:15 PDT, 249 views, channel "Naomi P". The description is empty — [S](https://www.youtube.com/watch?v=XVr34XeXvlE)

**Problem and target user as presented**
- OBSERVED: the narration opens with the tension: "Parents want independence. Children want peace of mind." — [S @0:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=0s)
- OBSERVED (frame): the landing page reads "Adult children worry. Parents hate being watched. Both are right." — [S @0:08](https://www.youtube.com/watch?v=XVr34XeXvlE&t=8s)
- OBSERVED (frame): the demo's patient header shows a 72-year-old woman, "Day 4 · left knee replacement · Diabetes · Hypertension". The demo user is therefore a post-discharge patient, and the family, a neighbour and building security are the responders — [S @0:28](https://www.youtube.com/watch?v=XVr34XeXvlE&t=28s)

**First 15 seconds**
- OBSERVED (frames): the landing page is on an `amplifyapp.com` domain, with the hero "Helps families care without watching." (0:00), the T1/T2/T3 tier strip (0:03), the "Both are right" panel (0:08), and "One orchestrator. Five specialists. Nothing skips the tier." (0:15). The voiceover pitches fall detection on the wrist, speaking a task, and reminders — [S @0:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=0s), [S @0:15](https://www.youtube.com/watch?v=XVr34XeXvlE&t=15s)

**Beat list**
- OBSERVED: **0:00–0:26** landing-page scroll under the pitch narration. At 0:22 the landing's watch scene shows the tiles "First movement" and "I'm okay" — [S @0:22](https://www.youtube.com/watch?v=XVr34XeXvlE&t=22s)
- OBSERVED: **0:26–0:55** `localhost:3000/checkin` "Rakshak" dashboard beside live camera footage of a physical Galaxy Watch. Hinglish dialogue appears on screen ("Namaste Lakshmi, aap kaise ho aaj?"), with a burned-in caption: "…Galaxy Wear OS smartwatch while the Rakshak web dashboard updates in real time." — [S @0:28](https://www.youtube.com/watch?v=XVr34XeXvlE&t=28s), [S @0:40](https://www.youtube.com/watch?v=XVr34XeXvlE&t=40s)
- OBSERVED: **0:55–1:31** fall scenario. The presenter says "I'm going to drop it from a height" (1:03), the watch asks "Are you okay? And can you get up?", and the reply is "slight pain in my leg" (1:10). The `localhost:3000/command` "Command Center" (browser tab "Rakshak — Post-Discharge Rec…") then shows a Hindi live transcript and Escalation Progress cards (Neighbour NOTIFIED, Building Security NOTIFIED, Daughter PENDING). A timeline runs "0:00 Trigger fired … 0:27 Handoff generated", the status reads "AWAITING HANDOVER", and a caption says it "adapts to the patients' language" — [S @1:03](https://www.youtube.com/watch?v=XVr34XeXvlE&t=63s), [S @1:28](https://www.youtube.com/watch?v=XVr34XeXvlE&t=88s)
- OBSERVED: **1:31–1:57** a team member on webcam holds a phone that receives an automated emergency call. The call reads out the patient's name, age, address and injury, then asks the listener to "press one" to confirm they are on their way. A caption reads "Also a whatsapp text message is sent to the guardian." — [S @1:41](https://www.youtube.com/watch?v=XVr34XeXvlE&t=101s), [S @1:43](https://www.youtube.com/watch?v=XVr34XeXvlE&t=103s)
- OBSERVED: **1:57–2:48** a static diagram, "SURAKSHA (ALLY) – AWS ARCHITECTURE", narrated service by service. Its zones are A People & Devices, B AWS Front Door, C Serverless Runtime, D AI & Voice, E Trust/Memory/Observability, and a Proactive & Family Escalation zone holding Step Functions, Web Push `waitForTaskToken` and EventBridge "every minute" — [S @2:08](https://www.youtube.com/watch?v=XVr34XeXvlE&t=128s)
- OBSERVED: **2:48–3:02** an "Explore the world" 3D storytelling scene with these cards:
  - Team StarBugs (2:51).
  - "How Suraksha works" AWS service tiles (2:54).
  - A book, "What it remembers / Most days, nothing" (2:57).
  - A watch reading "No answer" with event cards: AWS Lambda `POST /ally/watch {kind:"fall"}`, an Amazon Polly `on_possible_fall()`, a deterministic `GateResult(passed=True, score=0.8)`, and an Amazon Nova `judge` card reading "The model informs the decision. It never makes it." (3:00) — [S @2:54](https://www.youtube.com/watch?v=XVr34XeXvlE&t=174s), [S @3:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=179s)

**Seconds to problem, product and AWS**
- OBSERVED: the problem is clear by about 0:08, the marketing product shows at 0:00, and the working product (watch plus dashboard) at about 0:28.
- OBSERVED: AWS shows as service tags in the landing hero at 0:00 (small, low legibility) and the spoken "on AWS" at about 0:05. The full treatment is a static diagram at 1:57, with no console, logs or live Step Functions graph — [S @0:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=0s), [S @2:02](https://www.youtube.com/watch?v=XVr34XeXvlE&t=122s)

**Shown working vs only claimed**
- OBSERVED (shown working): watch UI synced with the web dashboard; Hindi/Hinglish voice dialogue; a check triggered by the fall; multi-party escalation status with timestamps; and an outbound phone call received on a real handset — [S @1:28](https://www.youtube.com/watch?v=XVr34XeXvlE&t=88s), [S @1:52](https://www.youtube.com/watch?v=XVr34XeXvlE&t=112s)
- OBSERVED (claimed only, in narration or diagram): Cedar authorising every tool with an audit, the Step Functions family chain, the EventBridge proactive sweep, Cognito JWT, and CloudTrail. The transcript names Cedar only in the architecture narration ("Seda authorizes every tool and records an audit") — [S @2:32](https://www.youtube.com/watch?v=XVr34XeXvlE&t=152s)

**Credibility and honesty**
- OBSERVED: honesty label in the 3D world: "Simulated in the browser · the real window is 2 minutes to answer…" — [S @3:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=179s)
- OBSERVED: no metrics, user counts or tests are shown on screen — [S](https://www.youtube.com/watch?v=XVr34XeXvlE)

**Voice, captions, music, pacing**
- OBSERVED: a human team member speaks on camera from 1:35. The intro and architecture sections are voiceover. Burned-in captions are explanatory notes (0:28–1:43), not full subtitles. The architecture section runs about 50 s (1:57–2:48) — [S @1:35](https://www.youtube.com/watch?v=XVr34XeXvlE&t=95s)

**Final 10 seconds and last frame**
- OBSERVED: 3D-world cards from 2:52. The last frame reads "One person, actually coming. Nobody else was told." with a "See the stack" button. No URL or repo is on screen — [S @3:02](https://www.youtube.com/watch?v=XVr34XeXvlE&t=181s)

### Inferences
- INFERENCE (strongest moment, 1:03–1:52): the physical watch drop leads to the watch's voice check, then the escalation board, then a real phone ringing. It is the only sequence that moves from a physical cause to a real-world effect in one flow, which answers judge scepticism about whether the system is real.
- INFERENCE (differentiating mechanism as shown): a tiered "check with the person first, then the nearest responder" ladder, plus a deterministic gate before the LLM judge ("informs, never makes"), on hardware the user already wears.
- INFERENCE (easy to replicate): a watch companion with family alerts, a landing page and an architecture diagram. Hard to replicate: the full chain to a real phone call, Hindi voice on a watch, and the 3D storytelling world.
- INFERENCE (voice): ASR mangling ("Suraka", "next year on ampl Simplify Cognto") suggests a human narrator rather than TTS, but this is unconfirmed.
- INFERENCE (corrections to 01_PREVIOUS_WINNERS.md §1):
  1. The video does not "centre on Amma's day". It demos the Rakshak post-discharge fall flow on localhost, while the Suraksha brand appears only on the landing page, the diagram title and the 3D world.
  2. The §15 hypothesis (missed wake window → Rahul → Priya → Cedar-allowed neighbour) is not shown. The shown order is neighbour and building security notified first, daughter pending.
  3. DEMO.md's "Hinglish check-in → patient status → fall detection" beats are confirmed.
  4. A "doctor dashboard with AI summary" and `/health/deep` were not seen in sampled frames.

### Gaps
- Whether the phone call came from a deployed AWS path (for example Amazon Connect or SNS) or from another service is not shown.
- The 0:35–0:55 stretch is Hindi audio with no English ASR, so its exact dialogue is unknown.

---

## 2. Beacon Night Shift (2nd, Build It): what does the video actually show?

### Takeaway
This is a tightly produced, chaptered video. Its motion-graphics cold open makes the 3 AM problem clear by about 0:13, and an animated architecture appears at 0:45. The product demo (1:07–2:06) **runs in local mode against moto with a scripted model**, which the description states and the UI labels ("local · moto"). Real-AWS proof is a roughly 5-second CLI sequence at 2:42–2:47. The climax is a second identical outage resolved under a Sleep Contract.

### Cited Findings
**Metadata**
- OBSERVED: title "Beacon Night Shift — the on-call agent that fixes the 3 AM page with your voice", 203 s, uploaded 2026-09-20 09:07 PDT, 283 views — [B](https://www.youtube.com/watch?v=a3SxZHvIkCo)
- OBSERVED: the description holds a mechanism summary, 20 chapter markers, the AWS service list and an "Honest note". The note says the demo section is "the product running in local mode against moto with the model scripted", because new-account verification blocked Bedrock, and that 2:42 shows the real account — [B description](https://www.youtube.com/watch?v=a3SxZHvIkCo)

**Problem and target user as presented**
- OBSERVED: the narration opens "It is 3:00 in the morning. Payments are failing" (0:00) and lists four questions (0:10). It names the user as solo engineers and small teams in India on call for overseas customers (0:25–0:32) — [B @0:00](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=0s), [B @0:25](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=25s)

**First 15 seconds**
- OBSERVED (frames): 0:00 black; 0:03 a phone lock screen at "03:12, Sunday 20 September" with an ALARM notification; 0:08 server-rack footage with kinetic text "alone / half-asleep"; 0:15 "YOUR QUESTIONS, IN ORDER — is it real?" — [B @0:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=3s), [B @0:15](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=15s)

**Beat list**
- OBSERVED: **0:22** "ONE MONTH ON CALL" calendar showing repeat pages. **0:30** "YOUR CUSTOMERS' PEAK IS YOUR NIGHT", with clocks reading New York 5:30 PM and Bengaluru 3:00 AM. **0:40** title card: "…fixes the 3 AM page with your voice — and does not wake you the second time." — [B @0:30](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=30s), [B @0:40](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=40s)
- OBSERVED: **0:46** animated 3D flow "Alarm → triage on Bedrock → Night Board": CloudWatch alarm → Lambda triage·Cordon → Bedrock Nova 2 Lite·Embeddings → DynamoDB → Night Board on S3 + CloudFront → You. **0:56–1:06** "BEFORE THE MODEL READS A SINGLE LOG LINE", with two deterministic cards: a golden-snapshot drift check and a CloudTrail → EventBridge change ledger — [B @0:46](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=46s), [B @1:06](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=66s)
- OBSERVED: **1:10** Night Board with one High incident. **1:16** Beacon's briefing, pinned to evidence chip E1. **1:23–1:45** user turns labelled "YOU · typed": "can you fix it" gets the reply "1 ingress rule on 1 security group … dry run passed under the remediator role", then "approve fix 1". KPIs read 1 incident, 1.1 min median recovery, **1 human woken**, **₹0.138 model cost per incident**. The top bar reads "live · night · incident 1: fix, verify, grant a contract · local · moto · v0.1.0" — [B @1:45](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=105s)
- OBSERVED: **1:56–2:04** the second incident carries a "handled while you slept" badge, with the message "This one was handled under your Sleep Contract; you were not woken." A "Resolved under Sleep Contract · 3/3 checks" panel shows an error-count chart falling to 0. KPIs now read 2 incidents, 33 s median, **1 human woken**, ₹0.124 per incident, and the Contracts tab shows a badge of 1 — [B @2:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=123s)
- OBSERVED: **2:10–2:17** "SAFETY IS CODE AND IAM, NOT A PROMPT": nine numbered guarantees, each paired with a source file (`remediation/registry.py`, `snapshot.py`, `approvals.py`, `verify.py`, and so on) — [B @2:17](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=137s)
- OBSERVED: **2:24–2:38** "Every box is a service in the account": a 3D diagram including Fargate + RDS "the patient", the Remediator "write-only, tag-scoped", Step Functions "the verified loop", and a voice turn of Strands · Transcribe · Polly — [B @2:31](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=151s)
- OBSERVED: **2:43–2:47** terminal on the real account:
  - `aws cloudformation list-stacks` shows four stacks (beacon-console, beacon-remediation, beacon, beacon-demo-infra) as CREATE/UPDATE_COMPLETE.
  - `aws cloudwatch describe-alarms` shows `beacon-demo-infra-errors` in ALARM.
  - `aws lambda list-functions` runs, then `make dry-run` — [B @2:46](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=166s), [B @2:47](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=167s)
- OBSERVED: **2:54** "BUILT TO BE RUN" list: log retention, alarms → SNS, HSTS/CSP, RDS password in Secrets Manager, PITR/TTLs, timeouts and retries, "Each claim is a test against the CloudFormation". **3:00** terminal: `git clone … make setup … make local`. **3:13** "WHAT THIS WEEKEND TAUGHT ME": five lessons — [B @2:54](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=174s), [B @3:13](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=193s)

**Seconds to problem, product and AWS**
- OBSERVED: problem about 0:13, AWS at 0:45 (animated diagram), product UI at 1:07–1:10 (chapter "1:07 The Night Board") — [B @0:46](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=46s), [B @1:10](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=70s)

**Shown working vs only claimed**
- OBSERVED (shown working in local/moto mode, model scripted per the description): evidence-pinned briefing, one allowlisted fix with dry run and blast radius, a typed approval phrase, 3/3 verification, contract-based unattended resolution, and ₹ cost per incident — [B @1:45](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=105s), [B @2:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=123s)
- OBSERVED (shown on the real account): deployed stacks, the alarm in ALARM state, and the Lambda functions list. The output of `make dry-run` was not legible in the frames — [B @2:47](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=167s)
- OBSERVED (claimed but not shown as user input): voice. The UI has a mic and a "Transcribe" control and reads "agent 358 ms · Nova 2 Lite · Strands · Polly", but both observed user turns are labelled "typed" — [B @1:45](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=105s), [B @2:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=123s)

**Voice, captions, music, pacing**
- OBSERVED: a single off-camera narrator. No burned-in subtitles appear in the demo or architecture frames; the cold open uses kinetic typography. There are 20 chapter markers in the description — [B](https://www.youtube.com/watch?v=a3SxZHvIkCo)

**Final 10 seconds and last frame**
- OBSERVED: lessons slide (3:13–3:16), a dot (3:18), then "Beacon Night Shift — Build for the fourth question" (3:20). At 3:22 it adds `github.com/Prashant-thakur77/Beacon` and "Built on AWS · First Commit 2026 · Bharat Builds Tour", then fades to dark at 3:23 — [B @3:22](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=202s)

### Inferences
- INFERENCE (strongest moment, 1:56–2:04): the same fault recurs and is handled "while you slept", with 3/3 checks and the KPI moving to 2 incidents and 1 human woken. It is a before/after built into one demo, and it pays off the title's promise ("does not wake you the second time").
- INFERENCE (credibility): it compensates for a mocked demo with three moves: (a) a candid label in both the UI and the description, (b) a few seconds of real-account CLI proof, and (c) source-file citations beside every safety claim. The second-place result suggests judges accepted labelled simulation when the rest was rigorous.
- INFERENCE (easy to replicate): an alarm summariser with chat-ops. Memorable: the nameable "Sleep Contract", the "fourth question" framing, and the ₹ cost per incident.
- INFERENCE (voice): human versus TTS cannot be determined. The script is very polished, and ASR is near-perfect apart from proper nouns.
- INFERENCE (corrections to 01_PREVIOUS_WINNERS.md §2, from the script):
  1. The script's real break (0:30–0:50: an RDS security-group rule revoked live, red logs, a visible Bedrock model ID) is not in the final video. It is replaced by motion graphics, and the demo runs on moto.
  2. The tally is "2 incidents · 33 s · 1 human woken · ₹0.124", not "2.2 min · 0 humans woken".
  3. Length is 3:23, not 3:00.
  4. The script's "captions on every spoken line" were not observed.
  5. AWS appears at 0:45, not 0:30, and the product at about 1:07, not 0:50.
  6. Approval was typed in the observed frames, not spoken.

### Gaps
- No Step Functions execution graph turning green was seen in the sampled frames; it may appear briefly between 1:29 and 1:44.
- The "244 tests" claim is not shown running in the video.

---

## 3. CampusEvac (3rd, Best UI): what does the video actually show?

### Takeaway
The video leads with the tagline "Two views. One safe exit." and a live two-player run shown as a large, labelled **Warden's view | Evacuee's view split screen**. It ends with an in-app debrief card and an emailed report, then tours real AWS consoles. It never frames a cost or disruption problem.

### Cited Findings
**Metadata**
- OBSERVED: title "first commit hackathon", 170 s, uploaded 2026-09-20 06:02 PDT, 159 views, channel "Afreen Hossain". The description is empty — [C](https://www.youtube.com/watch?v=FhgTfCz0ou8)

**First 15 seconds**
- OBSERVED: landing page "TWO VIEWS. ONE SAFE EXIT." with a pixel-art character over an isometric building. A ticker runs short claims, among them "THE WARDEN SEES WHAT YOU CAN'T", "NO GAME SERVER" and "TWO PLAYERS". The human narrator introduces the team and the tagline — [C @0:00](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=0s), [C @0:15](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=15s)

**Problem and target user as presented**
- OBSERVED: the only framing is "a campus evacuation drill" with "two views, one safe exit" (0:00–0:15). No problem statement about drill cost, disruption or untrained wardens is spoken in the transcript — [C @0:06](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=6s)

**Beat list**
- OBSERVED: **0:22** lobby showing "DRILL TV57Q" with a join code and invite link. **0:30** split screen labelled "WARDEN'S VIEW / EVACUEE'S VIEW"; the in-game narrator begins "Welcome to Campus Evac. This is a fire…" — [C @0:22](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=22s), [C @0:30](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=30s)
- OBSERVED: **0:45** the warden map flags "EAST PASSAGE UNSAFE". The evacuee HUD shows a message from the warden: "East route is unsafe. Proceed to the verified west route." — [C @0:45](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=45s)
- OBSERVED: **0:40–1:28** six objectives (backpack, lab access card, gas valve closed, route guide in Classroom A201). The warden view shows a "WAITING FOR…" countdown, and the narration mentions possible brief connection "hiccups" — [C @1:20](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=80s)
- OBSERVED: **1:42** "DRILL COMPLETE. THEY GOT OUT SAFELY.": Time 0:52, Steps 6/6, Health 99. Three debrief prompts follow ("Did we get out safely? / Where did coordination slip? / What do we practise next?") above a "VERIFIED AGAINST THE DRILL RECORD" badge — [C @1:42](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=102s)
- OBSERVED: **1:50** emailed report "You got out safely." (time, objectives, errors, health, objective splits). Spoken caveat: the "first reports may land in spam" because of the SES sandbox and a Gmail sender — [C @1:50](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=110s), [C @1:40](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=100s)
- OBSERVED: **2:00–2:38** live AWS consoles: Amplify deployments (2:00), AppSync channel namespaces (2:10), the SES account dashboard (2:20), and CloudFormation stacks for CDK (2:32). The narration covers a ~10 Hz live channel and a game channel, DynamoDB, SES v2 and CDK — [C @2:00](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=120s), [C @2:10](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=130s)

**Seconds to problem, product and AWS**
- OBSERVED: no problem statement; the tagline lands at 0:12. The product shows at 0:00 (landing) and 0:30 (gameplay). AWS is spoken at 0:56 ("synchronized in real time via AppSync") and first seen at 2:00 as a console — [C @0:56](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=56s)

**Voice, captions, music, pacing**
- OBSERVED: human narration with self-introduction and fillers ("uh"), plus in-game narration. Full burned-in auto-style captions run throughout, with ASR errors such as "Commit Bharat Bills" (0:03), "the vacuum moves" (0:40) and "court TV57Q" (0:22). ASR inserts "[music]" at 2:39 and 2:44 — [C @0:03](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=3s), [C @2:39](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=159s)

**Final 10 seconds and last frame**
- OBSERVED: the deployed URL in pixel font (2:40), then "check it out here :)" with the amplifyapp URL (2:46), then black (2:49) — [C @2:46](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=166s)

### Inferences
- INFERENCE (strongest moment, 0:45): one frame holds the whole mechanism. The warden flags a hazard and the evacuee receives the reroute, side by side under big labels. The 1:42 debrief card (with its "verified against the drill record" badge) is the strongest credibility moment.
- INFERENCE (why Best UI): consistent visual identity across landing, lobby, HUDs and report (pixel-art plus cream editorial cards), and a mechanic legible in a single frame. It needs no problem framing because the visual makes the mechanism self-explanatory.
- INFERENCE (shown vs claimed): two-client realtime sync, warden-to-evacuee messaging, objective progression, completion verification and an emailed report are shown working. Server-side score recomputation is represented only by the badge. Polly is never named in the transcript; the in-game narrator voice is probably TTS (Polly per the README, unconfirmed).
- INFERENCE (corrections to 01_PREVIOUS_WINNERS.md §3):
  1. The split-screen hypothesis is confirmed.
  2. The "ventilation intervention clears smoke" strongest-moment hypothesis is not observed.
  3. The README's problem framing (cost, rarity, the forgotten warden role) is absent from the video.
  4. AWS is shown through real consoles, not a diagram.
- INFERENCE (easy to replicate): a 3D evacuation game. Memorable: the labelled split screen and the debrief card's three questions.

### Gaps
- Smoke and ventilation mechanics were not observed in sampled frames.

---

## 4. Magpie (runner-up): what does the video actually show?

### Takeaway
A presenter-led pitch with polished animated inserts, then a lower-fidelity screen recording with a webcam inset. The standout evidence is a reconciliation scoreboard of **98.6% match rate · 100.0% auto-apply precision · 0.0% false matches on 11,269 records**. Two choices weaken it: it opens with 24 s of team intros and runs to 3:41.

### Cited Findings
**Metadata**
- OBSERVED: title "Magpie — AI-Native Finance Workspace | AWS First Commit | WeMakeDevs", 222 s (the player shows 3:41), uploaded 2026-09-20 10:59 PDT, 149 views, channel "Sanskar Joshi Arts". The description is two generic sentences — [M](https://www.youtube.com/watch?v=VAFMQW4o7iE)

**First 15 seconds**
- OBSERVED: four on-camera team members introduce themselves and their modules, 0:00–0:24 (modelling engine and undo, workspace grid and databases, containers and AWS, AI agents and reconciliation) — [M @0:00](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=0s), [M @0:15](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=15s)

**Problem and target user as presented**
- OBSERVED: from 0:24, "companies plan in one big sheet". Cell H47 is emptied: "The 50 lakhs becomes zero, but nobody notices" (0:33–0:35). Second pain: one payment yields four records, matched by hand, "thousands of rows at midnight" (0:38–0:49) — [M @0:30](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=30s)

**Beat list**
- OBSERVED: **0:52–1:09** solution with an animated waterfall: "3,387 STILL UNMATCHED", after "Exact reference match −7,871" (1:02). The narration claims about 11,000 records with "only six left for a human" (1:03–1:08), and "It plans, it reads, it does not write." (1:09) — [M @1:02](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=62s)
- OBSERVED: **1:12–1:34** AWS segment as an animated stack of boxes, then a side-by-side "AWS App Runner" (spinner) vs "ALB → Fargate" (streaming), labelled "0.4s · same question, same clock". The narration explains why App Runner was rejected and names CloudFront, the load balancer, Fargate, Secrets Manager and CloudWatch, in Mumbai — [M @1:22](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=82s)
- OBSERVED: **1:37–2:08** live app at `magpie.akkki.tech/models/revenue-model-2026`: a 24-month revenue plan with named formula references; a formula is edited and values update. A webcam inset of the presenter sits over a desktop recording — [M @1:40](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=100s), [M @2:02](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=122s)
- OBSERVED: **2:09–3:08** `magpie.akkki.tech/recon`. KPIs read Match rate 98.6%, Auto-apply precision 100.0%, False match rate 0.0%, Records 11,269, Outstanding 37, Cash at risk ₹1,29,93,999.10. A proposals queue is headed "No rule could name a cause — this is the queue it reads", with accept, reject and undo — [M @2:20](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=140s)
- OBSERVED: **3:09–3:35** "Ask the model" panel answering a question about 30% of the closing ARR, with its reasoning shown. **3:36–3:41** another team member thanks viewers on camera — [M @3:18](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=198s), [M @3:38](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=218s)

**Seconds to problem, product and AWS**
- OBSERVED: problem clear about 0:35; product shown as animation at 0:30 and live at 1:37; AWS at 1:12 (animated slide, no console) — [M @1:12](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=72s)

**Voice, captions, music, pacing**
- OBSERVED: human voices, all on camera; no burned-in captions in sampled frames. The demo narration is hesitant ("So, like…"), and the screen recording is small on a desktop with a webcam overlay — [M @2:30](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=150s)

**Final 10 seconds and last frame**
- OBSERVED: Ask-the-model panel (3:30–3:34), then a talking head saying thank you (3:38–3:41). No URL, repo or end card — [M @3:41](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=221s)

### Inferences
- INFERENCE (strongest moment, 2:20): the ground-truth scoreboard of three precision metrics on 11k+ records confirms the earlier hypothesis. The App Runner vs Fargate "same question, same clock" race (1:22) is a second, unusual credibility move: an architecture choice justified by a visible test.
- INFERENCE (inconsistency): the narration's "only six left for a human" contradicts the on-screen "Outstanding 37"; the earlier doc's 11,258 records differs from 11,269 on screen. Judges who notice may discount the claims.
- INFERENCE (shown vs claimed): grid edits, reconciliation metrics, the proposals queue with accept and undo, and a model answering a question are shown working. Ablation ("same match three ways") is narrated only.
- INFERENCE (corrections to 01_PREVIOUS_WINNERS.md §4):
  1. The video does show a live model answering in "Ask the model". This is not necessarily the README's adjudication tier, so the README admission still stands.
  2. The "less repair, more planning" story is present but delivered after the team intros.
  3. The length (3:41) exceeds the 3-minute target.

### Gaps
- The YouTube transcript panel failed for this video, so the transcript comes from a 2x-speed live auto-caption capture and timings may be off by about 1 s.

---

## 5. FreshTrace (runner-up): what is the product, and what does the video show?

### Takeaway
FreshTrace is an **IoT food-spoilage monitor**: an ESP32-S3 with a Sensirion SGP41 gas sensor (VOC/NOx) and a Bosch BME280, sitting in a food container and streaming JSON every second to AWS IoT Core. An EC2 "kinetic" engine turns the readings into a spoilage-risk percentage and remaining shelf life in hours, and SNS alerts fire at 80% or more. The video's proof is physical: moving the sensor from fresh to rotten tomatoes flips the dashboard to "83% · SPOILED".

### Cited Findings
**Metadata**
- OBSERVED: title "FreshTrace: Real-Time Biochemical Spoilage Intelligence with ESP32-S3 & AWS Cloud Platform", 179 s, uploaded 2026-09-20 11:22 PDT, 93 views, channel "Team FreshTrace" — [F](https://www.youtube.com/watch?v=2fs2fxV5wJw)
- OBSERVED: the description gives:
  - Hardware: ESP32-S3, SGP41, BME280, with mutual-TLS X.509 to IoT Core.
  - Dataflow: sensors → ESP32-S3 → IoT Core → SQS → EC2 inference worker → RDS/S3 → dashboard → SNS alerts.
  - Modelling: Arrhenius kinetic modelling and remaining useful shelf life (RUL).
  - Demo food: tomatoes.
  - Chapter markers and the repo link — [F description](https://www.youtube.com/watch?v=2fs2fxV5wJw)

**Problem and target user as presented**
- OBSERVED: the narration opens "In India, we waste 55 kilos of food per person annually". The pitch is a "tiny sensor for your fridge for your lunch boxes" (0:07). Later it addresses supply-chain auditors (2:30) and alerts to drivers (2:55) — [F @0:00](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=0s), [F @2:30](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=150s)

**First 15 seconds**
- OBSERVED: the dashboard shows "LIVE SPOILAGE ASSESSMENT 11% risk score · Fresh & Safe to Consume", "Remaining shelf life 62.9 hours left", "Degradation velocity −0.002", and "Bio vs Thermal risk decomposition". Header badges read "AWS Alerts (Risk ≥ 80%)" and "AWS IoT Core Active · FreshTrace-Node-01" — [F @0:01](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=1s)

**Beat list**
- OBSERVED: **0:28–0:42** hardware close-ups of the ESP32 board and sensor breakout. **0:42–0:50** the sensor goes into a box of fresh tomatoes — [F @0:30](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=30s), [F @0:40](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=40s)
- OBSERVED: **0:50–0:58** the AWS IoT "MQTT test client", filmed by a phone pointed at a laptop. It shows a JSON payload on topic `freshtrace/device/FreshTrace-Node-01/telemetry` with `device_id`, `food_type: "tomato"`, temperature (~25.8 °C), humidity (~74.6%), pressure, VOC/NOx raw and index values, and `wifi_rssi` — [F @0:52](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=52s)
- OBSERVED: **1:06–1:27** the sensor moves to a box of "very rotten" tomatoes and the graph drops. The banner reads "CRITICAL SPOILAGE DETECTED: 83% RISK LEVEL (≥ 80% Threshold Exceeded)", with sub-text about an alert dispatched via Amazon SNS, plus "Spoiled & Hazardous" and "SPOILED · Shelf life expired" — [F @1:10](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=70s), [F @1:26](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=86s)
- OBSERVED: **1:28–1:57** the model is explained over a "How FreshTrace Works" page at `freshtrace.s3-website.ap-south-1.amazonaws.com`. It shows a bio-risk formula (clamped VOC drop), the Arrhenius thermal rate k(T), and RUL = (0.85 − Risk)/(|Velocity| − ε). Stat tiles read "40–60% WASTE REDUCTION · < 1.0s EDGE INGEST LATENCY · 100% NON-INVASIVE SENSING · AWS IoT MQTT TELEMETRY" — [F @1:40](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=100s)
- OBSERVED: **1:58–2:59** console tour:
  - IoT Core MQTT test client (2:02).
  - EC2 instance "axios-backend-server" (2:12).
  - RDS "axios-db", PostgreSQL in ap-south-1 (2:22).
  - S3 buckets (2:40).
  - SNS topic "AxiosSpoilageAlerts" with confirmed SMS subscriptions (2:49–2:59) — [F @2:12](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=132s), [F @2:49](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=169s)

**Seconds to problem, product and AWS**
- OBSERVED: problem at about 0:05 (a stat), product at 0:00, AWS at 0:00 (badge). Console views come at 0:50 (phone-filmed) and from 1:58 — [F @0:01](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=1s)

**Credibility claims made without on-screen evidence**
- OBSERVED: "sub 15 millisecond response times" (2:15), alerts "in under 100 milliseconds" (2:55), and the "40–60% waste reduction" tile (1:40) — [F @2:15](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=135s), [F @2:55](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=175s)

**Voice, captions, music, pacing**
- OBSERVED: human narrator off camera ("Let me introduce you…", fillers "uh"). No captions. About a third of the runtime (1:58–2:59) is the AWS console tour — [F @0:22](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=22s)

**Final 10 seconds and last frame**
- OBSERVED: the SNS topic page (subscriptions list) is on screen from 2:49 until the video ends at 2:59, with no end card or call to action — [F @2:59](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=178s)

### Inferences
- INFERENCE (what the product is): confirms and sharpens the earlier low-confidence reading. It is not a per-food lookup but a fusion of two models: a gas-based bio-risk score and Arrhenius heat exposure. Velocity projects remaining shelf life in hours, and a state machine raises an alert. The user is the household first, with cold-chain and audit use as a stretch.
- INFERENCE (strongest moment, 1:06–1:27): the fresh vs rotten tomatoes swap is a physical, unfakeable-looking cause driving a big state change (11–21% → 83%, "SPOILED") plus an alert banner.
- INFERENCE (shown vs claimed): real telemetry into IoT Core, the dashboard reacting, and the existence of EC2, RDS, S3 and SNS resources are shown. An SMS or email actually arriving and the SQS stage are not shown. The latency and waste-reduction numbers are unsupported.
- INFERENCE: AWS resource names ("axios-…") differ from the product name. This suggests reused or renamed infrastructure; judges could read it as a mismatch.
- INFERENCE (relevance to Environmental Hacks): this is the closest prior winner to a food-waste or environment theme. It placed only as runner-up despite real hardware, consistent with the earlier doc's finding that topic alone earns nothing.

### Gaps
- Whether the model is calibrated against real spoilage data is not shown; only a fresh-vs-rotten contrast is shown.

---

## 6. Expressive Captions (runner-up): what does the video actually show?

### Takeaway
A self-demonstrating video: the presenter's own captions are generated by the product, complete with sentiment tags. The core is a **same-clip three-way comparison**, "Our default | After voice edits | Kalakar.io · default", stepping through six numbered capabilities driven by voice prompts spoken on camera. It ends on an animated AWS architecture and a live URL.

### Cited Findings
**Metadata**
- OBSERVED: title "Express!ons - First Commit Video Submission", 179 s, uploaded 2026-09-20 20:58 PDT, 91 views, channel "Sept1c". The description is only the GitHub link — [E](https://www.youtube.com/watch?v=D836OKdoY2g)

**First 15 seconds**
- OBSERVED: an on-camera presenter with animated word-by-word captions ("and our app", 0:03). At 0:06 the problem is stated, that short-form content is too complicated. Motion graphics show a phone surrounded by editing jargon (0:08) and a four-step chain, "Create videos → Caption it → Style it → Style the video" (0:15) — [E @0:03](https://www.youtube.com/watch?v=D836OKdoY2g&t=3s), [E @0:15](https://www.youtube.com/watch?v=D836OKdoY2g&t=15s)

**Problem and target user as presented**
- OBSERVED: creators who do not know editing; captions that understand Hindi plus English and react to "tone, pitch, volume, delivery"; and the promise "We turn your voice into actual edits." (0:53–0:55) — [E @0:29](https://www.youtube.com/watch?v=D836OKdoY2g&t=29s), [E @0:53](https://www.youtube.com/watch?v=D836OKdoY2g&t=53s)

**Beat list**
- OBSERVED: **0:22** editor UI ("Just upload"). **0:30** "NORMAL TRANSCRIPTION: har saal meri birthday". **0:40** "MEASURED FROM THIS VOICE-OVER": Tone / Pitch / Volume / Delivery. **0:44** editor with a word list carrying timings, preset "Dhamaka — tweaked", and a caption timeline. **0:50** presets panel — [E @0:30](https://www.youtube.com/watch?v=D836OKdoY2g&t=30s), [E @0:44](https://www.youtube.com/watch?v=D836OKdoY2g&t=44s)
- OBSERVED: **1:00–2:24** three-up comparison headed "Same clip. Voice prompts are spoken on camera — results appear live." The panels are labelled "OUR DEFAULT", "AFTER VOICE EDITS" and "KALAKAR.IO · DEFAULT — the best captioning tool in the market right now for Indian audience". Numbered steps: 01 Preset switch (1:12); caption position, narrated 1:17–1:22; 03 Timed emphasis (1:32); 04 Excitement, stretched (1:48); 05 Anger, shaken (2:04); 06 Image analysis, an emoji placed over the face (2:20) — [E @1:12](https://www.youtube.com/watch?v=D836OKdoY2g&t=72s), [E @2:04](https://www.youtube.com/watch?v=D836OKdoY2g&t=124s), [E @2:20](https://www.youtube.com/watch?v=D836OKdoY2g&t=140s)
- OBSERVED: **2:24–2:59** animated architecture:
  - AWS Lambda "Editor · React·Vite" and AWS App Runner "API · FastAPI · Python 3.12 · 1–25 instances autoscale".
  - S3 for videos and exports; DynamoDB for projects and jobs.
  - Bedrock "Claude Sonnet 4.6" (tone tags), Transcribe "hi-IN · word timings", Rekognition "DetectFaces · Labels".
  - LiveKit real-time audio → Fargate voice worker; an internal ALB; a private Fargate render server (Node · Chrome · Remotion).
  - `<CaptionRenderer project={json} />`, with editor preview = exported MP4 "exactly" (2:53).
  - `terraform apply` (2:55), a globe zooming to Mumbai ap-south-1 (2:57), and "LIVE" with a lambda-url (2:59) — [E @2:42](https://www.youtube.com/watch?v=D836OKdoY2g&t=162s), [E @2:53](https://www.youtube.com/watch?v=D836OKdoY2g&t=173s), [E @2:59](https://www.youtube.com/watch?v=D836OKdoY2g&t=178s)

**Seconds to problem, product and AWS**
- OBSERVED: problem 0:06–0:15, product 0:22, AWS 2:24 (animated diagram plus a Terraform terminal; no console) — [E @2:26](https://www.youtube.com/watch?v=D836OKdoY2g&t=146s)

**Voice, captions, music, pacing**
- OBSERVED: human presenter on camera. Burned-in captions throughout are the product's own output, including sentiment tags such as "excited" over "right now" at 2:59 — [E @2:59](https://www.youtube.com/watch?v=D836OKdoY2g&t=178s)

**Final 10 seconds and last frame**
- OBSERVED: headless Chrome render (2:50), preview = export (2:53), Terraform (2:55), the Mumbai globe (2:57), then the full architecture with a "LIVE" URL bar and the caption "right now" tagged "excited" (2:59) — [E @2:59](https://www.youtube.com/watch?v=D836OKdoY2g&t=178s)

### Inferences
- INFERENCE (strongest moment, 1:12–2:20): the same clip runs against the named market tool, while the presenter speaks each voice prompt on camera and the result appears live. "Anger, shaken" (2:04) is the most visible difference. The head-to-head inference in the earlier doc is confirmed, and the competitor is named explicitly.
- INFERENCE (dogfooding): the video's own captions act as a continuous product demo, so the product is visible in every second, not only in the demo segment.
- INFERENCE (shown vs claimed): presets, voice-prompted edits, sentiment-styled captions and face-anchored emoji are shown. The AWS stack, LiveKit voice path and "preview equals export" are shown only as animation.
- INFERENCE (corrections to 01_PREVIOUS_WINNERS.md §6):
  1. Rekognition is shown placing an emoji over the face, not captions "where my hand is".
  2. Bedrock is labelled "Claude Sonnet 4.6" in the diagram.
  3. Sarvam is not mentioned in the captured narration.

### Gaps
- Whether the voice prompts were processed live or composited afterwards cannot be verified from frames, beyond the on-screen claim that they were live.

---

## 7. Factcade (runner-up): what does the video actually show?

### Takeaway
A solo, voiceover-only screen recording. The big ₹ loss-per-hour headline cycles through five machine failures; one approved plan cuts exposure from ₹2,550 to ₹1,560 an hour. It **honestly shows the AI failing**: twice the plan reads "Rule-based plan. The AI copilot did not return a usable answer." AWS is never shown visually, the opening is builder-centric, and it ends on a static poster.

### Cited Findings
**Metadata**
- OBSERVED: title "Factcade — AI Operations Copilot for Your Factories", 207 s, uploaded 2026-09-20 10:32 PDT, 25 views, channel "Nawaz Ahmed Khan" — [X](https://www.youtube.com/watch?v=dzFcAaL3DCM)
- OBSERVED: the description gives the demo arc ("CNC-02 failure → ₹2,550/hr … → ₹1,560/hr"). It splits AWS services into "Build It" (Strands, Nova Pro, Bedrock) and "Ship It" (Lambda, API Gateway, DynamoDB, EventBridge, S3, Amplify), and states the demo runs against the live backend — [X description](https://www.youtube.com/watch?v=dzFcAaL3DCM)

**First 15 seconds**
- OBSERVED (frame): "₹3,300 loss per hour · up to 8 workers affected · 3 orders at risk · 100% of the failed stage's output lost", above a line graph (CNC-01/CNC-02 → Grinding [down] → Inspection → Packaging → Dispatch, at-risk stages dashed red). At 0:15 it resets to ₹0 with "Working…" — [X @0:00](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=0s), [X @0:15](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=15s)
- OBSERVED (narration): "I thought of doing something different than healthcare or working on education" (0:01) — [X @0:01](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=1s)

**Problem and target user as presented**
- OBSERVED: 63 million MSMEs suffer monthly losses; when one machine is down for one to two hours, the question is the loss each hour (0:17–0:45) — [X @0:17](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=17s)

**Beat list (the screen runs independently of the narration)**
- OBSERVED: **0:18** "CNC-01 is down. The line is losing ₹2,550 an hour and 1 order is at risk." **0:25** action plan (shift jobs to CNC-02, prioritise ORD-191, schedule maintenance, notify) with "Approve plan". **0:30** "Approved. Loss fell from ₹2,550 to ₹1,560 an hour while CNC-01 is out." — [X @0:18](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=18s), [X @0:30](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=30s)
- OBSERVED: **0:48–1:26** "Grinding is down… ₹3,300 an hour and 3 orders are at risk."
  - At 1:05 the action plan reads "Rule-based plan. The AI copilot did not return a usable answer."
  - The event log shows "Action plan generated (fallback)" at 19:41:09, against an earlier "Action plan generated (nova)" at 19:40:37.
  - At 1:26: "Approved. Nothing could be rerouted, so loss stays at ₹3,300 an hour."
  - A footnote reads "Sample factory with modeled figures… Rerouting is assumed to recover 60%…" — [X @1:05](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=65s), [X @1:26](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=86s)
- OBSERVED: **1:35–2:55** further failures:
  - Inspection: loading state "Factcade is reading the line…", then a plan "Written by the AI copilot on Amazon Bedrock" (1:45–1:55).
  - Packaging: "₹1,100 an hour" (2:05), with "Action plan generated (nova)" highlighted (2:15).
  - Dispatch: a rule-based fallback again (2:45).
  - A scroll of the event log (3:03–3:10) — [X @1:55](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=115s), [X @2:15](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=135s), [X @2:45](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=165s)
- OBSERVED: **2:08–2:19** narration on the AI/maths split: "the AI does not invent the factory numbers" (2:10). **2:19–2:42** AWS services narrated only. **2:42–3:21** future roadmap (telemetry, vibration, temperature) — [X @2:08](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=128s), [X @2:19](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=139s)

**Seconds to problem, product and AWS**
- OBSERVED: product at 0:00; problem at about 0:17–0:45; AWS has no visual at any sampled frame (only the 2:19 narration) — [X](https://www.youtube.com/watch?v=dzFcAaL3DCM)

**Voice, captions, music, pacing**
- OBSERVED: human, off camera, first person, with fillers. No captions. The transcript ends mid-sentence ("That saves a lot of money for", 3:21) — [X @3:21](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=201s)

**Final 10 seconds and last frame**
- OBSERVED: a static poster from 3:15 to 3:27: "Factcade — AI operations copilot for your factories · Detect · Predict · Prevent · Optimize". It carries "Loss due to downtime ₹12,00,000 per incident" and "Smarter Factories, Stronger India." over a stock-style worker-with-tablet image — [X @3:15](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=195s), [X @3:27](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=206s)

### Inferences
- INFERENCE (strongest moment, 0:18–0:30): the owner's own currency is the headline, and it visibly drops after approval (₹2,550 → ₹1,560). This is a static recalculation rather than the "ticking counter slowing" hypothesised earlier.
- INFERENCE (honesty as credibility): showing both "(nova)" and "(fallback)" plans, plus a "modeled figures" footnote, demonstrates the "AI never computes money / rule-based fallback" design working. In the sampled runs the AI path failed 2 of 5 times on camera.
- INFERENCE (weaknesses): the narration is not synchronised with the screen (for example, it describes a CNC failure with four stages while the screen shows the Grinding fallback, 1:15–1:30). The opening is about the builder, not the user. The poster's ₹12 lakh-per-incident figure has no source. Nothing visual proves AWS.
- INFERENCE (corrections to 01_PREVIOUS_WINNERS.md §7): the README's advice to show the CloudWatch log group on a second screen was not followed, and no AWS appears on screen. The placement suggests judges weighed the ₹-centred mechanism over AWS visuals for this runner-up slot.

### Gaps
- No evidence in the video shows the deployed backend; the "runs against the live backend" claim is description-only.

---

## Across all seven: which transferable principles explain the wins?

### Takeaway
Seven principles recur, and each pairs a specific user friction with a mechanism that is visible in one frame:
1. A repeat or physical event that changes the system's behaviour on camera.
2. The user's own unit of value as the headline number, moving after the action.
3. A same-input comparison against the status quo.
4. AI that advises while code and humans act, stated in so many words.
5. Visible honesty labels on anything simulated.
6. A mechanism made legible in a single composited frame.
7. AWS services mapped to verbs rather than listed.

### Cited Findings
- **P1, show the second time (built-in before/after).** OBSERVED: Beacon's repeat outage is "handled while you slept", with 3/3 checks and the KPI moving to 2 incidents and 1 human woken — [B @2:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=123s). Statement: *Beacon worked because it solved repeat-page fatigue for solo on-call engineers using a scoped, expiring Sleep Contract, proven by a second identical incident inside the same video.*
- **P2, a physical trigger leading to a real-world consequence, in one take.**
  - OBSERVED: Suraksha's watch drop leads to the watch's voice check, the escalation board and a phone call on a real handset — [S @1:03](https://www.youtube.com/watch?v=XVr34XeXvlE&t=63s), [S @1:41](https://www.youtube.com/watch?v=XVr34XeXvlE&t=101s)
  - OBSERVED: FreshTrace's fresh-to-rotten tomato swap takes the risk to 83% and "SPOILED" — [F @1:26](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=86s)
  - Statement: *Suraksha worked because it solved the "is she okay and who should come" friction for distant families of an elderly parent, using a tiered escalation ladder triggered by a real fall event and ending in a real call.*
- **P3, put the user's own unit on screen and make it move.**
  - OBSERVED: Factcade ₹2,550 → ₹1,560 an hour — [X @0:30](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=30s)
  - OBSERVED: Beacon "₹0.124 model cost per incident" and "humans woken" — [B @2:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=123s)
  - OBSERVED: FreshTrace "hours left" — [F @0:01](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=1s)
  - OBSERVED: CampusEvac time, steps and health — [C @1:42](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=102s)
  - Statement: *Factcade worked because it solved the "I can't see what a breakdown costs me" friction for small-factory owners, using a deterministic ₹/hour cascade the owner can watch fall after approving a plan.*
- **P4, compare on the same input against the status quo.**
  - OBSERVED: Expressive's same clip in three panels, including a named competitor's default — [E @1:12](https://www.youtube.com/watch?v=D836OKdoY2g&t=72s)
  - OBSERVED: Magpie's App Runner vs ALB→Fargate, "same question, same clock" — [M @1:22](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=82s)
  - Statement: *Expressive Captions worked because it solved flat, inaccurate Hinglish captions for short-form creators using prosody-driven styling, proven side by side against the market tool on identical footage.*
- **P5, ground-truth metrics on screen.** OBSERVED: Magpie shows 98.6% match, 100.0% precision and 0.0% false matches on 11,269 records — [M @2:20](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=140s). Statement: *Magpie worked because it solved manual reconciliation toil for finance teams using a rules-first matcher scored against a planted answer key, with precision shown rather than claimed.*
- **P6, say "AI advises, code and humans act" out loud and show the gate.** OBSERVED in four videos:
  - Suraksha: "The model informs the decision. It never makes it." — [S @3:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=179s)
  - Beacon: "Safety is code and IAM, not a prompt" — [B @2:10](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=130s)
  - Factcade: "the AI does not invent the factory numbers" — [X @2:10](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=130s)
  - Magpie: "It plans, it reads, it does not write." — [M @1:09](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=69s)
- **P7, label simulation visibly; candour did not block placement.** OBSERVED:
  - Beacon: "local · moto" in the UI plus the description's honest note — [B @1:45](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=105s)
  - Factcade: the fallback label and modelled-figures footnote — [X @1:05](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=65s)
  - Suraksha: "Simulated in the browser" — [S @3:00](https://www.youtube.com/watch?v=XVr34XeXvlE&t=179s)
  - CampusEvac: the SES sandbox and spam caveat — [C @1:40](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=100s)
- **P8, make the mechanism one frame.** OBSERVED: CampusEvac's labelled split screen, where the warden's warning appears on the evacuee's HUD — [C @0:45](https://www.youtube.com/watch?v=FhgTfCz0ou8&t=45s). Statement: *CampusEvac worked (Best UI) because it solved the untrained-coordination gap in fire drills for evacuees and wardens, using an asymmetric two-screen drill whose whole mechanic is visible in one split-screen frame.*
- **P9, map each AWS service to a job, not a list.**
  - OBSERVED: Beacon's flow, with every box labelled by role ("the patient", "write-only, tag-scoped", "the verified loop") — [B @2:31](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=151s)
  - OBSERVED: Expressive labels each service with its job ("hi-IN · word timings", "DetectFaces · Labels") — [E @2:42](https://www.youtube.com/watch?v=D836OKdoY2g&t=162s)
  - OBSERVED: Suraksha's zoned diagram — [S @2:08](https://www.youtube.com/watch?v=XVr34XeXvlE&t=128s)
- **P10, problem in 15 seconds or less, framed as a human tension or a vivid moment.** OBSERVED:
  - Suraksha: "Both are right." — [S @0:08](https://www.youtube.com/watch?v=XVr34XeXvlE&t=8s)
  - Beacon: a phone lighting up at 03:12 — [B @0:03](https://www.youtube.com/watch?v=a3SxZHvIkCo&t=3s)
  - FreshTrace: the 55 kg stat — [F @0:00](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=0s)

### Inferences
- INFERENCE: the top three are distinguished less by AI depth than by a **single memorable visual proof**: the real phone call (Suraksha), the second night with nobody woken (Beacon), and the labelled split screen (CampusEvac, which has no LLM). Runners-up had strong mechanisms but weaker openings, pacing or visual proof.
- INFERENCE: honesty labels appear in four of the seven, including first and second place. Labelled simulation is safe when paired with some real-environment proof (Beacon's CLI, Suraksha's real handset).
- INFERENCE: AWS presentation style varied widely among placed teams. Purposeful mapping of services to jobs (P9) looks more valuable than raw console screenshots, which take a lot of airtime (FreshTrace spent about 60 s).

### Gaps
- With n=7 and no score sheets, these principles are correlational. The 1,173 non-placing videos were not watched, so it is unknown how many shared the same traits and still lost.

---

## Across all seven: which anti-patterns were observed?

### Takeaway
Recurring weaknesses, mostly among the runners-up:
- Openings about the team or builder.
- Narration out of sync with, or contradicting, the screen.
- Phone-filmed screens.
- Unsupported impact numbers.
- No AWS visual.
- Endings without a call to action.
- Exceeding 3:00.
- Generic YouTube metadata.
- A brand mismatch between pitch and demo.

### Cited Findings
- OBSERVED (builder or team opening delays the problem): Magpie spends 0:00–0:24 on four intros — [M @0:00](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=0s); Factcade opens on the builder's motivation — [X @0:01](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=1s)
- OBSERVED (narration out of sync with the screen): Factcade narrates a CNC failure while the Grinding fallback plays — [X @1:19](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=79s)
- OBSERVED (narration contradicts the screen): Magpie says "only six left for a human" against "Outstanding 37" on screen — [M @1:03](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=63s), [M @2:20](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=140s)
- OBSERVED (phone camera filming a laptop, low legibility): FreshTrace — [F @0:52](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=52s), [F @1:26](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=86s)
- OBSERVED (unsupported impact or performance numbers): FreshTrace "40–60% waste reduction" (1:40), "sub 15 ms" (2:15) and "under 100 ms" (2:55); Factcade poster "₹12,00,000 per incident" (3:15) — [F @1:40](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=100s), [X @3:15](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=195s)
- OBSERVED (no AWS visual at all): Factcade — [X](https://www.youtube.com/watch?v=dzFcAaL3DCM)
- OBSERVED (endings without a call to action or URL): FreshTrace ends on the SNS console — [F @2:59](https://www.youtube.com/watch?v=2fs2fxV5wJw&t=178s); Magpie ends on a talking head — [M @3:41](https://www.youtube.com/watch?v=VAFMQW4o7iE&t=221s); Factcade ends on a poster with the narration cut mid-sentence — [X @3:21](https://www.youtube.com/watch?v=dzFcAaL3DCM&t=201s)
- OBSERVED (generic metadata): CampusEvac is titled "first commit hackathon" with an empty description; Suraksha's description is empty; Expressive's description is only a link — [C](https://www.youtube.com/watch?v=FhgTfCz0ou8), [S](https://www.youtube.com/watch?v=XVr34XeXvlE), [E](https://www.youtube.com/watch?v=D836OKdoY2g)
- OBSERVED (brand or variant mismatch): Suraksha's pitch leads to a "Rakshak" UI on localhost — [S @1:28](https://www.youtube.com/watch?v=XVr34XeXvlE&t=88s)
- OBSERVED (over 3:00): Suraksha 3:02, Beacon 3:23, Factcade 3:27, Magpie 3:41 — same video URLs

### Inferences
- INFERENCE: a long spoken list of AWS services (Suraksha about 50 s, FreshTrace about 60 s) carries little information per second, compared with Beacon's diagram that pairs each service with a verb, or Magpie's single comparative test.
- INFERENCE: even placed teams had these flaws, so they are not fatal, but none of the flaws helped. The cleanest videos (Beacon, CampusEvac, Expressive) avoided most of them.
- INFERENCE (what a competitor can easily replicate across the set): voice companions with alerts, alarm summarisers, 3D drill games, AI spreadsheets, sensor dashboards, auto-captioners and factory dashboards. What is hard to replicate is the specific visual proof: a real call, a contract-handled repeat incident, a same-clip competitor comparison, a planted-answer-key scoreboard, or a fresh/rotten physical swap.

### Gaps
- Audio-only qualities (music, voice warmth, sound design) could not be assessed and may matter to judges.
