---
name: coding-python
description: Coding practices required for all python backend code development
metadata:
    type: skill
    version: "1.0.0"
    updated-at: "2026-09-07"
---

# Coding Policy — FastAPI Enterprise

> **Project architecture: modular monolith.** The app is organized in `app/modules/<module_name>/` (e.g. `users`, `metrics`). Each module brings its own router, domain, schemas, service, and repository, and never imports another module's domain/repository directly. Shared infrastructure lives in `app/core/` and `app/db/`. The layers described below repeat **inside each module** (see section 11 for the full tree).

## 1. Application Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Router / Controller / Primary Adapter  (FastAPI)           │
│  - Defines endpoints                                         │
│  - Input/output validation with Pydantic                     │
│  - Pydantic → Dataclass conversion                            │
│  - Dependency injection                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │  Dataclass (no dict, no pydantic)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Service  (business logic)                                   │
│  - Orchestrates operations                                    │
│  - Does NOT know HTTP, does NOT know SQL, no DB connection, no ORM entities │
│  - Receives and returns Dataclasses                            │
└──────────────────────┬──────────────────────────────────────┘
                       │  Dataclass
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Repository / Adapter  (data access / external services)    │
│  - SQLAlchemy, Redis, HTTP clients, etc.                      │
│  - Receives and returns domain Dataclasses                     │
└─────────────────────────────────────────────────────────────┘
```

**Golden rule:** a layer only knows the layer immediately below it, and communicates with it via **typed Dataclasses**. Never dicts, never loose kwargs, never Pydantic leaking into the domain.


## Global (singleton) Vs Per-request Variable

┌─────────────────────────────────────────────────────────────┐
│  EXPENSIVE to create  →  must be SINGLETON (1 per process)  │
│                                                             │
│  • SQLAlchemy Engine                                         │
│    - Opens real TCP connections to Postgres                  │
│    - Builds the entire pool                                   │
│    - Cost: ~10-50ms + N persistent connections                 │
│                                                             │
│  • Redis client                                              │
│    - Opens a socket, negotiates protocol                        │
│    - Cost: ~5-20ms                                              │
│                                                             │
│  • HTTP clients (httpx, aiohttp)                              │
│    - Configure an internal connection pool                      │
│    - Cost: ~5-15ms                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CHEAP to create  →  must be PER-REQUEST (1 per request)    │
│                                                             │
│  • SQLAlchemy Session                                          │
│    - Only requests a connection from the pool (already exists)   │
│    - Cost: ~microseconds                                        │
│                                                             │
│  • Repository                                                   │
│    - Only holds a reference to the session                        │
│    - Cost: ~nanoseconds                                           │
│                                                             │
│  • Service                                                       │
│    - Only holds a reference to the repository                     │
│    - Cost: ~nanoseconds                                           │
└─────────────────────────────────────────────────────────────┘

## Dependency Injection
HTTP Request
    ↓
[1] Router                app/modules/users/router.py
    │                       ↑ receives UserServiceDep
    │
[2] Service               app/modules/users/service.py
    │                       ↑ receives UserRepositoryDep
    │
[3] Repository (adapter)  app/modules/users/repository.py
    │                       ↑ receives Session (injected in __init__)
    │
[4] SQLAlchemy Session    app/db/session.py  (get_db with yield, shared)
    │
[5] Engine + Pool         app/db/session.py  (module-level singleton, shared)
    ↓
Postgres / SQLite

And the DI graph that FastAPI resolves automatically:

```text
get_db()  ──→  get_user_repository(session)  ──→  get_user_service(repository)
                                                       ↓
                                              router uses UserServiceDep
```

1. app/db/session.py — the heart of the pool (shared across modules)
```py
engine = create_engine(...)              # singleton, holds the pool
SessionLocal = sessionmaker(bind=engine) # factory, NOT a session
def get_db() -> Iterator[Session]:
    db = SessionLocal()  # takes a connection from the pool
    try:
        yield db         # injected into the repository
    finally:
        db.close()       # returns the connection to the pool
