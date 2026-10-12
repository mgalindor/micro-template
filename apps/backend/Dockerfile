# Etapa de build: instala dependencias y el proyecto con uv
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Instala solo dependencias primero para cachear esta capa mientras no cambien
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# alembic.ini y migrations/ deben copiarse: core/migrations.py resuelve su ruta
# de forma relativa a la posicion del codigo fuente en /app
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Imagen final: sin uv, solo runtime
FROM python:3.13-slim-trixie

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Se copia /app completo (no solo .venv): instalacion editable requiere que
# alembic.ini y migrations/ mantengan su posicion relativa a src/
COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1

USER nonroot
WORKDIR /app

EXPOSE 8000

CMD ["fastapi", "run", "--host", "0.0.0.0", "src/backend/main.py"]
