#!/usr/bin/env python3
"""Posts 3 batches for hidden trainee S0 and checks a schema-valid GREEN response."""
import json
import time
import urllib.request

import jsonschema

from common import ROOT, device_token, outputs


def main():
    out = outputs()
    api, token = out["ApiUrl"].rstrip("/"), device_token()
    schema = json.loads((ROOT / "contracts" / "ingest_response.schema.json").read_text(encoding="utf-8"))
    sid = f"smoke-{int(time.time())}"
    t0 = int(time.time() * 1000) - 15_000
    resp = None
    for b in range(3):
        samples = [{"t": t0 + (b * 5 + k) * 1000, "bpm": 72} for k in range(5)]
        body = {"schema": 1, "trainee_id": "S0", "session_id": sid, "source": "simulated", "device": "smoke",
                "samples": samples}
        req = urllib.request.Request(f"{api}/v1/ingest", data=json.dumps(body).encode(), method="POST",
                                     headers={"content-type": "application/json", "x-device-token": token})
        with urllib.request.urlopen(req, timeout=15) as r:
            assert r.status == 200, r.status
            resp = json.loads(r.read().decode("utf-8"))
        jsonschema.validate(resp, schema)
    assert resp["state"] == "GREEN", resp
    print(f"OK {resp['state']}")


if __name__ == "__main__":
    main()
