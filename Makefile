.PHONY: check lint typecheck test validate fix build run serve

DATA ?= data
OUT  ?= docs/data

# --- Quality checks -------------------------------------------------

check: lint typecheck test validate

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run ty check

test:
	uv run python -m pytest

validate:
	uv run python -m pipeline.validate $(DATA)

fix:
	uv run ruff check --fix .
	uv run ruff format .

# --- Build and run --------------------------------------------------

build: validate
	uv run python -m pipeline.build $(DATA) $(OUT)

run:
	uv run python -m streamlit run app/main.py

serve:
	uv run python -m http.server 8000 --directory docs