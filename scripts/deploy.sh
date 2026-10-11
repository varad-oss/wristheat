#!/usr/bin/env bash
# One-command deploy: build Lambdas (+ dashboard if present), then cdk deploy to ap-south-1.
# Emails come from the environment or a git-ignored .env.deploy:
#   WH_SUPERVISOR_EMAIL=...  WH_BACKUP_EMAIL=...  WH_ACK_TIMEOUT_SECONDS=90
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$ROOT/.env.deploy" ] && set -a && . "$ROOT/.env.deploy" && set +a
export AWS_REGION=ap-south-1 AWS_DEFAULT_REGION=ap-south-1
bash "$ROOT/scripts/build_lambdas.sh"
mkdir -p "$ROOT/build/dashboard"
if [ -f "$ROOT/dashboard/package.json" ]; then
  (cd "$ROOT/dashboard" && npm run build && rm -rf "${ROOT:?}/build/dashboard" && cp -R dist "$ROOT/build/dashboard")
fi
[ -f "$ROOT/build/dashboard/index.html" ] || echo '<!doctype html><title>WristHeat</title><p>Dashboard not built yet.</p>' > "$ROOT/build/dashboard/index.html"
# Web Lambda package (used while CloudFront is unavailable): app code + the built SPA under static/.
rm -rf "${ROOT:?}/build/web" && mkdir -p "$ROOT/build/web"
cp -R "$ROOT/build/app/wristheat" "$ROOT/build/web/" && cp -R "$ROOT/build/dashboard" "$ROOT/build/web/static"
cd "$ROOT/infra"
ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
if ! aws cloudformation describe-stacks --stack-name CDKToolkit >/dev/null 2>&1; then
  npx cdk bootstrap "aws://$ACCOUNT/ap-south-1"
fi
npx cdk deploy --require-approval never --outputs-file outputs.json \
  -c supervisorEmail="${WH_SUPERVISOR_EMAIL:-}" -c backupEmail="${WH_BACKUP_EMAIL:-}" \
  -c ackTimeoutSeconds="${WH_ACK_TIMEOUT_SECONDS:-90}" "$@"
