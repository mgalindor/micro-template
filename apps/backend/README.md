# Backend

A reference/demo backend showcasing FastAPI application development practices and
principles: a modular-monolith architecture, clean separation between layers
(router → service → repository), typed domain models (dataclasses), Pydantic only
at the edges, structured logging, RFC 7807 Problem Details error handling, and
database schema versioning with Alembic.

## Repository objective

This project demonstrates how to structure a production-style FastAPI service
around two observability-oriented domains:

- **Metrics** — record numeric metrics with tags, and query them by tag filters
  and a date range.
- **Traces** — record observability spans (trace id, span id, parent span,
  service/span name, timing, status, attributes) and look up all spans that
  belong to a given trace id.

The codebase follows a **modular monolith**: each business domain lives under
`src/backend/modules/<module_name>/` with its own router, schemas,
domain layer (dataclasses/commands/exceptions), service, repository and ORM
model. Shared infrastructure (config, logging, base exceptions, DB session,
Problem Detail helpers) lives under `src/backend/core/` and
`src/backend/db/`.

All API routes are registered under the `/api` prefix (see `main.py`), leaving
the rest of the path space free for the React SPA served from `apps/frontend`
(see the root [README.md](../../README.md) for the full deployment story).

> [!WARNING]
> The `metrics` and `traces` modules are **example code** meant to illustrate
> the project's conventions. Once the first real feature has been
> implemented, remove the example code:
>
> - `src/backend/modules/metrics/`
> - `src/backend/modules/traces/`
> - `migrations/versions/4085f30c8a93_create_metrics_and_traces_tables.py`
> - the `metrics`/`traces` router includes in `src/backend/main.py`
> - `tests/unit/metrics/`, `tests/unit/traces/`
> - `tests/e2e/metrics/`, `tests/e2e/traces/`

## Tech stack

- **Language/runtime:** Python 3.13
- **Web framework:** [FastAPI](https://fastapi.tiangolo.com/) (`fastapi[standard]`, includes Uvicorn)
- **ORM / DB access:** SQLAlchemy 2.x (async) + `asyncpg` driver
- **Database:** PostgreSQL 17 (via Docker Compose)
- **Schema migrations:** Alembic (async template), auto-applied on app startup
- **Settings:** Pydantic Settings, grouped by domain (`DatabaseConfig`, `LoggingConfig`, `AppConfig`)
- **Logging:** `structlog` (structured, JSON-rendered logs)
- **Error handling:** RFC 7807 Problem Details (`application/problem+json`)
- **Package manager:** [`uv`](https://docs.astral.sh/uv/)
- **Testing:** `pytest` + `pytest-asyncio`
- **Linting/formatting:** `ruff`
- **Type checking:** `mypy`

## Requirements

- Python 3.13+
- NodeJS 22+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed
- Docker (or a local PostgreSQL 17 instance) to run the database
- [Bruno](https://www.usebruno.com/) (app and/or [`@usebruno/cli`](https://www.npmjs.com/package/@usebruno/cli))
  to run the e2e HTTP collection under `tests/e2e`

## Getting started

1. Install dependencies (creates/updates the local virtual environment):

   ```powershell
   uv sync
   ```

2. Start PostgreSQL (defined in the repo root `compose.yaml`):

   ```powershell
   docker compose up -d postgres
   ```

   Default credentials/database (see `compose.yaml`): user `metrics`, password
   `pa55word`, database `metrics`, port `5432`. These match the defaults in
   `DatabaseConfig` (`src/backend/core/config.py`) and are already set in the
   tracked `.env.local` file; override them there or via environment variables
   (e.g. `APP_DB__HOST`, `APP_DB__PORT`, `APP_DB__PASSWORD`) if needed.

   > Alembic migrations run automatically on application startup
   > (`settings.run_migrations_on_startup`, default `True`), so there is no
   > separate manual migration step required to get going.

## Useful commands to run the app

Run the API with the project's console script (starts Uvicorn on `0.0.0.0:8000`
with reload enabled):

```powershell
uv run backend
```

Or run it directly with the FastAPI CLI (useful for choosing a different port
or running in production mode):

```powershell
uv run fastapi dev src/backend/main.py
# or
uv run fastapi run src/backend/main.py --port 8000
```

Once running, interactive API docs are available at `http://localhost:8000/docs`
and API routes live under `http://localhost:8000/api/*`.

### Database / Alembic commands

The application loads an execute Alembic migrations automatically on startup. You can still run Alembic commands manually if needed:

```powershell
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
uv run alembic downgrade base
uv run alembic current
uv run alembic check   # verifies there is no drift between models and DB
```

## Code quality checks

```powershell
uv run ruff check .
uv run ruff format src tests
uv run mypy src/backend --ignore-missing-imports
```

## Running tests

Run the full unit test suite (services tested against fake repositories, no
real database required):

```powershell
uv run pytest -q
```

## Running the e2e tests with Bruno

The `tests/e2e` folder contains a [Bruno](https://www.usebruno.com/) HTTP
collection (`metrics` and `traces` requests) with a `local` environment
pointing at `http://localhost:8000/api`.

1. Install Bruno CLI (requires Node.js):

   ```powershell
   npm install -g @usebruno/cli
   ```

2. Make sure the app is running locally (see "Useful commands to run the app"
   above) and PostgreSQL is up.

3. Run the collection against the `local` environment:

   ```powershell
   cd tests/e2e
   bru run --env local
   ```

   To run a single request instead of the whole collection:

   ```powershell
   bru run metrics/"Find Metrics.bru" --env local
   ```

You can also open the `tests/e2e` folder as a collection in the Bruno desktop
app, select the **local** environment, and run requests interactively.
