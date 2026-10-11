"""Shared simulator helpers: payloads, HTTP posting, stack outputs and the device token."""
from __future__ import annotations

import json
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGION = "ap-south-1"


def make_payload(trainee_id: str, session_id: str, source: str, samples, replay_of: str | None = None,
                 device: str | None = None) -> dict:
    payload = {"schema": 1, "trainee_id": trainee_id, "session_id": session_id, "source": source,
               "device": device or ("SM-R920" if source == "replay" else "simulator"),
               "samples": [{"t": int(t), "bpm": int(min(230, max(30, round(b))))} for t, b in samples]}
    if replay_of:
        payload["replay_of"] = replay_of
    return payload


def post_batch(api_url: str, token: str, payload: dict) -> dict:
    req = urllib.request.Request(f"{api_url.rstrip('/')}/v1/ingest", data=json.dumps(payload).encode(),
                                 method="POST",
                                 headers={"content-type": "application/json", "x-device-token": token})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e


def stack_outputs(path: str | None = None) -> dict:
    p = pathlib.Path(path) if path else ROOT / "infra" / "outputs.json"
    data = json.loads(p.read_text())
    return data.get("WristHeat", next(iter(data.values())))


def resolve_api_and_token(api: str | None, token: str | None) -> tuple[str, str]:
    if not api:
        api = stack_outputs()["ApiUrl"]
    if not token:
        import boto3
        sm = boto3.client("secretsmanager", region_name=REGION)
        token = sm.get_secret_value(SecretId="wristheat/device-token")["SecretString"].strip()
    return api, token
