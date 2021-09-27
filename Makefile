install:
	poetry install

run:
	poetry run lexi

test:
	poetry run pytest

build: check
	poetry build
