.PHONY: dev start install test lint format clean pm2-start pm2-stop pm2-restart venv venv-windows venv-linux db-migrate db-migrate-update db-migrate-downgrade db-stamp db-history

venv-windows:
	powershell -NoExit -Command ".\.venv\Scripts\Activate.ps1"

venv-linux:
	bash -c "source ./.venv/bin/activate && exec bash"

ifeq ($(OS),Windows_NT)
venv: venv-windows
else
venv: venv-linux
endif

dev:
	nodemon --exec "uv run python main.py" --ext ".py"

start:
	uv run uvicorn app.main:app --host localhost --port 8000 --reload

install:
	uv sync

test:
	uv run python -m pytest

lint:
	uv run flake8 app/

format:
	uv run black app/

clean:
	uv run python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"

db-migrate:
	uv run alembic revision --autogenerate -m "$(MSG)"

db-migrate-update:
	uv run alembic upgrade head

db-migrate-downgrade:
	uv run alembic downgrade -1

db-stamp:
	uv run alembic stamp $(REV)

db-history:
	uv run alembic current
	uv run alembic history
