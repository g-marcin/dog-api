"""
Seed script for breed_variants table.
Reads breed data from JSON and populates breed_variants with proper breed_id references.

Usage:
    python -m seed.seed_breed_variants

Requires DATABASE_URL environment variable or .env file.
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
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    return url


def load_breeds_data() -> dict:
    with open(BREEDS_JSON_PATH, "r") as f:
        data = json.load(f)
    return data["message"]


def seed_breed_variants(dry_run: bool = False):
    """Seed breed_variants table from breeds.json"""
    engine = create_engine(get_database_url())
    breeds_data = load_breeds_data()

    with engine.connect() as conn:
        # Get existing breeds from database
        result = conn.execute(text("SELECT id, breed FROM breeds"))
        breed_map = {row[1]: row[0] for row in result}

        # Check for existing variants
        existing = conn.execute(text("SELECT COUNT(*) FROM breed_variants")).scalar()
        if existing > 0:
            print(f"breed_variants table already has {existing} rows. Skipping seed.")
            return

        # Prepare insert data
        inserts = []
        for breed_name, variants in breeds_data.items():
            breed_id = breed_map.get(breed_name)
            if breed_id is None:
                print(f"Warning: breed '{breed_name}' not found in database, skipping")
                continue
            for variant in variants:
                inserts.append({"breed_id": breed_id, "variant": variant})

        if dry_run:
            print(f"Dry run: would insert {len(inserts)} breed variants")
            for item in inserts[:10]:
                print(f"  - breed_id={item['breed_id']}, variant={item['variant']}")
            if len(inserts) > 10:
                print(f"  ... and {len(inserts) - 10} more")
            return

        # Insert variants
        if inserts:
            conn.execute(
                text("INSERT INTO breed_variants (breed_id, variant) VALUES (:breed_id, :variant)"),
                inserts
            )
            conn.commit()
            print(f"Successfully inserted {len(inserts)} breed variants")
        else:
            print("No variants to insert")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    seed_breed_variants(dry_run=dry_run)
