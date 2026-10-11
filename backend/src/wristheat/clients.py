"""Thin, injectable wrappers around the AWS clients the handlers use."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

TOKEN_TTL_S = 300


@dataclass
class Clients:
    _cache: dict = field(default_factory=dict)
    _token: tuple[float, str] | None = None

    def _client(self, name: str):
        if name not in self._cache:
            import boto3
            self._cache[name] = boto3.client(name)
        return self._cache[name]

    @property
    def sfn(self):
        return self._client("stepfunctions")

    @property
    def sns(self):
        return self._client("sns")

    @property
    def polly(self):
        return self._client("polly")

    @property
    def bedrock(self):
        return self._client("bedrock-runtime")

    @property
    def s3(self):
        return self._client("s3")

    @property
    def lam(self):
        return self._client("lambda")

    @property
    def secrets(self):
        return self._client("secretsmanager")

    def get_device_token(self) -> str:
        """Device token from Secrets Manager, cached for 5 minutes."""
        now = time.monotonic()
        if self._token is None or now - self._token[0] > TOKEN_TTL_S:
            value = self.secrets.get_secret_value(SecretId=os.environ["DEVICE_TOKEN_SECRET_ARN"])["SecretString"]
            self._token = (now, value.strip())
        return self._token[1]


def error_code(exc: Exception) -> str:
    return getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
