"""Shared helpers for the operator scripts: stack outputs and the device token."""
import json
import pathlib

import boto3

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGION = "ap-south-1"


def outputs(path: str | None = None) -> dict:
    p = pathlib.Path(path) if path else ROOT / "infra" / "outputs.json"
    data = json.loads(p.read_text())
    return data.get("WristHeat", next(iter(data.values())))


def device_token() -> str:
    sm = boto3.client("secretsmanager", region_name=REGION)
    return sm.get_secret_value(SecretId="wristheat/device-token")["SecretString"].strip()
