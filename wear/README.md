# WristHeat — Wear OS watch app

Galaxy Watch5 Pro (SM-R920, Wear OS 6 / Android 16). The app reads live heart rate with Health Services, uploads it every 5 s to the WristHeat API, shows the heat-strain state, and vibrates on the server's one-shot `alert`.

Prototype, not a medical device.

## Setup

1. **Developer mode on the watch:** Settings → About watch → Software → tap *Software version* 5×.
2. **Wi-Fi debugging:** Settings → Developer options → ADB debugging ON, Wireless debugging ON → *Pair new device*. On the Mac:
   ```bash
   adb pair <ip>:<pair-port>     # enter the 6-digit code from the watch
   adb connect <ip>:<port>       # the port shown under "IP address & Port"
   ```
   The port changes each time wireless debugging is toggled or the watch sleeps for long. If `adb devices` shows `offline`, re-run `adb connect` with the new port.
3. **Config** in `local.properties` (git-ignored, never commit):
   ```
   wristheat.apiBaseUrl=https://<api-id>.execute-api.ap-south-1.amazonaws.com
   wristheat.deviceToken=<32-char token from AWS Secrets Manager>
   wristheat.traineeId=T1
   wristheat.fakeApi=false      # true = no network; cycles canned responses
   wristheat.hrSource=exercise  # exercise | measure | fake
   ```
   Missing keys default to `""`, `T1`, `false`, `exercise`. A blank URL or token with `fakeApi=false` shows "Setup error: missing API URL or token".
4. **Build and install:**
   ```bash
   export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
   ./gradlew installDebug
   ```
5. **Permissions:** on the first *Start session* the watch asks for heart rate (`android.permission.health.READ_HEART_RATE` on Wear OS 6; `BODY_SENSORS` on older) and notifications. If heart rate is denied twice, the Retry chip opens the app's settings page.

## Switching the HR source

| `hrSource` | What it does | When to use |
|---|---|---|
| `exercise` (default) | Health Services `ExerciseClient` (RUNNING, HR only, no GPS) inside a foreground service of type `health`. Keeps running with the screen off. | Real sessions |
| `measure` | `MeasureClient`. Only delivers while the app is in front; the screen is kept on. | If the exercise fails on the watch |
| `fake` | 1 Hz synthetic HR: rest 72–75 for 150 s, ramp to 165 over 60 s, hold 600 s, decay to 95. | Emulator / UI checks |

`fakeApi=true` replaces the cloud with a scripted sequence (5 s per step): Calibrating ×4 → GREEN → AMBER (buzz) → AMBER ×3 → RED (buzz, repeats every 10 s until tapped) → RED ×3 → RECOVERING ×3 → GREEN with "Recovery confirmed" (buzz) → GREEN.

## Behaviour

- Samples are buffered in memory (cap 900, oldest dropped). Only strictly increasing timestamps are kept.
- Each request carries up to 600 samples. When the network fails, it retries after 2 → 4 → 8 → 16 → 30 s and shows "Offline · buffering N s".
- 401/404 stop the uploads and show "Setup error: unauthorized / unknown trainee". 400 drops that batch and continues.
- The watch vibrates only on `alert`: AMBER 2×200 ms, RED 3×600 ms (repeated every 10 s until tapped or the state leaves RED), RECOVERED 1×800 ms.
- The screen is kept on while a session is running.
- *Stop* asks "End session?". Yes calls `POST /v1/sessions/{id}/end` (best effort, 3 s).

## Verified on SM-R920 (11 Oct, 01:30–02:10 IST)

| Check | Result |
|---|---|
| HR rate, `ExerciseClient`, worn | 60 samples/min, steady over 5 min |
| Fake sequence (`fakeApi=true`, `hrSource=fake`) | Calibrating → GREEN → AMBER overlay + buzz → RED overlay + buzz, repeat after 10 s, stops on tap → RECOVERING → Recovery confirmed + buzz → GREEN. Screens in `docs/screens/` |
| Stop flow | Stop → "End session?" → Yes → `end: true`, service gone, back to Start |
| App in background, real HR | 30 uploads at 5 s and 141 samples in 150 s; no gap > 5 s |
| Screen off (Dozing) 90 s, real HR | 18 uploads at 5 s and 86 samples (~57/min); no gap > 5 s |
| `adb shell screenrecord` over Wi-Fi | Works (max 3 min per file) |

Screen-off HR uses the `HEART_RATE_5_SECONDS` batching override (supported on this watch). Without it, Health Services delivers HR in bursts of several minutes while the screen is off.

**Still to do:** real backend (W7), outdoor network fallback, 20-min battery figure.

## Recording the watch screen for the video

```bash
adb shell screenrecord --time-limit 180 /sdcard/wristheat.mp4
adb pull /sdcard/wristheat.mp4
```

## Logs

```bash
adb logcat -s WristHeatSession WristHeatHR WristHeatBuzz
```

## Known Samsung quirks

- If a Samsung Health workout is running, Health Services reports another app owns the exercise. The app shows "Stop the Samsung Health workout, then retry" instead of taking over.
- Starting a Samsung Health workout mid-session ends our exercise. The session stops and the error is shown.
- Wireless debugging drops when the watch sleeps; reconnect with the new port.
- After a crash or force-stop, our old exercise keeps running. Its late ENDED (superseded) update is ignored by checking the exercise start time.
- `adb shell input tap` while the screen is dozing only wakes it; wake first, then tap.

## Tests

```bash
./gradlew testDebugUnitTest
```
