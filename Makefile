# Shortcuts for the manual dev setup described in the README: Docker runs the
# databases, backend and frontend run natively so both keep their hot-reload.
# Needs a Unix shell (Linux, macOS, or WSL2 on Windows); the plain commands in the
# README work on native Windows too.
#
# The venv binaries are called directly instead of `source .venv/bin/activate`:
# make runs every recipe line in its own shell, so an activation would be gone
# again by the next line.

PYTEST_ARGS ?= -v

.DEFAULT_GOAL := help
.PHONY: help setup db db-test migrate backend frontend dev test down

help:
	@echo "make setup     Create the venv, install dependencies, seed .env (first run)"
	@echo "make dev       Run backend and frontend together in one terminal (interleaved logs)"
	@echo "make backend   Start the dev database, migrate, run the API on :8000 (hot-reload)"
	@echo "make frontend  Run the Vite dev server on :5173 (second terminal)"
	@echo "make test      Start the test database and run pytest"
	@echo "               e.g. make test PYTEST_ARGS='tests/auth -x'"
	@echo "make migrate   Apply Alembic migrations to the dev database"
	@echo "make down      Stop the containers"

# The `test -f` guard is what keeps a second run from overwriting an existing .env,
# API keys and all, with the empty template.
setup:
	test -f .env || cp .env.example .env
	cd backend && python3 -m venv .venv
	cd backend && .venv/bin/pip install -r requirements.txt
	cd frontend && npm ci
	@echo "Now fill in .env (API keys, POSTGRES_PASSWORD), then run: make backend"

db:
	docker compose up -d --wait db

db-test:
	docker compose up -d --wait db-test

migrate: db
	cd backend && .venv/bin/alembic upgrade head

backend: migrate
	cd backend && .venv/bin/uvicorn main:app --reload

frontend:
	cd frontend && npm run dev

# The backslashes keep this one single shell, so `wait` knows about the background
# jobs. `kill 0` signals the whole process group, so Ctrl-C takes uvicorn and vite
# down with it instead of leaving them behind holding their ports.
dev: migrate
	@trap 'kill 0' EXIT; \
	(cd backend && .venv/bin/uvicorn main:app --reload) & \
	(cd frontend && npm run dev) & \
	wait

test: db-test
	cd backend && .venv/bin/pytest $(PYTEST_ARGS)

# The profile has to be named here, otherwise db-test is not part of the target set.
down:
	docker compose --profile test down
