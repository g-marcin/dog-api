from logging.config import fileConfig
from pathlib import Path
import json
import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool, text

load_dotenv()

from app.model.database import Base

config = context.config

if database_url := os.getenv("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

SEED_DIR = Path(__file__).parent.parent / "seed"


def seed_data(connection) -> None:
    """Seed breeds and variants after migrations."""
    result = connection.execute(text(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'breeds')"
    ))
    if not result.scalar():
        return

    if connection.execute(text("SELECT COUNT(*) FROM breeds")).scalar() > 0:
        return

    breeds_path = SEED_DIR / "breeds.json"
    if not breeds_path.exists():
        print(f"Seed file not found: {breeds_path}")
        return

    with open(breeds_path) as f:
        breeds_data = json.load(f)["message"]

    for breed_name in breeds_data.keys():
        connection.execute(text("INSERT INTO breeds (breed) VALUES (:breed)"), {"breed": breed_name})

    breed_map = {
        row[1]: row[0]
        for row in connection.execute(text("SELECT id, breed FROM breeds"))
    }

    for breed_name, variants in breeds_data.items():
        for variant in variants:
            connection.execute(
                text("INSERT INTO breed_variants (breed_id, variant) VALUES (:breed_id, :variant)"),
                {"breed_id": breed_map[breed_name], "variant": variant}
            )

    print(f"Seeded {len(breeds_data)} breeds")


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

        with connection.begin():
            seed_data(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
