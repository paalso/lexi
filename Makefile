install:
	poetry install

run:
	poetry run lexi

test:
	poetry run pytest

build:
	poetry build

lint:
	poetry run flake8 lexi
