# Bijli Budget: competitive landscape and technical feasibility audit (household free-unit "cliff" budget + weather-normalised savings verification)

Researched Fri 9 Oct 2026, ~22:00–24:00 IST. Labels: **FACT** (sourced), **INFERENCE** (reasoned from sourced facts), **HYPOTHESIS** (untested). Builds on, and does not repeat, P-01/P-02 (concepts_personal_household.md), M-01/M-02 (concepts_mechanism_first.md), C-11/C-12 (concepts_community_institutional.md) and data_access.md in `/home/claude/research_notes/Environmental Hacks concept reset/`.

**Bottom line up front.**
- **Real cliffs exist, mostly in summer.** One unit over the threshold costs hundreds of rupees in Telangana, Karnataka, Punjab, Tamil Nadu, Kerala and Delhi. Delhi zero-bill households fell from 43.9 lakh in February 2025 to 18.3 lakh in July 2025.
- **No Indian DISCOM or smart-meter app found warns about, or projects against, a free-unit threshold.**
- **But the parts are already common hackathon builds:**
  - meter or bill photo → OCR
  - free-unit-aware bill calculator
  - an ML next-bill prediction that uses temperature

  At least one public repo built in the last two weeks (SmartBill, BESCOM) does all three.
- **What has no Indian consumer equivalent:**
  - weather-normalised verification of savings, with an honest uncertainty band
  - a probability of crossing the cliff, turned into a daily unit budget
- **These are the only defensible novelty. Both are statistically fragile on 12 monthly bills, and weakest in October.**

---

## Q1. Free-unit / subsidy rules as of Oct 2026: threshold, cycle, cliff vs marginal, beneficiaries

### Takeaway
**True cliffs, where one unit over the line makes the whole bill (or a large chunk) payable:**
- Telangana: >200 units/month → full bill.
- Karnataka: >200 → full bill; within 200, only units above the household's entitlement are charged.
- Punjab: >300/month, i.e. >600 per two-month bill → full bill.
- Tamil Nadu (new from 10 May 2026): above 500 units per two-month bill, free units drop from 200 to 100 and higher slabs apply → about ₹478 more for one extra unit.
- Kerala: above 250 units/month, every unit is billed at the higher non-telescopic rate → about ₹237 more.
- Madhya Pradesh: the subsidy is lost above 150 units.
- Delhi: the zero bill is lost at 201 units. The 50% subsidy (cap ₹800) then applies, so the jump is a few hundred rupees; the exact amount at 201 units is unconfirmed.

**Marginal schemes (no cliff):** Rajasthan (only excess units billed) and, apparently, Bihar (125 units deducted from the bill). Jharkhand's treatment above 200 units is unconfirmed.

