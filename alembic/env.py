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

if database_url := os.getenv("DB_POSTGRES_URL"):
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

    with open(breeds_path, encoding='utf-8') as f:
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


def seed_breed_descriptions(connection) -> None:
    """Seed breed descriptions after breeds are created."""
    result = connection.execute(text(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'breed_descriptions')"
    ))
    if not result.scalar():
        return

    if connection.execute(text("SELECT COUNT(*) FROM breed_descriptions")).scalar() > 0:
        return

    descriptions_path = SEED_DIR / "breed_descriptions.json"
    if not descriptions_path.exists():
        print(f"Seed file not found: {descriptions_path}")
        return

    breed_map = {
        row[1]: row[0]
        for row in connection.execute(text("SELECT id, breed FROM breeds"))
    }

    with open(descriptions_path, encoding='utf-8') as f:
        descriptions_data = json.load(f)

    count = 0
    for breed_name, desc in descriptions_data.items():
        if breed_name not in breed_map:
            print(f"Breed not found: {breed_name}")
            continue
        connection.execute(
            text("""
                INSERT INTO breed_descriptions (breed_id, description_en, description_pl)
                VALUES (:breed_id, :description_en, :description_pl)
            """),
            {
                "breed_id": breed_map[breed_name],
                "description_en": desc["description_en"],
                "description_pl": desc["description_pl"]
            }
        )
        count += 1

    print(f"Seeded {count} breed descriptions")


def seed_variant_descriptions(connection) -> None:
    """Seed variant descriptions after variants are created."""
    result = connection.execute(text(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'variant_descriptions')"
    ))
    if not result.scalar():
        return

    if connection.execute(text("SELECT COUNT(*) FROM variant_descriptions")).scalar() > 0:
        return

    descriptions_path = SEED_DIR / "variant_descriptions.json"
    if not descriptions_path.exists():
        print(f"Seed file not found: {descriptions_path}")
        return

    variant_map = {
        row[1]: row[0]
        for row in connection.execute(text("SELECT id, variant FROM breed_variants"))
    }

    with open(descriptions_path, encoding='utf-8') as f:
        descriptions_data = json.load(f)

    count = 0
    for variant_name, desc in descriptions_data.items():
        if variant_name not in variant_map:
            print(f"Variant not found: {variant_name}")
            continue
        connection.execute(
            text("""
                INSERT INTO variant_descriptions (variant_id, description_en, description_pl)
                VALUES (:variant_id, :description_en, :description_pl)
            """),
            {
                "variant_id": variant_map[variant_name],
                "description_en": desc["description_en"],
                "description_pl": desc["description_pl"]
            }
        )
        count += 1

    print(f"Seeded {count} variant descriptions")


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

        with connection.begin():
            seed_breed_descriptions(connection)

        with connection.begin():
            seed_variant_descriptions(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
