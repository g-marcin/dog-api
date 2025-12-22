.PHONY: dev start install test lint format clean

dev:
	python main.py

start:
	uvicorn app.main:app --host localhost --port 8000 --reload --root-path /dog-api

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

