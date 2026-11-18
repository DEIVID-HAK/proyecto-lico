import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/api': {
        // En docker-compose, el backend corre en http://backend:8000
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true,
      }
    }
  }
})
