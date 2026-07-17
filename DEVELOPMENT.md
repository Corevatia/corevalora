# Development

The setup for **working on** CoreValora: only the database stays in Docker, while
backend and frontend run natively as separate processes with **hot-reload**, so
changes to either show up instantly without rebuilding a container.

Just want to run the app? `docker compose up` needs none of this — see the
[README](README.md#quickstart).

## Prerequisites

- **Docker** — for the database and the test database.
- **Python 3.12** and **Node 20+**.
- A filled-in root `.env` — see [Configure environment](README.md#1-configure-environment).

> On **Windows**, run the commands below in **Git Bash** (ships with Git for
> Windows) so Unix commands like `cp` work. PowerShell alternatives are noted
> where they differ. **WSL2** works too and is the smoother path if you want the
> `make` shortcuts — but keep the repository inside the WSL filesystem
> (`/home/you/…`) rather than under `/mnt/c`. File-watching doesn't work reliably
> across that boundary, so hot-reload stops working without telling you.

The **frontend** has its own optional `frontend/.env` (`VITE_API_URL`). You only
need it if the backend isn't at the default `http://localhost:8000`; otherwise
skip it (`cp frontend/.env.example frontend/.env` to override).

## Run

Start only the database with Docker, then run the two services natively in separate
terminals.

```bash
docker compose up -d db
```

**Backend** (terminal 1):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate         # Linux / macOS
# source .venv/Scripts/activate   # Windows (Git Bash)
# .venv\Scripts\Activate.ps1      # Windows (PowerShell)
pip install -r requirements.txt
alembic upgrade head              # apply database migrations
uvicorn main:app --reload         # http://localhost:8000
```

> On Windows, **Git Bash is the smoother path**: the `source ...` command and the
> Unix-style `cp` work as-is. PowerShell needs an execution-policy tweak before
> `Activate.ps1` will run (e.g. `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)
> and uses backslash paths.

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

## Shortcuts

A `Makefile` wraps the commands above — run `make` to see every target:

```bash
make setup     # venv, dependencies and a starting .env (first run)
make dev       # backend + frontend in one terminal (mixed logs)
make backend   # database, migrations, API on :8000  (terminal 1)
make frontend  # Vite dev server on :5173            (terminal 2)
```

Needs a Unix shell — Linux, macOS, or WSL2. On native Windows, use the commands above.

## Testing

The backend suite (pytest) runs against a throwaway PostgreSQL container that lives
in tmpfs and starts empty on every run, so it never touches your dev database:

```bash
make test                            # brings up db-test, then runs pytest
make test PYTEST_ARGS='tests/auth'   # only part of the suite
```

Without make: `docker compose up -d --wait db-test`, then `cd backend && pytest`.
