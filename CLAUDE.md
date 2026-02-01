# Claude Code Rules for dog-api

## Shell Commands

Check the operating system before running shell commands:
- On Windows (`platform: win32`): Use PowerShell commands (Remove-Item, Get-ChildItem, Copy-Item, Move-Item)
- On Linux/macOS: Use bash commands (rm, ls, cp, mv)

## Database Migrations

When making database schema changes:
1. **Do NOT generate migration files directly** - Instead, add/modify SQLAlchemy models in `app/model/database.py`
2. Let the user generate migrations using `make db-generate` which runs Alembic autogenerate
3. The user will review and adjust the generated migration as needed

## Project Structure

- `app/model/database.py` - SQLAlchemy models and database connection
- `alembic/` - Database migrations
- `seed/` - Seed data files (JSON)
