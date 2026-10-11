import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
CONTRACTS_DIR = REPO / "contracts"

import os

os.environ.setdefault("POWERTOOLS_TRACE_DISABLED", "true")
os.environ.setdefault("WRISTHEAT_METRICS_OFF", "1")
os.environ.setdefault("AWS_DEFAULT_REGION", "ap-south-1")
