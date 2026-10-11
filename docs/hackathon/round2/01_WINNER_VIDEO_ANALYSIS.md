# R2-01 — Winner Demo Videos: What They Actually Show

This file completes and corrects `../01_PREVIOUS_WINNERS.md`. The first pass could not watch the videos, so it relied on the teams' written demo scripts. This pass watched them.

The full frame-by-frame evidence, with a timestamped link for every claim, is in [`evidence/A_winner_videos.md`](evidence/A_winner_videos.md). This file is the decision-relevant summary.

---

## Access and method (including the remaining limitation)

**The watch skill could not run from the cloud workspace.**
- Its network proxy returns 403 for both YouTube and Google's Gemini API (re-tested 9 Oct, 22:00 IST).
- So the videos were watched through the Claude app's built-in browser on the user's computer.

**How the videos were captured:**
- Auto-generated transcripts were read from YouTube's own transcript panel, for all 7 videos.
- Frames were drawn from the paused `<video>` element at 0, 3, 8 and 15 s, then every 7–10 s. That gave 30–40 frames per video, re-sampled at 1–2 s where a beat mattered.

**Remaining limitations:**
- No audio was heard, so voice type and music are only partly known.
- YouTube caption overlays were not captured.
- Judges' score sheets are not public. Every "why it won" statement is therefore INFERENCE (n = 7).

Labels used below:
- **OBSERVED:** seen at a timestamp, or read from YouTube metadata.
- **INFERENCE:** reasoning from those observations.

---

## Cross-video facts

| Video (place) | Length (OBSERVED) | Problem clear by | Working product on screen | How AWS is shown | Voice / captions |
|---|---|---|---|---|---|
| Suraksha (1st) | **3:02** | ~0:08 | 0:28 (watch + dashboard) | Service tags at 0:00; static diagram 1:57–2:48 | Narrator + team member on camera; burned-in captions |
| Beacon (2nd) | **3:23** | ~0:13 | 1:07 (Night Board) | 0:45 animated 3D architecture; 2:43–2:47 CLI on the real account | Off-camera narrator; kinetic type in the cold open |
| CampusEvac (3rd, Best UI) | 2:50 | Never stated as a problem; tagline at 0:12 | 0:22 lobby; 0:30 split screen | 2:00–2:38 live consoles (Amplify, AppSync, SES, CloudFormation) | Human; full burned-in captions |
| Magpie (RU) | **3:41** | ~0:35 | 1:37 | 1:12–1:31 animated stack + App Runner vs Fargate race | Human, on camera; no captions |
| FreshTrace (RU) | 2:59 | ~0:05 | 0:00 | IoT console filmed on a phone; 60 s console tour | Human, off camera; no captions |
| Expressive Captions (RU) | 2:59 | ~0:15 | 0:22 | Animated architecture + Terraform + live URL at the end | Human, on camera; product-made captions |
| Factcade (RU) | **3:27** | ~0:45 | 0:00 | **None.** Narrated only | Human, off camera; no captions |

**Corrections to the first pass:**

| Earlier claim | What the videos show (OBSERVED) |
|---|---|
| Suraksha's hypothesised "missed wake → Rahul → Priya → Cedar-gated neighbour" climax | **Not shown.** The video pitches Suraksha, then demos the earlier **Rakshak build on localhost**. A real Galaxy Watch is dropped, it asks "are you okay?" in Hindi, a dashboard escalates, and **a real phone rings** with an automated call. |
| Beacon's demo runs on live AWS | The product demo runs in **local mode against moto with a scripted model**, labelled "local · moto" in the UI. Real-AWS proof is a ~5 s CLI shot. |
| FreshTrace was low confidence | It is an **IoT food-spoilage monitor**: an ESP32 gas sensor streaming to IoT Core. Moving it from fresh to rotten tomatoes flips the dashboard to "83% · SPOILED". |
| "Target ≤ 2:55" | Correct for us, but **four placed videos ran past 3:00** (3:02, 3:23, 3:27, 3:41). INFERENCE: judges were lenient or watched the first 3 minutes. Overrunning is a risk to avoid, not a pattern to copy. |

---

## Per-project findings

### Suraksha (1st)

| Aspect | Finding |
|---|---|
| Problem / user | A parent ageing alone; remote adult children. "Both are right" (worry vs dignity) is stated by 0:08 |
| Sequence | Landing → watch drop → Hindi voice check on the watch → escalation board → real handset call → static architecture → closing line that the model informs the decision and never makes it (~3:00) |
| Strongest moment | A **physical trigger leading to a real-world consequence in one take**: watch drop → phone actually rings |
| Credibility devices | Real hardware; a "simulated in the browser" label; the line "the model informs the decision" |
| Easy to replicate | A voice companion with alerts |
| Memorable | The real call |
| Weaknesses | Brand mismatch (Suraksha pitch, Rakshak UI on localhost); a long spoken AWS list; empty YouTube description |

### Beacon Night Shift (2nd)

