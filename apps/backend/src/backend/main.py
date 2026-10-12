import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.core.config import settings
from backend.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessError,
    DomainError,
    ResourceNotFoundError,
)
from backend.core.logging import configure_logging, log
from backend.core.middleware import RequestIDMiddleware
from backend.core.migrations import upgrade_schema_to_head
from backend.core.models import problem_response
from backend.db.session import SessionLocal, engine
from backend.modules.metrics.router import router as metrics_router
from backend.modules.traces.router import router as traces_router
from backend.modules.users.bootstrap import ensure_admin_user
from backend.modules.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    if settings.run_migrations_on_startup:
        # alembic usa asyncio.run internamente: se corre en un hilo aparte para no
        # chocar con el event loop de FastAPI ya en marcha.
        await asyncio.to_thread(upgrade_schema_to_head)
        log.info("schema.migrated")
    async with SessionLocal() as session:
        await ensure_admin_user(session)
        await session.commit()
    log.info("app.startup")
    yield
    await engine.dispose()
    log.info("app.shutdown")


app = FastAPI(title="Metrics Collector", lifespan=lifespan)

app.add_middleware(RequestIDMiddleware)

# Prefijo /api reserva el resto de rutas para el SPA servido como estatico.
app.include_router(metrics_router, prefix="/api")
app.include_router(traces_router, prefix="/api")
app.include_router(users_router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        {"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]}
        for error in exc.errors()
    ]
    log.warning(
        "request_validation_error",
        path=str(request.url),
        errors=errors,
    )
    return problem_response(
        request,
        status_code=400,
        title="Request Validation Failed",
        detail="One or more fields failed validation.",
        type_="urn:problem-type:validation-error",
        errors=errors,
    )

@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(
    request: Request, exc: ResourceNotFoundError
) -> JSONResponse:
    log.warning(
        "resource_not_found",
        path=str(request.url),
        resource=exc.resource_name,
        id=str(exc.resource_id),
    )
    return problem_response(
        request,
        status_code=404,
        title="Resource Not Found",
        detail=str(exc),
        type_="urn:problem-type:resource-not-found",
        resource=exc.resource_name,
        id=str(exc.resource_id),
    )


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    log.warning("business_error", path=str(request.url), code=exc.code)
    return problem_response(
        request,
        status_code=412,
        title="Business Rule Violation",
        detail=str(exc),
        type_="urn:problem-type:business-error",
        code=exc.code,
    )


@app.exception_handler(AuthenticationError)
async def authentication_error_handler(
    request: Request, exc: AuthenticationError
) -> JSONResponse:
    log.warning("authentication_error", path=str(request.url), detail=str(exc))
    response = problem_response(
        request,
        status_code=401,
        title="Authentication Failed",
        detail=str(exc),
        type_="urn:problem-type:authentication-error",
    )
    response.headers["WWW-Authenticate"] = "Bearer"
    return response


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(
    request: Request, exc: AuthorizationError
) -> JSONResponse:
    log.warning("authorization_error", path=str(request.url), detail=str(exc))
    return problem_response(
        request,
        status_code=403,
        title="Authorization Failed",
        detail=str(exc),
        type_="urn:problem-type:authorization-error",
    )


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    log.warning("domain_error", path=str(request.url), detail=str(exc))
    return problem_response(
        request,
        status_code=400,
        title="Domain Error",
        detail=str(exc),
        type_="urn:problem-type:domain-error",
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Última línea de defensa: nunca exponer el detalle interno al cliente.
    log.error("unhandled_exception", path=str(request.url), exc_info=exc)
    return problem_response(
        request,
        status_code=500,
        title="Internal Server Error",
        detail="An unexpected error occurred while processing the request.",
        type_="urn:problem-type:internal-server-error",
    )


# El build del frontend (Vite) se copia aqui en la imagen Docker; en dev local
# esta carpeta puede no existir y el SPA simplemente no se sirve.
_STATIC_DIR = Path(__file__).resolve().parent / "static"

if _STATIC_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=_STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str) -> FileResponse:
        # Cualquier ruta fuera de /api devuelve index.html: el ruteo lo resuelve
        # React Router en el cliente.
        return FileResponse(_STATIC_DIR / "index.html")
