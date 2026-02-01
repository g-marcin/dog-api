import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ.setdefault("ROOT_PATH", "/dog-api")
os.environ.setdefault("BASE_URL_API", "http://localhost:8000")
os.environ.setdefault("BASE_URL_IMG", "https://mgrzmil.dev")
os.environ.setdefault("PORT", "8000")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://mgrzmil.dev,https://woof-app-ff670*.web.app")

ROOT_PATH = os.getenv("ROOT_PATH", "")
BASE_URL_API = os.getenv("BASE_URL_API", "http://localhost:8000")
BASE_URL_IMG = os.getenv("BASE_URL_IMG", "https://mgrzmil.dev")
PORT = int(os.getenv("PORT", 8000))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://mgrzmil.dev,https://woof-app-ff670*.web.app")

if ROOT_PATH:
    BASE_URL_API = BASE_URL_API.rstrip("/") + ROOT_PATH
    BASE_URL_IMG = BASE_URL_IMG.rstrip("/") + ROOT_PATH

ASSETS_DIR = Path(__file__).parent.parent / "dog-assets"

DB_POSTGRES_URL = os.getenv("DB_POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/dog_app")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "300"))
DB_POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
DB_PGBOUNCER_MODE = os.getenv("DB_PGBOUNCER_MODE", "transaction")

