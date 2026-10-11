# 00 — Rulebook & Judging

**Event:** Environmental Hacks, Event 02 of the Bharat Builds Tour (WeMakeDevs × AWS Builder Center)
**Extracted:** Thu 8 Oct 2026, ~22:40 IST, from the official pages listed under Sources. The tour rulebook says it was last updated 16 Sep 2026.
**Method:** Official text is paraphrased with a section reference. Anything not stated officially is tagged **INFERENCE**.

---

## 1. Snapshot

| Item | Official position | Where |
|---|---|---|
| Dates | Thu 8 Oct to Sun 11 Oct 2026, online from anywhere in India | Overview |
| In person | Optional build day, Sat 10 Oct, 8 AM–8 PM, Delhi Technological University. Attending adds nothing to your score | Overview, FAQ |
| Team size | 1–4 people; one submission per team; one team per person | Rules §02 |
| Eligibility | University students in India, aged 18+ | Rules §01 |
| Cost | Free | FAQ |
| Tracks | Air · Heat & Water · Waste & Energy. Pick one; each track is judged on its own | Overview, FAQ |
| Prize per track | ₹2,00,000 cash + $2,000 AWS credits to each track winner | Overview |
| Other prizes | 4 runners-up across tracks get $1,000 credits each. Top 5 blogs get AirPods. Top teams get tour swag | Overview |
| Amazon fast-track | Up to 10 students across all tracks (2027/2028 graduates). Decided separately from prizes | Rules §06, §08 |
| Required to win | Use at least one AWS open-source tool **or** deploy on AWS | Overview "Two ways to build", Judging #2 |
| Submission | Public repo + YouTube demo video under 3 minutes + short writeup | Rules §04 |
| Live demo | None. The video is what judges see | Judging #5, Rules §04 |

---

## 2. Time constraints

- **Start:** Thursday 8 Oct (kickoff). Project work may only begin once the clock starts. Learning, planning and practice beforehand are allowed (Rules §03).
- **End:** Sunday 11 Oct, the last day to submit (Schedule).
- **Update 9 Oct 22:20 IST (FACT), from the organisers' public API** ([`/hackathons/env`](https://wemakedevs-server.onrender.com/hackathons/env)):
  - Event start: `2026-10-08T02:30Z` (08:00 IST Thu).
  - **Submissions open:** `2026-10-11T02:30Z` = **08:00 IST Sun**.
  - **Event end:** `2026-10-11T14:30Z` = **20:00 IST Sun**.
  - Registrations: 8,653.
  - The schedule page still lists the hours as "being finalised". Treat 20:00 IST as the hard close unless the official page says otherwise.
- **Deadlines are strict.** The form closes at the deadline and nothing can be entered after it (Rules §04).
- **Internal plan (INFERENCE):**
  - Everything filmed by Sun 16:00.
  - Submitted by Sun 18:00.
  - That leaves a 2-hour buffer before the 20:00 close.

**Elapsed-time reality (INFERENCE):** We are entering at ~23:00 IST on Day 1. That leaves roughly 60–65 working hours, including video production. Scope must reflect that.

---

## 3. Tracks (official framing)

The listed problems are "a place to start, not a list to pick from". Anything that makes the air cleaner, the water safer or the city lighter fits (Tracks section).

| Track | Official one-liner (paraphrased) | Listed starting problems |
|---|---|---|
| **01 Air** | Help people breathe easier: track what's in the air, warn the most exposed, change what happens on bad days | AQI · pollution exposure · stubble burning · indoor air · school safety on bad days |
| **02 Heat & Water** | Too much water, too little, and the heat in between: monsoon floods and summer dry taps | Heatwaves · floods · monsoon waterlogging · droughts · water tankers · leaks · groundwater |
| **03 Waste & Energy** | Close the loop on what a city throws away and cut what it burns | Segregation · recycling · e-waste · informal recyclers · rooftop solar · EV nudges · public transport |

- You **must pick one track** (FAQ).
- **Each track has its own winner.** We compete only against entries in our own track.
- The Amazon fast-track shortlist is drawn from all three tracks together.

---

## 4. Eligibility and team rules (Rules §01–02)

- University student in India, 18 or older.
- Two accounts per person:
  - A WeMakeDevs account.
  - An **AWS Builder Center profile with university enrollment verified** (via SheerID).
- If verification is still pending, you can still submit and be judged for prizes. The Amazon fast-track and the Builder Center rewards wait on verification. **Action: every teammate verifies now.**
- Every member registers individually; a captain cannot register the team. Every member must also **check in to this hackathon**.
- Teammates may be from different universities and cities.
- Organisers, judges, and WeMakeDevs or AWS staff may take part but cannot win prizes.

---

## 5. What you build, and originality (Rules §03)

- **New work only.** A project begun before the clock started does not qualify, even if rewritten.
- **Allowed:** open-source libraries, frameworks, public APIs, boilerplate and starter templates. Judging covers only what was added during the event.
- **Licensing:** anything you did not write needs a credit and a licence that permits use.
- **AI coding tools are allowed** but must be **listed in the writeup**.
- **Rights:** you keep the rights to your project. WeMakeDevs and AWS may showcase it.
- **Disqualifiers:** copying someone else's work, passing off an old project as new, or a **repository whose history does not match the event dates** disqualifies the whole team (Rules §05).

