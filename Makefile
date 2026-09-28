.PHONY: install run test lint format clean

install:
poetry install

run:
poetry run uvicorn devflow_bot.presentation.api.main:app --reload

test:
poetry run pytest

lint:
poetry run ruff check src tests

format:
poetry run black src tests
poetry run ruff check --fix src tests

clean:
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
