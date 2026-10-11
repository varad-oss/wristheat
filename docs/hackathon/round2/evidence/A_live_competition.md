# Live competition scan: what Environmental Hacks teams are actually building (as of Fri 9 Oct 2026, ~14:00 IST)

Method note: the scan used the WeMakeDevs public API (found through the projects page), the WeMakeDevs space feed and topic pages on AWS Builder Center (read in the built-in browser), and GitHub repository search (browser, logged out). That search combined three queries: (a) event keywords in the name or description, created on or after 1 Oct; (b) "wemakedevs" OR "environmental hacks" OR "bharat builds" in the README, created on or after 7 Oct; (c) track names ("heat and water", "waste and energy", "air track") in the README, created on or after 7 Oct. README text was read from raw.githubusercontent.com. Together the queries returned **about 140 repositories, and 111 identifiable Environmental Hacks projects** remained after removing non-event repositories, placeholders and duplicates. Tags: FACT means sourced, INFERENCE means a judgement, HYPOTHESIS means untested.

## Q1. Live signals: public posts and repositories for Environmental Hacks since about 1 Oct 2026

### Takeaway
Teams are building in the open far more than expected: 111 identifiable projects already have public repositories or posts. **Heat & Water dominates the visible sample (53, 48%), ahead of Air (34, 31%) and Waste & Energy (24, 22%).** Two clusters are heavily saturated: flood/waterlogging (≈23) and "school air-quality plan for the principal" (10). Two ideas our 05 map called whitespace are already contested: worker heat/WBGT shift planning (5) and cleanest-hour school planning.

