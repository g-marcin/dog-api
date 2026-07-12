#!/usr/bin/env bash
# Regenerate api-types from the local OpenAPI schema and push it to the
# yalc store so a locally-linked consumer (e.g. woof-app) can pick up
# in-progress contract changes without publishing to npm.
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHONPATH=. uv run python scripts/export_openapi.py

cd packages/api-types
npm run yalc:push
