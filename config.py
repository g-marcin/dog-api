import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Keys that must be set in production. Locally they fall back to the defaults below;
# in production a missing key would silently point the app at localhost, so fail fast.
# deploy.yml imports this module against the rendered .env before touching the VPS.
REQUIRED_IN_PROD = ("DB_POSTGRES_URL", "API_IMG_BASE_URL", "API_CORS_ORIGINS")

APP_ENV = os.getenv("API_ENV", "development")
if APP_ENV == "production":
    missing = [key for key in REQUIRED_IN_PROD if not os.getenv(key)]
    if missing:
        sys.exit(f"Missing required env vars for API_ENV=production: {', '.join(missing)}")

ROOT_PATH = os.getenv("API_ROOT_PATH", "")
BASE_URL_API = os.getenv("API_BASE_URL", "http://localhost:8000")
BASE_URL_IMG = os.getenv("API_IMG_BASE_URL", "https://mgrzmil.dev")
PORT = int(os.getenv("API_PORT", 8000))
CORS_ORIGINS = os.getenv(
    "API_CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://mgrzmil.dev,https://woof-app-ff670*.web.app",
)
GIT_SHA = os.getenv("API_GIT_SHA", "unknown")

if ROOT_PATH:
    BASE_URL_API = BASE_URL_API.rstrip("/") + ROOT_PATH
    BASE_URL_IMG = BASE_URL_IMG.rstrip("/") + ROOT_PATH

ASSETS_DIR = Path(__file__).parent.parent / "dog-assets"

DB_POSTGRES_URL = os.getenv(
    "DB_POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/dog_app"
)
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "300"))
DB_POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
DB_PGBOUNCER_MODE = os.getenv("DB_PGBOUNCER_MODE", "transaction")
