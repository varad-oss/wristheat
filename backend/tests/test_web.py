import base64
import json

from wristheat.handlers import web


def event(path):
    return {"routeKey": "$default", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}}}


def setup_static(tmp_path, monkeypatch):
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_text("<!doctype html><title>WristHeat</title>")
    (tmp_path / "assets" / "app.js").write_text("console.log(1)")
    (tmp_path / "favicon.svg").write_text("<svg/>")
    (tmp_path / "font.woff2").write_bytes(b"\x00\x01binary")
    monkeypatch.setattr(web, "STATIC_DIR", tmp_path)
    monkeypatch.setenv("USER_POOL_ID", "ap-south-1_abc")
    monkeypatch.setenv("USER_POOL_CLIENT_ID", "client123")


def test_index_and_spa_fallback(tmp_path, monkeypatch):
    setup_static(tmp_path, monkeypatch)
    for path in ("/", "/incidents/inc-1", "/method"):
        r = web.handler(event(path), None)
        assert r["statusCode"] == 200 and "WristHeat" in r["body"]
        assert r["headers"]["content-type"].startswith("text/html")
        assert r["headers"]["cache-control"] == "no-cache"


def test_assets_have_types_and_long_cache(tmp_path, monkeypatch):
    setup_static(tmp_path, monkeypatch)
    r = web.handler(event("/assets/app.js"), None)
    assert r["headers"]["content-type"].startswith("text/javascript")
    assert "immutable" in r["headers"]["cache-control"]
    r = web.handler(event("/font.woff2"), None)
    assert r["isBase64Encoded"] is True and base64.b64decode(r["body"]) == b"\x00\x01binary"


def test_missing_asset_404_not_index(tmp_path, monkeypatch):
    setup_static(tmp_path, monkeypatch)
    assert web.handler(event("/assets/missing.js"), None)["statusCode"] == 404


def test_path_traversal_blocked(tmp_path, monkeypatch):
    setup_static(tmp_path, monkeypatch)
    r = web.handler(event("/../../etc/passwd"), None)
    assert r["statusCode"] in (200, 404) and "root:" not in r.get("body", "")


def test_config_json_is_same_origin(tmp_path, monkeypatch):
    setup_static(tmp_path, monkeypatch)
    r = web.handler(event("/config.json"), None)
    cfg = json.loads(r["body"])
    assert cfg == {"apiUrl": "", "region": "ap-south-1", "userPoolId": "ap-south-1_abc", "userPoolClientId": "client123"}
    assert r["headers"]["cache-control"] == "no-cache"


def test_unknown_api_path_is_json_404(tmp_path, monkeypatch):
    setup_static(tmp_path, monkeypatch)
    r = web.handler(event("/v1/public/unknown"), None)
    assert r["statusCode"] == 404 and r["headers"]["content-type"].startswith("application/json")
    assert json.loads(r["body"])["error"] == "not_found"