```

2. app/modules/users/repository.py — the adapter
```py
class UserRepository:
    def __init__(self, session: Session):  # session comes via DI
        self._session = session
    
    def get_by_id(self, user_id: int) -> User | None:
        orm = self._session.get(UserORM, user_id)
        return self._to_domain(orm) if orm else None  # ORM → dataclass
```

3. app/modules/users/service.py — business logic
```py
class UserService:
    def __init__(self, repository: UserRepository):  # repo comes via DI
        self._repository = repository
    
    def create(self, command: CreateUserCommand) -> User:
        if self._repository.get_by_email(command.email):
            raise EmailAlreadyExistsError(command.email)
        return self._repository.create(...)
```

4. app/modules/users/dependencies.py — the module wiring
```py
SessionDep          = Annotated[Session, Depends(get_db)]
UserRepositoryDep   = Annotated[UserRepository, Depends(get_user_repository)]
UserServiceDep      = Annotated[UserService, Depends(get_user_service)]
```

5. app/modules/users/router.py — the router that uses the service
```py
from fastapi import APIRouter, Depends
from app.modules.users.dependencies import UserServiceDep

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreateRequest,  # Pydantic - validates HTTP request
    service: UserServiceDep,
) -> UserResponse:
    user = service.create(payload.to_domain())  # .to_domain() → dataclass
    return UserResponse.from_domain(user)       # dataclass → Pydantic
```



## Rules
- Pydantic ONLY at the edges
- Dataclasses for communication between layers
- Configuration with Pydantic Settings
- Pydantic request models always have to include validations
- Request and responses have include body never list directly; always wrap in a Pydantic model

### 3.1 Definition
```python
# app/modules/users/domain/models.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

@dataclass(frozen=True, slots=True)
class User:
    id: int | None
    email: str
    full_name: str
    status: UserStatus
    created_at: datetime
    
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE
```

### 3.2 Why dataclasses and not dicts
| Aspect | `dict` | `dataclass` |
|---|---|---|
| IDE typing | ❌ `dict[str, Any]` or none | ✅ Full autocomplete |
| Type checking (mypy) | ❌ Loses info on every access | ✅ Compile-time errors |
| Runtime validation | ❌ `KeyError` in production | ✅ Clear `AttributeError` |
| Immutability | ❌ Mutable by default | ✅ `frozen=True` |
| Documentation | ❌ Implicit schema | ✅ Every field self-documented |
| Safe refactor | ❌ Renaming a field = silent bug | ✅ mypy catches it |

> **AI agent rule:** when an LLM (Copilot, Cursor, Claude) suggests `user_data: dict` or `**kwargs`, reject it. Always demand an explicit dataclass or TypedDict (the latter only for cases where the structure varies dynamically).

### 3.3 Pydantic ↔ Dataclass Conversion
```python
# app/modules/users/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from app.modules.users.domain.models import User, UserStatus

class UserCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")  # rejects extra fields
    
    email: EmailStr
    full_name: str
    
    def to_domain(self) -> "UserCreate":  # intermediate dataclass
        return UserCreate(
            email=self.email,
            full_name=self.full_name,
        )

# app/modules/users/domain/commands.py
@dataclass(frozen=True, slots=True)
class UserCreate:
    email: str
    full_name: str
```

> **Why not pass Pydantic directly to the service:** because it couples the domain to an HTTP schema. If tomorrow you want to consume this same service from a Celery worker or a CLI, you end up dragging Pydantic into places it doesn't belong.



---

## 5. Error Handling

### 5.1 Generic Exception Hierarchy (shared)

`app/core/exceptions.py` defines a **generic hierarchy per HTTP error category**, not one exception per use case. All modules reuse these bases:

```python
# app/core/exceptions.py — base shared by all modules
class DomainError(Exception):
    """Base for all business errors."""

class NotFoundError(DomainError):
    """A resource referenced by id does not exist. Maps to 404."""

class ConflictError(DomainError):
    """Duplicate state or concurrency conflict. Maps to 409."""

class BusinessRuleViolationError(DomainError):
    """Valid payload but violates a business rule. Maps to 412."""
