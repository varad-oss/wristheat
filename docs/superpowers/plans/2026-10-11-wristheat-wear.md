# WristHeat Watch App (Wear OS) — Agent Prompt and Implementation Plan

> **You are the Android engineer for WristHeat.** Read this whole document before writing code. It is self-contained: everything you need about the backend is in the "API contract" section. Work task by task, run the tests in each task, and commit after each task. If you are Claude Code, use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** a Wear OS app for a **Samsung Galaxy Watch5 Pro (SM-R920, Wear OS 6 / Android 16)**. It reads live heart rate with Google Health Services, uploads it every 5 s to the WristHeat cloud API, shows the returned heat-strain state on the watch, and **vibrates** when the state changes.

**Why it matters:** this is the physical "proof moment" of our hackathon video. A real person runs in the heat, their own watch measures them, AWS computes their heat strain, and the watch buzzes on camera. Reliability beats features.

**Architecture:**
- A foreground service of type `health` owns a Health Services `ExerciseClient` session (HR only).
- A pure-Kotlin `Uploader` batches samples and POSTs them with OkHttp.
- A `SessionRepository` exposes `StateFlow<UiState>` to Jetpack Compose for Wear OS screens.
- An `AlertPolicy` decides vibrations from the server's one-shot `alert` field.

**Tech Stack:** Kotlin, Jetpack Compose for Wear OS (Material 3), `androidx.health:health-services-client:1.1.0`, `androidx.concurrent:concurrent-futures-ktx` (for `ListenableFuture.await()`), OkHttp 4.12, kotlinx-serialization-json, kotlinx-coroutines, JUnit 4 + kotlinx-coroutines-test + OkHttp MockWebServer for tests.

