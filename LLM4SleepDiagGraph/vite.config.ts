import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// see https://stackoverflow.com/questions/73834404/react-uncaught-referenceerror-process-is-not-defined
// otherwise use import.meta.env.VITE_BACKEND_API_URL and expose it as such with the VITE_ prefix
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    define: {
      'process.env': env,
    },
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 5173
    }
  }
})