```

### 5.2 Per-module Domain Exceptions — ALWAYS extend a generic base

```python
# app/modules/users/domain/exceptions.py
from app.core.exceptions import NotFoundError, ConflictError

class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

class EmailAlreadyExistsError(ConflictError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} is already registered")
```

### 5.3 Global Exception Handlers — registered ONCE per category

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import NotFoundError, ConflictError, BusinessRuleViolationError

app = FastAPI()

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"title": "Resource Not Found", "status": 404, "detail": str(exc), "instance": request.url.path},
    )

@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"title": "Conflict", "status": 409, "detail": str(exc), "instance": request.url.path},
    )

@app.exception_handler(BusinessRuleViolationError)
async def business_rule_handler(request: Request, exc: BusinessRuleViolationError):
    return JSONResponse(
        status_code=412,
        content={"title": "Business Rule Violation", "status": 412, "detail": str(exc), "instance": request.url.path},
    )
```

> **Critical rule:** never add a new `@app.exception_handler(...)` in `main.py` for every new module exception. A new domain exception (e.g. `OrderAlreadyShippedError`) must **extend** one of the existing generic bases (`NotFoundError`, `ConflictError`, `BusinessRuleViolationError`, etc.) instead of inheriting directly from `DomainError`. By inheriting from the right base, the already-registered generic handler catches it automatically — no need to touch `main.py`. Only create a new base/handler when a genuinely new **category** of HTTP error appears (not a new use case).
>
> **Rule:** internal layers (service, repository) raise domain exceptions. Only the router (or the global handlers) translate them into `HTTPException` or `JSONResponse`.
>
> For the exact error body format (Problem Details, `location` field for validation errors, etc.) use the REST API best practices skill.

> **Modular monolith:** `app/main.py` is also the only place that imports and registers each module's router:
> ```python
> from app.modules.users.router import router as users_router
>
> app.include_router(users_router)
> ```

---

## 6. Structured Logging

```python
# app/core/logging.py
import structlog

log = structlog.get_logger()

# Usage
log.info("user.created", user_id=user.id, email=user.email)
log.error("payment.failed", order_id=order.id, reason=str(e))
```

> **Never** `print()`. **Never** `logging.info(...)` with concatenated strings. Always key-value fields so it's parseable by ELK/Datadog.

---

## 7. Mandatory Type Hints

```python
# ✅ Good
def calculate_total(items: list[OrderItem], tax_rate: Decimal) -> Decimal:
    ...

# ❌ Bad
def calculate_total(items, tax_rate):
    ...
```

Rules:
- All public functions with type hints (arguments and return).
- `mypy --strict` must pass on `app/modules/*/domain/`, `app/modules/*/service.py`, `app/modules/*/repository.py`.
- `Optional[T]` is replaced by `T | None` (Python 3.10+).
- For collections: `list[T]`, `dict[K, V]`, `set[T]` (not `List`, `Dict` from the `typing` module).

---


## 9. Testing

### 9.1 Structure
```
tests/
├── unit/                # Tests without I/O (services, domain logic), organized by module
│   └── users/
│       └── test_user_service.py
├── integration/         # Tests with DB (testcontainers), organized by module
│   └── users/
│       └── test_users_api.py
└── e2e/                 # Tests with TestClient or AsyncClient against the full app
```

### 9.2 Pattern
```python
# tests/unit/users/test_user_service.py
import pytest
from app.modules.users.service import UserService
from app.modules.users.domain.commands import UserCreate
from app.modules.users.repository import UserRepository  # protocol
from tests.fakes import FakeUserRepository

def test_create_user_sets_default_status():
    repo = FakeUserRepository()
    service = UserService(repo)
    
    user = service.create(UserCreate(email="a@b.com", full_name="Alice"))
    
    assert user.email == "a@b.com"
    assert user.status == UserStatus.ACTIVE
```

> **Rule:** services are tested with repository **fakes** (not a real DB). Repositories are tested with **testcontainers** (real DB, not in-memory SQLite). The HTTP layer is tested with `httpx.AsyncClient` + `ASGITransport`.

