import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/static/build/',
  plugins: [tailwindcss()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    origin: 'http://127.0.0.1:5173',
    cors: { origin: /^http:\/\/(localhost|127\.0\.0\.1):8000$/ },
  },
  build: {
    outDir: 'static/build',
    emptyOutDir: true,
    manifest: true,
    rolldownOptions: { input: 'frontend/main.js' },
  },
});
