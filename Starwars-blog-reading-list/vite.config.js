import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            '/people': 'http://127.0.0.1:3000',
            '/planets': 'http://127.0.0.1:3000',
            '/vehicles': 'http://127.0.0.1:3000',
            '/users': 'http://127.0.0.1:3000',
            '^/favorite/': 'http://127.0.0.1:3000'
        }
    },
    build: {
        outDir: 'dist'
    }
})
