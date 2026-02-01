"""
Seed script for breeds table.
Reads breed data from JSON and populates breeds table.

Usage:
    python -m seed.seed_breeds

Requires DB_POSTGRES_URL environment variable or .env file.
"""
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

BREEDS_JSON_PATH = Path(__file__).parent.parent.parent / "tmp" / "breeds.json"


def get_database_url() -> str:
    url = os.getenv("DB_POSTGRES_URL")
    if not url:
        raise RuntimeError("DB_POSTGRES_URL environment variable not set")
    return url


def load_breeds_data() -> dict:
    with open(BREEDS_JSON_PATH, "r") as f:
        data = json.load(f)
    return data["message"]


def seed_breeds(dry_run: bool = False):
    """Seed breeds table from breeds.json"""
    engine = create_engine(get_database_url())
    breeds_data = load_breeds_data()

    with engine.connect() as conn:
        # Check for existing breeds
        existing = conn.execute(text("SELECT COUNT(*) FROM breeds")).scalar()
        if existing > 0:
            print(f"breeds table already has {existing} rows. Skipping seed.")
            return

        # Get breed names (keys from the JSON)
        breed_names = list(breeds_data.keys())

        if dry_run:
            print(f"Dry run: would insert {len(breed_names)} breeds")
            for name in breed_names[:10]:
                print(f"  - {name}")
            if len(breed_names) > 10:
                print(f"  ... and {len(breed_names) - 10} more")
            return

        # Insert breeds
        inserts = [{"breed": name} for name in breed_names]
        conn.execute(
            text("INSERT INTO breeds (breed) VALUES (:breed)"),
            inserts
        )
        conn.commit()
        print(f"Successfully inserted {len(breed_names)} breeds")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    seed_breeds(dry_run=dry_run)
