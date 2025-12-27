import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        host: '0.0.0.0',
        port: 3001,
        proxy: {
            '/api/vuln': {
                target: 'http://localhost:8004',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/vuln/, ''),
            },
            '/api/fixes': {
                target: 'http://localhost:8002',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/fixes/, '/fixes'),
            },
            '/api/logparser': { // Proxy for LogParser Service
                target: 'http://localhost:8001',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/logparser/, ''),
            },
            '/api/reports': { // Proxy for ReportGenerator Service
                target: 'http://localhost:8005',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/reports/, ''),
            },
            '/api/rabbit': { // Proxy for RabbitMQ Management
                target: 'http://localhost:15672/api',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/rabbit/, ''),
            },
            '/api/logcollector': {
                target: 'http://localhost:3344',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/logcollector/, ''),
            },
            '/api': {
                target: process.env.REACT_APP_API_URL || 'http://localhost',
                changeOrigin: true,
            }
        }
    }
})
