#!/usr/bin/env bash
# Builds Lambda code and dependency layers for arm64 / Python 3.12 without Docker.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
B="$ROOT/build"
rm -rf "${B:?}/app" "${B:?}/layer-core" "${B:?}/layer-sci"
mkdir -p "$B/app" "$B/layer-core/python" "$B/layer-sci/python"

install() {  # install <requirements> <target>
  if command -v uv >/dev/null 2>&1; then
    uv pip install --quiet --target "$2" --python-platform aarch64-manylinux2014 --python-version 3.12 \
      --only-binary :all: -r "$1"
  else
    python3 -m pip install --quiet --target "$2" --platform manylinux2014_aarch64 --implementation cp \
      --python-version 3.12 --only-binary=:all: -r "$1"
  fi
}

install "$ROOT/backend/requirements-core.txt" "$B/layer-core/python"
install "$ROOT/backend/requirements-sci.txt" "$B/layer-sci/python"
# boto3/botocore come with the Lambda runtime; drop copies pulled in transitively.
rm -rf "$B"/layer-*/python/{boto3,botocore,s3transfer}*
find "$B" -name '__pycache__' -type d -prune -exec rm -rf {} +
cp -R "$ROOT/backend/src/wristheat" "$B/app/"
find "$B/app" -name '__pycache__' -type d -prune -exec rm -rf {} +
du -sh "$B"/app "$B"/layer-core "$B"/layer-sci
