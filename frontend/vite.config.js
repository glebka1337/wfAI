import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
const backendUrl = process.env.VITE_BACKEND_URL || 'http://localhost:8000';
console.log('🔧 Vite Proxy Target:', backendUrl);

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: backendUrl,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
    host: true, // Needed for Docker
    watch: {
      usePolling: true // Needed for Docker volumes on some systems
    }
  }
})
