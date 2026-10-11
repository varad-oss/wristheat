# WristHeat

A supervisor watches a group exerting in heat; each wearer's own smartwatch streams heart rate to AWS. WristHeat turns it into an **estimated** core-temperature trend and strain index, fuses it with site WBGT and air quality, and runs a closed loop: the wrist vibrates, the supervisor is alerted in English and Hindi, unacknowledged alerts escalate, and an incident closes only when **the data confirms recovery**.

Built for AWS Environmental Hacks (Heat & Water track), 11 Oct 2026. Prototype, not a medical device.

- **Live dashboard:** `DashboardUrl` from `infra/outputs.json` after deploy (link added at submission)
- **Spec:** [`docs/superpowers/specs/2026-10-11-wristheat-design.md`](docs/superpowers/specs/2026-10-11-wristheat-design.md) · **Plan:** [`docs/superpowers/plans/2026-10-11-wristheat-cloud.md`](docs/superpowers/plans/2026-10-11-wristheat-cloud.md)
- **Architecture:** [`docs/architecture.md`](docs/architecture.md)

## How it works

```
Watch (Wear OS) ──5 s──► API Gateway ──► Lambda ingest: ECTemp → PSI → level → state machine ──► DynamoDB
                                              │ reply: state + one-shot alert (watch vibrates)
                                              └─ RED ► Step Functions: Notify (SNS + Polly EN/HI)
                                                       → WaitForAck (90 s) → Escalate (backup) → WaitForAck
                                                       → WaitForRecovery (released by ingest) → Close (Bedrock report)
EventBridge Scheduler (10 min) ► Lambda context: Open-Meteo → Liljegren WBGT (thermofeel) → Sites
React dashboard on S3 + CloudFront ── Cognito ──► supervisor API (roster every 3 s, acknowledge)
```

## AWS services and the job each one does

| Service | Job |
|---|---|
| API Gateway (HTTP API) | Receives the watch stream; JWT-protects supervisor routes |
| Lambda (Python 3.12, arm64) | Runs the risk engine, context fetch, workflow steps, supervisor API |
| DynamoDB (on-demand, TTL) | Stores readings, per-minute estimates, session state, incidents, sites |
| Step Functions (Standard) | Runs the escalation: notify → wait for acknowledgement → escalate → wait for confirmed recovery → close |
| EventBridge Scheduler | Refreshes site heat and air every 10 min |
| Amazon Polly (neural, Kajal, en-IN + hi-IN) | Spoken alert in English and Hindi |
| Amazon SNS (email) | Alerts the supervisor, then the backup contact |
| Amazon Bedrock (Converse, Nova Lite via the APAC inference profile) | Writes the incident report from logged facts only |
| Amazon S3 | Alert audio and dashboard assets |
| Amazon CloudFront | Serves the dashboard over HTTPS |
| Amazon Cognito | Supervisor sign-in |
| AWS Secrets Manager | Holds the device token |
| CloudWatch + X-Ray (via Powertools for AWS Lambda) | Logs, custom metrics, a WristHeat dashboard, traces |
| AWS CDK (TypeScript) / CloudFormation | Entire stack as code, one deploy command |

## Quick start

Prerequisites: AWS credentials for ap-south-1 (`aws login`), Node ≥ 20, Python 3.12, [uv](https://docs.astral.sh/uv/) (or pip). No Docker.

```bash
# 1. Python env and tests
python3.12 -m venv .venv && uv pip install --python .venv/bin/python -r backend/requirements-dev.txt
make test                                        # engine, API, escalation, simulator
(cd infra && npm ci && npm test)                 # CDK assertions
(cd dashboard && npm ci && npm test)             # dashboard

# 2. Deploy (emails in a git-ignored .env.deploy: WH_SUPERVISOR_EMAIL=…, WH_BACKUP_EMAIL=…)
npx --prefix infra cdk bootstrap aws://<account>/ap-south-1   # once per account
bash scripts/deploy.sh                           # builds layers (pip --platform manylinux2014_aarch64), dashboard, cdk deploy
.venv/bin/python scripts/seed.py --name "<wearer>" --age <n> --supervisor-email <email>
.venv/bin/python scripts/smoke.py                # → OK GREEN
```

Confirm both SNS subscription emails from the inbox once.

**Watch config** (`wear/local.properties`, never committed):
```
wristheat.apiBaseUrl=<ApiUrl from infra/outputs.json>
wristheat.deviceToken=<aws secretsmanager get-secret-value --secret-id wristheat/device-token --query SecretString --output text --region ap-south-1>
wristheat.traineeId=T1
```

**Simulator** (labelled SIMULATED everywhere):
```bash
.venv/bin/python simulator/simulate.py --backfill-minutes 15 --surge-after 60      # S1–S4
.venv/bin/python simulator/simulate.py --only S3 --backfill-minutes 18 --surge-after 30   # escalation demo
.venv/bin/python simulator/simulate.py --only S3 --profile easy96                  # S3 recovers → incident closes
.venv/bin/python simulator/export_session.py --session <sid>                      # record a real session
.venv/bin/python simulator/replay.py --fixture fixtures/<file>.json --as R1        # REPLAY badge
```

## Honesty

1. "WristHeat estimates a core-temperature *trend* from heart rate using ECTemp (US Army Research Institute of Environmental Medicine). It is not a thermometer and not a medical device."
2. "ECTemp was validated with chest-strap heart rate (about ±0.6 °C). It has not been validated on wrist optical sensors like the one in this watch, and studies found it misses many cases above 39 °C. Treat it as an early indicator, never as clearance to continue."
3. "WBGT is computed for open ground in sun from Open-Meteo forecast data (Liljegren method). Shade, indoor and local conditions differ."
4. "The rules that combine strain with the heat flag are our own heuristic, not a published standard."
5. "Trainees marked SIMULATED are generated by our simulator. REPLAY shows a real session recorded earlier. LIVE is a real person wearing the watch now."
6. "ECTemp is patented (US 10702165). This is a non-commercial research prototype."

We do not claim any prevented illness, clinical accuracy or measured impact.

## Data attribution

- Weather data by Open-Meteo.com (CC BY 4.0)
- Air quality: Copernicus Atmosphere Monitoring Service via Open-Meteo

All Open-Meteo variable names in spec §8 were confirmed with a live call on 11 Oct (fixtures in `backend/tests/fixtures/`); no substitutions were needed.

## AI tools used

- **Claude (Claude Code)** for research, design, the cloud backend, dashboard, simulator and tests, and the Wear OS app.
- **Amazon Bedrock (Nova Lite)** at runtime, only to word the incident report from logged facts; a deterministic template is used if it fails.

## Known limits

- The incident list uses a DynamoDB Scan with a filter; fine below ~1,000 incidents, not beyond.
- WBGT is open-field in sun from forecast data, not a measurement at the athlete's location.
- ECTemp is unvalidated on wrist optical heart rate; the ± 0.6 °C band is the chest-strap figure.
- One site per deployment; one shared device token.

See [`CREDITS.md`](CREDITS.md) for sources and licences.
