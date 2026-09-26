.DEFAULT_GOAL := help
.PHONY: help install start test lint format format-check check clean smoke openapi-export \
	db-generate db-upgrade db-downgrade db-stamp db-history

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies (incl. dev tools)
	uv sync

start: ## Run dev server with auto-reload
	uv run uvicorn app.main:app --host localhost --port 8000 --reload

test: ## Run tests (needs DB_POSTGRES_URL with migrated schema)
	uv run pytest

lint: ## Lint with ruff
	uv run ruff check .

format: ## Format and autofix with ruff
	uv run ruff format .
	uv run ruff check --fix .

format-check: ## Fail if files are not formatted
	uv run ruff format --check .

check: lint format-check test ## Run everything CI runs

clean: ## Remove Python caches
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache

smoke: ## Smoke-test a running instance (URL=https://api.mgrzmil.dev by default)
	scripts/smoke_test.sh $(URL)

openapi-export: ## Export OpenAPI spec for api-types
	PYTHONPATH=. uv run python scripts/export_openapi.py

db-generate: ## Autogenerate a migration (MSG="description")
	uv run alembic revision --autogenerate -m "$(MSG)"

db-upgrade: ## Apply all migrations
	uv run alembic upgrade head

db-downgrade: ## Roll back one migration
	uv run alembic downgrade -1

db-stamp: ## Stamp DB at a revision without running it (REV=...)
	uv run alembic stamp $(REV)

db-history: ## Show current revision and history
	uv run alembic current
	uv run alembic history