---

## 6. AWS requirements

| Requirement | Detail | Where |
|---|---|---|
| Mandatory to win a prize | Use an AWS open-source project **or** AWS services | Judging #2 |
| Two ways to build, in any track | **Build It:** locally with AWS open-source tools, no account needed. **Ship It:** deployed on AWS with a URL. Build It and Ship It are no longer tracks | Overview, FAQ |
| Visible in the video | "Your demo video has to show it". Naming AWS in the writeup alone is not enough | Rules §03 |
| Starting-point list (not a rule) | **Agents/AI:** Strands Agents SDK, PartyRock / SageMaker AI. **Containers:** Finch, EKS Distro/Anywhere / EKS, ECS, Fargate. **Serverless:** SAM CLI, LocalStack / Lambda, API Gateway, Step Functions. **Servers:** Firecracker, Corretto / EC2, Lightsail, App Runner, Amplify Hosting. **Data:** OpenSearch / S3, DynamoDB, RDS, Aurora. **Auth:** Cedar / Cognito. **Plumbing:** CloudFront, Route 53, EventBridge, SQS, SNS, CloudWatch | Overview |
| Cost | New accounts get up to $200 Free Tier credits. Once exhausted, a further $25 code per team (one form, filled by the team leader). Debit card or RuPay works for signup (~₹2 verification) | Resources, FAQ |
| Fairness | "We judge what you built, not what you spent." Local and deployed projects are scored with the same care | Judging |

**Notes on AWS (INFERENCE):**

- Amazon Bedrock is not on the starting-point list. It is still an AWS service and therefore qualifies. The top two First Commit winners both used Bedrock (see 01).
- First Commit gave cloud architecture explicit weight only in its Ship It prize. Environmental Hacks has no Ship It prize, so architecture is judged under the general "Built on AWS" criterion.
- A purposeful, visible use of AWS (each service doing a job in the story) will read better than many decorative services.

---

## 7. Submission package (Rules §04)

1. **Public repository.**
2. **Demo video:**
   - Up to 3 minutes. The rule says "under three minutes", so target **≤ 2:55**.
   - Uploaded to **YouTube** as public or unlisted.
   - **Check that the link opens in a signed-out browser.**
3. **Short writeup** covering the problem, the build, and **where AWS fits**. Also list **the AI coding tools used** and credit third-party code and data.
4. **Optional blog:** publish a blog on **AWS Builder Center** and link it in the submission. It is eligible for the top-5 blog prize.

Submit on this hackathon's own form, **once per team**, before the deadline.

**Judges score only what is submitted.**
- There is no live demo and no call.
- If the video does not show something, it does not count.
- A feature that exists only in the writeup does not count.

---

## 8. Judging criteria

There are five criteria and **no weights are published**. Assume equal weight unless the organisers say otherwise (INFERENCE).

| # | Criterion | What it officially asks (paraphrased) | What judges actually see | Implication for us |
|---|---|---|---|---|
| 1 | **Idea & Impact** | Does it fix a real environmental problem, and what changes for the people living with it? "A small problem solved well beats a big one solved vaguely." | Video opening, writeup | One precise user, one painful moment, one measurable change. Name the environmental quantity: kWh, µg/m³, litres or kg. |
| 2 | **Built on AWS** | AWS open source or AWS services. Mandatory to win | Video (must show), repo, writeup | AWS must be load-bearing and on screen: console, logs, a Step Functions graph, not just a logo slide. |
| 3 | **Design & usability** | Can the people living with the problem use it? Is it clear, easy to navigate, and built for where they are? Would an outsider know what to do? | Video UI, live URL if provided | Mobile-first, one primary action per screen, local language where it matters, obvious next step. |
| 4 | **Execution** | Does it work? Not perfect, not polished: working. "One feature that runs beats five that almost do." | Video, repo | One complete loop, shown end-to-end on real data, with failure states handled. |
| 5 | **Demo video** | Three minutes, recorded, showing what it does, who it is for, and where AWS fits | The video | Script it before building. Problem within ~15 s, product within ~30 s, AWS visible early, captions. |

**Process (Rules §05):**
- Venue and online entries go to the same panel with the same criteria.
- The panel's decision is final. Scores are not published.
- Winners are announced on the hackathon page and by email.

---

## 9. Disqualifiers and hard failure modes

| Risk | Consequence | Mitigation |
|---|---|---|
| Copying others' work or reusing an old project | Whole team disqualified | Fresh repo created after kickoff; no imported code beyond OSS libraries and templates |
| Repo history doesn't match event dates | Whole team disqualified | Commit early and often from today. Never squash everything into one commit, and never push a pre-built tree in one go (see 01: one First Commit runner-up had a single commit, a risk we won't take) |
| No AWS use | Not eligible for any prize | AWS is core to the design, not bolted on |
| AWS not shown in the video | "Does not count" | AWS shots scripted into the video |
| Video over 3 min, not on YouTube, or private | Likely unjudgeable | Target 2:50; check unlisted link while signed out |
| Late submission | Form closed, no entry | Internal deadline 2 h before the official one |
| Uncredited or unlicensed third-party code or data | Violates §03 | `CREDITS.md` with licences; verify dataset licences (e.g. NASA POWER is CC BY 4.0) |
| AI tools not listed | Violates §03 | List them in the writeup and README |
| Conduct violations | Participation ends, no appeal | — |

