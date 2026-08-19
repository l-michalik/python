.PHONY: install lint type test cov mut bench db api

install:
	uv sync

lint:
	uv run ruff check . && uv run ruff format --check .

type:
	uv run mypy

test:
	uv run pytest -m "not slow and not db"

test-all:
	uv run pytest

cov:
	uv run pytest --cov --cov-report=term-missing --cov-report=html -m "not slow and not db"

mut:
	uv run mutmut run --paths-to-mutate src/joboffers/normalize

bench:
	uv run python -m joboffers.bench.concurrency

db:
	docker compose up -d

api:
	uv run uvicorn joboffers.api.app:app --reload
