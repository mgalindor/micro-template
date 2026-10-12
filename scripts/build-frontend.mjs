// Builds the frontend (Vite) and copies the output into the backend's static
// folder, so FastAPI can serve it directly (same layout the Dockerfile produces).
import { execSync } from 'node:child_process'
import { cpSync, existsSync, rmSync } from 'node:fs'
import path from 'node:path'

const rootDir = path.resolve(import.meta.dirname, '..')
const frontendDir = path.join(rootDir, 'apps/frontend')
const staticDir = path.join(rootDir, 'apps/backend/src/backend/static')

execSync('npm run build', { cwd: frontendDir, stdio: 'inherit' })

if (existsSync(staticDir)) rmSync(staticDir, { recursive: true, force: true })
cpSync(path.join(frontendDir, 'dist'), staticDir, { recursive: true })

console.log(`Frontend build copied to ${path.relative(rootDir, staticDir)}`)
