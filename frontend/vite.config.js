import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    strictPort: true,
    allowedHosts: [
      "04083dbd-d36d-4f6d-a31b-60a2c71f49ea-00-3nxqn6ftxkbnl.kirk.replit.dev",
      "localhost",
      "127.0.0.1"
    ],
    proxy: {
      // Proxy API requests to Flask backend
      '/api': {
        target: 'http://localhost:5001', // Flask backend port
        changeOrigin: true,
        secure: false,
      }
    }
  },
  preview: {
    port: 5000,
  },
  build: {
    outDir: 'dist',
  }
})
