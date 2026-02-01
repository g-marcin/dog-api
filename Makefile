.PHONY: dev start install test lint format clean pm2-start pm2-stop pm2-restart venv venv-windows venv-linux

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
	nodemon --exec "python main.py" --ext ".py"

start:
	python -m uvicorn app.main:app --host localhost --port 8000 --reload

install:
	pip install -r requirements.txt

test:
	pytest

lint:
	flake8 app/ || true

format:
	black app/ || true

clean:
	find . -type d -name __pycache__ -exec rm -r {} + || true
	find . -type f -name "*.pyc" -delete || true

db-migrate:
	alembic revision --autogenerate -m "$(MSG)"

db-migrate-update:
	alembic upgrade head

db-migrate-downgrade:
	alembic downgrade -1

pm2-start:
	pm2 start ecosystem.config.js

pm2-stop:
	pm2 stop dog-api

pm2-restart:
	pm2 restart dog-api

