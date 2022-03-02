.PHONY: test

format:
	black src tests

validate-format:
	black --check src tests

lint:
	pylint src

unit-test:
	python -m unittest discover tests/ut

int-test:
	python -m unittest discover tests/int

check: validate-format lint

test: unit-test int-test

start:
	uvicorn --host 0.0.0.0 --port 80 src.app.main:app --reload

dev-up:
	docker-compose -f dev.docker-compose.yaml up --build -d

dev-shell:
	docker-compose -f dev.docker-compose.yaml exec uq-dev bash

dev-down:
	docker-compose -f dev.docker-compose.yaml down