| Aspect | Finding |
|---|---|
| Problem / user | A solo on-call engineer at 3 AM; four questions framed by 0:13 |
| Sequence | Cold open → animated architecture (0:45) → Night Board (1:07) → voice "approve fix one" (1:29) → Step Functions verify → Sleep Contract → **second identical outage handled, nobody woken** (1:56–2:03) → safety montage → CLI on the real account (2:43) |
| Strongest moment | The repeat incident resolved under the contract. The KPI moves to "2 incidents, 1 human woken" |
| Credibility devices | "Safety is code and IAM, not a prompt" (2:10); local/moto honestly labelled; tests |
| Easy to replicate | An alarm summariser |
| Memorable | "Sleep Contract"; "approve fix one" |
| Weaknesses | 3:23 long; real-AWS proof only seconds long |

### CampusEvac (3rd, Best UI)

| Aspect | Finding |
|---|---|
| Problem / user | Wardens and evacuees. The problem is never framed in cost terms |
| Sequence | Tagline (0:12) → lobby (0:22) → split screen with live play (0:30) → warden's warning appears on the evacuee's HUD (0:45) → debrief card → emailed report → console tour (2:00–2:38) |
| Strongest moment | The **mechanism in one frame**: a labelled split screen showing cause and effect across two roles |
| Credibility devices | Real consoles; SES sandbox caveat stated |
| Memorable | "Two views. One safe exit." |
| Weaknesses | No problem framing; generic YouTube title; empty description |

### Magpie (RU)

| Aspect | Finding |
|---|---|
| Strongest moment | A ground-truth scoreboard: 98.6% match, 100.0% precision, 0.0% false matches on 11,269 records (2:20) |
| Weaknesses | 24 s of team intros; narration contradicts the screen ("only six left" vs "Outstanding 37"); 3:41 long |

### FreshTrace (RU)

| Aspect | Finding |
|---|---|
| Strongest moment | A physical swap (fresh → rotten tomatoes) moves the number on screen |
| Weaknesses | Phone-filmed screens; unsupported numbers ("40–60% waste reduction", "sub 15 ms"); ends on the SNS console |

### Expressive Captions (RU)

| Aspect | Finding |
|---|---|
| Strongest moment | A **same-clip, three-panel comparison against a named competitor's default** (1:12) |
| Credibility devices | The video's own captions are product output; each AWS service is labelled with its job |

### Factcade (RU)

| Aspect | Finding |
|---|---|
| Strongest moment | ₹2,550 → ₹1,560 per hour after an approved plan (0:30) |
| Credibility devices | It shows the AI failing honestly ("Rule-based plan. The AI copilot did not return a usable answer.") |
| Weaknesses | No AWS visual at all; builder-centric opening; narration out of sync with the screen; poster ending |

---

## Transferable principles

Each principle is stated as "X worked because it solved Y for Z using A". All are INFERENCE from n = 7.

1. **Show the second time.** Beacon worked because it solved repeat-page fatigue for solo on-call engineers using a scoped standing approval, proven by a second identical incident inside the same video.
2. **A physical trigger with a real consequence, in one take.** Suraksha's watch drop leads to a ringing phone. FreshTrace's tomato swap leads to "SPOILED".
3. **Put the user's own unit on screen and make it move.** Factcade's ₹/hour; Beacon's "humans woken"; FreshTrace's "hours left".
4. **Compare against the status quo on the same input.** Expressive's same clip beside a competitor's output. Magpie's same question run on two stacks.
5. **Ground-truth metrics, not claims.** Magpie's planted answer key.
6. **Say "AI advises; code and humans act" out loud.** Four of seven did, in so many words.
7. **Label simulation visibly.** Four of seven did, including first and second place. Candour did not block placement *when paired with some real-environment proof*.
8. **Make the mechanism readable in one frame.** CampusEvac's split screen.
9. **Map each AWS service to a job, not a list.** Beacon and Expressive did this. Long spoken lists (Suraksha ~50 s, FreshTrace ~60 s) carry little information per second.
10. **Problem within 15 s, framed as a tension or a vivid moment.**

**What separated the top three (INFERENCE):** not AI depth but **one memorable visual proof**:
- the real call;
- the second night with nobody woken;
- the split screen (CampusEvac has no LLM at all).

## Anti-patterns observed (even placed teams had them; none helped)

- Team or builder intros before the problem.
- Narration out of sync with, or contradicting, the screen.
- Phone-filmed screens.
- Unsupported impact numbers.
- No AWS visual.
- Endings without a URL or call to action.
- Overrunning 3:00.
- Generic YouTube titles and empty descriptions.
- Brand mismatch between pitch and demo.

## What this changes for our concept choice

| Implication | Consequence for concept selection |
|---|---|
| A **real-world event captured on camera** was the strongest differentiator among placed entries | Concepts whose core loop can happen physically, in one take, on our own devices score higher on "demo" |
| Labelled replays are acceptable, but need **some live, real proof** next to them | — |
| How AWS is shown didn't predict placement, but **services labelled by job** read best | — |
