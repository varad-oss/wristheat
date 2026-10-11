# WristHeat architecture

```mermaid
flowchart LR
  W["Galaxy Watch5 Pro<br/>Wear OS app<br/>HR ~1 Hz (Health Services)"] -- "POST /v1/ingest every 5 s<br/>x-device-token" --> API
  SIM["simulator.py / replay.py<br/>SIMULATED / REPLAY"] -- same endpoint --> API
  API["API Gateway<br/>HTTP API"] --> ING["Lambda ingest<br/>ECTemp → PSI → level → state machine"]
  ING -- "readings, minutes,<br/>sessions, incidents" --> DDB[("DynamoDB<br/>on-demand, TTL")]
  ING -- "state + one-shot alert" --> W
  ING -- "RED → StartExecution" --> SFN
  subgraph SFN["Step Functions: wristheat-escalation"]
    N["Notify<br/>Polly EN/HI → S3<br/>SNS supervisor"] --> A["WaitForAck<br/>(task token, 90 s)"]
    A -- timeout --> E["Escalate<br/>SNS backup"] --> A2["WaitForAckAfterEscalation"]
    A --> R["WaitForRecovery<br/>(released by ingest)"]
    A2 --> R
    R --> C["Close<br/>metrics + Bedrock report"]
  end
  SCH["EventBridge Scheduler<br/>every 10 min"] --> CTX["Lambda context<br/>Open-Meteo → Liljegren WBGT"] --> DDB
  DASH["React dashboard<br/>S3 + CloudFront"] -- "Cognito JWT<br/>roster every 3 s, ack" --> API
  API --> SUP["Lambda supervisor API"] --> DDB
  SUP -- "SendTaskSuccess (ack)" --> SFN
  C -- "Converse" --> BR["Amazon Bedrock<br/>Nova Lite (APAC profile)"]
```

The risk engine is pure Python (`backend/src/wristheat/{ectemp,strain,engine}.py`) with no AWS imports, so it is tested offline against the golden values in the spec (§7).
