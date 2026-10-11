import json

import jsonschema
import pytest

from conftest import CONTRACTS_DIR

EXAMPLES = sorted((CONTRACTS_DIR / "examples").glob("ingest_*.json"))


def _schema(name):
    return json.loads((CONTRACTS_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_examples_match_schemas(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    kind = "request" if path.name.startswith("ingest_request") else "response"
    jsonschema.validate(doc, _schema(f"ingest_{kind}.schema.json"))


def test_example_count():
    assert len(EXAMPLES) == 6