---

## 10. Prize mechanics worth knowing

- **Track winner ×3:** ₹2,00,000 + $2,000 credits each. Each track is judged independently.
- **Runners-up ×4:** $1,000 credits each, drawn from all tracks. No separate entry needed.
- **Blogs ×5:** AirPods. Requires a post on AWS Builder Center linked in the submission. **Cheap upside: write it on Sunday from our docs.**
- **Fast-track interviews:**
  - Up to 10 students. 10 is a ceiling, not a promise.
  - Pre-final-year (2028) and final-year (2027) students only.
  - Separate from prizes, decided by different people against different criteria.
  - Requires correct registration details and a verified Builder Center profile before the hackathon.
  - Interviews are for a 6-month internship or a full-time role.
  - Terms come from Amazon and can change.

---

## 11. Rules that shape architecture and implementation

These are decisions derived from the rules above. They are binding on Phase 12.

| # | Decision | Derived from |
|---|---|---|
| R1 | **Design the demo moment first.** Every judged feature must be visible within 2:55 of video. | Rules §04, Judging #5 |
| R2 | **AWS must be load-bearing and visible.** Each service should map to a verb in the story (schedule, verify, read, notify). Show it on screen: console, CloudWatch logs, Step Functions execution graph. | Rules §03, Judging #2 |
| R3 | **Deploy it (Ship It path), with a public URL in README and writeup.** INFERENCE: not required, but it makes "it works" verifiable, and all three First Commit prize winners had live links. | Judging #4 |
| R4 | **Fresh repo with continuous commit history from Day 1.** Our research docs are planning artefacts, so they may live in the repo, created during the event. | Rules §03, §05 |
| R5 | **Free-tier-safe stack.** Use Lambda, DynamoDB on-demand, S3, EventBridge, Step Functions, Bedrock pay-per-token and Amplify Hosting. Avoid NAT gateways, always-on RDS, SageMaker real-time endpoints and OpenSearch domains. | Resources (credits) |
| R6 | **Built for where the user is.** Mobile-first web, Hindi plus English where it matters, works on a mid-range Android phone over mobile data. | Judging #3 |
| R7 | **Real data in the demo.** Any simulation is labelled on screen. | Judging #4; our Engineering Rules |
| R8 | **One complete loop beats breadth.** No feature enters scope unless it appears in the video. | Judging #4 |
| R9 | **The writeup explains AWS, but nothing is claimed only in the writeup.** | Rules §04 |
| R10 | **We compete only inside our track,** so the crowding analysis (05) is track-specific. | Overview |

---

## 12. Open questions to resolve today

Ask on WeMakeDevs Discord, or email contact@wemakedevs.org.

1. The exact submission deadline (time and timezone) and the form URL.
2. Whether a deployed URL is a form field. Probably optional.
3. Whether Environmental Hacks judges will be published. First Commit published 28.
4. Whether the 3-minute limit is strict to the second, or "up to 3:00" is acceptable. Until answered, assume strict: target ≤ 2:55.

---

## 13. Who judged the previous event (profile only)

First Commit (Event 01) listed **28 judges**:

| Profile | Count | Examples / note |
|---|---|---|
| Developer relations and community leads | ~10 | New Relic, Qualcomm, Appwrite, Storyblok and others |
| Senior, staff and platform engineers | ~9 | Adobe, Unity, Loco and others |
| ML and data engineers | ~3 | Includes Apple |
| Founders and CEOs | ~4 | — |
| Amazon | 2 | One SDE, one Solutions Architect |

Environmental Hacks mentors are 20 AWS staff (cloud, database, support and AI/ML engineers, TAMs, consultants). Judges are not yet listed.

**INFERENCE:** expect technically strong generalists, not environmental scientists.
- Domain mechanics must be made self-evident on screen.
- Technical rigour (verification, safety, real data) will be noticed and rewarded.

---

## Sources

- [Environmental Hacks: overview, tracks, prizes, judging, FAQ](https://www.wemakedevs.org/aws/env)
- [Environmental Hacks: rules](https://www.wemakedevs.org/aws/env/rules) and [tour-wide rulebook (last updated 16 Sep 2026)](https://www.wemakedevs.org/aws/rules)
- [Environmental Hacks: schedule (deadline hour still to be announced)](https://www.wemakedevs.org/aws/env/schedule)
- [Environmental Hacks: mentors](https://www.wemakedevs.org/aws/env/mentors)
- [Bharat Builds Tour home](https://www.wemakedevs.org/aws)
- [First Commit (Event 01) overview and judging](https://www.wemakedevs.org/aws/first-commit) and [First Commit judges](https://www.wemakedevs.org/aws/first-commit/judges)
