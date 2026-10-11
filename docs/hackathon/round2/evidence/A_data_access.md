# Data-source capability catalogue for an India-focused, software-only hackathon prototype (verified Fri 9 Oct 2026, ~14:00–15:00 IST)

How this was checked. The workspace shell is blocked by its proxy: `curl` to grid-india.in, api.data.gov.in and api.openaq.org returned `CONNECT tunnel failed, response 403`. Live calls were therefore made from the Claude desktop built-in browser on the user's machine: one tab, which was closed afterwards. JSON was parsed with in-page JavaScript, and cross-origin `fetch()` was used where CORS allowed it. Documentation was read with WebFetch.

Every live call below gives its exact URL and what came back. No keys were requested, nothing was signed up for, and no forms were submitted. Tags:
- **FACT**: sourced or observed live.
- **INFERENCE**: reasoned from facts.
- **HYPOTHESIS**: unverified.

Verdict scale: **VERIFIED** / **VERIFIED-BUT-CONSTRAINED** / **PLAUSIBLE-UNTESTED** / **UNSUPPORTED**.

---

## 1. Air quality for Indian cities right now

### Takeaway
No free, keyless API gives *live* CPCB station readings that we could verify today.
- **Keyless and live:** Open-Meteo's CAMS model (0.4° ≈ 45 km, 3-hourly, ~4.5 days of usable forecast) and FIRMS's public 24-hour fire CSVs.
- **Real CPCB/DPCC/IITM station data:** the keyless OpenAQ S3 archive has it, but its newest file was ~4 days old (2026-10-05).
- **Need a key we did not obtain:** the OpenAQ v3 API (free sign-up) and WAQI. The WAQI `demo` token only ever returns Shanghai.
- **Not usable:** data.gov.in's real-time AQI says it has no API, and its API host timed out.

### Cited Findings

**Verdict summary**

| Source | Auth / billing | India coverage observed | Freshness observed | Verdict |
|---|---|---|---|---|
| Open-Meteo Air Quality (CAMS global) | None (non-commercial) | Any lat/lon; Delhi grid point 28.60, 77.20 | Current 13:30 IST value; non-null forecast to 13 Oct 17:00 | VERIFIED-BUT-CONSTRAINED (model, coarse) |
| OpenAQ v3 API | Free API key required (`X-API-Key`) | Not testable without key | Not testable | PLAUSIBLE-UNTESTED |
| OpenAQ S3 archive | None (public bucket, HTTPS listing works) | DPCC, CPCB and IITM stations in Delhi and Pune confirmed | Latest daily file 2026-10-05 (~4 days lag); 15-min rows | VERIFIED-BUT-CONSTRAINED (lag) |
| WAQI `demo` token | Demo token | Returns Shanghai for Delhi, geo and "here" | n/a | UNSUPPORTED |
| WAQI with own token | Free token (name + email + ToS) | Not tested | Not tested | PLAUSIBLE-UNTESTED (restrictive terms) |
| data.gov.in real-time AQI | Page says the API does not exist | n/a | Host timed out | UNSUPPORTED |
| Google Air Quality API | Billing account required | Not tested | Not tested | PLAUSIBLE-UNTESTED (billing-gated) |
| NASA FIRMS API | Free MAP_KEY by email | Not tested with key | n/a | PLAUSIBLE-UNTESTED |
| NASA FIRMS public 24 h CSV | None | South Asia file; India detections present | Latest SNPP detection 11:29 IST today | VERIFIED |

**Open-Meteo Air Quality API: live call (FACT)**
- URL called: `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=28.61&longitude=77.21&hourly=pm2_5,pm10,us_aqi,european_aqi,nitrogen_dioxide&current=pm2_5,pm10,us_aqi&forecast_days=7&timezone=Asia/Kolkata`
- **Auth and grid:** HTTP 200 with no key. The returned grid point was 28.599998, 77.20001.
- **Current block:** `time 2026-10-09T13:30`, `interval 3600`, PM2.5 47.1 µg/m³, PM10 77.5 µg/m³, US AQI 164.
- **Hourly series:**
  - 168 hourly steps, 2026-10-09T00:00 to 2026-10-15T23:00.
  - **Only 114 PM2.5 values are non-null; the last is 2026-10-13T17:00.** Asking for 7 days yields ~4.5 days of usable forecast.
- **Sample, 9 Oct (PM2.5 / PM10 / NO₂):**

  | Hour (IST) | PM2.5 | PM10 | NO₂ |
  |---|---|---|---|
  | 10:00 | 78.7 | 211.4 | 20.2 |
  | 14:00 | 45.4 | 74.3 | 13.6 |
  | 19:00 | 57.6 | 161.1 | 28.0 |

  The intraday pattern is visible, but at 45 km resolution.
