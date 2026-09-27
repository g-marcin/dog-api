import os
import subprocess
import sys
from pathlib import Path

import config

REPO_ROOT = Path(__file__).resolve().parent.parent


def import_config(**overrides):
    # Run in a subprocess: config validates at import time and exits on failure.
    # Empty strings mark keys as missing; load_dotenv never overrides a key already
    # in the environment, so a developer's local .env can't fill the gap.
    env = {**os.environ, **overrides}
    return subprocess.run(
        [sys.executable, "-c", "import config"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def test_production_exits_listing_all_missing_keys():
    result = import_config(API_ENV="production", **{key: "" for key in config.REQUIRED_IN_PROD})
    assert result.returncode != 0
    for key in config.REQUIRED_IN_PROD:
        assert key in result.stderr


def test_production_starts_when_required_keys_set():
    result = import_config(
        API_ENV="production",
        DB_POSTGRES_URL="postgresql://u:p@db:5432/dog_app",
        API_IMG_BASE_URL="https://cdn.example.com",
        API_CORS_ORIGINS="https://example.com",
    )
    assert result.returncode == 0, result.stderr


def test_development_does_not_enforce_required_keys():
    result = import_config(API_ENV="", **{key: "" for key in config.REQUIRED_IN_PROD})
    assert result.returncode == 0, result.stderr
