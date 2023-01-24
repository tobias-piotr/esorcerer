.PHONY: lint
## Run pre-commit hooks
lint:
	pre-commit run --all-files

.PHONY: test
## Run tests
test:
	pytest

.PHONY: build
## Build the image
build:
	docker compose build

.PHONY: up
## Start the container
up:
	docker compose up

.PHONY: enter
## Enter the fastapi container
enter:
	docker compose exec fastapi bash