- **Docs:** the global domain is "CAMS Global Atmospheric Composition Forecasts" at "0.4° (~45 km)", "3-Hourly", updated "Every 12 hours, 5 days forecast". `forecast_days` accepts 0–7 and `past_days` 0–92. Attribution to CAMS and Open-Meteo is mandatory, and the service is free for non-commercial use — [Open-Meteo AQ docs](https://open-meteo.com/en/docs/air-quality-api)
- **Usage limits:** non-commercial use is capped at "<10'000 API calls per day, 5'000 per hour and 600 per minute" (300,000 per month). Data is under CC BY 4.0. Educational and non-profit apps with no ads or subscriptions count as non-commercial — [Open-Meteo terms](https://open-meteo.com/en/terms)

**OpenAQ v3 API (FACT)**
- URL called: `https://api.openaq.org/v3/locations?coordinates=28.61,77.21&radius=25000&limit=5`
- Response body: `{"message": "Unauthorized. A valid API key must be provided in the X-API-Key header."}`
- **Docs:**
  - The API "uses API keys to authenticate requests"; requests without a key are denied.
  - Keys come from registering at explore.openaq.org/register and are sent in `X-API-Key`.
  - Rate-limit numbers are on a separate page that was not captured.
  - [OpenAQ API key docs](https://docs.openaq.org/using-the-api/api-key)
- A cross-origin `fetch()` from another origin also failed (CORS on the 401). A browser front-end would need a proxy such as Lambda anyway, because the key must not be shipped to clients (INFERENCE).

**OpenAQ S3 archive on AWS Open Data: live listing and file reads (FACT)**
- **Listing URL pattern:** `https://openaq-data-archive.s3.amazonaws.com/?list-type=2&prefix=records/csv.gz/locationid=<ID>/year=2026/month=10/`. Files were read at `https://openaq-data-archive.s3.amazonaws.com/records/csv.gz/locationid=<ID>/year=2026/month=10/location-<ID>-20261005.csv.gz`, gunzipped in-browser.
- **No auth.** The bucket root lists only the `records/` prefix, so there is **no station index file**. You need location IDs from the API (key) or from elsewhere.
- **Indian stations confirmed, with the latest file on 9 Oct ≈ 14:30 IST = 2026-10-05 for all:**

  | ID | Station | First row in the 2026-10-05 file | Rows that day |
  |---|---|---|---|
  | 50 | "Punjabi Bagh, Delhi - DPCC" | PM10 251.0 µg/m³ at 2026-10-05T03:30+05:30 | 949 |
  | 235 | "Anand Vihar, New Delhi - DPCC" | PM10 202.0 | 969 |
  | 5626 | "DTU, New Delhi - CPCB" | PM10 287.0 | 872 |
  | 6356 | "Pusa, Delhi - DPCC" | PM10 183.0 | 989 |
  | 10486 | "Mundka, Delhi - DPCC" | PM10 349.0 | 923 |
  | 11603 | "Chandni Chowk, Delhi - IITM" | PM10 334.6 | 967 |
  | 11613 | "Revenue Colony-Shivajinagar, Pune - IITM" | PM10 55.68 | 649 |

- **Row format and cadence:** each row has `location_id, sensors_id, location, datetime, lat, lon, parameter, units, value`. Timestamps run at 15-minute steps (e.g. `…T23:45:00+05:30`, `…T00:00:00+05:30`). Parameters include PM10, CO (ppb) and others.
- **Location 8118 "New Delhi-8118"** (28.63576, 77.22445; PM2.5 only) has its **last file on 2026-09-24**, ending 16:00 IST. That feed appears to have stopped.
- Registry entry: [OpenAQ on AWS Open Data](https://registry.opendata.aws/openaq/). Per-provider licences vary, as already noted in 03_PROBLEM_LANDSCAPE.

**WAQI / aqicn (FACT)**
- **URLs called, all HTTP 200 with `"status":"ok"` but Shanghai data:**
  - `https://api.waqi.info/feed/delhi/?token=demo`
  - `https://api.waqi.info/feed/geo:28.61;77.21/?token=demo`
  - `https://api.waqi.info/feed/here/?token=demo`
  - `https://api.waqi.info/feed/shanghai/?token=demo`
- **Every call returned identical Shanghai data:** `idx 1437`, `"city":{"name":"Shanghai (上海)"}`, `aqi 61`, `dominentpol o3`, `pm25 34`, `time "2026-10-09 15:00:00" +08:00`.
- **The demo token cannot serve India.**
- **Token and terms:**
  - A token needs name, email and ToS agreement.
  - "The default quota is 1,000 (one thousand) requests per second".
  - "The data can not be used in paid applications or services".
  - "can not be redistributed as cached or archived data".
  - "Attribution to the World Air Quality Index Project as well as originating EPA is mandatory".
  - Public use by a non-profit "requires prior notification (by email)".
  - Sources: [aqicn API](https://aqicn.org/api/); [token page](https://aqicn.org/data-platform/token/)

**data.gov.in real-time AQI (FACT)**
- Resource page: "The API for this resource does not exist. Please click the 'Request API' button…". Granularity is listed as "Hourly" — [data.gov.in resource](https://www.data.gov.in/resource/real-time-air-quality-index-various-locations)
- URL called: `https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?format=json&limit=3`. Result: browser `ERR_CONNECTION_TIMED_OUT` after 50 s; the shell returned a proxy 403.
- Caveat: the resource ID was recalled from memory and was not confirmed on the page (HYPOTHESIS that it is the AQI resource).

**Google Air Quality API (FACT, docs only)**
- You must "enable billing" on the project and send an API key or OAuth token.
- "query rate limit of 6,000 requests per minute for each API method".
- The $200 monthly credit ran "until February 28, 2025", replaced by free usage thresholds whose value was not shown.
- [Google AQ usage and billing](https://developers.google.com/maps/documentation/air-quality/usage-and-billing)

**NASA FIRMS (FACT)**
- **API without a key:** URL `https://firms.modaps.eosdis.nasa.gov/api/area/csv/NOKEY/VIIRS_SNPP_NRT/68,6,98,37/1` returned `Invalid MAP_KEY.`
- **MAP_KEY page:** "sign up for free MAP_KEY using your email"; "MAP_KEY limit is 5000 transactions / 10-minute interval. Larger transactions may count as multiple requests (ex. requesting 7 days)" — [FIRMS map_key](https://firms.modaps.eosdis.nasa.gov/api/map_key/)
- **Keyless public 24-hour CSVs:** read on 9 Oct ~14:30 IST, all HTTP 200. The India box was a crude 6–37°N, 68–97.5°E; the "Punjab box" was 29.5–32.5°N, 73.8–77°E. Both boxes include parts of neighbouring countries.

  | File | Total detections | India box | Punjab box | Acquisition window (UTC) |
  |---|---|---|---|---|
  | `https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_Asia_24h.csv` | 1,006 | 715 | 28 | 2026-10-08 06:16 to **2026-10-09 05:59** (= 11:29 IST today) |
  | `…/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_Asia_24h.csv` | 1,260 | 934 | 38 | latest 2026-10-08 22:29 |
  | `…/modis-c6.1/csv/MODIS_C6_1_South_Asia_24h.csv` | 203 | 142 | — | latest 2026-10-09 04:38 |

- **Sample VIIRS row:** `30.23278,76.06738,333.22,0.43,0.38,2026-10-08,0803,N,nominal,2.0NRT,293.31,2.81,D`, i.e. lat, lon, bright_ti4, scan, track, acq_date, acq_time UTC, satellite, confidence, version, bright_ti5, FRP (MW), day/night.

### Inferences
- **For a "right now, near me" air number:**
  - The only verified keyless live option is Open-Meteo's CAMS forecast. It is a 45 km model, not a measurement, so label it on screen as "model estimate".
  - **US AQI 164 with an instantaneous PM2.5 of 47 µg/m³** is consistent with US AQI being computed on a trailing 24 h average (early-morning PM2.5 was ~79). Users will see an AQI that disagrees with the hourly PM2.5.
- **For real station observations:**
  - The OpenAQ S3 archive gives genuine CPCB/DPCC/IITM data at 15-minute resolution, keyless, on AWS. That makes it a good "AWS Open Data" story for baselines and history.
  - Its ~4-day lag rules it out as "live".
  - Getting live station values needs a free OpenAQ key, obtained by a team member (HYPOTHESIS that API latency is about 1–2 h; not tested).
- **WAQI terms** forbid caching or archiving and require prior notice for non-profit public use. That is a poor fit for a 48-hour hackathon with a public repo.
- **FIRMS 24-hour CSVs** are a strong, keyless, near-real-time "stubble fire" signal for Punjab/Haryana in October. Stubble-burning season is under way: 28–38 VIIRS detections fell in the Punjab box in 24 h.

### Gaps
- OpenAQ v3 rate limits and actual API freshness for Indian CPCB stations were not captured (no key; the rate-limits page was not fetched).
- Whether the S3 archive lag is always ~4 days or varied today; only one snapshot was taken.
- Mumbai and Bengaluru station IDs in OpenAQ were not identified. Only Delhi and Pune were probed, by guessed IDs.
- data.gov.in: whether any other CPCB dataset has a working API, and whether the API host is reachable from AWS ap-south-1 (it timed out from the user's network).
- Google Air Quality API per-1,000 pricing and India-specific pricing were not captured.

---

## 2. Weather and heat

### Takeaway
Open-Meteo is fully VERIFIED for India with no key:
- **Forecast:** 16-day hourly, including `wet_bulb_temperature_2m`, `apparent_temperature`, `uv_index` and `shortwave_radiation`.
- **Archive:** data through yesterday.
- **Flood (GloFAS v4):** 5 km, daily, real discharge for the Ganga at Patna.

The limit is that 15-minute data and "nowcasts" for India are **interpolated hourly**, not native. There is no true precipitation nowcast.

### Cited Findings

**Verdict summary**

| Source | Auth | Granularity verified | Verdict |
|---|---|---|---|
| Open-Meteo Forecast | None | Hourly × 16 days; current at 15-min interval; Delhi and Chennai | VERIFIED |
| Open-Meteo Historical | None | Daily through 2026-10-08 (yesterday) | VERIFIED |
| Open-Meteo Flood (GloFAS v4) | None | Daily; past 3 days + 7-day forecast at Patna | VERIFIED |
| Open-Meteo 15-minutely (India) | None | Returns 96 steps per day, but interpolated from hourly | VERIFIED-BUT-CONSTRAINED |

**Forecast, Delhi (FACT)**
- URL called: `https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.21&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,wet_bulb_temperature_2m,uv_index,shortwave_radiation,precipitation&current=temperature_2m,apparent_temperature,relative_humidity_2m&forecast_days=16&timezone=Asia/Kolkata`
- **Response:** HTTP 200; grid 28.576448, 77.18678; elevation 217 m; 384 hourly steps to 2026-10-24T23:00. All 384 `wet_bulb_temperature_2m` and `uv_index` values are non-null.
- **Current, 2026-10-09T14:00 (interval 900):** 31.8 °C, RH 49 %, apparent temperature 35.0 °C.
- **Hourly values:**

  | Time (IST) | Temp | RH | Apparent | Wet-bulb | UV | Shortwave |
  |---|---|---|---|---|---|---|
  | 9 Oct 14:00 | 32.0 °C | 47 % | 34.9 °C | 23.4 °C | 4.6 | 600 W/m² |
  | 10 Oct 13:00 | 32.1 °C | 46 % | 35.3 °C | 23.3 °C | 5.45 | 708 W/m² |

**Forecast, Chennai (FACT)**
- URL called: `https://api.open-meteo.com/v1/forecast?latitude=13.08&longitude=80.27&hourly=temperature_2m,apparent_temperature,wet_bulb_temperature_2m,uv_index,shortwave_radiation&current=temperature_2m,apparent_temperature,wet_bulb_temperature_2m&forecast_days=3&timezone=Asia/Kolkata`
- Grid 13.110721, 80.2459.
- Current at 14:00: 33.0 °C, apparent 36.5 °C, **wet-bulb 25.2 °C**. Wet-bulb works in `current` even though the docs list it only for hourly and daily.
- Hourly values:

  | Time (IST) | Temp | Apparent | Wet-bulb | UV | Shortwave |
  |---|---|---|---|---|---|
  | 9 Oct 14:00 | 32.8 °C | 36.4 °C | 25.3 °C | 6.2 | 646 W/m² |
  | 10 Oct 12:00 | 33.6 °C | 38.1 °C | 24.8 °C | 8.55 | 892 W/m² |

**15-minutely data (FACT)**
- URL called: `https://api.open-meteo.com/v1/forecast?latitude=13.08&longitude=80.27&minutely_15=precipitation,temperature_2m&forecast_days=1&timezone=Asia/Kolkata`. It returned 96 steps, e.g. 14:00 33.0 °C, 14:15 32.9, 14:30 32.8, 14:45 32.7; precipitation 0.
- Docs: 15-minutely is "Only available in Central Europe and North America. Other regions use interpolated hourly data." Forecasts go up to 16 days. Best Match picks "the highest-resolution applicable model" per location; global models include ECMWF IFS 9 km and GFS 0.11–0.25° — [Open-Meteo forecast docs](https://open-meteo.com/en/docs)

**Historical / archive (FACT)**
- URL called: `https://archive-api.open-meteo.com/v1/archive?latitude=28.61&longitude=77.21&start_date=2026-09-25&end_date=2026-10-08&daily=temperature_2m_max,precipitation_sum&timezone=Asia/Kolkata`
- HTTP 200 with all 14 days, **including yesterday, 2026-10-08**.
- Tmax ran 31.2 (25 Sep), 28.2 (28 Sep), 35.7 (5 Oct), 33.5 (8 Oct). Precipitation was 4.6 mm on 26 Sep.
- Docs:
  - ERA5 is 0.25°, "Daily with 5 days delay"; ERA5-Land is 0.1°, also 5 days delay.
  - ECMWF IFS 9 km is "Every 6 hours with no delay".
  - "The default Best Match combines IFS HRES, ERA5 and ERA5-Land seamlessly."
  - Data goes back to 1940.
  - [Open-Meteo historical docs](https://open-meteo.com/en/docs/historical-weather-api)

**Flood API (GloFAS) (FACT)**
- URL called: `https://flood-api.open-meteo.com/v1/flood?latitude=25.61&longitude=85.14&daily=river_discharge,river_discharge_mean,river_discharge_max&past_days=3&forecast_days=7`. Patna was snapped to 25.625, 85.125.
- `river_discharge` (m³/s), from observed to forecast:

  | Date | Discharge | Note |
  |---|---|---|
  | 2026-10-06 | 31,987.96 | |
  | 2026-10-07 | 29,647.32 | |
  | 2026-10-08 | 27,732.19 | |
  | **2026-10-09** | **26,060.53** | today |
  | 2026-10-12 | 21,927.05 | |
  | 2026-10-15 | 18,449.15 | ensemble max 18,662.79 |

- Docs:
  - GloFAS v4 is 0.05° (~5 km), daily, with a 30-day forecast plus a 7-month seasonal outlook and 50 ensemble members.
  - The reanalysis runs 1984 to July 2022.
  - "Due to the 5 km resolution the closest river might not be selected correctly".
  - The forecast-length statements on the page are internally inconsistent (92 vs 210 days vs 12 months).
  - [Open-Meteo flood docs](https://open-meteo.com/en/docs/flood-api)

### Inferences
- Wet-bulb, apparent temperature, UV and shortwave radiation are all available hourly for 16 days at ~9–11 km. That is enough to drive a WBGT estimate (e.g. ECMWF thermofeel, Apache-2.0, per 03_PROBLEM_LANDSCAPE) for any Indian worksite or school.
- The recession at Patna (32k → 18k m³/s over 10 days) shows the flood API returns real, changing values for major Indian rivers. It is useful for "post-monsoon recession" or riverine-risk demos, not for urban waterlogging.
- Urban waterlogging needs rainfall intensity at sub-hourly, sub-km resolution. Open-Meteo cannot provide that for India, because its 15-minute data is interpolated.

### Gaps
- Which model Best Match actually uses for India: the response did not state it (it could be inferred from the grid spacing). The docs do not name India.
- IMD APIs and nowcasts were not tested in this session.
- Whether Open-Meteo's rate limits would be shared across all users of a deployed app. Calls from a Lambda share one IP; calls from browsers spread across IPs (INFERENCE).

---

## 3. Electricity grid carbon intensity and demand for India

### Takeaway
**Grid-India's daily PSP report is the standout verified source.**
- It is a public, keyless XLS published each morning for the previous day.
- It includes a **15-minute all-India SCADA time series** of demand, thermal, gas, nuclear, hydro, wind and solar MW, plus regional and state energy and source-wise generation.
- From it you can compute a real D-1 intraday carbon-intensity curve for India.

Electricity Maps has five Indian regional zones, but every data endpoint needs an auth token. The free-tier terms are unclear. WattTime was not verifiable.

### Cited Findings

**Verdict summary**

| Source | Auth / billing | India granularity | Freshness | Verdict |
|---|---|---|---|---|
| Grid-India daily PSP (XLS) | None | All-India 15-min by fuel; regional and state daily | Previous day, posted the next morning | VERIFIED-BUT-CONSTRAINED (D-1; scrape; no licence stated) |
| Electricity Maps API | Auth token required; free tier for "individual users and developers" | Zones IN-NO, IN-WE, IN-SO, IN-EA, IN-NE (TIER_A) | Not testable | PLAUSIBLE-UNTESTED |
| WattTime | Unknown | Unknown | Unknown | PLAUSIBLE-UNTESTED (docs did not render) |
| CEA emission factor | Public PDF | National | Annual | VERIFIED earlier (03 doc), not re-fetched |

**Grid-India daily PSP: live fetch and parse (FACT)**
- **Listing page:** `https://grid-india.in/en/reports/daily-psp-report`.
  - It shows "08.10.26_NLDC_PSP" posted "09-10-2026" as both XLS (~300 KB) and PDF (~2 MB), with daily history back through September.
  - The listing is loaded from `https://webapi.grid-india.in/api/v1/file`.
  - File names carry a random suffix (e.g. `_724`), so the listing must be scraped to get the URL.
- **File fetched:** `https://webcdn.grid-india.in/files/grdw/2026/10/08.10.26_NLDC_PSP_724.xls`. HTTP 200, `application/vnd.ms-excel`, 314,880 bytes, OLE2 magic `d0 cf 11 e0`. It was parsed with SheetJS 0.18.5.
- **Sheets:** `MOP_E, MOP_E1, IR-Line, CrossBorder, TimeSeries`.
- **Key values for 8 Oct 2026 (MOP_E):**
  - **Demand:**
    - All-India demand met at the 19:00 evening peak was **233,690 MW**, with a shortage of 4,732 MW.
    - Maximum demand met during the day was **260,724 MW at 15:48**, in the "Solar hr", with 0 shortage. The non-solar-hour maximum was 235,276 MW, with a 4,731 MW shortage.
    - Energy met was **5,466.07 MU**.
  - **Source-wise gross generation, 5,871 MU in total:**

    | Source | MU | Share |
    |---|---|---|
    | Coal | 4,002.36 | 68.15 % |
    | Lignite | 70.53 | 1.20 % |
    | Hydro | 525.57 | 8.95 % |
    | Nuclear | 181.93 | 3.10 % |
    | Gas, naphtha and diesel | 175.56 | 2.99 % |
    | RES | 915 | 15.61 % |

    Within RES, solar was 725.85 MU and wind 151.29 MU. The non-fossil share was **27.65 %**.
  - **State rows** (state max demand MW / energy MU), for example:

    | State | Max demand (MW) | Energy (MU) |
    |---|---|---|
    | Delhi | 6,186 | 130.52 |
    | UP | 23,734 | 450.54 |
    | Maharashtra | 32,389 | 675.3 |
    | Tamil Nadu | 20,618 | 424.54 |
    | Karnataka | 17,519 | 334.71 |

- **TimeSeries sheet:** "15 Min (INSTANTANEOUS) ALL INDIA GRID FREQUENCY, GENERATION & DEMAND MET (SCADA DATA)". Columns: TIME, frequency, demand met, storage demand, nuclear, wind, solar, hydro, gas, thermal, storage, others, net demand met, total generation, transnational exchange.
  - **09:45:** demand 252,127 MW, solar 80,062 MW, thermal 142,790 MW, total generation 252,603 MW.
  - **23:45:** demand 219,719 MW, solar 0, thermal 168,320.6 MW, total 220,984 MW.
- **Disclaimer in the file:**
  - "data is provided 'as is'".
  - "subject to errors due to telemetry loss/freeze".
  - Demand and RE are "incident on transmission system… behind the meter (BTM) generation excluded", so rooftop solar is not in these numbers.
- No licence is stated on the file or the page (gap).

**Electricity Maps (FACT)**
- `https://api.electricitymap.org/v3/carbon-intensity/latest?zone=IN-NO` returned `{"error":"Invalid auth-token","message":"Please provide a valid authentication header…"}`.
- `https://api.electricitymap.org/v3/zones` returned HTTP 200 without auth. India appears as "IN" (Mainland India) with `subZoneKeys` IN-EA, IN-NE, IN-NO, IN-SO, IN-WE, each `tier: "TIER_A"` and `isCommerciallyAvailable: true`.
- **Free tier:**
  - "Free for individual users and developers. For commercial use, check prices"; "can be used for free by developers for applications outside of their commercial workplace".
  - Endpoints and limits are not stated, and the page mentions a "free 30-day trail" — [Electricity Maps free tier](https://electricitymaps.com/free-tier)
  - The pricing page lists only paid plans (e.g. "€6,000 / Year" per signal) and a "14-day trial… No payment information required". This contradicts the 30-day figure — [Electricity Maps pricing](https://www.electricitymaps.com/pricing)

**WattTime (gap)**
- `https://docs.watttime.org/` rendered no content via WebFetch, so India coverage was not verified.

**CEA emission factor (FACT, from 03_PROBLEM_LANDSCAPE, not re-fetched)**
- 0.710 tCO₂/MWh (FY24-25) and 0.675 (FY25-26) — [CEA CO₂ baseline v22 user guide](https://cea.nic.in/wp-content/uploads/baseline/2026/09/User_Guide__Version_22.0.pdf)

**Time-of-day tariffs (FACT from 03, not re-verified)**
- Since 1 Apr 2025, ToD tariffs apply to smart-metered non-agricultural consumers: solar hours 10–20 % cheaper, peak 10–20 % dearer — [EastMojo](https://eastmojo.com/national/2023/06/23/new-power-tariff-rule-save-up-to-20-for-usage-during-solar-hours/). State orders were not checked this session.

### Inferences
- **A D-1 carbon curve is computable.** A 15-minute all-India "grid carbon curve" for yesterday comes from Grid-India TimeSeries by weighting thermal and gas MW with emission factors.
  - Thermal share of generation was ~56.5 % at 09:45 (142,790 / 252,603) vs ~76.2 % at 23:45 (168,321 / 220,984).
  - That is a large solar-hour dip, which supports "shift load to solar hours" nudges (EV charging, ACs, pumps). It is consistent with the ToD tariff logic.
- **Freshness is yesterday's data only.** Any "now" claim has to be a forecast or a typical-day profile, labelled as such.
- **Lambda pipeline:** EventBridge Scheduler (daily) triggers a Lambda to scrape the listing, download the XLS, parse it and store to S3/DynamoDB. That is a clean, visible AWS pipeline, and the file is small (~300 KB).
- **Regional granularity:** Electricity Maps' regional zones would add NO/WE/SO/EA/NE carbon signals. Without a token tested, treat it as optional.

### Gaps
- Licence and terms of use for Grid-India reports (none seen).
- Whether Grid-India or Vidyut PRAVAH/MERIT expose a real-time (same-day) machine-readable feed; not checked.
- Electricity Maps free-tier endpoint list, history depth, request limits and India availability on the free tier.
- WattTime India coverage.
- State DISCOM ToD tariff orders (e.g. DERC, MERC, BESCOM) in machine-readable form; not researched in the timebox.

---

## 4. Mobility

### Takeaway
**What works today, keyless:**
- **OSRM** public demo routing returns Indian routes.
- **Overpass (OSM)** works, but the public server returned 504 for 2 of 4 city queries.
- **Bengaluru BMTC GTFS** is current as a community feed via Mobility Database (dated Sep 2026, valid to Sep 2027).

**Gated or stale:**
- **Delhi OTD:** static GTFS is form-gated and last updated June 2024; real-time needs registration with a phone number.
- **Amazon Location Service:** documented in ap-south-1 with "Good" India routing and "Comprehensive" address coverage, but untestable here.
- **Google Routes:** needs billing.

### Cited Findings

**Verdict summary**

| Source | Auth | India result | Verdict |
|---|---|---|---|
| OSRM public demo | None | Delhi route OK | VERIFIED-BUT-CONSTRAINED (demo server, free-flow) |
| Overpass API (overpass-api.de) | None | Bengaluru and Mumbai OK; Delhi and Chennai 504 | VERIFIED-BUT-CONSTRAINED (load-dependent) |
| Delhi OTD static GTFS | Purpose form + T&C (not submitted) | Counts visible; last updated 20 Jun 2024 | PLAUSIBLE-UNTESTED |
| Delhi OTD GTFS-realtime | Registration with name, email and phone for key | n/a | PLAUSIBLE-UNTESTED |
| BMTC GTFS (Mobility Database mdb-2595) | None | Latest 8 Sep 2026; valid to 7 Sep 2027 | PLAUSIBLE-UNTESTED (metadata verified, zip not downloaded) |
| Amazon Location Service | AWS account | ap-south-1 endpoints; India coverage "Good" | PLAUSIBLE-UNTESTED (docs only) |
| Google Routes API | Billing required | n/a | PLAUSIBLE-UNTESTED (billing-gated) |

**OSRM (FACT)**
- URL called: `https://router.project-osrm.org/route/v1/driving/77.2090,28.6139;77.0688,28.5562?overview=false`
- Response: `"code":"Ok"`, distance **22,473.2 m**, duration **1,636.8 s** (27.3 min). The origin snapped to "Kartavya Path".
- It is CORS-enabled (called cross-origin from a page).

**Overpass (FACT)**
- **First call:** `https://overpass-api.de/api/interpreter?data=[out:json][timeout:25];area["name"="Bengaluru"]["boundary"="administrative"]->.a;(node["amenity"="recycling"](area.a);way["amenity"="recycling"](area.a););out count;` (URL-encoded)
  - Result: 61 nodes + 19 ways = **80** recycling amenities.
  - `timestamp_osm_base 2026-10-09T08:33:11Z`; "made available under ODbL".
- **Second batch** (recycling / recycling with `recycling:electrical_appliances=yes` / `waste_basket` / `drinking_water`):

  | City | Recycling | E-waste | Waste baskets | Drinking water | Result |
  |---|---|---|---|---|---|
  | Bengaluru | 80 | 0 | 493 | 116 | OK |
  | Mumbai | 4 | 1 | 158 | 76 | OK |
  | Delhi | — | — | — | — | HTTP 504, "server is probably too busy" |
  | Chennai | — | — | — | — | HTTP 504, "server is probably too busy" |

  Snapshot timestamp 2026-10-09T08:42:16Z.

**Delhi Open Transit Data (FACT)**
- `https://otd.delhi.gov.in/data/static/` shows: STOPS 3,464; ROUTES 543; STOP TIMES 378,324; TRIPS 16,562; each "Last Updated: June 20, 2024".
- "Download Data" opens a modal form: "Kindly state purpose…", Usage Type (Commercial / Non-Commercial), Purpose (Academia, R&D…), "By clicking this, you agree to our Terms and Conditions". It was not submitted.
- `https://otd.delhi.gov.in/data/realtime/` shows "Request For API Access and API Private Key" with Name, Email and Contact Number fields.
- DMRC static data (`/data/staticDMRC`) sits behind the same purpose form.
- Terms are a PDF at `https://otd.delhi.gov.in/terms`.

**BMTC (FACT)**
- Mobility Database lists "Bangalore Metropolitan Transport Corporation (BMTC) GTFS Schedule feed (Community Feed)":
  - Latest download "Tue Sep 08 2026"; service range "Sep 7, 2026" to "Sep 7, 2027"; validator 8.0.1 "No errors".
  - Producer URL `https://github.com/Vonter/bmtc-gtfs/raw/refs/heads/main/gtfs/bmtc.zip`; licence not stated.
  - [Mobility Database mdb-2595](https://mobilitydatabase.org/feeds/gtfs/mdb-2595)
- BMTC and BMRCL first published GTFS (routes, stops, schedules, fares), hosted by DULT, per a report of 22 Aug 2024; licence not mentioned — [Deccan Herald](https://www.deccanherald.com/amp/story/india/karnataka/bengaluru/in-historic-first-namma-metro-bmtc-open-up-their-data-to-help-public-transport-users-in-bengaluru-3160955)

**Amazon Location Service (FACT, docs)**
- **Endpoints:** ap-south-1 has Maps (`maps.geo.ap-south-1.api.aws`), Places, Routes, Geofences, Trackers and Metadata — [AWS endpoints: Location](https://docs.aws.amazon.com/general/latest/gr/location.html)
- **India coverage (IND):**
  - Maps "Good", Route "Good", Places point address "Comprehensive", POI "Good".
  - Car and scooter routing "Good"; truck routing "Unsupported".
  - Traffic "Flow" in Central, North and South India.
  - Address validation is not available for India.
  - [Amazon Location data quality and coverage](https://docs.aws.amazon.com/location/latest/developerguide/data-quality.html)
- The underlying data provider is not named on that page.

**Google Routes (FACT, docs)**
- "you must enable billing on each of your projects" — [Routes usage and billing](https://developers.google.com/maps/documentation/routes/usage-and-billing)

### Inferences
- **Amazon Location Service** gives the "meaningful AWS" box for routing and geocoding in India, including scooter routing (relevant to two-wheeler commuters and gig riders), at no extra third-party sign-up. OSRM is a keyless fallback for development.
- **OSM coverage of recycling points is very sparse** (Mumbai: 4; e-waste: 0–1). A waste-drop-off map built on OSM alone would look empty in a demo.
- **The public Overpass server is not reliable enough to call live during a recorded demo.** Pre-fetch to S3 instead.
- **Transit-aware concepts are easiest in Bengaluru**, where the GTFS is current and downloadable without a form. Delhi's static data is over two years old and needs a form submission by a human teammate.

### Gaps
- Mumbai (BEST, Mumbai Metro) GTFS availability was not researched.
- Delhi OTD real-time feed freshness and licence are behind registration.
- The OSRM demo server usage policy was not fetched. Known informally: light use only, no SLA (HYPOTHESIS).
- Whether Amazon Location Routes v2 returns sensible Indian routes and travel times: not callable here.
- Google Routes per-1,000 pricing (India price list) was not captured.

---

## 5. Personal devices and phone sensors

### Takeaway
**What a web app can use:**
- **Geolocation and DeviceMotion:** DeviceMotion needs an explicit permission call on iOS 14.5+, and per BCD also in Chrome 152.
- **Web Bluetooth** works only in Chromium browsers (Chrome desktop/Android, Edge, Samsung Internet), not Safari, iOS or Firefox. It is experimental.

**Wearable cloud APIs are effectively closed to us this weekend:**
- **Fitbit Web API:** support ended 30 Sep 2026; turned off 30 Oct 2026. Its successor, Google Health API, is "not onboarding new projects".
- **Garmin:** business-only.
- **Strava:** API terms since 1 Jun 2026 prohibit using its data in any AI application, and new apps are capped at 1 athlete.

User-exported files are the realistic route for personal data.

### Cited Findings

**Verdict summary**

| Source | Access | Verdict |
|---|---|---|
| Web Bluetooth (Heart Rate GATT) | Chromium only; experimental; secure context; user gesture | VERIFIED-BUT-CONSTRAINED (no iOS) |
| DeviceMotionEvent | Broad support; `requestPermission()` on iOS 14.5+ and Chrome 152 | VERIFIED (BCD data) |
| Geolocation | Secure context; standard | PLAUSIBLE-UNTESTED (not re-checked) |
| Fitbit Web API → Google Health API | Legacy off 30 Oct 2026; new projects not onboarded; restricted scopes | UNSUPPORTED |
| Garmin Connect Developer Program | "only for business use" | UNSUPPORTED |
| Strava API | OAuth; 1-athlete default; AI-use ban | UNSUPPORTED for an AI/Bedrock concept |
| Android Health Connect / Apple HealthKit | Native app needed | PLAUSIBLE-UNTESTED (not fetched) |
| Google Maps Timeline export | Device-based; export path not confirmed | PLAUSIBLE-UNTESTED |
| Apple Health export | Not researched | PLAUSIBLE-UNTESTED |

**Web Bluetooth (FACT)**
- URL called: `https://bcd.developer.mozilla.org/bcd/api/v0/current/api.Bluetooth.json` (MDN browser-compat-data). Support for `requestDevice`:

  | Browser | Supported from |
  |---|---|
  | Chrome | 56 |
  | Chrome Android | 56 |
  | Edge | 79 |
  | Samsung Internet | 6.0 |
  | Firefox | false |
  | Firefox Android | false |
  | Safari | false |
  | Safari iOS | false |

  Status is `experimental: true`.
- MDN: "can only be used in a secure context". A new-device prompt requires transient activation, i.e. a user gesture — [MDN Web Bluetooth](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)

**DeviceMotionEvent (FACT)**
- URL called: `https://bcd.developer.mozilla.org/bcd/api/v0/current/api.DeviceMotionEvent.json`
- Event support: Chrome 31, Chrome Android 31, Firefox 6, Safari 17, Safari iOS 4.2.
- `requestPermission_static`: Safari iOS 14.5, Chrome 152, Chrome Android 152. It is not supported in Firefox or Samsung Internet.

**Fitbit and Google Health API (FACT)**
- The page says the Fitbit Web API "is now called the Google Health API".
- "Support for the Fitbit Web API ends" **September 30, 2026**; it "will be turned off" **October 30, 2026**.
- "All Google Health API scopes are categorized as Restricted, necessitating a privacy and security review".
- "we are not onboarding new projects at this time".
- [Google Health API: about](https://developers.google.com/health/about)

**Garmin (FACT)**
- The program "is available for enterprise use" and "it is only for business use".
- Approval status comes "within two business days"; a "typical integration takes between 1 and 4 weeks".
- [Garmin program FAQ](https://developer.garmin.com/gc-developer-program/program-faq/)

**Strava (FACT)**
- **Policy effective June 1, 2026:**
  - §5.3: you may not use Strava data "in connection with the development, training, evaluation, or operation of any AI Application". The Strava MCP is excepted.
  - §2.3/6.1: you may not display other users' data.
  - §6.2: no caching beyond "seven (7) days".
  - §3.3: Standard tier needs "an active Strava subscription".
  - [Strava API policy](https://www.strava.com/legal/api_policy)
- **Rate limits:** 200 requests per 15 min and 2,000 per day overall; 100 per 15 min and 1,000 per day non-upload. New apps get "an athlete capacity of 1" — [Strava rate limits](https://developers.strava.com/docs/rate-limits/)
- A third-party summary adds that some club and segment endpoints were removed on 1 Sep 2026, and a new base URL arrives in 2027 — [Terra blog, 6 Sep 2026](https://tryterra.co/blog/strava-api-changes-2026). This is a secondary source.

**Google Maps Timeline (FACT, partial)**
- Timeline data "comes directly from your device"; Timeline is not available on computers; an encrypted backup can go to Google servers — [Google Maps help](https://support.google.com/maps/answer/6258979?hl=en)
- The fetched pages did not describe an export method or format — [Google account help](https://support.google.com/accounts/answer/14200149?hl=en)

### Inferences
- **Heart rate is the only realistic wearable-to-web path in 48 h,** via Web Bluetooth's standard Heart Rate Service. It works on Chrome Android or desktop with a device that advertises that service.
  - HYPOTHESIS: chest straps and some Garmin or Wear OS watches in "broadcast HR" mode do; Apple Watch and most Fitbits do not.
  - It will not work for iPhone users, so the demo must not depend on it.
- **Phone motion and location** are fine in a web app. On iOS, add a "Start sensors" button that calls `DeviceMotionEvent.requestPermission()`.
- **For personal history, prefer user-uploaded files** (GPX, Apple Health `export.zip`, Timeline JSON) parsed on AWS. Do not build OAuth integrations; all three cloud APIs are closed, ending or AI-prohibited.

### Gaps
- Samsung Health (Data SDK / partner programme) was not researched.
- Android Health Connect and Apple HealthKit docs were not fetched. That they are native-only is well known but unverified this session (HYPOTHESIS).
- The Google Timeline on-device export path and JSON format in 2026 are unconfirmed.
- Apple Health export format was not checked.
- The Geolocation BCD entry was not fetched.

---

## 6. Waste and consumption

### Takeaway
**There are no machine-readable national waste or recycler APIs.**
- **CPCB e-waste recycler lists** circulate as PDFs; the copy found is dated June 2023.
- **BEE's star-label database** is a public HTML search form with no export or API visible.
- **OSM recycling coverage** is sparse in Indian cities.

Waste concepts will rely on user-provided inputs (photos, bills) more than on live public data.

### Cited Findings

**Verdict summary**

| Source | Format / access | Verdict |
|---|---|---|
| CPCB / DPCC approved e-waste recycler lists | PDF links; CPCB list "updated on 08.06.2023" | PLAUSIBLE-UNTESTED (PDF not opened; stale) |
| BEE star label (beestarlabel.com) | Public POST search form, 40+ categories, no export | VERIFIED-BUT-CONSTRAINED (scrape only; licence unknown) |
| OSM recycling and waste amenities | Overpass; ODbL | VERIFIED-BUT-CONSTRAINED (sparse) |
| Municipal waste portals | Not researched | — |
| Electricity bill formats | Not researched | — |

**CPCB e-waste recyclers (FACT)**
- NDMC page links "CPCB approved list of E-Waste Recyclers/ Dismantler (updated on 08.06.2023)" and a "DPCC approved list of E-waste dismantlers/recyclers/refurbishers/collection center of recycler" (undated). Both are PDFs — [NDMC e-waste vendors page](https://www.ndmc.gov.in/cpcb_and_dpcc_approved_e-waste_vendors_list.aspx); [PDF](https://www.ndmc.gov.in/pdf/cpcb_approved_list_of_e-waste_recyclers_dismantler.pdf)

**BEE star label (FACT)**
- `https://www.beestarlabel.com/SearchCompare` returned "Search And Compare" with an `Equipment` dropdown. Categories include:

  | Group | Categories |
  |---|---|
  | Air conditioning | Room AC (Fixed Speed), Room AC (Variable Speed), Evaporative Air Coolers, Light Commercial AC |
  | Refrigeration | Frost Free Refrigerators, Direct Cool Refrigerators, Deep Freezers |
  | Fans and lighting | Ceiling Fan, Table/Wall Fan, Pedestal Fan, LED LAMPS |
  | Solar | Grid Connected Solar Inverter, Solar Photovoltaic, Solar Water Heater |
  | Other | Stationary Storage Type Electric Water Heater, Washing Machine, Microwave Oven, Induction Hob, Colour TV/UHD TV, Tyres |

- The form posts to `/SearchCompare`.
- There are no download, export or API links on the page; there is a manufacturer "Login".
- The search was not submitted.

**OSM counts (FACT)**
- See Section 4: Bengaluru has 80 recycling amenities and 0 tagged for e-waste; Mumbai has 4 and 1.

### Inferences
- **An appliance-energy concept** (e.g. "is my AC worth replacing?") can use BEE category rules and the user's own label photo or model number. Live lookup of BEE model data would need scraping a form. That is legally unclear and fragile for a recorded demo.
- **The recycler PDF** (2023) could be turned once into a labelled static fixture with a stated as-of date. It must not be presented as live.

### Gaps
- The CPCB EPR e-waste portal (eprewastecpcb.in) registered-recycler listing format and currency were not checked.
- SBM-Urban, municipal waste dashboards and Swachh Survekshan data APIs were not researched.
- DISCOM bill layouts (BSES, Tata Power-DDL, BESCOM, MSEDCL) and whether Textract reads them were not tested.
- BEE data licence and terms were not checked.

---

## 7. AWS capabilities relevant to these prototypes (docs only; AWS was not called)

### Takeaway
ap-south-1 (Mumbai) supports most of what a prototype needs:
- **Bedrock:**
  - **Claude Sonnet 5 / Opus 5:** In-Region via bedrock-mantle, and Geo.
  - **Claude Haiku 4.5:** Geo/Global.
  - **Nova Micro/Lite/Pro:** Geo (India) cross-region.
  - **Embedding models:** in-region.
- **AgentCore:** Runtime, Gateway, Memory, Identity, Tools, Observability, Policy and Evaluations.
- **Amazon Location:** Maps, Places and Routes, with good India coverage.
- **Polly:** Hindi and Indian-English neural voice Kajal.
- **Transcribe:** hi-IN and 10 other Indian languages, batch and streaming.

**Watch-outs:**
- On the new AWS **Free plan**, AgentCore is "Paid plan exclusive", and Free-plan accounts are limited to select services and close after 6 months or when credits run out.
- Timestream for LiveAnalytics carries an "availability change" notice.

### Cited Findings

**Bedrock models in ap-south-1 (FACT)**
- Source: [Regional availability by models (markdown)](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.md), parsed in-browser across 145 model entries.
- Geo routing covers defined geographies "(US, EU, Japan, Australia, or India)". Geo and Global are "Priced at source Region rates; no surcharge".

| Model (as named on the page) | Access from ap-south-1 |
|---|---|
| Claude Opus 5, Claude Sonnet 5 | In-Region (bedrock-mantle), Geo, Global |
| Claude Haiku 4.5 | Geo, Global |
| Claude Haiku 5.5, Sonnet 5.5, Opus 5.5, Sonnet 4.6, Opus 4.5–4.8 | Global only |
| Amazon Nova Micro / Lite / Pro | Geo only |
| Amazon Nova 2 Lite | Global only |
| Nova 2 Sonic, Nova Canvas, Nova Reel | Not listed for ap-south-1 |
| Titan Text Embeddings V2, Titan Multimodal Embeddings G1 | In-Region |
| Cohere Embed English / Multilingual | In-Region (Embed v4: Global) |
| Meta Llama 3 8B / 70B Instruct | In-Region |
| Mistral Large 3, Ministral 3 (3B/8B/14B), Voxtral Mini / Small | In-Region |
| Qwen3 VL 235B A22B; Gemma 3 4B/12B/27B; NVIDIA Nemotron Nano 12B v2 VL (vision-language) | In-Region |
| OpenAI gpt-oss-20b / 120b | In-Region |

- **Conflict:** an earlier WebFetch summary of the same page said Amazon Nova Multimodal Embeddings is In-Region in ap-south-1, but the in-browser parse did not list it. Unresolved.

**Bedrock AgentCore (FACT)**
- Mumbai is "✓ Yes" for Runtime (microVMs and Instances), Gateway, Memory, Identity, Built-in Tools, Observability, Policy, Evaluations and harness.
- It is "No" for payments, Agent Registry and the Web Search Tool.
- [AgentCore regions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html)

**AWS Free Tier (FACT)**
- **Free plan:** "up to $200 USD free credits" ($100 at sign-up plus up to $100 for activities). It is "Limited to select services only".
- "The account closes on its own 6 months after you open it or when your credits run out, whichever comes first".
- **Bedrock AgentCore is marked "Paid plan exclusive".** The page does not confirm Bedrock credit coverage on the Free plan.
- [AWS Free Tier](https://aws.amazon.com/free/)
- The rulebook adds a $25-per-team code once credits are exhausted (00_RULEBOOK.md).

**Amazon Location (FACT)**
- See Section 4: ap-south-1 endpoints for Maps, Places, Routes, Geofences and Trackers; India routing "Good" and point addresses "Comprehensive".

**Amazon Polly (FACT)**

| Language | Voice | Engines |
|---|---|---|
| hi-IN | Kajal (bilingual) | Neural |
| hi-IN | Aditi (bilingual) | Standard |
| en-IN | Kajal | Neural and Generative |
| en-IN | Raveena | Standard |
| en-IN | Aditi | Standard |

- No long-form engine is available for these voices, and no other Indian languages are listed — [Polly voices](https://docs.aws.amazon.com/polly/latest/dg/available-voices.html)

**Amazon Transcribe (FACT)**
- **Batch and streaming:** hi-IN, en-IN, bn-IN, gu-IN, kn-IN, ml-IN, mr-IN, or-IN, pa-IN, ta-IN and te-IN.
- **Streaming caveat:** for the regional languages, streaming is unavailable only in af-south-1, ap-northeast-1, ap-southeast-5, ap-southeast-7 and cn-northwest-1, so Mumbai is fine.
- **Custom language models:** hi-IN only (batch).
- [Transcribe supported languages](https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html)

**Timestream (FACT)**
- The LiveAnalytics docs carry a heading "Amazon Timestream for LiveAnalytics availability change" and recommend Timestream for InfluxDB instead — [Timestream docs](https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html)

### Inferences
- **Pick Claude Sonnet 5 (Geo/In-Region) or Nova Lite/Pro (Geo, India)** for an India-resident inference story ("data stays in India"). Global-only models such as Sonnet 5.5 and Haiku 5.5 work from Mumbai but may process data anywhere.
- **The AWS account plan matters.** Using AgentCore requires the account to be on the Paid plan (credits still apply). Plain Bedrock `InvokeModel`/`Converse` plus Lambda and Step Functions avoids that risk.
- **Avoid Timestream for time series** (availability change). Use DynamoDB (on-demand) or S3 + Athena; both are free-tier-friendly (consistent with Rulebook R5).
- **Polly Kajal and Transcribe hi-IN** make a Hindi voice loop (speak a question, get a spoken answer) feasible entirely in ap-south-1.

### Gaps
- Bedrock Agents (classic), Knowledge Bases, Guardrails and Flows availability in ap-south-1: the feature-by-region page has moved, and the replacement was not checked.
- Which listed models accept image input. Claude, Nova Lite/Pro, Qwen3 VL and Nemotron VL are presumed multimodal (INFERENCE from model families), not verified on model cards.
- Amazon Translate Indian-language pairs, Textract support for Hindi text and Indian bill layouts, Rekognition, IoT Core, EventBridge Scheduler and Step Functions in ap-south-1: none verified this session.
- HYPOTHESIS: Textract text detection officially supports a limited set of Latin-script languages and not Devanagari. Verify before relying on Hindi bill OCR.
- The exact date and terms of the Timestream LiveAnalytics availability change were not captured.
- Bedrock per-token pricing in ap-south-1 and whether Free-plan credits cover Bedrock.
