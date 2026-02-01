# Claude Code Rules for dog-api

## Database Migrations

When making database schema changes:
1. **Do NOT generate migration files directly** - Instead, add/modify SQLAlchemy models in `app/model/database.py`
2. Let the user generate migrations using `make db-generate` which runs Alembic autogenerate
3. The user will review and adjust the generated migration as needed

## Project Structure

- `app/model/database.py` - SQLAlchemy models and database connection
- `alembic/` - Database migrations
- `seed/` - Seed data files (JSON)
