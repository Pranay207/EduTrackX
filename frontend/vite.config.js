import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    strictPort: true,
    allowedHosts: [
      "04083dbd-d36d-4f6d-a31b-60a2c71f49ea-00-3nxqn6ftxkbnl.kirk.replit.dev"
    ]
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
