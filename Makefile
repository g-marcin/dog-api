.PHONY: dev start install test lint format clean

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