### Cited Findings
**Event-level facts**
- FACT: Environmental Hacks shows **registration_count = 8,481**; `projects_published: false`; submissions open 2026-10-11T02:30Z and the event ends 2026-10-11T14:30Z (20:00 IST). — [WeMakeDevs API /hackathons/env](https://wemakedevs-server.onrender.com/hackathons/env)
- FACT: The project list endpoint returns HTTP 403 "Projects have not been published yet." It will be the canonical source once published. — [API /hackathons/env/projects](https://wemakedevs-server.onrender.com/hackathons/env/projects)
- FACT: First Commit had registration_count 13,667 and 1,180 projects, a ratio of 8.6%. — [API /hackathons/first-commit](https://wemakedevs-server.onrender.com/hackathons/first-commit); [recap](https://www.wemakedevs.org/blogs/first-commit-hackathon-recap-and-whats-next). Kunal Kushwaha's Builder Center post says "16,000 students" took part in First Commit, which conflicts with 13,667. — [Builder Center post](https://builder.aws.com/post/3KGj9FkeKgzYIxKTNs7AFg4EcpU_p/environmental-hacks-the-second-bharat-builds-hackathon)
- FACT: About 1,000 builders are expected at DTU on 10 Oct. The DTU workshop is the "Strands Agents hands-on: build your first agent" session (11:00–12:30). — [WeMakeDevs blog, Delhi day](https://www.wemakedevs.org/blogs/what-is-happening-in-delhi-on-10-october)
- FACT: The WeMakeDevs Builder Center space has 4,042 members. Most posts since 1 Oct are about team-finding, verification and credits. Only three are project posts: FloodGuard AI, the Air Quality Advisor and the event announcement. — [WeMakeDevs space](https://builder.aws.com/connect/space/29f78273-9a25-34b1-818f-eec9b0bacb31/wemakedevs)

**Builder Center project posts and articles**
- FloodGuard AI (Jalasutram Sai Sanjana), Heat & Water. ML waterlogging-risk prediction per location, built as S3 → model → Lambda → API Gateway → dashboard. Posted 8 Oct ("Day 1"). — [post](https://builder.aws.com/post/3KQErOT95rN94BMZie1vdt2M18G_p/day-1-or-bharat-builds-aws-environmental-hacks)
- Air Quality Advisor for Delhi (Abhinav Gupta, solo), Air. Pick an area and get a plain-language "should I step outside" verdict from WAQI data, on Spring Boot and Elastic Beanstalk. Posted about 6 Oct. — [post](https://builder.aws.com/post/3KJHlbkvtTbl6w7uxz21dzEld2k_p/building-an-air-quality-advisor-for-delhi-solo-with-spring-boot-and-aws); [repo](https://github.com/Abhinavgupta2404/aqiadvisor)
- Waterlog Watch (Abinivesh M), Heat & Water, Chennai. A citizen photo goes to Bedrock Nova Lite, which returns depth, severity, passability and hazards as JSON. The app then draws a live map, checks routes with Amazon Location Service, uses "still flooded/cleared" votes for self-healing, and adds a ward dashboard. Already deployed in ap-south-1. Published 8 Oct. — [article](https://builder.aws.com/content/3KOwALE7mzZeZ48dh80pCBmr6Ci/waterlog-watch-ai-verified-flood-alerts-on-aws); [repo](https://github.com/abinivesh-m/waterlog-watch)

**Complete list of live projects found (GitHub; "upd" is the last-updated time in UTC on 9 Oct; every repo was created on or after 1 Oct, most on 7–9 Oct)**

*Air track (34)*
| # | Project | One-line idea | Link | Upd |
|---|---|---|---|---|
| 1 | SAANS (School Air Action Notification System) | A deterministic rules engine sets the school's action tier for the day, in the principal's language | [LangerSword/saans](https://github.com/LangerSword/saans) | 8 Oct 22:40 |
| 2 | Khidki | "Open the classroom window at the right minute" (indoor/outdoor ventilation timing) | [bhavya-jpg/khidki](https://github.com/bhavya-jpg/khidki) | 8 Oct 11:34 |
| 3 | BreatheSafe | AQI forecast plus GO/CAUTION/NO-GO school advisories across India (Lambda, EventBridge, SNS) | [Manasa-L-Hegde/breathesafe_aqi_advisory-](https://github.com/Manasa-L-Hegde/breathesafe_aqi_advisory-) | 8 Oct 05:42 |
| 4 | School Air Alert | 6 PM forecast of next-day school-hours PM2.5 for Delhi; tells principals whether to move assembly and PE indoors (Hindi/English) | [Mayanknishad9/school-air-alert](https://github.com/Mayanknishad9/school-air-alert) | 9 Oct 07:29 |
| 5 | Kal Ki Hawa | ML forecast of tomorrow's air for Delhi schools | [KorraSanthosh/aws_weather_predictor](https://github.com/KorraSanthosh/aws_weather_predictor) | 9 Oct 06:48 |
| 6 | HawaHawai | School air-safety advisor for one Delhi-NCR school | [sayan1506/HawaHawai](https://github.com/sayan1506/HawaHawai) | 9 Oct 06:03 |
| 7 | SaansSafe | Air forecast turned into an assembly, PE and recess plan plus a parent notice (EN/HI) | [bled1908/SaansSafe](https://github.com/bled1908/SaansSafe) | 9 Oct 05:21 |
| 8 | SaansSaathi | Morning school-day plan (assembly indoors, PE at the cleanest hour, windows), principal approval, Hindi voice notes for parents | [Yashika2211/saans-saathi](https://github.com/Yashika2211/saans-saathi) (duplicate: [santhisathi](https://github.com/Yashika2211/santhisathi)) | 8 Oct 18:00 |
| 9 | Saans (yashyp12) | Hourly AQI forecast plus timetable gives per-activity actions for principals | [yashyp12/saans](https://github.com/yashyp12/saans) | 8 Oct 15:25 |
| 10 | ClearHour | "The cleanest hour of the school day for 1,110 Delhi schools"; 5:30 AM WhatsApp to principals | [Shreyash-Sachit-Sahu/ClearHour](https://github.com/Shreyash-Sachit-Sahu/ClearHour) | 8 Oct 12:07 |
| 11 | AirSafe | Personalised exposure insights for planned outdoor activities | [nithing007/AirSafe](https://github.com/nithing007/AirSafe) | 9 Oct 04:08 |
| 12 | Is it safe outside today? | Personalised meaning of AQI for Delhi NCR residents | [Shivapal460/AQI-SAFE-TODAY](https://github.com/Shivapal460/AQI-SAFE-TODAY) | 9 Oct 03:51 |
| 13 | Air Quality Advisor | See the Builder Center item above | [Abhinavgupta2404/aqiadvisor](https://github.com/Abhinavgupta2404/aqiadvisor) | 2 Oct |
| 14 | ALive | Personal PM2.5 "dosimeter" for Delhi with no hardware; prices each trip in inhaled smoke | [GC-WORK11/alive-mirror](https://github.com/GC-WORK11/alive-mirror) | 9 Oct 08:41 |
| 15 | Saans (smog dose for delivery riders) | Exposure for delivery riders on two-wheelers | [Goyamjain06/goyam_aws](https://github.com/Goyamjain06/goyam_aws) | 9 Oct 02:41 |
| 16 | VayuDrishti | Hyperlocal air-quality intelligence ("Why this wins" README) | [Anurag13075/Vayudrishti](https://github.com/Anurag13075/Vayudrishti) | 9 Oct 06:49 |
| 17 | ClearSky Intelligence | Smart-city urban air intelligence and decision support | [Ishaan-Chaturved1/clearsky-intelligence](https://github.com/Ishaan-Chaturved1/clearsky-intelligence) | 9 Oct 06:46 |
| 18 | better_AQI | Hyperlocal AQ, clean-commute planning and health advisories | [akshayaparida/better_AQI](https://github.com/akshayaparida/better_AQI) | 8 Oct 18:30 |
| 19 | AeroPulse India | "National Environmental Command Center" air telemetry platform | [Adithya-2007/AWS-Dummy](https://github.com/Adithya-2007/AWS-Dummy) | 8 Oct 18:06 |
| 20 | airsafe-environmental-hacks-2026 | Generic AI air-quality monitoring | [drishti1201/airsafe-environmental-hacks-2026](https://github.com/drishti1201/airsafe-environmental-hacks-2026) | 9 Oct 07:42 |
| 21 | BreatheRoute | Healthiest walking and cycling routes | [Universal-codeweb/BreatheRoute](https://github.com/Universal-codeweb/BreatheRoute) | 9 Oct 06:58 |
| 22 | EcoRoute AI | Route or departure time that minimises exposure (README does not name the event; "envh" repo, track text matched) | [Kishores57/envh](https://github.com/Kishores57/envh) | 8 Oct 16:58 |
| 23 | AERIS | FIRMS fires to smoke plume to exposure to action for authorities (Strands) | [sinhaaditya5/AERIS](https://github.com/sinhaaditya5/AERIS) | 9 Oct 06:22 |
| 24 | Whiff | When the smoke will reach you, with day planning (HI/EN) | [aashvi0722/Whiff](https://github.com/aashvi0722/Whiff) | 9 Oct 05:27 |
| 25 | Smoke Arrival | Forecasts *when* stubble smoke reaches a city, as a time | [areen-dev/smoke-arrival](https://github.com/areen-dev/smoke-arrival) | 8 Oct 19:46 |
| 26 | ParaliTrace | Where smoke goes in the next 48 h and which fields to stop first | [mehratanveer6/paralitrace](https://github.com/mehratanveer6/paralitrace) | 8 Oct 14:32 |
| 27 | StubbleWatch | FIRMS fires plus wind, giving smoke arrival in Delhi | [damnRITIJ/TrioBuilds](https://github.com/damnRITIJ/TrioBuilds) | 8 Oct 17:11 |
| 28 | clearsky (stubble) | Book straw pickup over WhatsApp to prevent burning | [sanskarjoshiii/clearsky](https://github.com/sanskarjoshiii/clearsky) | 9 Oct 05:27 |
| 29 | ParaliSetu | Turns stubble into farmer income | [Rishabhbansal005/ParaliSetu](https://github.com/Rishabhbansal005/ParaliSetu) | 9 Oct 07:48 |
| 30 | Parali Mitra | Farmer field check-up showing Sentinel-2 burn history and what burning costs (README does not name the event; track text matched) | [pankaj-cod/amazon_hackathon](https://github.com/pankaj-cod/amazon_hackathon) | 8 Oct 06:37 |
| 31 | HawaCommand | AI command centre that dispatches Delhi's anti-smog machines to hotspots and "proves every fix worked" | [shankywho/HawaCommand](https://github.com/shankywho/HawaCommand) | 9 Oct 04:44 |
| 32 | KilnWatch | Finds brick kilns around Delhi on Sentinel-2 and produces an inspection plan | [aryamanraj2/KilnWatch](https://github.com/aryamanraj2/KilnWatch) | 8 Oct 17:31 |
| 33 | Ground Truth | Which Delhi air-quality monitor readings can be trusted: each monitor checked hourly against its neighbours, its history and physics | [thegoodengineers/ground-truth](https://github.com/thegoodengineers/ground-truth) | 9 Oct 08:31 |
| 34 | AlgaeAir | Frontend for a microalgae bioreactor concept | [ayushagarwalhere/atmos](https://github.com/ayushagarwalhere/atmos) | 8 Oct 11:18 |

*Heat & Water track (53)*
| # | Project | One-line idea | Link | Upd |
|---|---|---|---|---|
| 35 | Waterlog Watch | Photo-verified flood map, route check and ward dashboard (Chennai) | [abinivesh-m/waterlog-watch](https://github.com/abinivesh-m/waterlog-watch) | 8 Oct 08:14 |
| 36 | FloodLens | Street-level flood-risk intelligence | [tanishk006/Floodlens](https://github.com/tanishk006/Floodlens) | 9 Oct 08:10 |
| 37 | BaarishSaathi | Mumbai waterlogging early warning and alternate routes | [HarshalChugwani2005/BaarishSaathi](https://github.com/HarshalChugwani2005/BaarishSaathi) | 9 Oct 07:54 |
| 38 | Nikasi | Go/caution/no-go for named Delhi underpasses in rain | [Vaidik-7781/nikasi](https://github.com/Vaidik-7781/nikasi) | 9 Oct 06:22 |
| 39 | Underpass Watch Delhi | Underpass flood early warning plus community status (solo) | [MonalikaDoda/Underpass-Watch-Delhi](https://github.com/MonalikaDoda/Underpass-Watch-Delhi) | 9 Oct 06:20 |
| 40 | Aquashield (anshu07) | Delhi underpasses: predict, verify, route, act | [anshu07-code/Aquashield](https://github.com/anshu07-code/Aquashield) | 8 Oct 17:21 |
| 41 | NirmalDhara | One camera network for flood depth from photos plus drain-waste tracking | [ravithejanaini/NirmalDhara](https://github.com/ravithejanaini/NirmalDhara) | 9 Oct 06:14 |
| 42 | FloodVision | Computer vision reads flood depth from reference objects (cones, tyres) and alerts above 30 cm | [Raghavpatil10/FloodVision_Environmental_Hacks](https://github.com/Raghavpatil10/FloodVision_Environmental_Hacks) | 9 Oct 05:43 |
| 43 | JalMarg (Sashang) | Urban flood-depth intelligence and monsoon navigation | [Sashang-debug/Jalmarg](https://github.com/Sashang-debug/Jalmarg) | 8 Oct 20:37 |
| 44 | JalMarg (triyanshag) | Agentic AI for waterlogging: verify, measure, predict, route | [triyanshag777/jalmarg](https://github.com/triyanshag777/jalmarg) | 8 Oct 18:20 |
| 45 | MonsoonRoute | Rain-aware route choice for Mumbai commuters | [0xshariq/monsoon-route](https://github.com/0xshariq/monsoon-route) | 8 Oct 20:33 |
| 46 | FloodGuard AI (repo) | Urban flood/waterlogging prediction, Next.js simulator (DTU) | [Rudraksh2996/FloodGuard-AI](https://github.com/Rudraksh2996/FloodGuard-AI) | 8 Oct 19:09 |
| 47 | FloodGuard AI (Builder Center post) | Per-location ML waterlogging risk (may be the same team as #46; not verified) | [post](https://builder.aws.com/post/3KQErOT95rN94BMZie1vdt2M18G_p/day-1-or-bharat-builds-aws-environmental-hacks) | 8 Oct |
| 48 | WaterLine | Urban monsoon telemetry and "submerged hazard memory" | [AnshuPriya-1/Waterline](https://github.com/AnshuPriya-1/Waterline) | 8 Oct 18:43 |
| 49 | AquaPin | Crowdsourced waterlogging severity pins | [rabbitc0der/aquapin](https://github.com/rabbitc0der/aquapin) | 8 Oct 17:01 |
| 50 | Enki | Citizen flood map for India | [HimanshuJha-2005/Enki](https://github.com/HimanshuJha-2005/Enki) | 8 Oct 17:40 |
| 51 | JalNet | Map-first water/flood observations with route warnings and rewards | [farhanakhtar0x66/jalnet](https://github.com/farhanakhtar0x66/jalnet) | 9 Oct 08:29 |
| 52 | 4clique | 3D waterlogging digital twin, Bengaluru ORR | [Reddawn1111/awsproj](https://github.com/Reddawn1111/awsproj) | 8 Oct 14:27 |
| 53 | CASCADE | Glacial-lake outburst flood telemetry and early warning | [suryaprasanthcse/CASCADE-GLOF-Telemetry](https://github.com/suryaprasanthcse/CASCADE-GLOF-Telemetry) | 8 Oct 18:53 |
| 54 | Flood/drought NGO alert SaaS | Detects flood/drought risk and alerts the nearest NGOs | [me-agrim-rehan/Wemakedevs-hackathon](https://github.com/me-agrim-rehan/Wemakedevs-hackathon) | 8 Oct 16:47 |
| 55 | ZeroGrid | Offline mesh disaster telemetry and rerouting | [hehemohit/Zero_Grid](https://github.com/hehemohit/Zero_Grid) | 8 Oct 01:55 |
| 56 | Chennai Unsaid | Area disclosure for renters: does it flood, how hot it runs | [tanishkabhatera-bit/chennai-unsaid](https://github.com/tanishkabhatera-bit/chennai-unsaid) | 8 Oct 13:28 |
| 57 | SiltProof | Tells a ward engineer how much of a drain-desilting bill to pay, with evidence | [Somsubhra-Nandi/siltproof](https://github.com/Somsubhra-Nandi/siltproof) | 9 Oct 06:36 |
| 58 | ClimateOps | Multi-hazard monitoring for floods, droughts and heatwaves | [officialshrutakirti94/ClimateOps](https://github.com/officialshrutakirti94/ClimateOps) | 9 Oct 04:38 |
| 59 | JalTaap | Heat, floods, drought, groundwater, tankers and leaks "on one desk" | [manish-yadav-iitg/jaltaap](https://github.com/manish-yadav-iitg/jaltaap) | 8 Oct 23:29 |
| 60 | Jal-Sanchar | Operational hydrology, street heat stress and fleet dispatch | [RajatRawal-06/AWS](https://github.com/RajatRawal-06/AWS) | 9 Oct 05:11 |
| 61 | Tript-Dhara | Municipal heat and water resilience platform | [shauryasharmathe3rd/AWS-EVMH](https://github.com/shauryasharmathe3rd/AWS-EVMH) | 9 Oct 07:24 |
| 62 | AquaGrid | Urban water and climate operations for municipalities and facilities | [piyush123710/AquaGrid-…](https://github.com/piyush123710/AquaGrid-Intelligent-Urban-Water-Climate-Operations-Platform) | 8 Oct 06:48 |
| 63 | JalSetu | Water-crisis "intelligent response" (live on Amplify) | [rpulijala18/jalsetu](https://github.com/rpulijala18/jalsetu) | 9 Oct 05:17 |
| 64 | AquaShield (AquaSentinels) | Decision layer for emergency water management | [Roshanambilwade/AquaShield](https://github.com/Roshanambilwade/AquaShield) | 9 Oct 05:12 |
| 65 | Project Bhumi (HWSI) | Prioritises heat-and-water resources for District Disaster Management Authorities | [my-project-repo/HWSI-…](https://github.com/my-project-repo/HWSI-Heat-Water-Stress-Decision-Support-System) | 9 Oct 07:17 |
| 66 | ShiftShield | "The heat alert that proves the rest happened" | [gufran-09/Shift-Shield](https://github.com/gufran-09/Shift-Shield) | 9 Oct 08:42 |
| 67 | Heat-safe shift planner | Construction supervisor's safe hours, with a Hindi voice note for the crew (Android) | [Mehulsri07/heat-shift-bot](https://github.com/Mehulsri07/heat-shift-bot) | 9 Oct 06:32 |
| 68 | ₹800 | Plans an outdoor worker's jobs around the heat without losing income (OR-Tools CP-SAT on Lambda, Hindi) | [himanshu748/rs800](https://github.com/himanshu748/rs800) | 9 Oct 05:45 |
| 69 | Chhaon | WBGT hour-by-hour crew plan, Hindi break announcements and a first-aid protocol | [souvikDevloper/chhaon](https://github.com/souvikDevloper/chhaon) | 9 Oct 03:31 |
| 70 | HeatShift | Personal heat risk and work/rest/hydration plan for gig and outdoor workers | [ansh-logics/Environmental-Hacks-Heatshift](https://github.com/ansh-logics/Environmental-Hacks-Heatshift) | 8 Oct 15:05 |
| 71 | HeatCredit | Heat-resilience decision engine for schools, hospitals and facilities, within a budget | [RishvinReddy/heatcredit-…](https://github.com/RishvinReddy/heatcredit-environmental-hacks-2026) | 9 Oct 04:19 |
| 72 | HEPo | Urban heat pockets from geotagged temperatures (PWA) | [Raone666/HEPo](https://github.com/Raone666/HEPo) | 8 Oct 17:28 |
| 73 | HeatRoute | Thermal-aware pedestrian routing | [matorverse/HeatRoute](https://github.com/matorverse/HeatRoute) | 8 Oct 18:18 |
| 74 | CHHAYA | Shade- and flood-aware pedestrian routing | [teamaekovera-glitch/chhaya](https://github.com/teamaekovera-glitch/chhaya) | 7 Oct 15:49 |
| 75 | Teesri Shikayat | Dirty-tap-water tripwire: three neighbour reports warn the area; only residents close the case | [aryangorde6/teesri-shikayat](https://github.com/aryangorde6/teesri-shikayat) | 9 Oct 08:00 |
| 76 | Outbreak Watch | Early warning for contaminated drinking water, Bengaluru | [prathignas/outbreak-watch-water_safety](https://github.com/prathignas/outbreak-watch-water_safety) | 9 Oct 07:22 |
| 77 | PaaniAlert | WhatsApp reports of unsafe water, clustered into boil-water warnings | [ruthvik418/paanialert](https://github.com/ruthvik418/paanialert) | 8 Oct 18:42 |
| 78 | Upstream | "Seismology for sewage": locates a sewage leak from when each home first sees dirty water | [qwertyuiopas17/gege](https://github.com/qwertyuiopas17/gege) | 9 Oct 07:58 |
| 79 | JalSakshi | Households confirm by Hindi phone check-in whether tap water came; repairs count only when they confirm | [Galabavamsi/jalsakshi](https://github.com/Galabavamsi/jalsakshi) | 8 Oct 22:59 |
| 80 | LeakLedger | Water-meter reconciliation and repair verification | [madhavkant29/LeakLedger](https://github.com/madhavkant29/LeakLedger) | 9 Oct 07:11 |
| 81 | TankSaathi | Heat-aware rooftop tank and leak warning for hostels and shared buildings | [navneet-cerecode/tanksaathi](https://github.com/navneet-cerecode/tanksaathi) | 8 Oct 13:09 |
| 82 | AquaAgent | Physics-grounded anomaly detection for hidden water loss | [aadesh2036/AquaAgent](https://github.com/aadesh2036/AquaAgent) | 8 Oct 16:06 |
| 83 | JalSanket | Evidence-first groundwater telemetry triage | [tauqxxr7/JalSanket](https://github.com/tauqxxr7/JalSanket) | 8 Oct 06:47 |
| 84 | Talaab | Per-pond "dry-by" countdowns and pumping flags from Sentinel-2 | [shloknarvekar/talaab](https://github.com/shloknarvekar/talaab) | 9 Oct 07:28 |
| 85 | Maharashtra drought water ops | Drought water-operations toolkit | [shrishshh/maharashtra-drought-water-ops](https://github.com/shrishshh/maharashtra-drought-water-ops) | 8 Oct 13:32 |
| 86 | Second Tap | Treated water from apartment STPs supplied to nearby construction sites | [RehaanDev/second-tap-…](https://github.com/RehaanDev/second-tap-env-hacks-track2-heat-water) | 8 Oct 17:01 |
| 87 | QuenchSip | Refill-station water planning for plastic-free events (track not stated) | [kavyan256/quenchsip](https://github.com/kavyan256/quenchsip) | 8 Oct 15:50 |

*Waste & Energy track (24)*
| # | Project | One-line idea | Link | Upd |
|---|---|---|---|---|
| 88 | Swachh.ai | Location-aware waste-disposal assistant with RAG over SWM 2016, E-Waste 2022 and Battery 2022 rules | [grvd5678/swachh-ai](https://github.com/grvd5678/swachh-ai) | 9 Oct 07:30 |
| 89 | SortSmart | Household "which bin" advisor (SAM) | [dcain2336/sortsmart](https://github.com/dcain2336/sortsmart) | 8 Oct 14:22 |
| 90 | CleanItUp | Mobile AI waste assistant | [mansingh-04/Environmental-Hacks](https://github.com/mansingh-04/Environmental-Hacks) | 8 Oct 20:33 |
| 91 | Indohood | Household segregation with green credits | [aakashshakya0001-png/Indohood](https://github.com/aakashshakya0001-png/Indohood) | 8 Oct 19:30 |
| 92 | BinGo | Community waste zones with a QR household ID scanned at the vehicle bay | [pradeep-kumarl/bingo](https://github.com/pradeep-kumarl/bingo) | 8 Oct 14:02 |
| 93 | EcoPulse | Community accountability and incentive platform | [GurukantPatil01/Enviormental_hacks](https://github.com/GurukantPatil01/Enviormental_hacks) | 8 Oct 20:34 |
| 94 | WasteWise | Waste project (README unreadable) | [Faizan-313/wastewise](https://github.com/Faizan-313/wastewise) | 8 Oct 10:23 |
| 95 | KabadiAI | Photograph e-waste to learn hazard, value and where to take it | [Kaltroniz/KabbadiAI](https://github.com/Kaltroniz/KabbadiAI) | 9 Oct 08:38 |
| 96 | RE:GENESIS | E-waste computer vision, disassembly plan and KMS-signed "second-life passports" | [mitra9917/ReGenesis](https://github.com/mitra9917/ReGenesis) | 9 Oct 06:36 |
| 97 | KabadiPlus v2 | E-waste circular decision and pickup (Bedrock Nova) | [ajayg10/scrapmitra](https://github.com/ajayg10/scrapmitra) | 8 Oct 20:46 |
| 98 | KabadiConnect | "Uber-style" scrap pickup with an AI price estimate | [ADITYASINGH1206/Kabaddi-connect](https://github.com/ADITYASINGH1206/Kabaddi-connect) | 8 Oct 17:46 |
| 99 | Environmental Recovery Platform | Routes household recyclables into the kabadiwala network | [KarthikeyaPila/Environmental-Hacks](https://github.com/KarthikeyaPila/Environmental-Hacks) | 8 Oct 19:51 |
| 100 | E-waste reverse-logistics engine | E-waste reverse logistics | [vishal-kumar2/matrix01](https://github.com/vishal-kumar2/matrix01) | 8 Oct 10:29 |
| 101 | ReLoop | Photograph a device, get a value estimate, a resell/repair/recycle decision, pickup and points (README does not name the event; track text matched) | [akarshjain05/reloop](https://github.com/akarshjain05/reloop) | 8 Oct 06:53 |
| 102 | AnnaSetu | Routes FPO produce (sell, process, donate, compost) to avoid food waste | [Lakshya1901/aws](https://github.com/Lakshya1901/aws) | 8 Oct 11:00 |
| 103 | GhostPipe | Detects fly-ash diversion (NTPC Dadri to Yamuna) and subsidy fraud | [Chirragchhabria/ghostpipe](https://github.com/Chirragchhabria/ghostpipe) | 8 Oct 19:52 |
| 104 | ReForge | Cardboard measurements to a validated cutting plan (upcycling) | [SwarnavaItIs/ReForge_Environmental_Hacks](https://github.com/SwarnavaItIs/ReForge_Environmental_Hacks) | 9 Oct 08:27 |
| 105 | SunSense | 3D globe rooftop solar potential, PM Surya Ghar subsidy and payback | [sagnikvolt/SunSense](https://github.com/sagnikvolt/SunSense) | 9 Oct 08:00 |
| 106 | SolarScope | Segments usable roof from obstructions on Indian rooftops in aerial images | [Pai05/solarscope](https://github.com/Pai05/solarscope) | 9 Oct 06:26 |
| 107 | RoofRight | Electricity bill to a solar application pack for housing societies | [rohanjain1648/RoofRight](https://github.com/rohanjain1648/RoofRight) | 8 Oct 19:58 |
| 108 | SolarSaathi | Neutral rooftop-solar AI advisor (README does not name the event; track text matched) | [ManikantaArigela/aws-hackthon](https://github.com/ManikantaArigela/aws-hackthon) | 8 Oct 17:15 |
| 109 | SolNet AI | Peer-to-peer rooftop-solar router and virtual microgrid simulation (README does not name the event; track text matched) | [atharvrajgite-oss/evs](https://github.com/atharvrajgite-oss/evs) | 8 Oct 20:03 |
| 110 | Pravaah | Water- and carbon-aware scheduling of AI workloads, with savings receipts | [Dutta-06/bharatbuilds](https://github.com/Dutta-06/bharatbuilds) | 8 Oct 18:57 |
| 111 | grid-nudge | No README; the name suggests energy nudges | [CSNEHA20/grid-nudge](https://github.com/CSNEHA20/grid-nudge) | 8 Oct 19:45 |

*Event-named placeholders with no idea visible yet (not counted):* [newone-ss/Amazon_Environmental_Hacks](https://github.com/newone-ss/Amazon_Environmental_Hacks), [ayushtomar236/EnvironmentalHacks](https://github.com/ayushtomar236/EnvironmentalHacks), [23f2001033/Environmental-Hacks](https://github.com/23f2001033/Environmental-Hacks), [TeenaBaskar2007/Environmental-Hacks](https://github.com/TeenaBaskar2007/Environmental-Hacks), [charan22-eng/Bharat-Builds-Tour](https://github.com/charan22-eng/Bharat-Builds-Tour), [Yashwitha-valmiki/Enviromental_Hacks](https://github.com/Yashwitha-valmiki/Enviromental_Hacks), [AWS-env/environmental-hacks](https://github.com/AWS-env/environmental-hacks) (idea "still being decided"), [ancientdev0x/aws-env](https://github.com/ancientdev0x/aws-env), [Aryan107rn/We_make_dev_hackathon](https://github.com/Aryan107rn/We_make_dev_hackathon), [Goyamjain06/Edge_testcase](https://github.com/Goyamjain06/Edge_testcase) (placeholder for #15).

**Naming convergence (FACT, from the list above):** "Saans" ×5 (#1, #7, #8, #9, #15). Jal- ×8 (JalMarg ×2, JalTaap, JalSetu, JalSakshi, JalSanket, Jal-Sanchar, JalNet). Aqua- ×6 (Aquashield ×2, AquaPin, AquaGrid, AquaAgent, plus the JalSetu/AquaShield family). Parali- ×3. Kabadi- ×4. FloodGuard ×2. ClearSky ×2. AirSafe ×2. Hawa- ×2.

### Inferences
- INFERENCE: The public GitHub sample over-represents teams that are organised and spec-driven: many READMEs carry CLAUDE.md files, phase plans and "verify/prove" framing. Median teams that start late on Sat/Sun, or keep repositories private, are under-sampled. The true field is probably more generic than this sample.
- INFERENCE (field size): at First Commit's 8.6% registration-to-submission ratio, 8,481 registrations imply **about 730 submissions** (plausible range 600–900; registrations may still rise). The 111 visible projects are roughly 15% of that.
- INFERENCE (track split): the visible sample is H&W 48% / Air 31% / W&E 22%, against the 05-map assumption of 35/35/30. **Heat & Water, not Air, looks like the most crowded track**, driven by floods. W&E is the least crowded.
- INFERENCE: Scaling the sample to about 730 projects (×6.5, a crude estimate) gives roughly 150 flood/waterlogging projects, about 65 school-air planners, about 50 stubble/smoke projects, about 45 e-waste/kabadi apps, about 33 worker-heat planners and about 26 pre-install solar tools.

### Gaps
- LinkedIn, X/Twitter, Reddit and YouTube were **not effectively searched**. LinkedIn and X need sign-in, which this research does not do, and web search returned no indexed posts for "Environmental Hacks" from Oct 2026 (search engines lag several days). Medium, Hashnode and dev.to returned no hits through web search.
- Builder Center has no keyword search the browser could use (the `/search?q=` route returns 404). Topic pages `#environmentalhacks` and `#bharatbuilds` do not exist. Only the WeMakeDevs space feed and the `#hackathon`/`#sustainability` topics were scanned, so other Builder Center articles may exist.
- GitHub logged-out search caps results and can miss repositories that do not use the keywords. Private repositories are invisible.
- Repository creation dates were not captured individually: the queries filtered on creation ≥ 1 Oct or ≥ 7 Oct, and the table shows last-updated times.
- I did not verify whether thegoodengineers/ground-truth belongs to our own team. Nothing in /home/claude/docs references it.

## Q2. WeMakeDevs blog and tour pages: problem statements, workshops and seeded ideas

### Takeaway
The organisers seeded six concrete example ideas, and **the field copied the school-air one heavily: 10 of 34 visible Air projects are versions of "tell the principal whether to move PE and assembly indoors."** The flood-route example (seed #4) is also heavily followed. Seeds #3 (tanker predictor) and #5 (bin-photo checker with a building score) are followed far less than expected.

### Cited Findings
- FACT: The tracks and example problems are: Air (AQI, exposure, stubble burning, indoor air, school safety on bad days); Heat & Water (heatwaves, floods, monsoon waterlogging, droughts, tankers, leaks, groundwater); Waste & Energy (segregation, recycling, e-waste, informal recyclers, rooftop solar, EV nudges, public transport). The page says these are "a place to start, not a list to pick from." — [Event page](https://www.wemakedevs.org/aws/env)
- FACT: The judging criteria are Idea & Impact ("A small problem solved well beats a big one solved vaguely"), Built on AWS (mandatory for prizes), Design & usability, Execution ("One feature that runs beats five that almost do") and a 3-minute demo video. There is no live demo, and each track is judged separately. — [Event page](https://www.wemakedevs.org/aws/env)
- FACT: Prizes are ₹2,00,000 plus $2,000 in credits per track winner, $1,000 in credits for each of the top 4 runners-up, AirPods for the top 5 blogs, and an Amazon fast-track for the top 10 students. — [Event page](https://www.wemakedevs.org/aws/env)
- FACT: The six seeded example ideas from the "Announcing Environmental Hacks" post (29 Sep 2026) are:
  1. A morning message for one school, combining readings and forecast, telling the principal whether PE and assembly should move indoors.
  2. An exposure planner for outdoor workers such as delivery riders, giving the cleanest hours on their usual route.
  3. A tanker predictor for one housing society, from logged deliveries.
  4. A monsoon commute helper using resident reports of which routes flood first.
  5. A segregation checker: a bin photo is read by a model, a person confirms it, and the building tracks its score for a month.
  6. A rooftop-solar payback estimator using irradiance data for a pincode.

  — [WeMakeDevs blog](https://www.wemakedevs.org/blogs/announcing-environmental-hacks)
- FACT: The same post calls map dashboards weak ("a map mostly tells people something they can already sense"). It asks what someone should do differently, lists datasets (CPCB, OpenAQ, NASA FIRMS, IMD, India-WRIS, data.gov.in, and Sentinel-2, Landsat, GOES and NASA POWER on the AWS Open Data registry), and stresses honesty about data freshness. — [WeMakeDevs blog](https://www.wemakedevs.org/blogs/announcing-environmental-hacks)
- FACT: Kunal Kushwaha's announcement adds three more seed phrases: "tracking air quality in your city, cutting food waste on campus, or helping people use less energy at home." — [Builder Center post](https://builder.aws.com/post/3KGj9FkeKgzYIxKTNs7AFg4EcpU_p/environmental-hacks-the-second-bharat-builds-hackathon)
- FACT: The schedule page names no workshops beyond the DTU day. The only named workshop is Strands Agents "build your first agent." — [Schedule](https://www.wemakedevs.org/aws/env/schedule); [Delhi day blog](https://www.wemakedevs.org/blogs/what-is-happening-in-delhi-on-10-october)
- FACT: The two official build guides use non-environmental examples: CitationPulse (serverless) and SchemeProof (open-source stack with deterministic rules plus a local LLM summary). — [Serverless guide](https://www.wemakedevs.org/blogs/how-to-build-a-live-data-project-on-the-aws-serverless-stack); [Open-source guide](https://www.wemakedevs.org/blogs/how-to-build-a-real-data-ai-project-on-the-aws-open-source-stack)

### Inferences
- INFERENCE: Seed take-up in the visible sample:
  - Seed 1 (school air): 10 projects.
  - Seed 2 (outdoor-worker exposure): 3–4 projects (#14, #15, #21, #22).
  - Seed 3 (tanker): 0 direct projects. JalTaap and the Maharashtra drought ops repo touch tankers.
  - Seed 4 (flood commute from reports): at least 8 projects.
  - Seed 5 (bin photo plus building score): 4 projects.
  - Seed 6 (solar payback): 4 projects.
- INFERENCE: The "deterministic engine plus LLM explains" pattern from the SchemeProof guide is visible in many READMEs ("agents explain it and never override", "deterministic rules engine"). The architecture pattern is therefore no longer a differentiator either.
- INFERENCE: Judges will see many entries that follow the blog's advice word for word: a specific decider, an action, and Hindi output. Following that advice is now table stakes.

### Gaps
- The mentors page and the community-partners page were not read. Any problem statements from community partners are unknown.

## Q3. Comparable events (2024–2026): what student teams repeatedly build

### Takeaway
Evidence here is thinner, but it points the same way. Devpost keyword volumes are highest for waste classification, AQI and flood alerts, and low for heat and rooftop solar. Duplicate names are common: "FloodSense" appears on Devpost as well as twice at First Commit. Ideas we considered novel, such as heat practice plans with a compliance log and rooftop-solar payback under local rules, already exist on Devpost.

### Cited Findings
- FACT (Devpost full-text search result counts, all years, keyword matches, so noisy):
  - "waste classification": 1,142 — [Devpost](https://devpost.com/software/search?query=waste+classification)
  - "AQI": 578 — [Devpost](https://devpost.com/software/search?query=AQI)
  - "flood alert": 456 — [Devpost](https://devpost.com/software/search?query=flood+alert)
  - "carbon footprint tracker": 371 — [Devpost](https://devpost.com/software/search?query=carbon+footprint+tracker)
  - "rooftop solar": 147 — [Devpost](https://devpost.com/software/search?query=rooftop+solar)
  - "heatwave": 144 — [Devpost](https://devpost.com/software/search?query=heatwave)
  - "stubble burning": 35 — [Devpost](https://devpost.com/software/search?query=stubble+burning)
- FACT: Devpost examples that mirror ideas live in this event:
  - Flagline: heat forecasts and meter readings turned into practice plans, recheck reminders, athlete check-ins and a compliance log for Texas UIL. — [Devpost](https://devpost.com/software/search?query=AQI)
  - HeatSafe: cooler walking routes. — [Devpost](https://devpost.com/software/search?query=AQI)
  - Adem: next-day heat stress ranking of Singapore HDB blocks for senior outreach. — [Devpost](https://devpost.com/software/search?query=heatwave)
  - Sunscore: BC 2026 rooftop-solar payback. — [Devpost](https://devpost.com/software/search?query=rooftop+solar)
  - Project Parali, and StubbleX listed 4 times: stubble marketplaces. — [Devpost](https://devpost.com/software/search?query=stubble+burning)
  - FloodSense (listed twice) and Saakshi (farmer flood warnings with photo damage evidence). — [Devpost](https://devpost.com/software/search?query=flood+alert)
  - BinMe, AI WasteWise and Trash Royale (waste classification and sorting games). — [Devpost](https://devpost.com/software/search?query=waste+classification); [Devpost](https://devpost.com/software/search?query=carbon+footprint+tracker)
- FACT: SIH 2025 had 2,877+ problem statements from 100+ organisations across seven themes, including Sustainability and Social Good. — [dev.to SIH 2025 guide](https://dev.to/avinash201199/smart-india-hackathon-sih-2025-828) (secondary source; official list at sih.gov.in not accessed)
- FACT (secondary source, unofficial list): SIH 2024 Clean & Green Technology statements included satellite AQ downscaling with AI/ML, solar capture and tracking, agri water footprints, GOBARdhan biogas kits and controls, a BRSR platform for India Post, green hydrogen, and waste segregation and sanitation with IoT. — [Engineers Planet](https://engineersplanet.com/top-10-problem-statements-with-solution-ideas-for-smart-india-hackathon-2024-clean-green-technology/)
- FACT: The Amity "Sustainovation 2025" hackathon (3–5 Sep 2025) had 30 teams on clean water, clean energy and healthy soil; winners are not named. — [EducationWorld](https://educationworld.in/amity-university-hosts-sustainovation-2025-hackathon-on-sustainable-innovation/)
- FACT: The MoEFCC Eco-Creativity & Innovation Hackathon (Dec 2024) had 35 projects from 14 states. One was a solar model to protect people from air pollution; winners are not named. — [NewsOnAir](https://www.newsonair.gov.in/eco-creativity-and-innovation-hackathon-environment-secy-confers-awards-to-students-for-innovative-projects)
- FACT (older context, 2023, outside the date range): in the Tech To The Rescue × AWS Air Quality Hackathon (170+ teams, 33 solutions), the winners were a lung-damage visualiser and game, a sensor-data chatbot with memes and legislation search, and a Bedrock data-ingestion tool. Common entries were dashboards, chatbots and awareness games. — [Tech To The Rescue](https://techtotherescue.org/news/meet-the-winners-of-the-air-quality-hackathon)

### Inferences
- INFERENCE: Across comparable events the recurring student builds are: waste photo classifiers and sorting games, AQI dashboards and "is it safe" advisors, flood alert maps, carbon-footprint trackers, stubble marketplaces and solar calculators. Heat-worker scheduling and water-supply verification are comparatively rare on Devpost but are clustering in this event because of the seeds and the Indian context.

### Gaps
- No primary list of SIH 2024 or 2025 environment winners was found within the timebox; college achievement pages are scattered. The official sih.gov.in problem-statement files were not accessed.
- Devpost counts are full-text keyword hits across all years, not 2025–26 gallery counts. No specific 2025–26 Devpost climate hackathon gallery was enumerated.

## Q4. Environmental entries among First Commit's 1,180 projects

### Takeaway
I pulled all 1,180 titles from the public API. Roughly 35–45 are environmental (about 3–4%). They cluster in food waste (7), energy and grid (about 9), waste platforms (6), and floods and climate hazards (8). There is only **1** air-quality entry and **0** heat entries. None placed.

### Cited Findings
- FACT: The API returns all 1,180 First Commit projects (title, track, GitHub, deployed link, YouTube) in one response. — [API /hackathons/first-commit/projects](https://wemakedevs-server.onrender.com/hackathons/first-commit/projects); [gallery](https://www.wemakedevs.org/aws/first-commit/projects/all)
- FACT (classified by title keywords, then by hand; GitHub slugs in brackets):
  - **Food waste and surplus (7):** AWS Smart Food Waste Management (hariombhu/AWS_SMART_FOOD_WASTE_MANAGEMENT); Waste Food Management System (keshav-dev07); SmartPantry (Ajayrx/awspantry); UseItUp (abhranshu/Bharat-Builds-); FoodLoop (lavanyakarna/foodloop); SurplusLink (35250/SurplusLink); sparrow food redistribution (keanesc).
  - **Waste and circular (6–7):** Chokho AI; TrashTag Environmental Recovery (Vivek1035/TrashTag); Waste2Value AI; Sustainify AI eco-disposal scanner (Mayank-Rana1/Sustainify); Kabad Sathi (Swamiviresh/Kabad-Sathi); DeadStock Exchange (industrial surplus to raw material); CivicFlow "Cleaner Cities" (unclear).
  - **Floods and climate hazards (8):** FloodRoute; FloodSense ×2 (Aayush2883, Yug21x); ResQNet flood coordination; NER Landslide Guard; LandslideGuard AI; VayuDrishti cyclone detection from satellite; HYRA climate-hazard risk forecasting. There are also about 7 generic disaster-response platforms (Aegis, Sahaay, DRR, Rescue-Link, RescueGrid, SETU crisis grid, VANNATE).
  - **Energy and grid (about 9):** SolarLens quote checker; RoofGrid (unverified, possibly solar); SmartCharge grid-aware EV charging; PulseGrid microgrid load shedding; EnerFabric DER orchestration; GridFlex smart buildings; polar-station energy management; Tripwire electricity theft; Thermion data-centre cooling.
  - **Green cloud (2):** EcoInference Gateway; ecocloud-sentinel.
  - **Air (1):** Vayu AI satellite–ground fusion. **Geospatial (1):** Terra (satellite analysis from natural-language questions).
  - **Weather and agri-climate:** Weather Buddy; GramSankalpa. There are also about 12 agriculture apps (crop advisory, mandi prices, crop insurance, cold storage).
  - **Heat:** none. **Drinking water and leaks:** none identifiable.

  — [API](https://wemakedevs-server.onrender.com/hackathons/first-commit/projects)
- FACT: None of these placed. The winners were Suraksha, Beacon Night Shift and CampusEvac; the runners-up were Magpie, FreshTrace, Expressive Captions and Factcade. — [Recap](https://www.wemakedevs.org/blogs/first-commit-hackathon-recap-and-whats-next)

### Inferences
- INFERENCE: Name collisions carried over: FloodSense ×2 at First Commit, and FloodGuard, VayuDrishti and Sustainify/Kabad repeat in Environmental Hacks. At least one author returned with a reworked idea: "VayuDrishti" was the First Commit cyclone project, and an unrelated team (Anurag13075, who also built Fasal Rakshak at First Commit) now uses that name for Air.
- INFERENCE: First Commit's open theme under-predicted the heat and water-supply clusters, which are large now. Theme seeding (Q2) matters more than past behaviour.

### Gaps
- Classification is title-based. About 10 ambiguous titles (RoofGrid, GREEN-ROOM, GreenPhoenix, CampusCycle, hydroKernel, CivicFlow and others) were not checked against their repositories.

## Q5. Evidence-based overlap matrix

### Takeaway
Crowded, by evidence:
- Flood and waterlogging maps, routes and photo depth (H&W).
- School air-quality planners for principals (Air).
- Stubble-smoke arrival and parali marketplaces (Air).
- Multi-hazard "command desks" (H&W).
- E-waste and kabadi photo-to-pickup apps (W&E).

Newly contested, against our prediction: worker heat/WBGT shift planners (5), cleanest-hour school planning, drinking-water contamination crowd alerts (4), and water-supply/leak verification (4).

Still rare (0 found): tanker delivery and price verification, rooftop-solar **post-install** performance, SWM 2026 bulk-generator compliance, time-of-day tariff load shifting, EV/public-transport nudges, and informal-recycler (picker) price transparency.

### Cited Findings
#### Matrix
Counts come from the 111-project live sample (Q1). FC = First Commit (Q4). Per-project links are in Q1 by row number. The tier is INFERENCE, based on sample share and the organisers' seeding.

| Cluster | Track | Live count (share of 111) | FC count | Comparable-event signal | Seeded? | Tier | Evidence (row #) | What a differentiated version would need |
|---|---|---:|---:|---|---|---|---|---|
| Flood/waterlogging: crowd map, photo depth CV, route check, prediction | H&W | **18** (16%); 23 with GLOF, NGO alert, mesh, disclosure, desilting | 4 (+4 hazard) | Devpost "flood alert" 456; FloodSense duplicates | Yes (#4) | **Crowded** | 35–57 | Avoid, unless the user is not a commuter and the output is a payment or contract decision (e.g. SiltProof's bill verification, #57) |
| School air plan for the principal (PE/assembly/windows/cleanest hour) | Air | **10** (9%; 29% of Air) | 0 | (none comparable) | Yes (#1) | **Crowded** | 1–10 | Avoid. Several already have timetable, WhatsApp, Hindi and approval steps |
| Stubble fire to smoke arrival / plume | Air | **5** | 0 | Devpost "stubble" 35 | Track list | **Crowded** (for this niche) | 23–27 | Avoid |
| Parali/stubble farmer side (straw pickup, marketplace, burn history) | Air | **3** | 0 | StubbleX ×4, Project Parali on Devpost | Track list | Moderate | 28–30 | Baler-operator scheduling with verified pickup, not a marketplace |
| Personal "is it safe outside" / AQI advisor | Air | **5** | 0 | Devpost AQI 578; TTTR winners | Kunal seed | Crowded (generic) | 11–15 | Avoid; dosimeter or delivery-rider angles are already taken |
| AQI dashboard / "command centre" / hyperlocal intelligence | Air | **5** | 1 (Vayu AI) | TTTR 2023 dashboards | Blog calls maps weak | Crowded, weak | 16–20 | Avoid |
| Clean-air routing / departure timing | Air | **2** (+1 within better_AQI) | 0 | — | Yes (#2) | Moderate | 21–22, 18 | — |
| Municipal enforcement (anti-smog dispatch, kilns) | Air | **2** | 0 | — | No | Moderate | 31–32 | Verify enforcement outcomes against the data trust layer |
| Sensor data trust (which monitors to believe) | Air | **1** | 0 | — | No | Rare | 33 | Already taken by Ground Truth |
| Multi-hazard heat/water "one desk" platforms | H&W | **8** (7%) | ~7 disaster platforms | — | No | **Crowded, weak** | 58–65 | Avoid; this is the "big problem solved vaguely" judges warn about |
| Worker heat: WBGT / work–rest shift planning | H&W | **5** (4.5%) | 0 | Devpost Flagline (practice plans plus compliance log) | Track list ("heatwaves") | **Moderate, newly contested** (05 map had it as whitespace) | 66–70 | Must beat Chhaon (WBGT, Hindi breaks, first aid), ShiftShield ("proves the rest happened") and ₹800 (income-aware OR-Tools) |
| Facility/municipal heat prioritisation, heat pockets, shade routes | H&W | **4** | 0 | Devpost Adem, HeatGuard, HeatSafe | No | Moderate | 71–74 | — |
| Drinking-water contamination crowd alerts | H&W | **4** | 0 | — | No | Moderate | 75–78 | — |
| Water supply / leak / NRW verification | H&W | **4** | 0 | — | Track list ("leaks") | Moderate | 79–82 | LeakLedger and JalSakshi already do the "verify the repair" loop |
| Groundwater / drought / ponds | H&W | **3** | 0 | — | Track list | Moderate–low | 83–85 | — |
| **Tanker delivery: booking, prediction, volume/price verification** | H&W | **0** (only mentioned inside JalTaap, #59) | 0 | — | Yes (#3), not taken up | **Rare** | — | Still open: verify delivered volume and price per society |
| Water reuse (STP to construction, refill events) | H&W | **2** | 0 | — | No | Rare | 86–87 | — |
| Household segregation advisor / "which bin" / credits | W&E | **4** (+BinGo, EcoPulse, WasteWise = 7) | 6–7 waste platforms | Devpost "waste classification" 1,142 | Yes (#5) | **Crowded** (generic) | 88–94 | Avoid at household level |
| E-waste / kabadi photo to value to pickup marketplace | W&E | **7** (6%; 29% of W&E) | 1 (Kabad Sathi) | — | Track list | **Crowded** | 95–101 | Picker-side price receipts, or authorised-recycler certificates for institutions |
| Food waste | W&E | **1** | **7** | Devpost Gro-Sential and similar | Kunal seed ("food waste on campus") | Low now (was crowded at FC) | 102 | — |
| Industrial waste compliance (fly ash) | W&E | **1** | 0 | — | No | Rare | 103 | — |
| Rooftop solar **pre-install** (potential, subsidy, payback, application) | W&E | **4** (+SolNet P2P) | 1–2 (SolarLens, RoofGrid?) | Devpost "rooftop solar" 147; Sunscore | Yes (#6) | Moderate | 105–109 | Avoid pre-install calculators |
| **Rooftop solar post-install performance / maintenance** | W&E | **0** | 0 (SolarLens is pre-install) | — | No | **Rare** | — | Expected vs actual generation, diagnosis, vendor action, verified fix |
| Green compute / carbon-aware scheduling | W&E | **1** | 2 | Devpost GridShift | No | Rare (off-theme risk) | 110 | — |
| **EV / public-transport nudges, ToD tariff load shifting** | W&E | **0–1** (grid-nudge, #111, unknown) | 1 (SmartCharge) | Devpost carbon trackers 371 | Track list | **Rare** | 111 | An institutional decider, e.g. a hostel or RWA shifting loads to ToD windows, with bill-verified savings |
| **SWM 2026 bulk-generator compliance (campus/RWA)** | W&E | **0** (Swachh.ai covers household rules; BinGo covers community zones) | 0 | SIH 2024 waste segregation PS | No | **Rare** | — | A compliance loop with an auditable output |
| **Informal recycler / picker price transparency** | W&E | **0** (all kabadi apps are citizen-side) | 0 | — | Track list ("informal recyclers") | **Rare** | — | Receipts and prices for pickers, not the household |

### Inferences
- INFERENCE (the 05 map versus the evidence):
  - Confirmed crowded: flood alerts, school AQI and the waste classifier (though fewer classifiers than predicted).
  - **Under-predicted:** multi-hazard platforms (8), the stubble/smoke niche (8 in total), e-waste/kabadi (7), drinking-water quality (4), and worker-heat scheduling (5, predicted ≤1).
  - **Over-predicted:** generic carbon trackers (0 seen), EV finders (0), food waste (1), indoor-air IoT (1 concept), AQI-forecasting ML as a standalone (absorbed into the school apps).
  - **Still whitespace:** solar post-install; tanker verification; SWM bulk-generator compliance; ToD load shifting; picker-side pricing; EV/transit nudges.
- INFERENCE: Patterns 1–4 of the 05 map ("information beats intervention", "citizen user", "AI as a chat skin", "no verification") **no longer describe the visible strong tail**. Many repos now name a decider (principal, supervisor, ward engineer, caretaker) and add a verification loop: ShiftShield, HawaCommand, LeakLedger, JalSakshi, Teesri Shikayat, SiltProof and GhostPipe. A specific decider, an action and a verification step are now the expected baseline for top entries. Differentiation has to come from the **choice of problem and decider** (still-rare clusters) and the quality of execution, not from that framing.
- INFERENCE: W&E is the least crowded track (22% of the visible sample), and its most-seeded subclusters (bin checker, solar payback) drew moderate numbers. A rare-cluster W&E entry likely faces the weakest direct competition.
- HYPOTHESIS: The number of school-air entries will grow after the DTU day (Delhi, smog season, 1,000 attendees). The final field may hold 50+ school-air projects.

### Gaps
- Counts are a snapshot taken about 2 days before submission, from public repositories only. Final submissions will differ, and the API at `/hackathons/env/projects` can confirm them after publication (after the event).
- Track labels for #22, #30, #101, #108, #109 and #111 are inferred from README track text, not an explicit event mention. #47 may duplicate #46.
