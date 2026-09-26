# FastAPI Starter (fastgen)

A **production-shaped FastAPI starter** that stays organized as it grows: `src/`
layout, vertical-slice modules with an auto-maintained registry, async
SQLAlchemy, Alembic migrations, and a working CRUD example out of the box.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy 2.0">
  <img src="https://img.shields.io/badge/Alembic-migrations-orange" alt="Alembic">
  <img src="https://img.shields.io/badge/pytest-passing-brightgreen" alt="pytest">
  <img src="https://img.shields.io/badge/ruff-linted-000000?logo=ruff" alt="ruff">
</p>

## ✨ What you get

- **src/ layout** — no more `main.py` in the repo root; `src.main:app` is the entrypoint
- **Vertical-slice modules** — `src/modules/<feature>/` with `domain/` → `application/` → `infrastructure/` → `api/`, one folder per business unit
- **Auto-maintained registry** — `src/modules/__init__.py` maps every module to its import path; routers auto-mount into `main.py` from it, so adding a module never means touching `main.py`
- **Async SQLAlchemy 2.0** — `Mapped`/`mapped_column`, `AsyncAttrs`, `expire_on_commit=False`, a single `get_session` dependency
- **Alembic from day one** — schema lives in migrations, not `create_all`
- **A worked example** — the `note` module ships with real fields, validation, CRUD endpoints and endpoint tests
- **Zero lock-in** — plain FastAPI + SQLAlchemy. Nothing here depends on any generator, template magic, or framework

## 🚀 Quick start

```bash
uv sync                                  # install dependencies
uv run alembic upgrade head              # create the schema
uv run uvicorn src.main:app --reload     # http://localhost:8000/docs
```

Try the example CRUD:

```bash
curl -X POST localhost:8000/notes -H 'Content-Type: application/json' -d '{"title":"hello"}'
curl localhost:8000/notes
```

Run the tests:

```bash
uv run pytest
```

## 🧱 Project structure

```
my-app/
├── src/
│   ├── main.py                  # FastAPI app; module routers auto-load from the registry
│   ├── core/                    # shared infra (config + async database)
│   │   ├── config.py            # pydantic-settings, reads .env
│   │   └── database.py          # Base / engine / get_session
│   └── modules/
│       ├── __init__.py          # 📇 module registry (auto-maintained)
│       └── note/                # one vertical slice per business domain
│           ├── domain/          # entities + repository port (no I/O, no framework)
│           │   ├── model.py     # SQLAlchemy entity on Base
│           │   └── repository.py
│           ├── application/     # use cases + DTOs (free of HTTP)
│           │   ├── schemas.py   # NoteBase / NoteCreate / NoteUpdate / NoteRead
│           │   └── note_service.py
│           ├── infrastructure/  # SQLAlchemy adapter for the repository port
│           │   └── note_repository.py
│           ├── api/
│           │   └── router.py    # APIRouter(prefix="/notes"), SessionDep, 404 mapping
│           └── tests/
├── migrations/                  # Alembic (alembic.ini at the project root)
└── tests/                       # project-level tests (ASGI client fixture)
```

## ➕ Adding a module

With [fastgen-cli](https://github.com/YIbaikaishui/fastgen-cli) (zero install —
`uvx` runs it without installing anything):

```bash
uvx fastgen-cli make module order
```

That scaffolds `src/modules/order/` (domain / application / infrastructure / api
/ tests), registers it, and the router is served on the next restart — `main.py`
is never edited by hand:

```python
# src/modules/__init__.py — auto-maintained registry
modules: dict[str, str] = {
    "note": "src.modules.note",
    "order": "src.modules.order",
}

__all__ = ["modules"]

# src/main.py — the auto-mount block, generated once, never hand-edited
# --- fastgen: auto-mount (do not remove) ---
for _import_path in modules.values():
    _module = importlib.import_module(_import_path)
    app.include_router(_module.router)
# --- fastgen: end auto-mount ---
```

Check the project's module map anytime:

```bash
uvx fastgen-cli list
```

You can of course add modules by hand too — the registry is a plain dict.

## 🔁 Migrations

After changing a model:

```bash
uv run alembic revision --autogenerate -m "add note.done"
uv run alembic upgrade head
```

## 🧭 Conventions (fixed)

- One module = one folder; layers are `domain/` (entities + repository port), `application/` (schemas + service, no HTTP), `infrastructure/` (SQLAlchemy adapter), `api/` (router), `tests/`
- Sessions come from `src.core.database.get_session`; routers alias it as `SessionDep`
- Models use SQLAlchemy 2.0 `Mapped[...]` / `mapped_column(...)`; `__tablename__` is plural
- Schemas follow `XBase` / `XCreate` / `XUpdate` / `XRead`; `XRead` has `from_attributes=True`
- Services raise domain errors (`NoteNotFound`); routers map them to `HTTPException`
- Schema is managed by Alembic — never `create_all` at runtime

## 📄 License

MIT