**Spec:** `docs/superpowers/specs/2026-10-11-wristheat-design.md` (the team's design spec; §5 is the API, §10 the watch). You do not need it to finish this plan; this document carries everything you need.

**Deadline:** the watch must work end-to-end by **09:30 IST Sun 11 Oct**. Outdoor filming starts ~12:00. The hackathon closes 20:00.

## Global Constraints

- `applicationId` / package `com.wristheat.watch`; `minSdk 30`, `targetSdk 36`, `compileSdk 36`.
- Location in the team repo: `wristheat/wear/`. Move or recreate the existing Android Studio "Empty Wear App" project there; the Gradle root is `wear/`.
- Permissions, exactly:
  ```xml
  <uses-permission android:name="android.permission.BODY_SENSORS" android:maxSdkVersion="35" />
  <uses-permission android:name="android.permission.health.READ_HEART_RATE" />
  <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
  <uses-permission android:name="android.permission.FOREGROUND_SERVICE_HEALTH" />
  <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
  <uses-permission android:name="android.permission.VIBRATE" />
  <uses-permission android:name="android.permission.WAKE_LOCK" />
  ```
  - At runtime, request `android.permission.health.READ_HEART_RATE` on API 36+ and `BODY_SENSORS` on ≤ 35 (Google's guidance for Wear OS 6).
  - Do **not** request location, GPS or activity recognition. If `startExerciseAsync` throws a `SecurityException` that names ACTIVITY_RECOGNITION, add that permission and request it; nothing else.
- Configuration comes from `wear/local.properties` (git-ignored, **never commit**) through `BuildConfig`:
  ```
  wristheat.apiBaseUrl=https://<api-id>.execute-api.ap-south-1.amazonaws.com
  wristheat.deviceToken=<32-char token from AWS Secrets Manager>
  wristheat.traineeId=T1
  wristheat.fakeApi=false      # true = no network; cycles canned responses
  wristheat.hrSource=exercise  # exercise | measure | fake
  ```
  The cloud team will send you the URL and the token-fetch command when their milestone M1 is deployed (~03:00 IST). Until then, use `fakeApi=true`.
- HTTPS only. Timeouts: connect 5 s, read 10 s.
- All timestamps sent are **epoch milliseconds UTC**.
- **Commit after every task** (small commits; the event checks that repo history matches the event dates). Don't commit `local.properties`, `build/`, `.gradle/`, `.idea/`.
- The watch shows English only, short strings. Colour is never the only signal; always show the state word.

## Review Focus

1. **Network drops outdoors for minutes** → samples must buffer (cap 900, drop oldest), the UI must say "Offline · buffering Ns", and the batch must upload when the network returns. *Tests:* `UploaderTest.capsAt900DropsOldest`, `UploaderTest.backoffSequence`.
2. **Health Services delivers duplicate or out-of-order points** → send strictly increasing `t` only. *Test:* `SampleBufferTest.dropsNonIncreasing`.
3. **The server sends `alert: "RED"` once, but the wearer doesn't look** → the RED vibration repeats every 10 s until tapped, and stops when the state leaves RED. *Test:* `AlertPolicyTest.redRepeatsUntilAcknowledgedOrStateChanges`.
4. **Bad config (wrong token or trainee)** → a 401/404 must show "Setup error: unauthorized / unknown trainee" and stop retrying, not loop forever. *Test:* `UploaderTest.fatalOn401And404`.
5. **Screen turns off or the app is backgrounded mid-run** → HR collection continues (foreground service + exercise). *Manual test:* Task 8 step 4.

---

## API contract (authoritative copy)

**`POST {apiBaseUrl}/v1/ingest`** — headers `content-type: application/json`, `x-device-token: <token>`.

Request (send every 5 s; `samples` may be empty, which acts as a poll):
```json
{
  "schema": 1,
  "trainee_id": "T1",
  "session_id": "3f6c1e9a-0b7d-4a51-9a52-0c3c0d2f8e11",
  "source": "live",
  "device": "SM-R920",
  "samples": [ {"t": 1791700000000, "bpm": 92}, {"t": 1791700001000, "bpm": 93} ]
}
```

| Field | Rule |
|---|---|
| `session_id` | a new `UUID.randomUUID().toString()` per session |
| `bpm` | `Int` (round the Health Services `Double`) |
| `samples` | at most 600 per request, ascending `t` |

Response 200 (every field is always present; nullable ones may be `null`):
```json
{
  "schema": 1, "trainee_id": "T1", "session_id": "…",
  "accepted": 5, "dropped": 0,
  "state": "AMBER",
  "state_since": 1791700660000,
  "calibration_remaining_s": 0,
  "hr_now": 163, "hr0": 74,
  "core_est_c": 37.78, "core_band_c": 0.6,
  "psi": 5.6, "minutes_to_red": 7,
  "env": {"wbgt_c": 31.4, "flag": "RED", "pm25": 72.0, "us_aqi": 158, "updated_at": 1791700200000, "stale": false},
  "advice": {"en": "Strain rising. Slow down and drink water.", "hi": "…"},
  "alert": "AMBER",
  "incident_id": null,
  "server_time": 1791700665300
}
```

| Field | Values / meaning |
|---|---|
| `state` | `CALIBRATING` \| `GREEN` \| `AMBER` \| `RED` \| `RECOVERING` |
| `env` | may be `null`; `env.flag` ∈ `NONE`, `WHITE`, `GREEN`, `YELLOW`, `RED`, `BLACK` |
| `alert` | `NONE` \| `AMBER` \| `RED` \| `RECOVERED`. **One-shot:** each non-NONE value is sent in exactly one response. Vibrate only on this field, never on `state` |
| `hr0`, `core_est_c`, `psi` | `null` while calibrating |

Errors: `{"error": "<code>", "message": "…"}` with codes `unauthorized` (401), `unknown_trainee` (404), `bad_request` / `source_mismatch` (400).

**`POST {apiBaseUrl}/v1/sessions/{session_id}/end`** (same header) → `{"ended": true}`. Call it when the wearer taps Stop.

**Example files:** the repo has `contracts/examples/ingest_response.{calibrating,amber_alert,red_alert,recovered_alert,env_missing}.json`. Copy them into `wear/app/src/test/resources/contracts/` and parse them in tests. If they are not in the repo yet, create them from the response JSON above with the matching `state`/`alert`.

---

## File map (`wear/app/src/main/java/com/wristheat/watch/`)

```
AppConfig.kt                 BuildConfig → typed config
data/Models.kt               @Serializable request/response models
data/Api.kt                  interface Api; OkHttpApi; FakeApi
data/SampleBuffer.kt         strictly increasing buffer, cap 900
data/Uploader.kt             5-s cadence, batching, backoff, fatal errors (pure Kotlin, injectable clock)
sensors/HeartRateSource.kt   interface + ExerciseHeartRateSource + MeasureHeartRateSource + FakeHeartRateSource
session/UiState.kt           UI model
session/SessionRepository.kt StateFlow<UiState>, reduces server responses
session/AlertPolicy.kt       pure logic: which vibration, repeats, acknowledgement
session/Haptics.kt           VibratorManager wrapper
session/SessionService.kt    foreground service (type health) wiring everything
ui/MainActivity.kt           permission flow, keep-screen-on, navigation
ui/screens/{Start,Calibrating,Live,AlertOverlay,StopConfirm,SetupError}.kt
ui/theme/Colors.kt           GREEN #1f7a4d, AMBER #b26a00, RED #b42318, RECOVERING #1d5fa8
```

Tests live in `wear/app/src/test/java/com/wristheat/watch/`.

---

### Task W1: Project setup, config, manifest

**Files:** `wear/settings.gradle.kts`, `wear/app/build.gradle.kts`, `wear/app/src/main/AndroidManifest.xml`, `AppConfig.kt`, `wear/.gitignore`

**Interfaces:**
- Produces: `object AppConfig { val apiBaseUrl: String; val deviceToken: String; val traineeId: String; val fakeApi: Boolean; val hrSource: String }`, read from `BuildConfig` fields `API_BASE_URL`, `DEVICE_TOKEN`, `TRAINEE_ID`, `FAKE_API`, `HR_SOURCE`.

- [ ] **Step 1:** Move the existing template project into `wristheat/wear/` (or create "Empty Wear App" there). Set the SDK levels from Global Constraints. Enable `buildFeatures { buildConfig = true; compose = true }`. Add the kotlinx-serialization plugin and the dependencies from Tech Stack (use the latest stable Compose for Wear OS Material 3 and OkHttp 4.12.x).
- [ ] **Step 2:** In `app/build.gradle.kts`, load `rootProject.file("local.properties")` with `java.util.Properties` and emit `buildConfigField("String", "API_BASE_URL", "\"…\"")` etc. Missing keys default to `""`, `"T1"`, `false`, `"exercise"`.
- [ ] **Step 3:** Manifest:
  - the permissions from Global Constraints;
  - `<uses-feature android:name="android.hardware.type.watch" />`;
  - `<service android:name=".session.SessionService" android:exported="false" android:foregroundServiceType="health" />`;
  - meta-data `com.google.android.wearable.standalone = true`.
- [ ] **Step 4:** Build and run on the watch (`samsung SM-R920` in Device Manager). Expected: the template UI opens. Run `./gradlew testDebugUnitTest`. Expected: BUILD SUCCESSFUL.
- [ ] **Step 5: Commit.** `chore(wear): project setup, config from local.properties, permissions`

### Task W2: Contract models

**Files:** `data/Models.kt`; Test `data/ModelsTest.kt` + `src/test/resources/contracts/*.json`

**Interfaces:**
- Produces:
  - `@Serializable data class Sample(val t: Long, val bpm: Int)`
  - `IngestRequest(schema: Int = 1, trainee_id, session_id, source: String = "live", device: String = "SM-R920", samples: List<Sample>)`
  - `Env(wbgt_c: Double?, flag: String, pm25: Double?, us_aqi: Int?, updated_at: Long, stale: Boolean)`
  - `Advice(en: String, hi: String)`
  - `IngestResponse(…all fields of the contract…, env: Env?, alert: String, incident_id: String?)`
  - `ApiError(error: String, message: String = "")`
  - `val WhJson = Json { ignoreUnknownKeys = true; explicitNulls = false }`
  - Use `@SerialName` where you choose camelCase Kotlin names; JSON names must match the contract exactly.

- [ ] **Step 1: Failing tests:**
  - `parsesAllExamples`: each example file decodes. `amber_alert.alert == "AMBER"`; `calibrating.hr0 == null && calibrating.calibration_remaining_s == 95`; `env_missing.env == null`; `red_alert.incident_id != null`.
  - `encodesRequestFieldNames`: the encoded JSON contains `"trainee_id"`, `"session_id"` and `"samples":[{"t":1791700000000,"bpm":92}]`.
- [ ] **Step 2:** Run `./gradlew testDebugUnitTest --tests '*ModelsTest*'`. Expected: FAIL.
- [ ] **Step 3:** Implement. **Step 4:** Run. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(wear): API contract models`

### Task W3: Api client, sample buffer, uploader

**Files:** `data/Api.kt`, `data/SampleBuffer.kt`, `data/Uploader.kt`; Tests `data/SampleBufferTest.kt`, `data/UploaderTest.kt`, `data/OkHttpApiTest.kt`

**Interfaces:**
- Produces:
  ```kotlin
  sealed interface ApiResult {
      data class Ok(val body: IngestResponse) : ApiResult
      data class Fatal(val code: String) : ApiResult        // 401, 404 → stop
      data class BadRequest(val code: String) : ApiResult   // 400 → drop this batch, continue
      data class Retry(val reason: String) : ApiResult      // IOException, 5xx, 429
  }
  interface Api { suspend fun ingest(req: IngestRequest): ApiResult; suspend fun endSession(sessionId: String): Boolean }
  class OkHttpApi(baseUrl: String, token: String, client: OkHttpClient = defaultClient()) : Api
  class FakeApi : Api   // returns calibrating ×4, then GREEN, AMBER(alert AMBER), AMBER ×3, RED(alert RED), RED ×3,
                        // RECOVERING ×3, GREEN(alert RECOVERED), then GREEN forever; fills hr_now from the request
  class SampleBuffer(cap: Int = 900) {
      fun add(s: Sample): Boolean    // false if s.t <= last added t
      fun peek(max: Int): List<Sample>
      fun remove(n: Int)
      val size: Int
      fun oldestT(): Long?
  }
  interface Clock { fun nowMs(): Long }
  class Uploader(
      api: Api, buffer: SampleBuffer, clock: Clock,
      traineeId: String, sessionId: String,
      onResponse: (IngestResponse) -> Unit,
      onStatus: (UploadStatus) -> Unit,
  ) {
      suspend fun tick()             // one upload attempt if due
      fun nextDelayMs(): Long
  }
  sealed interface UploadStatus {
      data object Ok : UploadStatus
      data class Offline(val bufferedSeconds: Int) : UploadStatus
      data class Fatal(val code: String) : UploadStatus
  }
  ```
- Behaviour:
  - Normal cadence 5,000 ms.
  - Each tick sends `buffer.peek(600)`, or an empty list as a poll.
  - On `Ok`: remove the sent samples.
  - On `BadRequest`: remove them, log, continue.
  - On `Retry`: keep them; delays go 2,000 → 4,000 → 8,000 → 16,000 → 30,000 → 30,000 ms; reset to 5,000 after an Ok.
  - On `Fatal`: report it and stop ticking.
  - `bufferedSeconds = (now - oldestT)/1000`.

- [ ] **Step 1: Failing tests:**
  - `SampleBufferTest.dropsNonIncreasing`: adding t = 1000, 2000, 2000, 1500, 3000 keeps 3 items.
  - `SampleBufferTest.capsAt900DropsOldest`: add 950 increasing → size 900, oldest t is the 51st.
  - `UploaderTest.sendsBatchEvery5s`
  - `UploaderTest.backoffSequence`: a fake Api returning Retry ×6 → `nextDelayMs()` sequence `[2000,4000,8000,16000,30000,30000]`; then Ok → `5000`.
  - `UploaderTest.fatalOn401And404`: the status is `Fatal("unauthorized")` and further ticks don't call the Api.
  - `UploaderTest.badRequestDropsBatch`
  - `UploaderTest.emptyPollWhenNoSamples`
  - `OkHttpApiTest` (MockWebServer):
    - sends the header `x-device-token`, path `/v1/ingest`, content-type JSON;
    - maps 200 → Ok, 401 → Fatal("unauthorized"), 404 → Fatal("unknown_trainee"), 400 → BadRequest, 503 → Retry;
    - parses the UTF-8 Hindi `advice.hi` intact.
- [ ] **Step 2:** Run. Expected: FAIL. **Step 3:** Implement. **Step 4:** Run. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(wear): API client, sample buffer and uploader with backoff`

### Task W4: Heart-rate sources (Health Services) and permissions

**Files:** `sensors/HeartRateSource.kt`, `ui/MainActivity.kt` (permission request part)

**Interfaces:**
- Produces:
  ```kotlin
  data class HrSample(val tMs: Long, val bpm: Int)
  interface HeartRateSource {
      suspend fun start(onSample: (HrSample) -> Unit, onError: (String) -> Unit)
      suspend fun stop()
  }
  class ExerciseHeartRateSource(context: Context) : HeartRateSource
  class MeasureHeartRateSource(context: Context) : HeartRateSource
  class FakeHeartRateSource(scope: CoroutineScope) : HeartRateSource
  // Fake: 1 Hz; 72→75 for 150 s, ramp to 165 over 60 s, hold 600 s, then decay to 95

  fun heartRatePermissions(): Array<String>
  // API ≥ 36 (Build.VERSION_CODES.BAKLAVA): arrayOf(HealthPermissions.READ_HEART_RATE)
  // else: arrayOf(Manifest.permission.BODY_SENSORS)
  // plus POST_NOTIFICATIONS on API ≥ 33
  ```
- `ExerciseHeartRateSource.start`:
  1. `val ec = HealthServices.getClient(ctx).exerciseClient`.
  2. Check `ExerciseType.RUNNING in ec.getCapabilitiesAsync().await().supportedExerciseTypes` and that `DataType.HEART_RATE_BPM` is in that type's supported data types; else `onError("hr_unsupported")`.
  3. `ec.setUpdateCallback(callback)`.
  4. `ec.startExerciseAsync(ExerciseConfig(exerciseType = ExerciseType.RUNNING, dataTypes = setOf(DataType.HEART_RATE_BPM), isAutoPauseAndResumeEnabled = false, isGpsEnabled = false)).await()`.
  5. In `onExerciseUpdateReceived(update)`:
     ```kotlin
     val bootInstant = Instant.ofEpochMilli(System.currentTimeMillis() - SystemClock.elapsedRealtime())
     update.latestMetrics.getData(DataType.HEART_RATE_BPM).forEach { dp ->
         onSample(HrSample(dp.getTimeInstant(bootInstant).toEpochMilli(), dp.value.roundToInt()))
     }
     ```
  6. Ignore `bpm <= 0`.
  7. If another app owns an exercise (Samsung Health workout running), surface `onError("exercise_in_use")`. The UI then says "Stop the Samsung Health workout, then retry".
  8. `stop()` → `ec.endExerciseAsync().await()` and `ec.clearUpdateCallbackAsync(callback)`.
- `MeasureHeartRateSource`: `measureClient.registerMeasureCallback(DataType.HEART_RATE_BPM, cb)`. In `onDataReceived(data)` read `data.getData(DataType.HEART_RATE_BPM)` the same way. Unregister on stop. It works only while the app is in the foreground, so the screen is kept on.

- [ ] **Step 1:** Implement the three sources plus `heartRatePermissions()`. MainActivity requests permissions with `rememberLauncherForActivityResult(RequestMultiplePermissions())` on first Start; if denied, show "Heart-rate permission needed" with a retry chip.
- [ ] **Step 2: Device spike.** A debug screen (temporary) shows live BPM from `ExerciseHeartRateSource` and counts samples per minute. Run on the watch, worn. Expected: BPM updates about once per second and ≥ 50 samples/min. **Record the samples/min figure in the commit message.** If the exercise fails on the Galaxy watch, switch `hrSource=measure` and record why.
- [ ] **Step 3: Commit.** `feat(wear): Health Services HR sources and permission flow (N samples/min on SM-R920)`

### Task W5: Session service, repository, alert policy, haptics

**Files:** `session/UiState.kt`, `session/SessionRepository.kt`, `session/AlertPolicy.kt`, `session/Haptics.kt`, `session/SessionService.kt`; Tests `session/SessionRepositoryTest.kt`, `session/AlertPolicyTest.kt`

**Interfaces:**
- Produces:
  ```kotlin
  data class UiState(
      val phase: Phase,                 // IDLE, STARTING, RUNNING, ENDING, SETUP_ERROR
      val state: String?,               // server state
      val hrLocal: Int?,                // last local sample (instant feedback)
      val hrServer: Int?, val coreEst: Double?, val psi: Double?, val minutesToRed: Int?,
      val calibrationRemainingS: Int?,
      val wbgt: Double?, val flag: String?, val envStale: Boolean,
      val adviceEn: String?,
      val upload: UploadStatus,
      val overlay: Overlay?,            // AMBER, RED, RECOVERED or null
      val error: String?,
  )
  object SessionRepository {
      val ui: StateFlow<UiState>
      fun onLocalSample(s: HrSample)
      fun onResponse(r: IngestResponse)
      fun onStatus(u: UploadStatus)
      fun onError(code: String)
      fun dismissOverlay()
  }
  class AlertPolicy(clock: Clock) {
      fun onResponse(alert: String, state: String): List<Buzz>   // Buzz.AMBER, Buzz.RED, Buzz.RECOVERED
      fun onTick(state: String): List<Buzz>                       // RED repeat every 10,000 ms until acknowledged
      fun acknowledgeRed()
  }
  class Haptics(context: Context) { fun play(b: Buzz) }
  // Patterns (VibrationEffect.createWaveform, ms):
  //   AMBER     [0,200,150,200]
  //   RED       [0,600,200,600,200,600]
  //   RECOVERED [0,800]
  class SessionService : LifecycleService()   // ACTION_START / ACTION_STOP intents
  ```
- `SessionService` on `ACTION_START`:
  1. `ServiceCompat.startForeground(this, 1, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_HEALTH)`. Use an ongoing notification "WristHeat session running" on channel `session`.
  2. Create `sessionId = UUID.randomUUID()`.
  3. Pick the source by `AppConfig.hrSource` and the API by `AppConfig.fakeApi`.
  4. Each sample → `buffer.add` + `SessionRepository.onLocalSample`.
  5. Run a coroutine loop: `uploader.tick(); delay(uploader.nextDelayMs())`, plus a 1-s ticker for `AlertPolicy.onTick`.

  On `ACTION_STOP`: stop the source, `api.endSession(sessionId)` (best effort, 3 s timeout), `stopForeground(STOP_FOREGROUND_REMOVE)`, `stopSelf()`.
- Overlay rules:
  - `alert` AMBER → overlay AMBER, auto-dismiss after 5 s.
  - `alert` RED → overlay RED, stays until tapped (tap = `acknowledgeRed()` + dismiss).
  - `alert` RECOVERED → overlay RECOVERED, auto-dismiss after 8 s.
  - If `state` leaves RED, clear the RED overlay and stop repeats.

- [ ] **Step 1: Failing tests:**
  - `AlertPolicyTest.noneNeverBuzzes`
  - `AlertPolicyTest.amberBuzzesOnce`
  - `AlertPolicyTest.redRepeatsUntilAcknowledgedOrStateChanges`: RED at t = 0 → buzz; ticks at 5 s → none; 10 s → RED; 20 s → RED; acknowledge → none at 30 s. Separately, a state change to RECOVERING stops repeats.
  - `AlertPolicyTest.recoveredBuzzesOnce`
  - `SessionRepositoryTest.reducesResponse`: amber_alert.json → `overlay == AMBER`, `psi == 5.6`, `flag == "RED"`.
  - `SessionRepositoryTest.fatalShowsSetupError`
- [ ] **Step 2:** Run. Expected: FAIL. **Step 3:** Implement. **Step 4:** Run. Expected: PASS.
- [ ] **Step 5: Commit.** `feat(wear): session service, repository, alert policy and haptics`

### Task W6: Screens

**Files:** `ui/MainActivity.kt`, `ui/screens/*.kt`, `ui/theme/Colors.kt`

**Interfaces:**
- Consumes: `SessionRepository.ui`; starts and stops `SessionService` with intents.

**Screens** (round 450×450 display; large type; every state shown as a word, not just a colour):
- **Start (IDLE):**
  - title "WristHeat";
  - line "Heat-strain early warning";
  - big chip "Start session";
  - small text "Trainee T1 · prototype, not a medical device".
- **Calibrating:**
  - "Sit still";
  - countdown `m:ss` from `calibrationRemainingS` (before the first response, count down locally from 2:00);
  - live local BPM;
  - "Measuring your resting heart rate".
- **Live:**
  - outer ring = `psi/10` progress in the state colour;
  - centre: state word (GREEN / AMBER / RED / RECOVERING), BPM (large, `hrLocal`), "Core ~37.8 ±0.6°C";
  - below: "WBGT 31.4 · RED flag" (or "Heat data stale"), "~6 min to RED" when present;
  - sync dot: green = Ok, grey + "Offline · buffering 45 s";
  - scroll down: advice text, then a "Stop" chip → StopConfirm ("End session?" Yes/No).
- **AlertOverlay:**
  - RED: full-screen RED background, "STOP" (huge), `adviceEn`, "Tap when you've stopped";
  - AMBER: amber background, "SLOW DOWN", advice, auto-dismiss;
  - RECOVERED: green, "Recovery confirmed", "Resume only at an easier pace".
- **SetupError:** "Setup error: <code>", "Check token and trainee in local.properties".
- **Keep screen on** while `phase == RUNNING` (`window.addFlags(FLAG_KEEP_SCREEN_ON)`; clear it on stop).

- [ ] **Step 1:** Implement with Compose for Wear OS Material 3.
- [ ] **Step 2:** Check in the **emulator** (Wear OS Large Round) with `fakeApi=true, hrSource=fake`. Expected sequence within ~2 min: Calibrating → GREEN → AMBER overlay (buzz logged) → RED overlay (repeats every 10 s until tap) → RECOVERING → "Recovery confirmed". Take a screenshot of each screen into `wear/docs/screens/`.
- [ ] **Step 3: Commit.** `feat(wear): calibrating, live, alert and stop screens`

### Task W7: Real backend integration (after cloud milestone M1)

**Files:** `wear/local.properties` (not committed), `wear/README.md`

- [ ] **Step 1:** Put the real `apiBaseUrl`, `deviceToken` and `traineeId=T1` in `local.properties`; set `fakeApi=false`, `hrSource=exercise`. Build and install on the watch.
- [ ] **Step 2: Indoor test, worn.**
  - Start → Calibrating (sit 2 min) → GREEN.
  - Exercise hard until HR stays ≥ 160 for 5–6 min (stairs at a run, running in place or burpees) → AMBER overlay and vibration. With a yellow-or-worse heat flag, AMBER comes after ~2 min at that effort. With a low flag (early morning) it needs PSI ≥ 5, roughly 5 min at 160+. If HR can't stay that high indoors, confirm the AMBER buzz with `fakeApi=true` and leave the real AMBER for the outdoor run.
  - Sit → RECOVERING → after a few minutes "Recovery confirmed" vibration.
  - Expected: the cloud team's dashboard mirrors each state within ~10 s.
- [ ] **Step 3:** Ask the cloud team to confirm in DynamoDB/CloudWatch that `Readings` has ≥ 50 samples per minute with no gap > 30 s.
- [ ] **Step 4:** Write `wear/README.md`: setup (developer mode, Wi-Fi debugging, `local.properties` keys, permissions), how to switch `hrSource`, known Samsung quirks.
- [ ] **Step 5: Commit.** `docs(wear): setup and integration notes`

### Task W8: Filming readiness

- [ ] **Step 1: Background test.** Start a session, let the screen dim or press the side button to leave the app for 2 min, return. Expected: no gap in samples (the foreground service kept running). If there is a gap, keep the app in front with the screen on during filming and note it in the README.
- [ ] **Step 2: Outdoor network test.** Walk 100 m from the Wi-Fi router. The watch should fall back to the paired phone's Bluetooth/LTE; check "Offline" never lasts more than ~30 s. Expected: buffered samples upload when back online.
- [ ] **Step 3: Battery.** Note the battery % before and after a 20-min session (expected ~5–10%).
- [ ] **Step 4: Screen recording for the video.** Confirm `adb shell screenrecord /sdcard/wristheat.mp4` works over Wi-Fi debugging (max 3 min per file), so the video can show a crisp inset of the watch screen. Pull with `adb pull`.
- [ ] **Step 5: Release build.** Build a debug-signed APK `wear/app/build/outputs/apk/debug/app-debug.apk` and keep it installed. Tag the commit `watch-v1`.
- [ ] **Step 6: Commit and report back to the team.** Report: samples/min, permission flow OK, AMBER/RED/RECOVERED buzz confirmed on wrist, background result, offline result, battery numbers.

---

## What NOT to build

Phone companion app, Health Connect, GPS/location, Hindi on the watch, settings screens, login, tiles or complications, data storage beyond the in-memory buffer, Play Store signing.
