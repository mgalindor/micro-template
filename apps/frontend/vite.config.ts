import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // VITE_BACKEND_URL lets each dev point the proxy at a different local/remote
  // backend (defaults to the FastAPI dev server on :8000). See .env.local.
  const backendUrl = env.VITE_BACKEND_URL || 'http://localhost:8000'

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api': backendUrl,
      },
    },
  }
})
