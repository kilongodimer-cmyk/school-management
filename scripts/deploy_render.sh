#!/usr/bin/env bash
set -euo pipefail

if [ -z "${RENDER_API_KEY:-}" ] || [ -z "${RENDER_SERVICE_ID:-}" ]; then
  echo "RENDER_API_KEY and RENDER_SERVICE_ID must be set as environment variables"
  echo "Set them locally or in CI before running this script"
  exit 1
fi

echo "Triggering deploy for service ${RENDER_SERVICE_ID}..."

curl -s -X POST "https://api.render.com/v1/services/${RENDER_SERVICE_ID}/deploys" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{ "clearCache": true }' \
  | python -m json.tool

echo "Deploy triggered. Check Render dashboard or logs for progress."
