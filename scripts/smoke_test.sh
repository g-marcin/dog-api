#!/usr/bin/env bash
# Smoke-test a running dog-api instance after a deploy.
# Helpers come from https://github.com/g-marcin/smoke-test-action (lib.sh).
# Usage: scripts/smoke_test.sh [BASE_URL]
#   scripts/smoke_test.sh                          # prod (https://api.mgrzmil.dev)
#   scripts/smoke_test.sh http://localhost:8000    # local dev server
# Optional env:
#   EXPECTED_SHA         fail unless /healthcheck reports this commit in X-Git-Sha
#   CORS_ORIGIN          origin that must be allowed by CORS (default https://mgrzmil.dev)
#   APP_SMOKE_TEST_LIB   path to a local lib.sh (set by the action in CI)

# eval, not source <(...): process substitution can't be sourced by macOS bash 3.2.
if [[ -n "${APP_SMOKE_TEST_LIB:-}" ]]; then source "$APP_SMOKE_TEST_LIB"
else
    lib="$(curl -fsSL --max-time 10 https://raw.githubusercontent.com/g-marcin/smoke-test-action/v1/lib.sh)" \
        || { echo "Failed to fetch smoke-test lib" >&2; exit 1; }
    eval "$lib"
fi

smoke_init "${1:-https://api.mgrzmil.dev}"

check_redirect "GET / redirects to docs" "/" "/docs"
check_json "healthcheck" "/healthcheck" '.status == "success"'
check_sha "/healthcheck"
check_cors "${CORS_ORIGIN:-https://mgrzmil.dev}"
check_json "list all breeds" "/breeds/list/all" '.status == "success" and (.message | length > 0)'
check_json "breed sub-breeds" "/breed/hound/list" '.status == "success"'
check_json "random image URL has no //" "/breeds/image/random" \
    '.status == "success" and (.message | test("^https?://[^/]+(/[^/]+)+$"))'
check_json "random breed image" "/breed/hound/images/random" '.status == "success"'
check_image_from "image served" "/breeds/image/random"
check_json "breed description" "/breed/hound/description" \
    '.status == "success" and (.message.description_en | length > 0)'
check_json "variant description" "/breed/hound/basset/description" \
    '.status == "success" and (.message.description_en | length > 0)'
check_status "metrics exposed" "/metrics"

finish
