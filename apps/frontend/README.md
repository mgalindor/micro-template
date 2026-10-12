# Frontend

React + Vite + TypeScript SPA, consumed by the FastAPI backend (see the
[root README](../../README.md) for the deployment strategy).

> [!WARNING]
> The `metrics` and `traces` features are **example code** meant to illustrate
> the project's conventions. Once the first real feature has been
> implemented, remove the example code:
>
> - `src/features/metrics/`
> - `src/features/traces/`
> - `src/lib/api/metrics.ts`
> - `src/lib/api/traces.ts`
> - `src/types/metrics.ts`
> - `src/types/traces.ts`
> - the `metrics`/`traces` routes in `src/app/router.tsx`

## Stack

- **Build tool:** [Vite](https://vite.dev/)
- **Routing:** `react-router-dom` (`src/app/router.tsx`)
- **Data fetching:** native `fetch` wrapped in `src/lib/api/client.ts`, with
  a minimal hook (`useApiQuery`) for GETs with loading/error state.
- **Styling:** CSS Modules (`*.module.css` next to each component)

## Structure

```
src/
  app/        Layout, router
  features/   One folder per business domain (metrics, traces)
  lib/api/    HTTP client and fetching hooks
  types/      TS types mirroring the backend response schemas
```

## Local development

```powershell
npm install
npm run dev
```

Vite runs on `http://localhost:5173` and proxies `/api/*` to the backend. The
proxy target comes from `VITE_BACKEND_URL` (see `.env.local`); edit it if
your backend runs on a different host/port:

```
VITE_BACKEND_URL=http://localhost:8000
```

The HTTP client always calls relative paths (`/api/...`), so it works the same
in dev and in production (where FastAPI serves both the build and the API from
the same origin).

## Build

```powershell
npm run build
```

Generates `dist/`, which in production gets copied into the backend image
(see the root `Dockerfile`) and served as static files by FastAPI.

## Lint

```powershell
npm run lint
```


See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