### Cited Findings
**Delhi**
- FACT: Current structure as of 21 Aug 2026: up to 200 units/month free; 201–400 units get a 50% subsidy capped at ₹800. The government is "considering" an opt-out option and annual registration. Over 73 lakh consumers, 84.1% domestic. Subsidy allocation ₹4,037.63 cr (to Feb 2026); FY27 budget ₹3,500 cr. — [ThePrint/PTI, 21 Aug 2026](https://theprint.in/india/delhi-govt-considers-giving-power-consumers-option-to-opt-out-of-subsidy/3021878/)
- FACT: Tata Power-DDL's billing FAQ says that up to 200 units "subsidy equals the entire current month's bill amount"; for 201–400 units the subsidy is "up to Rs 800 per month"; none above 400. It cites GoNCTD order F11(111)/2012/Power/Vol-III/1417-1427 of 20.04.20. — [TPDDL Billing FAQs, Jan 2024](https://www.tatapower-ddl.com/Editor_UploadedDocuments/Content/FAQs_BIlling_Jan'24.pdf)
- FACT: Slabs are pro-rated by billing-period length: slab = days between readings ÷ days in month (e.g. a period of 02.09–02.10 gives a factor of about 1.0311). The 200-unit line therefore moves with the length of the cycle. — [TPDDL Billing FAQs](https://www.tatapower-ddl.com/Editor_UploadedDocuments/Content/FAQs_BIlling_Jan'24.pdf)
- FACT: Tariff is ₹3.00/unit for 0–200 and ₹4.50 for 201–400 (DERC order effective 1 Aug 2024). Fixed charge is ₹20/kW up to 2 kW. The subsidy is opt-in. The same article contradicts itself on how the 50% is computed (its 201-unit row, ₹800 vs ₹850 cap). — [Housing.com, updated 16 Oct 2025](https://housing.com/news/electricity-rates-in-delhi/)
- FACT: The CM's own examples when the 2019 scheme launched:
  - 200 units: ₹622 → ₹0
  - 250 units: ₹800 → ₹252
  - 300 units: ₹971 → ₹526
  - 400 units: ₹1,320 → ₹1,075

  No 201-unit example was given. — [The Quint, 1 Aug 2019](https://www.thequint.com/news/india/arvind-kejriwal-delhi-electricity-power-200-units)
- FACT (conflicting description): Citizen Matters describes the 201–400 benefit as a flat "Rs 800 off", not 50%. — [Citizen Matters, 31 Jan 2020](https://citizenmatters.in/delhi-elections-aap-report-card-electricity/)
- FACT: Seasonal swing in zero bills in 2025:

  | Month | Zero bills |
  |---|---|
  | Feb | 43,86,631 |
  | Apr | 36,95,975 |
  | May | 24,83,959 |
  | Jul | 18,26,223 |
  | Sep | 21,95,989 |
  | Oct | 26,59,447 |

  October 2025 had 49,64,036 subsidy beneficiaries in total, including 23,04,590 on the 50% subsidy. — [Daily Pioneer, 2025](https://www.dailypioneer.com/2025/state-editions/zero-power-bills-surge-under-8monthold-bjp-government.html)
- FACT: A CAG report tabled by CM Rekha Gupta found:
  - 0–200 units: over 3 mn beneficiaries, averaging about ₹6,000/yr each.
  - Above 200 units: about 1.66 mn beneficiaries, averaging over ₹10,000/yr each.
  - The 400-unit line covered about 80% of domestic consumers.

  — [Construction World, 13 Aug 2026](https://www.constructionworld.in/energy-infrastructure/power-and-renewable-energy/cag-flags-discrepancies-in-delhi-power-subsidy-scheme/95980)
- FACT: TPDDL's customer handbook points users to a "Subsidy Eligibility Calculator" on its website. A sample bill shows a subsidy line of −880.00, without explaining the formula. — [TPDDL Customer Handbook FY26](https://tatapower-ddl.com/Editor_UploadedDocuments/Content/Customer_Handbook_FY26.pdf)

**Punjab**
- FACT:
  - 300 free units a month (implicitly 600 per two-month bill).
  - Above that, the standard rate applies to every unit: "It's a full waiver, not a part-discount."
  - Rate above 300 units is ₹7.05 under PSERC's FY 2026-27 order (effective 1 Apr 2026). Rates within 300 depend on load: ₹3.85 (≤2 kW), ₹4.25 (2–7 kW), ₹5.00 (7–20 kW).
  - Dropping back under 300 in the next cycle restores the waiver.

  — [Daily Pioneer, 26 Jun 2026](https://dailypioneer.com/news/how-punjabs-300-unit-free-electricity-scheme-actually-works)
- FACT (older; current status unverified): the 2022 notification said general-category consumers above 600 units/two months pay for the entire usage, while SC/BC/BPL households pay only the excess. — [Business Today, 24 Jul 2022](https://www.businesstoday.in/latest/economy/story/punjabs-pspcl-issues-notification-for-300-units-of-free-electricity-342512-2022-07-24)
- FACT: About 90% of households get "zero" bills (headline). — [The Statesman tag page](https://www.thestatesman.com/tag/free-power-units). Around 51 lakh households were projected to get zero bills (2022). — [Tribune](https://www.tribuneindia.com/news/punjab/around-51-lakh-households-to-get-zero-electricity-bill-punjab-cm%C2%A0bhagwant-mann-413023)

**Karnataka (Gruha Jyothi)**
- FACT:
  - Entitlement is the 2022-23 average + 10% (or +10 units if the average is below 90), capped at 200.
  - Use above the entitlement but at or below 200: the net difference is billed.
  - Above 200: the household pays the "entire bill".

  — [Outlook Money, Apr 2024 (updated Sep 2024)](https://outlookmoney.com/news/karnataka-residents-may-lose-gruha-jyothi-scheme-coverage-if-they-dont-check-this-tips-to-reduce-electricity-usage)
- FACT (third-party blog, not official): 1.64–1.74 crore beneficiaries. Door-to-door verification began 1 Jul 2026, and beneficiaries must re-apply. FY27 budget ₹10,578 cr. — [Barristery, Jul 2026](https://www.barristery.in/2026/07/gruha-jyothi-scheme-karnataka-2026.html)
- FACT: BESCOM billed July 2026 on the previous 3-month average while that verification ran, adjusting in August. — [Deccan Herald, 6 Jul 2026](https://www.deccanherald.com/india/karnataka/bengaluru/karnataka-gruha-jyothi-door-to-door-verification-your-july-power-bill-will-be-based-on-3-month-average-usage-what-this-means-4063463)

**Telangana (Gruha Jyothi)**
- FACT: A household using 201 units pays the full bill for all 201 units. "Numerous customers turned ineligible during the summer season" (TGNPDCL SE, Kamareddy); a resident said "We crossed the 200 units mark." — [Deccan Chronicle, 21 Jun 2024](https://deccanchronicle.com/news/excess-use-of-power-affects-gruha-jyothi-beneficiaries-900090)
- FACT: Headline: "Beneficiaries who use even one unit above 200 units not eligible for zero bill." — [Telangana Today tag page](https://telanganatoday.com/tag/zero-bill)
- FACT: 10.52 lakh beneficiaries in Greater Hyderabad. Officials said over 2 lakh eligible consumers miss out because they use more than 200 units. — [Siasat, 5 Dec 2024](https://www.siasat.com/over-10-5-lakh-beneficiaries-avail-free-electricity-in-hyderabad-3142852/amp/)
- FACT (from earlier dossier): 42.25 lakh beneficiaries statewide. — [Siasat](https://www.siasat.com/telangana-free-electricity-scheme-beneficiaries-struggle-to-receive-zero-bill-3079517/amp/)

**Tamil Nadu (new 2026)**
- FACT: TNERC Order No. 5 of 2026; G.O. (Ms) No. 50 of 10 May 2026:
  - At or below 500 units per two-month bill: 200 units free (was 100).
  - Above 500: still 100 free.
  - Provisional subsidy ₹1,545.14 cr for FY27.

  — [SolarQuarter, 29 May 2026](https://solarquarter.com/2026/05/29/tnerc-approves-%e2%82%b91545-14-crore-subsidy-as-tamil-nadu-expands-free-electricity-benefit-up-to-500-units/)
- FACT (community blog): slab tables give an energy charge of ₹1,570 at 500 units vs about ₹2,048 at 501 units (the 501 figure is computed from its tables), a jump of about ₹478. — [Verified.RealEstate, 8 Jun 2026](https://community.verified.realestate/article/tamil-nadu-electricity-charges-2026-how-the-200-units-free-power-scheme-works-below-and-above-500-units/)
- FACT: A Play Store app, "TNEB Bill Calculator – TVK 200 Free Scheme" (1K+ installs, updated 3 Sep 2026), already estimates bills under the new scheme. — [Google Play](https://play.google.com/store/apps/details?id=tneb.free200)

**Bihar**
- FACT: 100% subsidy on up to 125 units/month for about 1.67 crore families, effective on bills from 1 Aug 2025. — [ETV Bharat, 18 Jul 2025](https://www.etvbharat.com/en/!state/bihar-cabinet-approves-free-electricity-scheme-enn25071805576)
- FACT: For postpaid bills, "the first 125 units deducted from the total charge and only the remaining balance payable". This implies a marginal design. On prepaid smart meters the 125-unit deduction is automated on the meter server. — [Patna Press, 2 Aug 2025](https://patnapress.com/125-units-of-free-electricity-for-bihar-households-sbpdcl-begins-implementation-as-per-cms-promise/)

**Jharkhand**
- FACT: 200 units/month free from 2024 (100 from 2022); about 41.4 lakh consumers. — [AIR, 29 Jun 2024](https://www.newsonair.gov.in/jharkhand-govt-takes-decision-for-200-units-per-month-free-electricity-for-domestic-consumers)
- FACT: Households using more than 200 units are "ineligible"; 33.5 lakh rural and 6.5 lakh urban beneficiaries. — [Vikaspedia](https://en.vikaspedia.in/viewcontent/schemesall/state-specific-schemes/welfare-schemes-of-jharkhand/mukhyamantri-urja-khushhali-yojana?lgn=en)

**Rajasthan**
- FACT: 100 free units under the Mukhyamantri scheme. A 150-unit scheme from 14 Oct 2025 is tied to installing ≥1.1 kW rooftop solar under PM Surya Ghar. DISCOMs charge normal rates "only for units consumed beyond the free limit", i.e. marginal. — [Vikaspedia](https://en.vikaspedia.in/viewcontent/schemesall/state-specific-schemes/welfare-schemes-of-rajasthan/150-unit-nishulk-bijli-yojana?lgn=en)

**Himachal Pradesh**
- FACT: 125 free units continue, per the CM on 19 Aug 2025; 300 units are "under consideration". — [The Statesman, 19 Aug 2025](https://www.thestatesman.com/india/himachal-cm-assures-125-units-free-electricity-continuity-free-300-units-under-consideration-in-himachal-assembly-1503473854.html)

**Madhya Pradesh (Atal Griha Jyoti)**
- FACT: Eligibility requires ≤150 units/month; the subsidy covers the first 100 units; households above 150 in a month are not eligible. — [Public Services Map](https://www.publicservicesmap.in/schemes/atal-graha-jyoti-yojana--agjy?lang=en)

**Kerala (not a free-unit scheme, but a cliff)**
- FACT: Billing is telescopic up to 250 units/month and non-telescopic above. At 249 units the bill is ₹1,399.15; at 252 units it is ₹1,650.60 (excluding fixed charges). — [Onmanorama, 6 Dec 2024](https://www.onmanorama.com/news/kerala/2024/12/06/electricity-tariff-hike-in-kerala-impact-on-consumers.amp.html)

### Inferences
- **Delhi cliff size (INFERENCE):**
  - If the 50% applies to the whole bill, a 201-unit bill is ₹604.50 energy + ₹40 fixed (2 kW), ≈ ₹645 before surcharges and tax. That puts the payable amount at roughly ₹320–450.
  - The 2019 official example (250 units → ₹252) is consistent with a jump of a few hundred rupees.
  - If the benefit is a flat "₹800 off", there is almost no cliff at 201.
  - Either way, the household loses the "zero bill". Treat the Delhi cliff as "₹0 → about ₹250–450, to be verified against a real 201–250-unit bill or TPDDL's subsidy calculator".
- **True cliffs by state (INFERENCE):**
  - Telangana: 201 units costs the full 201-unit bill (about ₹900–1,000 at slab rates; not computed from an official order).
  - Punjab general category: 601 units/two months costs about 600 × ₹3.85–5 plus the higher slab, i.e. ₹2,500+.
  - Karnataka: >200.
  - TN: 501 units/two months (≈₹478).
  - Kerala: 251 units (≈₹237).
  - MP: 151 units.
  - Jharkhand: >200, if "ineligible" means the full bill.
- **Mostly marginal (INFERENCE):** Bihar and Rajasthan. Karnataka is also marginal between the entitlement and 200.
- **The cliff is a summer phenomenon (INFERENCE):** Delhi lost about 25.6 lakh zero bills from February to July 2025 and regained about 4.6 lakh from September to October. October is the month many Delhi households cross back *under* 200, so in October the product's pitch flips from "don't fall off" to "get back under".
- **Thresholds stretch with cycle length (INFERENCE from the TPDDL proration FAQ and Punjab's 600/two months):** any rule engine must pro-rate the threshold by the billing-period days, not the calendar month.

### Gaps
- No official text giving the Delhi bill payable at exactly 201 units. DERC and GoNCTD orders were not retrieved; the power.delhi.gov.in PDF found is the 2015 per-unit subsidy letter, partly unreadable in the scanned copy.
- Whether Punjab's SC/BC/BPL "pay only excess" rule still applies in 2026.
- Jharkhand: is it the full bill or the excess above 200?
- Official current beneficiary counts for Karnataka, Telangana, TN, Rajasthan, Himachal and MP. Karnataka's figure is from a blog.

---

## Q2. KILL TEST: do DISCOM / smart-meter / third-party apps already warn about the threshold or project the cycle?

### Takeaway
- **DISCOM and smart-meter apps:** none of the 21 Play Store listings checked (on 9 Oct 2026) mentions a free-unit threshold warning, a projection against a subsidy line, weather awareness, or savings verification. They show history or daily use, recharge, and generic tips.
- **Closest DISCOM-side features:**
  - Bihar Sugam (Secure Meters) predicts the days left on a *prepaid balance*.
  - The MSEDCL Genus app claims "consumption forecasts" and "intelligent alerts", but MSEDCL has no free-unit scheme.
  - Oracle Opower (US) has a mid-cycle bill forecast and a weather-attributed bill comparison; India's BRPL pilot of Opower reports measured only 0.32% savings.
- **Third-party hackathon repos already cover much of (a)–(b):**
  - SmartBill (BESCOM Telegram bot): meter/bill photo → OCR → Gruha Jyothi cliff logic → Random-Forest next-bill prediction using temperature.
  - WattWise (Telangana): meter photo → Gruha Jyothi bill.
- **Not found anywhere for Indian consumers:** a weather-normalised savings verification or a probability-of-crossing daily budget.

### Cited Findings
**DISCOM apps (Play Store descriptions read live on 9 Oct 2026, FACT)**
- BRPL POWER App (10L+, updated 20 May 2026): account, bill and payment history, pay, "Check your consumption", complaints. No alerts or projections. — [Play](https://play.google.com/store/apps/details?id=com.bses.bsesapp)
- BYPL Connect (5L+, 16 Dec 2025): bills, prepaid balance check. — [Play](https://play.google.com/store/apps/details?id=com.bses.bypl.prod)
- My Tata Power (10L+, 11 Aug 2026) and My Tata Power Plus (1L+, 27 Aug 2026): "view and pay your bills, monitor usage… receive notifications, optimize consumption with ways to save". No threshold or projection. — [Play](https://play.google.com/store/apps/details?id=com.sew.tatapower), [Play](https://play.google.com/store/apps/details?id=com.tatapower.consumerapp)
- BESCOM Mithra (10L+, 17 Aug 2026), with no alert or forecast keywords — [Play](https://play.google.com/store/apps/details?id=com.bescom.consumerengagementmasters). Smart Meters-BESCOM (1L+, 25 Sep 2026): "View Consumption Information", recharge, complaints — [Play](https://play.google.com/store/apps/details?id=consumerapp.bsmart.bcits.BESCOMcis)
- PSPCL Consumer Services (10L+), PSPCL Consumer App (5L+, Sirhind pilot) and PSPCL Smart Meter Services (50K+; "view consumption history"): no threshold features. — [Play](https://play.google.com/store/apps/details?id=in.pspcl.distribution.cs), [Play](https://play.google.com/store/apps/details?id=com.pspcl.consumerapp), [Play](https://play.google.com/store/apps/details?id=com.zenium.pspcl)
- TGSPDCL Citizen App (10L+, 2 Sep 2026): bills, bill history, tariff details, "Energy Saving Tips". — [Play](https://play.google.com/store/apps/details?id=supply.power.tsspdcl)
- Bihar Bijli Smart Meter (SEW; 50L+, 11 Nov 2025): usage information, recharge, bills. — [Play](https://play.google.com/store/apps/details?id=com.sew.scm.eesl)
- Bihar Sugam Smart Meter (Secure Meters; 50L+, 27 Oct 2025): low or no balance alerts, high-load alerts, "Balance projection: predicts the days left before your balance runs out", daily/weekly/monthly usage and cost. — [Play](https://play.google.com/store/apps/details?id=com.mysugam.nbpdcl&hl=en_IN)
- UPPCL SMART (Jio; 10L+, 4 Sep 2026): daily/weekly/monthly use including "appliance level consumption", "personalized tips", "push notifications, emails, and SMS alerts for important updates". — [Play](https://play.google.com/store/apps/details?id=com.jio.uttarurja)
- Mahavitaransmart (Genus for MSEDCL; 50K+, 23 Sep 2026): "intelligent alerts, consumption forecasts, and personalized energy-saving insights" (no detail). — [Play](https://play.google.com/store/apps/details?id=com.genus.app.mahavitaransmart_app). Genus's product page lists "configurable thresholds" but no alerts or forecasts. — [Genus](https://genuspower.com/product/smart-meter-mobile-app/?rp=arc)
- Mahavitaran (1Cr+, 4 Sep 2026): includes "Estimate your monthly electricity consumption and bill amount", i.e. a calculator. — [Play](https://play.google.com/store/apps/details?id=com.msedcl.app)
- DGVCL Smart Meter, PGVCL Vij Connect and UPPCL Smart Consumers: generic usage tracking only. — [Play](https://play.google.com/store/apps/details?id=com.sew.intellismart.dgvcl), [Play](https://play.google.com/store/apps/details?id=com.edf.scm), [Play](https://play.google.com/store/apps/details?id=com.uppcl)

**Older DISCOM features (FACT)**
- Tata Power's AMR "Know Your Electricity Consumption" (2018): monthly, daily and hourly usage, ToD guidance; no budgets, projections or weather. — [T&D India, 31 Oct 2018](https://www.tndindia.com/tata-power-launches-energy-management-tool-consumers/amp/)
- TPDDL smart meters (2020): MDI and power factor visible about every 4 h in the app; SMS alerts only "planned" for MDI and PF. — [T&D India, 22 Jun 2020](https://www.tndindia.com/smart-meters-boost-efficiency-tata-power-ddl-consumers/amp/)
- TPDDL already runs a browser camera "scan the meter" self-reading flow ("Scan display of the meter when parameter of kWh/kW is displayed"), with a manual or photo fallback. — [TPDDL press release](https://tatapower-ddl.com/pr-details/199/1354086/tata-power--ddl-promotes-self-meter-reading-to-ensure-consumer-safety-during-covid-19)

**International utility software (FACT)**
- Oracle Opower Bill/Usage Forecast:
  - shows usage so far, a projected total for the cycle, and a "typical" value from last year's bills;
  - flags use more than 30% above baseline;
  - needs AMI interval data;
  - the documentation describes no weather normalisation and no tier alerts.

  — [Oracle docs](https://docs.oracle.com/en/industries/energy-water/energy-efficiency/energy-efficiency-overview/Content/Customer_Experience_Overview/Bill-Usage-Forecast.htm)
- Oracle Opower Bill Comparison explains bill changes by "weather, energy use, bill period length, rates" (e.g. "$24 more due to weather"); the method is undocumented. — [Oracle docs](https://docs.oracle.com/en/industries/energy-water/customer-service-interface/bill-advisor-overview/bill-comparison-module--csi-ba.html)

**Third-party apps and hackathon repos (FACT; GitHub read live on 9 Oct 2026)**
- **SmartBill** (repo `SudeepSBingolli/BESCOM-Bill-Chatbot`, created 27 Sep 2026): a Telegram bot for Bangalore.
  - "snap a photo of your meter or printed BESCOM bill slip" → vision OCR (Gemini, OpenAI or Claude).
  - Exact bill with pro-rated Gruha Jyothi; flowchart node "Exceeded (> 200 u/month) → Disqualified… Pay 100%".
  - "Random Forest ML Model (Historical Trends & Temperature)" predicts the next month's units and bill.
  - Its README does not mention a daily budget, an action ranking or savings verification.

  — [GitHub](https://github.com/SudeepSBingolli/BESCOM-Bill-Chatbot)
- **WattWise** (repo `chennakeshavareddy7314/Electricity-Bill-Tracker`, pushed 9 Oct 2026): previous bill + current meter photo → tesseract OCR with a user-correction step → Telangana slab bill with Gruha Jyothi "(≤ 200 units → ₹0)". It was built for a different hackathon brief ("Electricity Bill Tracker"). — [GitHub](https://github.com/chennakeshavareddy7314/Electricity-Bill-Tracker)
- **BijliBachat** (`KLC-coder/bijlibachat`, 2 Oct 2026): appliance load calculator, monthly savings targets, schedule cuts for AC and geysers, "Tariff Slab Awareness: helps households stay below expensive electricity tariff slabs". — [GitHub](https://github.com/KLC-coder/bijlibachat)
- **BijliSaarthi** (28 Sep 2026): next-hour ML consumption forecast, a budget comparison and tips. — [GitHub](https://github.com/sanchita-1111/BijliSaarthi-A-Personalized-Household-Electricity-Saving-Assistant)
- **VoltWise AI** (lablab, 10 May 2026): MSEDCL bill parsing (English and Marathi), tariff engine, what-if simulation. Forecasting, weather and threshold alerts are not mentioned. — [lablab](https://lablab.ai/ai-hackathons/amd-developer/spandan/voltwise-ai)
- **Pakistan analogue:** many "bijli" bill apps target Pakistan's 200-unit "protected" cliff (e.g. BijliSmart AI, Bijli-Ustad on GitHub). Pakistan's government Power Smart App takes meter photos for billing but has no threshold warning. — [Geo](https://www.geo.tv/latest/611545-how-can-apna-meter-apni-reading-app-help-you-avoid-overbilling)
- **The live Environmental Hacks list** (111 projects) had no free-unit or meter-budget project as of 9 Oct morning. `grid-nudge` still has no README, as rechecked tonight. — [live_competition.md](/home/claude/research_notes/Environmental%20Hacks%20concept%20reset/live_competition.md), [GitHub](https://github.com/CSNEHA20/grid-nudge)

### Inferences
- **Kill test result: PARTIAL PASS (INFERENCE).**
  - No DISCOM app found projects against a free-unit line, warns before a cliff, or verifies savings.
  - But "meter photo → units → cliff-aware bill" and "ML next-bill prediction with temperature" are commodity. SmartBill already has them, and an LLM coding assistant produces them quickly.
  - A judge who has seen SmartBill-style projects will discount parts (a) and (b) unless the projection is visibly better: probabilistic, aware of cycle dates and pro-ration, and tied to a daily budget.
- **Smart-meter apps with daily data are where DISCOMs could add this cheaply (INFERENCE).** Bihar Sugam already projects prepaid balance; projecting against 125 free units would be a small change. It doesn't matter much, because Bihar's scheme is marginal (no cliff).
- **The verification half (d) has no consumer-facing Indian equivalent** (INFERENCE, based on these listings and searches). Internationally, weather attribution exists inside utility software (Opower), not as a household-run tool.

### Gaps
- App UIs were not opened (no sign-in). Listings can under-describe features; e.g. BESCOM smart-meter or PSPCL smart apps may show "units this month" without saying so.
- SMS campaigns: no evidence found that any DISCOM sends "you are near 200/300 units" SMS. Absence in news is not proof.
- No access to the iOS store or to the TGSPDCL/BESCOM web portals behind login.

---

## Q3. Competitors (India and abroad): what they do, and whether any verifies weather-normalised savings for consumers

### Takeaway
- **Abroad:** utility platforms do mid-cycle forecasts (Opower Bill Forecast), weather-attributed bill comparisons (Opower Bill Comparison), and disaggregation and high-bill agents (Bidgely). Program-level M&V uses CalTRACK/OpenEEmeter. None is a free, household-run tool that verifies a household's own action with a counterfactual and uncertainty.
- **In India:** only behavioural home energy reports (BRPL × Opower, measured 0.32%), DISCOM apps, calculators and hackathon bill analysers.

### Cited Findings
- FACT: BRPL ran a randomised home-energy-report pilot (Oracle Opower software) with 2 lakh consumers from Oct 2018 for 15 months. Measured savings were 3.08 MU = **0.32%** of consumption (medium users 0.32%, high users 0.31%). — [BRPL DSM deck, SEforALL](https://seforall.org/system/files/2024-05/BRPL_DSM%20Initiatives%20in%20BSES%20Rajdhani%20Power%20Limited.pdf)
- FACT: The IEA policy database lists the same programme with an "estimated 1–3%" reduction. This conflicts with BRPL's measured 0.32%. — [IEA](https://www.iea.org/policies/17804-opower-home-energy-reports-in-india)
- FACT: Bidgely's Sept 2026 "Agentic CX" adds agents for high-bill analysis, home audits, solar, EV and rate selection. It acquired Grid4C in March 2025. No Indian utility customers were named. — [YesPress](https://yespress.io/bidgely)
- FACT: CalTRACK/OpenEEmeter billing methods:
  - Fit usage against HDD and CDD with a balance-point search.
  - Choose among intercept-only, CDD-only, HDD-only and CDD+HDD models by adjusted R².
  - Weight by days.
  - Treat periods <25 days as missing, and periods >70 days as missing.
  - Output `metered_savings` (avoided energy use).

  — [eemeter CalTRACK compliance](https://eemeter.readthedocs.io/caltrack_compliance.html)
- FACT: The established method that judges may recognise:
  - International M&V (IPMVP Option C) adjusts the baseline to current weather — [EnergyCAP, via C-12](https://www.energycap.com/?p=1910)
  - the US PRISM degree-day method — [ACEEE 1986](https://www.aceee.org/files/proceedings/1986/data/papers/SS86_Panel9_Paper_30.pdf); title only, from the earlier dossier
- FACT: Bijli Bachao offers state-wise bill calculators. — [Bijli Bachao](https://www.bijlibachao.com/?p=71) (from earlier dossier)
- FACT: Mahavitaran and many Play-Store calculators estimate the bill from units, e.g. "Electricity Bill Calculator" (RJ App Studio) estimates per appliance. — [Play](https://play.google.com/store/apps/details?id=com.sapientinfo.energytracker)

### Inferences
- **What the competitors fail to do (INFERENCE, from listings and docs):**
  1. No Indian tool combines the state's cliff rule, pro-rated to cycle length, with a weather-driven projection *and* turns the gap into a daily kWh budget.
  2. None gives a household a counterfactual: "this bill would have been X in this weather, ±Y; your change saved Z or can't tell yet".
  3. Opower-style feedback produced tiny measured savings in Delhi (0.32%). Generic feedback is not enough, which supports targeting the moment of the cliff. The improvement from targeting is a HYPOTHESIS.
- **OpenEEmeter (eemeter) is an off-the-shelf engine** for the regression (INFERENCE). Using it on Lambda makes the M&V claim credible ("CalTRACK-compliant method") and saves build time. It is designed for ≥365 days of baseline and for monthly, not two-monthly, periods. Punjab and TN two-month bills would be treated as missing under default settings.

### Gaps
- Opower's Bill Comparison attribution method is undocumented.
- Whether any Indian DISCOM offers Bidgely-style disaggregation to households in 2026: no evidence found.

---

## Q4. Evidence of impact: feedback/budget effect sizes, bunching at thresholds, AC share

### Takeaway
- **Feedback effects are small and context-dependent:** Opower in the US 1.9–2.0%; BRPL Delhi measured 0.32%; Ghaziabad weekly peer comparison 7% in summer; prepaid metering in Cape Town about 13%.
- **No published estimate of bunching below Delhi's 200-unit line was found.** A 2025 Punjab RCT is premised on bunching and on households "exceeding by a small amount", but has no published results.
- **Cooling is about 40% of household electricity nationally**, so near the cliff the controllable margin is mostly cooling.

### Cited Findings
- FACT: Opower home energy reports cut consumption by "1.9 to 2.0 percent relative to baseline". — [Allcott, MIT CEEPR](https://ceepr.mit.edu/workingpaper/social-norms-and-energy-conservation)
- FACT: India (Ghaziabad) RCT:
  - Weekly peer-comparison reports cut **summer** consumption by **7%**, equivalent to a tariff increase of about 12.5%.
  - Adding monetary rewards removed the reduction.

  — [Sudarshan, JEBO 2017, via EPIC](https://epic.uchicago.edu/research/nudges-in-the-marketplace-the-response-of-household-electricity-consumption-to-information-and-monetary-incentives)
- FACT: An earlier write-up of the same study reported about 11%; >500 households, May–Sep 2012. — [Ideas for India, 2013](https://www.ideasforindia.in/topics/urbanisation/electricity-demand-in-urban-indian-households-influencing-consumer-behaviour)
- FACT: Switching to prepaid metering cut use by "about 13 percent", persisting into the following year (Cape Town, >4,000 households). — [Jack & Smith, NBER w22895](https://www.nber.org/papers/w22895)
- FACT: BRPL's Opower pilot measured 0.32%. — [SEforALL/BRPL](https://seforall.org/system/files/2024-05/BRPL_DSM%20Initiatives%20in%20BSES%20Rajdhani%20Power%20Limited.pdf)
- FACT: AEA RCT 0016183, Punjabi & Barnwal (MSU):
  - Premise: administrative data suggest households "bunch" below Punjab's 10 kWh/day line, and many exceed it by small amounts because they lack real-time consumption information.
  - Arms: a meter-reading tutorial + calculator, and the same + SMS reminders every two weeks; 1,000 households.
  - Intervention Jun–Jul 2025; **no results posted**.

  — [AEA registry](https://www.socialscienceregistry.org/trials/16183)
- FACT: Delhi zero bills swing from 43.9 lakh (Feb) to 18.3 lakh (Jul 2025), showing seasonal crossing at scale. — [Daily Pioneer](https://www.dailypioneer.com/2025/state-editions/zero-power-bills-surge-under-8monthold-bjp-government.html)
- FACT (anecdotal behaviour): Delhi households installing multiple meters to stay in the low slabs. — [Newslaundry, 2019](https://www.newslaundry.com/2019/12/02/delhi-aam-aadmi-party-electricity-subsidy). Himachal MLAs cite BPL households with many meters. — [The Statesman, 2025](https://www.thestatesman.com/india/himachal-cm-assures-125-units-free-electricity-continuity-free-300-units-under-consideration-in-himachal-assembly-1503473854.html)
- FACT: Fans, ACs and coolers are **40%** of household electricity (CLASP–BEE 2024 survey). 13.3% of households own an AC (17% urban, 4% rural). — [Down To Earth, 12 May 2026](https://www.downtoearth.org.in/amp/story/energy/cooling-appliances-now-drive-indias-household-electricity-use)
- FACT: In UP smart-meter data (93 households, Aug 2019):
  - ACs ran 7 h/day on average.
  - 60% of households *underestimated* AC use by about 4 h, supporting the information-friction premise.

  — [CEEW](https://www.ceew.in/publications/smart-meter-data-enabled-transition-energy-efficient-cooling)
- FACT: BEE says each +1 °C on the AC setpoint saves about 6% of AC electricity. — [Powerline, 2018](https://powerline.net.in/2018/07/06/mop-proposes-change-default-temperature-setting-acs/)
- FACT (earlier dossier): 43% AC ownership in a Delhi survey. — [Carbon Brief](https://www.carbonbrief.org/guest-post-how-energy-demand-for-cooling-in-indias-cities-is-changing)

### Inferences
- **Impact pitch (INFERENCE):** generic feedback has measured close to zero in Delhi (0.32%). The strongest Indian evidence (7%) came from frequent, personal, summer-season information. The concept should claim at most "low single-digit %" for general users. For near-cliff households it can claim discrete avoided crossings, valued in rupees, which is a FACT-based stake. The kWh avoided is a HYPOTHESIS.
- **Rebound (HYPOTHESIS):** households shown large headroom may consume more. Showing only "on track / at risk", not the units of headroom, is a design mitigation. Ghaziabad's finding that money incentives crowded out the effect argues against rupee-only framing.
- **Environmental framing (INFERENCE):** every kWh avoided ≈ 0.71 kg CO₂ (CEA v22 via earlier dossier, [CEA](https://cea.nic.in/wp-content/uploads/baseline/2026/09/User_Guide__Version_22.0.pdf)). The cliff is one of the rare cases where the subsidy design rewards conservation, and the tool aligns the household's financial incentive with emissions.

### Gaps
- No published bunching estimate for Delhi, Telangana or Karnataka thresholds.
- No Indian evidence that a threshold-specific alert reduces crossings. The Punjab RCT would answer this, but no results are public.
- AC share of *summer* consumption specifically for near-threshold households (≈150–250 units) is unknown. The national 40% is an annual average.

---

## Q5. Feasibility: bill history, meter-photo reading, Open-Meteo, ERA5 lag, October seasonality

### Takeaway
- **Weather data: verified live.** Open-Meteo returned 466 days for Delhi through today. ERA5-only data lags about 6 days, but "best match" fills it. A 16-day forecast is available.
- **Meter OCR with a vision LLM is proven but unreliable unsupervised.** TPDDL itself scans meters in-browser, and two hackathon repos already do it. But the best VLMs score only 53–80% on real digital displays, so a confirm step plus a "reading must increase" check is mandatory.
- **Printed 12-month history on paper bills: not verified.** DISCOM apps and portals *do* expose bill history, so use app screenshots.
- **October is weak for cooling in Bengaluru (0 CDD) but usable in Delhi, Hyderabad and Chennai.** Delhi's October 2026 is running warmer than October 2025, which makes a live "naive vs weather-adjusted" contrast possible.

### Cited Findings
**Open-Meteo, live calls run in the browser on 9 Oct 2026 ~22:30 IST (FACT)**
- Archive call: `https://archive-api.open-meteo.com/v1/archive?latitude=28.61&longitude=77.21&start_date=2025-07-01&end_date=2026-10-09&daily=temperature_2m_mean,temperature_2m_max&timezone=Asia/Kolkata`
  - Returned 466 days, zero nulls, last value 2026-10-09 (27.6 °C mean). Grid point 28.58, 77.19; elevation 217 m.
  - Delhi monthly CDD (base 24 °C, daily mean): Jul-25 172, Aug-25 145, Sep-25 178, **Oct-25 66**, Nov-25 1, Dec–Jan 0, Feb-26 2, Mar-26 59, Apr-26 182, **May-26 276, Jun-26 276**, Jul-26 194, Aug-26 162, Sep-26 134, **Oct 1–9 2026: 47**.
  - With base 18 °C: Oct-25 249, May-26 462.
- Same endpoint with `models=era5` and `models=era5_land`: the last non-null day was **2026-10-03**, i.e. about 6 days of lag. Docs say "5 days delay"; the default "best match" blends IFS so there is no gap. — [Open-Meteo historical docs](https://open-meteo.com/en/docs/historical-weather-api)
- Forecast call: `https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.21&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&forecast_days=16&timezone=Asia/Kolkata`
  - Returned 9–24 Oct 2026 daily means of 24.4–30.8 °C (maxima 26.5–36 °C).
  - CDD24 for 10–24 Oct ≈ 48.
- Other cities, CDD24 by month, Oct 2025–Sep 2026 (same archive):

  | City | Monthly CDD24 |
  |---|---|
  | Bengaluru | 0 Oct–Jan; peak 145 (Apr); Jun–Aug 2–12 |
  | Hyderabad | Oct-25 42; Apr–May 242–252; Sep-26 104 |
  | Chennai | Oct-25 100; May–Jul 234–240 |
  | Ludhiana | Oct-25 40; Jun 247 |
  | Patna | Oct-25 95; Jun 247 |

- Terms: free for non-commercial use, <10,000 calls/day, CC BY 4.0. — [Open-Meteo terms](https://open-meteo.com/en/terms) (via data_access.md)

**Meter reading (FACT)**
- TPDDL's self-reading flow asks consumers to "Scan display of the meter when parameter of kWh/kW is displayed" in the browser camera, with a photo or manual fallback. — [TPDDL](https://tatapower-ddl.com/pr-details/199/1354086/tata-power--ddl-promotes-self-meter-reading-to-ensure-consumer-safety-during-covid-19)
- MeasureBench (18 VLMs) on real-world digital displays: Gemini-2.5-Pro 80.2%, GPT-5-Mini 70.8%, GPT-5 66.7%, Qwen3-VL-8B 53.1%. Analog dials 10–32%. Models recognise units well (>90%) but misread values. — [arXiv 2510.26865](https://arxiv.org/pdf/2510.26865)
- SmartBill uses Gemini, OpenAI or Claude vision on meter photos. WattWise uses tesseract and states "OCR on real meter photos is imperfect… always shows the [value]… can be corrected". — [SmartBill](https://github.com/SudeepSBingolli/BESCOM-Bill-Chatbot), [WattWise](https://github.com/chennakeshavareddy7314/Electricity-Bill-Tracker)
- Pakistan's government Power Smart App bills directly from consumer meter photos. — [Geo](https://www.geo.tv/latest/611545-how-can-apna-meter-apni-reading-app-help-you-avoid-overbilling)

**Bill history (FACT)**
- DISCOM apps expose history:
  - BRPL "View your bill & payment history… Check your consumption" — [Play](https://play.google.com/store/apps/details?id=com.bses.bsesapp)
  - TGSPDCL "Bill History" — [Play](https://play.google.com/store/apps/details?id=supply.power.tsspdcl)
  - My Tata Power lists billing, reading and payment history — [TPDDL handbook](https://tatapower-ddl.com/Editor_UploadedDocuments/Content/Customer_Handbook_FY26.pdf)
- The MSEDCL billing FAQ sample bill shows only the current cycle's previous reading, date and units. Its app's "Submit Reading" works only in the 5 days before the scheduled reading. — [MSEDCL FAQ](https://www.mahadiscom.in/en/billing-faqs/)
- An MSEDCL HT bill (Nov 2024) compares only with the previous month. — [Mahadiscom PDF](https://mahadiscom.in/consumer/wp-content/uploads/2024/12/155-519_170019002163_202411-oa-print1.pdf)
- An MSEDCL grievance order reproduces 29 months of a consumer's consumption, so the DISCOM holds the history even if the bill does not print it. — [CGRF Nagpur 2018](https://www.mahadiscom.in/wp-content/uploads/2018/06/NagpurU14_1529307588686.pdf)
- A TPDDL sample bill shows a slab table covering 3 months. — [TPDDL handbook](https://tatapower-ddl.com/Editor_UploadedDocuments/Content/Customer_Handbook_FY26.pdf)

**Smart-meter coverage (FACT)**
- 7.24 crore smart meters installed by 30 Jun 2026, counting consumer, distribution-transformer and feeder meters together; 5.73 crore under RDSS. Sanctioned under RDSS: 19.79 crore consumer meters. — [T&D India, 6 Aug 2026](https://www.tndindia.com/indias-smart-meter-population-at-7-24-crore-parliament/amp/)
- Time-of-day tariffs for non-agricultural consumers were due by 1 Apr 2025: peak 10–20% higher, solar hours 10–20% lower. — [Housing.com](https://housing.com/news/govt-amends-electricity-rules-introduces-tod-tariff-smart-metering)

**Own simulation, run locally (INFERENCE from simulation; household parameters are HYPOTHESIS)**
- Model: a Delhi household with 4 kWh/day baseload + 0.9 kWh per CDD24. It gives monthly kWh of 114–372, crossing 200 in Apr–Oct.
- Fit: 12 monthly bills (Oct-25 to Sep-26) using the live CDD figures above; 4,000 trials per noise level.

| Monthly noise | Mean R² | 90% prediction half-width, May-like month | Oct-like month |
|---|---|---|---|
| 5% | 0.99 | ±6.4% | ±11.9% |
| 10% | 0.95 | ±12.7% | ±23.8% |
| 15% | 0.89 | ±19.2% | ±35.7% |

### Inferences
- **Projection (b) is technically easy (INFERENCE).** The value is in getting the cycle dates, the pro-rated threshold and the uncertainty right.
- **The "unit cliff" projection is meaningful in October for Delhi (INFERENCE).** Many households hover near 200: the Delhi zero-bill count rose by 4.6 lakh from September to October 2025.
- **October 2026 in Delhi is running hot (INFERENCE from the live data).** CDD24 for 1–24 Oct 2026 is about 47 + 48 = **95**, against **66 for all of October 2025**. A household comparing this October's bill with last October's would wrongly blame itself. This is exactly the counterfactual demo, using real weather.
- **Verification (d) from monthly bills can only detect large changes (INFERENCE from the simulation).** At a realistic 10% noise, a single October bill cannot show a saving under about 24%; a peak-summer bill needs more than about 13%. The honest "can't tell yet" state will be the *common* outcome, not the exception. Short-interval verification from meter photos taken hours apart, normalised by hourly cooling degree-hours, is the only way to show a real verified saving inside 46 hours.
- **Meter OCR is a convenience, not the product (INFERENCE).** It must ship with:
  - a "confirm or edit" step;
  - a check that the reading is ≥ the last reading;
  - a check on digit count;
  - an instruction to photograph the kWh screen (Indian LCD meters scroll through several parameters).

  Smart-meter households should paste or screenshot app data instead.
- **Bengaluru or Mysuru teammates' bills will show almost no cooling signal (INFERENCE).** The weather model collapses to baseload there. Pick a Delhi, Hyderabad, Chennai, Punjab or Patna household for the demo.

### Gaps
- No sample residential bill image from BSES, TPDDL, BESCOM, PSPCL, TSSPDCL or MSEDCL could be read (Scribd needs JS and serves images), so whether the paper bill prints 6–12 months of history is unverified for each DISCOM. Fallback: the team photographs their own bill or app history.
- VLM accuracy on Indian single-phase LCD meters specifically was not measured. MeasureBench is general.
- Indian LCD auto-scroll timing per manufacturer was not sourced.

---

## Q6. Breadth: households under threshold schemes; usefulness without free units

### Takeaway
- **Sourced threshold-scheme households:** Delhi ~0.5 cr, Punjab ~0.5 cr, Karnataka ~1.6 cr, Telangana ~0.4 cr, Bihar ~1.7 cr, Jharkhand ~0.4 cr. That totals **≈5 crore**, plus TN (all domestic), Rajasthan, Himachal and MP, which are unsourced.
- **True-cliff states alone** (Delhi, Punjab, Karnataka, Telangana, Jharkhand) ≈ 3.5 crore. Only the slice within ~15% of the line in a given month is actively served.
- **Outside free-unit states** the engine still applies to non-telescopic cliffs (Kerala 250), TN's 500-unit step, MP's 150, and weather-normalised verification. ToD tariffs are a different (time) dimension that the concept does not address.

### Cited Findings
- FACT: Delhi 49.6 lakh subsidy beneficiaries (Oct 2025) — [Pioneer](https://www.dailypioneer.com/2025/state-editions/zero-power-bills-surge-under-8monthold-bjp-government.html)
- FACT: Punjab ~51 lakh zero bills (2022 projection) — [Tribune](https://www.tribuneindia.com/news/punjab/around-51-lakh-households-to-get-zero-electricity-bill-punjab-cm%C2%A0bhagwant-mann-413023)
- FACT: Karnataka 1.64–1.74 cr (blog) — [Barristery](https://www.barristery.in/2026/07/gruha-jyothi-scheme-karnataka-2026.html)
- FACT: Telangana 42.25 lakh — [Siasat](https://www.siasat.com/telangana-free-electricity-scheme-beneficiaries-struggle-to-receive-zero-bill-3079517/amp/)
- FACT: Bihar 1.67 cr families — [ETV Bharat](https://www.etvbharat.com/en/!state/bihar-cabinet-approves-free-electricity-scheme-enn25071805576)
- FACT: Jharkhand 41.4 lakh — [AIR](https://www.newsonair.gov.in/jharkhand-govt-takes-decision-for-200-units-per-month-free-electricity-for-domestic-consumers)
- FACT: Kerala non-telescopic billing above 250 units/month — [Onmanorama](https://www.onmanorama.com/news/kerala/2024/12/06/electricity-tariff-hike-in-kerala-impact-on-consumers.amp.html)
- FACT: TN 500-unit step — [SolarQuarter](https://solarquarter.com/2026/05/29/tnerc-approves-%e2%82%b91545-14-crore-subsidy-as-tamil-nadu-expands-free-electricity-benefit-up-to-500-units/)
- FACT: MP 150-unit eligibility — [Public Services Map](https://www.publicservicesmap.in/schemes/atal-graha-jyoti-yojana--agjy?lang=en)
- FACT: ToD tariffs: peak +10–20%, solar hours −10–20% — [Housing.com](https://housing.com/news/govt-amends-electricity-rules-introduces-tod-tariff-smart-metering)

### Inferences
- **Who is actually served at any moment is far smaller than ≈5 crore (INFERENCE).** In Delhi, about 25 lakh households cross between February and July. That swing is the most defensible "addressable" figure, from FACT data.
- **Without a cliff, the product reduces to a bill forecaster plus weather-normalised verification (INFERENCE).** Telescopic slabs (e.g. MSEDCL) create only marginal steps. The verification half is the part that generalises nationally, and it is also the hardest to demonstrate convincingly.

### Gaps
- Official 2026 beneficiary counts for most states.
- Size of the near-threshold band (e.g. households at 170–230 units) in any state: no distribution data was found.

---

## Verdict for the coordinator

### (i) Capability table for the main user journey

| Step | Status | Evidence / constraint |
|---|---|---|
| A1. Ingest bill history (12+ months of units and dates) from a DISCOM-app screenshot or bill photo → Bedrock vision / Textract → confirm table | **VERIFIED-BUT-CONSTRAINED** | Apps expose bill history (BRPL, TGSPDCL, Tata Power listings, FACT). Paper bills printing 12 months is **unverified**. Extraction from the team's own screenshots is untested, but LLM table extraction is routine. Two-month bills (Punjab, TN) give only 6 points a year. |
| A2. Read the kWh register from a meter photo | **VERIFIED-BUT-CONSTRAINED** | Precedents: TPDDL's in-browser scan, SmartBill and WattWise (FACT). Best VLMs reach only 53–80% on real digital displays (FACT), so a confirm step, a reading-must-increase check and "photograph the kWh screen" guidance are required. Untested on the team's own meters. |
| B1. Daily temperature → cooling degree-days, last 12+ months and 16-day forecast | **VERIFIED** | Live calls today: Delhi 466 days to 9 Oct 2026; forecast to 24 Oct; ERA5-only lag 6 days, blended "best match" none. |
| B2. State rule engine (threshold, pro-rating, cliff vs marginal) | **VERIFIED-BUT-CONSTRAINED** | Telangana, Karnataka, Punjab, TN, Kerala and MP rules sourced. Delhi's 201-unit payable amount is unresolved (₹0 → roughly ₹250–450, INFERENCE). Bihar is marginal; Jharkhand is unclear. Pro-rating is documented by TPDDL. |
| B3. Weather-regressed projection to cycle end, with P(cross threshold) | **PLAUSIBLE-UNTESTED** | Method standard (CalTRACK/eemeter, FACT). On 12 monthly points, accuracy is ±13% in summer and ±24% in October at 10% noise (own simulation). Weak in Bengaluru (≈0 October CDD). |
| C. Daily unit budget + "single biggest action" | **PLAUSIBLE-UNTESTED** | The budget is arithmetic. The "biggest action" needs the user's appliance inventory and BEE's 6%/°C (FACT). Ranking actions per household is HYPOTHESIS-grade without sub-metering. |
| D1. Verify savings from the next *bill* (counterfactual ± band) | **VERIFIED-BUT-CONSTRAINED** | Method is real (IPMVP Option C / CalTRACK). It cannot be shown with a real *post* bill inside 46 h. It can only detect large changes, and "can't tell yet" will be common. Use a real past change (e.g. a new AC, a move) if a teammate has one; otherwise label it synthetic. |
| D2. Verify savings from the next *meter photo* (hours apart, normalised to hourly CDD) | **PLAUSIBLE-UNTESTED** | Feasible this weekend with the team's own meters. October nights in Delhi are mild (forecast means 24–29 °C), so AC load and signal may be small. Chennai and Hyderabad are better. |
| E. AWS load-bearing | **PLAUSIBLE** | Bedrock vision/Textract (A1, A2), Lambda running eemeter/statsmodels (B3, D), EventBridge Scheduler for re-read nudges, Step Functions for the read → validate → project → verify loop, DynamoDB ledger. SMS needs DLT registration (earlier dossier), so use web push or email. |

### (ii) Minimum working demonstration (no outside person, no privileged data, no hardware)

**Data the team supplies itself, all real:**
1. One teammate's household, ideally in Delhi, Hyderabad, Chennai, Punjab or Patna, not Bengaluru:
   - 12–13 months of bill history: DISCOM-app screenshots or photos of past bills (units, reading dates);
   - the last bill's closing reading and date.
2. Three or four photos of that teammate's own meter's kWh screen: Fri night, Sat morning, Sat night, Sun morning. These are timestamped, real readings, and need nobody else's cooperation.
3. Their city's Open-Meteo archive and forecast (live, keyless; verified today).
4. A cited rule pack for that state, plus Delhi and Telangana as worked examples.

**Demo sequence:**
1. History → fit (base + CDD slope) → decomposition chart. Live hook for Delhi: "October 2026 has about 95 CDD by the 24th vs 66 in all of October 2025. A naive comparison blames you; weather-adjusted, you're on track."
2. Meter photos → units so far this cycle (from the last bill reading) → projection with a 16-day forecast → P(cross the pro-rated threshold) → daily budget (e.g. "≤5.1 units/day for 14 days").
3. Verification:
   - **Forward:** Sat night with one action (AC +2 °C or geyser off) against a Fri-night baseline normalised by hourly cooling degree-hours → "verified −X kWh" or "can't tell".
   - **Backward:** a real past change in the bill history if one exists; otherwise a clearly **labelled** synthetic shift.
4. If the household is not near a threshold, run a **labelled** what-if on their real fitted model, e.g. the same household with baseload +1.5 kWh/day.

### (iii) Strongest skeptical-judge objection, and whether it is answerable

**Objection:** "This is another 'snap your meter, get your bill' app. SmartBill already does meter OCR, the Gruha Jyothi cliff and a temperature-aware prediction. DISCOM smart-meter apps already show daily use, one already projects balance, and the 7.24 crore smart meters will make photos pointless. Your 'verified savings' from 12 noisy bills can't detect realistic 5–10% changes, and India's only measured feedback programme saved 0.32%."

**Answerable, partially:**
1. **Novelty is narrow but real.** No Indian app found does a pro-rated, probabilistic crossing forecast with a daily budget, or a household-run counterfactual with uncertainty (FACT for the listings checked). Show SmartBill-style output next to yours and make the difference visible: the probability, the band, and the "can't tell" state.
2. **Smart meters are not yet universal.** RDSS consumer-meter installs are a minority of the 19.79 crore sanctioned (INFERENCE from FACT totals). The engine also takes smart-meter app data, so it is not tied to photos.
3. **The noise objection is true for monthly bills.** Answer it by: showing the band honestly; using meter-reading cadence (days, not months) to shrink it; citing that feedback timed to a salient moment (7% in the Ghaziabad summer study) beats generic reports (0.32%).
4. **The environmental claim must be modest:** kWh avoided at the margin near the cliff, with rebound acknowledged.

### (iv) Functional improvement or re-presentation?

**Mixed, and closer to re-presentation for parts (a)–(c) as usually built:**
- **(a) Meter/bill reading: re-presentation (FACT).** Done by TPDDL's own self-reading tool, SmartBill and WattWise.
- **(b) Projection: partially new.**
  - SmartBill predicts next month's bill with temperature, and Opower (US) forecasts the cycle against last year (FACT).
  - The new parts are projecting against a pro-rated *policy cliff*, as a *probability*, mid-cycle, from the household's own photos (INFERENCE).
- **(c) Daily budget + single action: incremental.** Commodity tips and appliance calculators exist (BijliBachat, Play-store calculators; FACT). A cliff-derived daily budget is a modest functional step (INFERENCE).
- **(d) Weather-normalised verification: genuine functional improvement for Indian households.** No consumer equivalent was found (INFERENCE; utility-side analogues exist abroad: Opower Bill Comparison, CalTRACK/OpenEEmeter, FACT). It is also the hardest to demonstrate in 46 hours and in October.

**Recommendation (INFERENCE):** if built, lead with (d)+(b) as "your bill, weather-adjusted: did you actually save, and will you fall off the cliff?" and treat OCR as plumbing. Choose a teammate household in a city with an October cooling signal. Do not claim impact beyond low single-digit % or discrete avoided cliff crossings.