### 9.3 Dependency Override in Tests
```python
# tests/integration/users/test_users_api.py
from app.main import app
from app.modules.users.dependencies import get_user_service

def test_create_user_endpoint(client, fake_user_service):
    app.dependency_overrides[get_user_service] = lambda: fake_user_service
    response = client.post("/users", json={"email": "a@b.com", "full_name": "Alice"})
    assert response.status_code == 201
    app.dependency_overrides.clear()
```

---

## 10. Explicit Anti-patterns (PR rejection)

| Anti-pattern | Why it's bad | Alternative |
|---|---|---|
| `def endpoint(db: Session = Depends(get_db))` that does `db.query(...)` directly | Business logic in the router, not testable without a DB | Service + Repository |
| Passing `dict` between layers | Loses types, unsafe refactor | Dataclass |
| `from app.modules.users.orm import UserORM` in the service | Couples the domain to the ORM | Repository returns a dataclass |
| Importing `repository`/`orm` from another module directly | Breaks isolation between modules, couples the monolith | Consume the other module's public `service`, or move the shared part to a shared kernel in `app/core/` |
| `global DB_SESSION` | Thread-unsafe, not testable | Depends |
| `@app.on_event("startup")` (deprecated) | Replaced by `lifespan` | Use the `lifespan` context manager |
| Adding a `@app.exception_handler(MyNewException)` in `main.py` for every new exception | `main.py` grows without limit, duplicates HTTP-translation logic per use case | Inherit from the correct generic base (`NotFoundError`, `ConflictError`, `BusinessRuleViolationError`) in `app/core/exceptions.py` |
| `Optional[X]` | Verbose in Python 3.10+ | `X \| None` |
| `print()` for logging | Not structured, not filterable | `structlog` |
| `try/except: pass` | Hides errors, never re-logged | `log.exception()` or `raise` |
| `from typing import List, Dict` | Deprecated in 3.9+ | `list`, `dict` builtins |
| Magic numbers (`pool_size=5`) | No context | Named constants or config |

---

## 11. Recommended Folder Structure (modular monolith)

```
app/
├── main.py                     # FastAPI app + lifespan, includes each module's router
├── core/
│   ├── config.py               # Shared settings (Pydantic Settings)
│   ├── logging.py               # structlog config
│   └── exceptions.py           # DomainError base + global handlers
├── db/
│   ├── session.py              # engine, get_db (shared singleton)
│   └── base.py                 # SQLAlchemy declarative Base
├── modules/
│   ├── users/                   # ← one module = one self-contained business domain
│   │   ├── router.py            # module's FastAPI endpoints
│   │   ├── schemas.py           # Pydantic (request/response)
│   │   ├── domain/
│   │   │   ├── models.py        # domain dataclasses
│   │   │   ├── commands.py      # command dataclasses (service input)
│   │   │   └── exceptions.py    # module's domain exceptions
│   │   ├── service.py           # business logic
│   │   ├── repository.py        # data access
│   │   ├── orm.py               # SQLAlchemy models (table=True)
│   │   └── dependencies.py      # Annotated types + module wiring
│   └── <other_module>/          # same pattern, copy the "users" folder as a template
└── tests/
    ├── unit/<module>/
    ├── integration/<module>/
    └── e2e/
```

**Module isolation rules:**
- A module never imports `domain`, `repository`, or `orm` from another module directly.
- The only way to communicate between modules is through another module's public `service` (injected via `Depends`), or by extracting the shared part to `app/core/` (shared kernel).
- Every new module is created by copying the `modules/users/` structure and adjusting names.
- `app/main.py` is the only place that knows about all modules (calls `app.include_router(...)` for each one).

---

## 12. Code Review (PR checklist)

- [ ] Do routers only orchestrate (no business logic)?
- [ ] Are requests/responses Pydantic, and the domain Dataclass?
- [ ] Do layers communicate with Dataclasses, not dicts?
- [ ] Are dependencies injected via `Depends()`, not globals?
- [ ] Are domain exceptions translated in handlers?
- [ ] Structured logging, no prints?
- [ ] Complete type hints? Does mypy pass?
- [ ] Unit tests for the new logic?
- [ ] Do Ruff format + ruff check pass?

