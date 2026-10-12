---
client: client-name-here
project: project-name-here
summary: project summary goes here
type: project-brief
created-at: YYYY-MM-DD
working-mode: yolo|relaxed|strict
configured: false
---


# project-name-here

Template to quickly bootstrap full-stack web mini-projects: **React (Vite +
TypeScript)** on the frontend and **FastAPI (Python 3.13)** on the backend, in
a single repository (monorepo), with a deployment pattern designed to
simplify operating small projects as much as possible.


## Main features

- **feature**: description 


## Requirements 
- [Python](https://www.python.org/) 3.13 o superior
- [uv](https://docs.astral.sh/uv/) (gestor de entornos/dependencias de Python)
- [Node.js](https://nodejs.org/) (LTS recomendado) y npm (se instala junto con Node.js)


## Structure

```
apps/
  backend/    FastAPI, modular monolith (sample metrics + traces domains)
  frontend/   React + Vite + TypeScript, React Router, CSS Modules
Dockerfile    Multi-stage build: compiles the frontend and serves it from FastAPI
compose.yaml  Postgres + combined image, to spin everything up with one command
docs/         Specs / architecture decisions
```

Each folder (`apps/backend`, `apps/frontend`) has its own README with
command details, conventions, and tests.

## Getting Started

How to get the project up and running locally.

## Deployment strategy

**By default, FastAPI serves the static React build** (see
`apps/backend/src/backend/main.py`): all API routes live under
`/api/*`, and any other route returns `index.html` so React Router can
resolve client-side routing. This allows deploying **a single service**
(e.g. on Railway) instead of two.

Reasons for this default on mini-projects:

- A single domain, no CORS configuration needed.
- A single build/deploy pipeline and a single set of environment variables.
- Fewer moving parts to maintain when reusing this template for the next
  small project.

The root `Dockerfile` builds in 3 stages: compiles `apps/frontend` (Node),
compiles/installs `apps/backend` (uv), and copies the frontend build output
into the final Python image as static files.

### Escape hatch: splitting frontend and backend

If a specific project grows and needs CDN/edge caching or PR preview
deployments, it can be split without restructuring the repo:

- **Backend on Railway**: configure the service with *Root Directory* =
  `apps/backend` and use `apps/backend/Dockerfile` (standalone, without the SPA).
- **Frontend on Vercel**: configure the project with *Root Directory* =
  `apps/frontend`, and set `VITE_API_BASE_URL` (or whichever variable your
  HTTP client uses) pointing to the backend's domain on Railway. You'll need
  to configure CORS in FastAPI for the Vercel domain.

## Local development

A root [package.json](package.json) wires both apps together for convenience:

```powershell
npm install                 # once, installs root tooling (concurrently) + frontend deps
uv sync --directory apps/backend   # once, creates the backend venv

npm run dev                 # runs frontend (Vite) + backend (uvicorn, reload) in parallel
npm run build                # builds the frontend and copies dist/ into the backend's static folder
npm start                    # build + start a single FastAPI process serving API and SPA
```

1. Backend only (see [apps/backend/README.md](apps/backend/README.md) for details):

   ```powershell
   cd apps/backend
   uv sync
   docker compose up -d postgres   # from the repo root
   uv run backend
   ```

2. Frontend only (see [apps/frontend/README.md](apps/frontend/README.md)):

   ```powershell
   cd apps/frontend
   npm install
   npm run dev
   ```

   Vite runs on `http://localhost:5173` and proxies `/api/*` to the URL set in
   `VITE_BACKEND_URL` (defaults to `http://localhost:8000`, see
   `apps/frontend/.env.local` and `vite.config.ts`), so the frontend's HTTP
   client always calls relative paths (`/api/...`).

3. To test the combined build via Docker (single image, as in production):

   ```powershell
   docker compose up --build
   ```

   The full app (API + SPA) is available at `http://localhost:8000`.


