#!/usr/bin/env bash
# Smoke-test a running dog-api instance after a deploy.
# Usage: scripts/smoke_test.sh [BASE_URL]
#   scripts/smoke_test.sh                          # prod (https://api.mgrzmil.dev)
#   scripts/smoke_test.sh http://localhost:8000    # local dev server
set -uo pipefail

BASE="${1:-https://api.mgrzmil.dev}"
BASE="${BASE%/}"
FAILED=0

pass() { printf '  \033[32mPASS\033[0m %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m %s -- %s\n' "$1" "$2"; FAILED=$((FAILED + 1)); }

# check_json NAME PATH JQ_FILTER: expects 200 and a truthy jq filter on the body.
check_json() {
    local name="$1" path="$2" filter="$3" body code
    body="$(curl -s -w '\n%{http_code}' "$BASE$path")"
    code="${body##*$'\n'}"
    body="${body%$'\n'*}"
    if [[ "$code" != "200" ]]; then
        fail "$name" "HTTP $code"
    elif ! echo "$body" | jq -e "$filter" >/dev/null 2>&1; then
        fail "$name" "unexpected body: ${body:0:120}"
    else
        pass "$name"
    fi
}

echo "Smoke testing $BASE"

# Root redirect to docs
read -r code url < <(curl -s -o /dev/null -L -w '%{http_code} %{url_effective}\n' "$BASE/")
[[ "$code" == "200" && "$url" == "$BASE/docs" ]] \
    && pass "GET / redirects to docs" \
    || fail "GET / redirect" "ended at $url with HTTP $code"

check_json "healthcheck" "/healthcheck" '.status == "success"'
check_json "list all breeds" "/breeds/list/all" '.status == "success" and (.message | length > 0)'
check_json "breed sub-breeds" "/breed/hound/list" '.status == "success"'
check_json "random image URL has no //" "/breeds/image/random" \
    '.status == "success" and (.message | test("^https?://[^/]+(/[^/]+)+$"))'
check_json "random breed image" "/breed/hound/images/random" '.status == "success"'
check_json "breed description" "/breed/hound/description" \
    '.status == "success" and (.message.description_en | length > 0)'
check_json "variant description" "/breed/hound/basset/description" \
    '.status == "success" and (.message.description_en | length > 0)'

code="$(curl -s -o /dev/null -w '%{http_code}' "$BASE/metrics")"
[[ "$code" == "200" ]] && pass "metrics exposed" || fail "metrics" "HTTP $code"

echo
if [[ "$FAILED" -gt 0 ]]; then
    echo "$FAILED check(s) failed"
    exit 1
fi
echo "All checks passed"
