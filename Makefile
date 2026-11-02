.PHONY: infra-up infra-down migrate test lint

infra-up:
	docker compose up -d

infra-down:
	docker compose down

migrate:
	cd backend && alembic upgrade head

test:
	cd backend && pytest -v

lint:
	cd backend && ruff check . && mypy app