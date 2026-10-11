"""Serves the dashboard SPA from the Lambda package over the HTTP API's $default route.

Fallback for accounts where CloudFront is not yet enabled: same-origin with the API, so no CORS is needed.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import pathlib

STATIC_DIR = pathlib.Path(__file__).resolve().parents[2] / "static"
TEXT_TYPES = ("text/", "application/javascript", "application/json", "image/svg+xml")
EXTRA_TYPES = {".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
               ".html": "text/html; charset=utf-8", ".svg": "image/svg+xml", ".woff2": "font/woff2",
               ".json": "application/json; charset=utf-8", ".mp3": "audio/mpeg"}


def _resp(status: int, body: bytes | str, ctype: str, cache: str) -> dict:
    headers = {"content-type": ctype, "cache-control": cache, "x-content-type-options": "nosniff"}
    if isinstance(body, str) or ctype.startswith(TEXT_TYPES):
        text = body if isinstance(body, str) else body.decode("utf-8")
        return {"statusCode": status, "headers": headers, "body": text, "isBase64Encoded": False}
    return {"statusCode": status, "headers": headers, "body": base64.b64encode(body).decode(), "isBase64Encoded": True}


def _config() -> dict:
    return {"apiUrl": "", "region": os.environ.get("AWS_REGION", "ap-south-1"),
            "userPoolId": os.environ.get("USER_POOL_ID", ""), "userPoolClientId": os.environ.get("USER_POOL_CLIENT_ID", "")}


def handler(event, context):
    path = event.get("rawPath") or ((event.get("requestContext") or {}).get("http") or {}).get("path") or "/"
    if path == "/config.json":
        return _resp(200, json.dumps(_config()), "application/json; charset=utf-8", "no-cache")
    root = STATIC_DIR.resolve()
    target = (root / path.lstrip("/")).resolve()
    inside = target == root or root in target.parents
    if inside and target.is_file():
        ctype = EXTRA_TYPES.get(target.suffix) or mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        cache = "no-cache" if target.suffix == ".html" else "public, max-age=31536000, immutable"
        return _resp(200, target.read_bytes(), ctype, cache)
    # Missing files under /assets are real 404s; any other path is an SPA route.
    if path.startswith("/assets/") or "." in path.rsplit("/", 1)[-1]:
        return _resp(404, json.dumps({"error": "not_found", "message": path}), "application/json; charset=utf-8", "no-cache")
    index = root / "index.html"
    if not index.is_file():
        return _resp(503, "Dashboard not built.", "text/plain; charset=utf-8", "no-cache")
    return _resp(200, index.read_bytes(), "text/html; charset=utf-8", "no-cache")
