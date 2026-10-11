"""Test doubles for AWS clients."""
from __future__ import annotations


class ClientError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.response = {"Error": {"Code": code, "Message": code}}


class Recorder:
    def __init__(self, name, fail: dict | None = None, returns: dict | None = None):
        self.name, self.calls, self.fail, self.returns = name, [], fail or {}, returns or {}

    def __getattr__(self, op):
        if op.startswith("_"):
            raise AttributeError(op)

        def call(**kwargs):
            self.calls.append((op, kwargs))
            if op in self.fail:
                raise self.fail[op]
            ret = self.returns.get(op, {})
            return ret(**kwargs) if callable(ret) else ret
        return call

    def ops(self, op):
        return [kw for o, kw in self.calls if o == op]


class FakeClients:
    def __init__(self, token="tok-0123456789abcdef0123456789abcd", **fail):
        self.token = token
        self.sfn = Recorder("sfn", fail.get("sfn"), {"start_execution": lambda **kw: {
            "executionArn": f"arn:aws:states:ap-south-1:123:execution:wristheat-escalation:{kw['name']}"}})
        self.sns = Recorder("sns", fail.get("sns"))
        self.polly = Recorder("polly", fail.get("polly"), {"synthesize_speech": lambda **kw: {
            "AudioStream": _Stream(b"ID3fake")}})
        self.bedrock = Recorder("bedrock", fail.get("bedrock"), {"converse": lambda **kw: {
            "output": {"message": {"content": [{"text": "Report text. Estimated values; not a medical assessment."}]}}}})
        self.s3 = Recorder("s3", fail.get("s3"), {"generate_presigned_url": lambda **kw:
                                                   f"https://s3.example/{kw['Params']['Key']}?sig"})
        self.lam = Recorder("lambda", fail.get("lam"))
        self.secrets = None

    def get_device_token(self) -> str:
        return self.token


class _Stream:
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data
