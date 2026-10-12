# Imagen unica: FastAPI sirve tanto la API (/api/*) como el build estatico del SPA.
# Util para desplegar el mini-proyecto como un solo servicio (p. ej. en Railway).

# Etapa 1: build del frontend (Vite)
FROM node:22-slim AS frontend-builder
WORKDIR /frontend
COPY apps/frontend/package*.json ./
RUN npm ci
COPY apps/frontend/ ./
RUN npm run build

# Etapa 2: instala dependencias y el proyecto backend con uv
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS backend-builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Instala solo dependencias primero para cachear esta capa mientras no cambien
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=apps/backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=apps/backend/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# alembic.ini y migrations/ deben copiarse: core/migrations.py resuelve su ruta
# de forma relativa a la posicion del codigo fuente en /app
COPY apps/backend/ /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Imagen final: sin uv ni node, solo runtime
FROM python:3.13-slim-trixie

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Se copia /app completo (no solo .venv): instalacion editable requiere que
# alembic.ini y migrations/ mantengan su posicion relativa a src/
COPY --from=backend-builder --chown=nonroot:nonroot /app /app
# El build del SPA se sirve como estatico desde backend/main.py (ver _STATIC_DIR)
COPY --from=frontend-builder --chown=nonroot:nonroot /frontend/dist /app/src/backend/static

ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1

USER nonroot
WORKDIR /app

EXPOSE 8000

CMD ["fastapi", "run", "--host", "0.0.0.0", "src/backend/main.py"]
