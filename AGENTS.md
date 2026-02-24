# AGENTS

## Purpose
This file orients coding agents to the repo conventions, commands, and
style rules. Keep edits aligned with the existing FastAPI + SQLModel
structure.

## Repository Snapshot
- Language: Python (>=3.14)
- Frameworks: FastAPI, SQLModel, SQLAlchemy
- Entry point: `main.py` (creates `app`)
- DB: local Postgres URL in `app/db.py`
- Tooling: Ruff (lint + format) via pre-commit

## Build, Lint, Test

### Install / Build
There is no explicit build step; install deps and run the app.

- Install (uv, preferred):
  `uv sync`
- Install (pip, alternative):
  `python -m pip install -e .`

### Run App (local)
- Dev server (uvicorn):
  `uvicorn main:app --reload`
- Dev server (fastapi CLI):
  `fastapi dev main.py`

### Lint / Format
- Lint (Ruff):
  `ruff check .`
- Lint + auto-fix (Ruff):
  `ruff check . --fix`
- Format (Ruff):
  `ruff format .`
- Pre-commit (Ruff hooks):
  `pre-commit run --all-files`

### Tests
No test suite is configured yet; `pytest` is not listed in dependencies.
If tests are added, use these conventions:

- Run all tests:
  `python -m pytest`
- Run a single file:
  `python -m pytest path/to/test_file.py`
- Run a single test (node id):
  `python -m pytest path/to/test_file.py::TestClass::test_name`
- Run tests by name pattern:
  `python -m pytest -k "employee and not slow"`

If you add tests, update `pyproject.toml` with `pytest` and any plugins.

## Code Style Guidelines

### Imports
- Order imports in three blocks with a blank line between:
  1) standard library
  2) third-party
  3) local application modules (`app.*`)
- Use explicit imports (avoid wildcard imports).
- Prefer `from x import y` for commonly used names; keep modules small.

### Formatting
- Use Ruff formatting (`ruff format`).
- 4-space indentation; no tabs.
- Keep lines reasonably short (Ruff default formatting).
- One blank line between top-level definitions.
- Trailing commas in multi-line constructs for stable diffs.

### Types and Annotations
- Use type annotations for public functions and route handlers.
- Prefer built-in generic types (e.g., `list[Employee]`).
- Use `Optional[T]` and explicit `= None` when fields are nullable
  (matches current models and schemas).
- Keep return types explicit for endpoints (e.g., `-> Employee`).

### Naming Conventions
- Modules: `snake_case.py` (current layout already follows this).
- Classes: `PascalCase` (`Employee`, `EmployeeCreate`).
- Functions: `snake_case` (`create_employee`, `get_session`).
- Constants: `UPPER_SNAKE_CASE` (`POSTGRESQL_URL`).
- Use descriptive route names and consistent endpoint paths.

### FastAPI / SQLModel Patterns
- Routes live in `app/routes/*` and are registered in `main.py`.
- Use `APIRouter()` and keep endpoints focused on one responsibility.
- Use SQLModel models in `app/models.py` and schema classes in
  `app/schemas.py`.
- Use dependency-injected sessions (`SessionDep`) for DB access.
- Wrap DB operations with commit/refresh when mutating state.
- For partial updates, use `model_dump(exclude_unset=True)`.

### Error Handling
- Use `HTTPException` for request errors with explicit status codes.
- Prefer `status` constants (`status.HTTP_404_NOT_FOUND`).
- Return `None` only when response status is 204 or explicit.
- Keep validation and domain errors clear and consistent.

### API Behavior
- Use async endpoints only when awaiting IO; sync is fine for DB-only calls.
- Keep path parameters typed (e.g., `employee_id: int`).
- Return ORM/SQLModel instances only when they are valid response models.
- Favor list responses as `list[Model]` and cast query results explicitly.
- Include `status_code=204` for deletes that return `None`.
- Avoid mixing response shapes within the same endpoint.
- Use `.model_dump()` for create/replace payloads before constructing models.
- For PATCH, use `exclude_unset=True` to avoid overwriting fields.
- Raise 404 for missing resources before mutation.

### Data Modeling
- Use SQLModel `Field` for primary keys and indexed fields.
- Keep schema classes separate from persistence models.
- Ensure schema defaults match DB defaults when relevant.

### Dependency and Config Notes
- DB URL is set in `app/db.py` for local Postgres. If you change it,
  keep it centralized and configurable (env var or settings).
- `create_db_and_tables()` currently runs on app lifespan start.
  Be cautious about auto-migrations in production contexts.

## Project Conventions

### File Layout
- `main.py`: FastAPI app and router registration.
- `app/db.py`: engine, session dependency, and DB init.
- `app/models.py`: SQLModel table definitions.
- `app/schemas.py`: request/response schemas.
- `app/routes/`: API endpoints (group by domain).

### Testing Conventions (when added)
- Name tests `test_*.py` in a `tests/` folder.
- Keep unit tests deterministic and fast; isolate DB where possible.
- Use fixtures for shared setup (e.g., test DB sessions).

### Logging
- Prefer structured, minimal logging in endpoints; avoid noisy logs.
- If adding logging, use the standard library `logging` module.

## Cursor / Copilot Rules
- No Cursor rules found in `.cursor/rules/` or `.cursorrules`.
- No Copilot rules found in `.github/copilot-instructions.md`.

## Agent Tips
- Read existing code for patterns before introducing new ones.
- Keep changes small and consistent with existing style.
- Update this file if you introduce new tooling or conventions.
