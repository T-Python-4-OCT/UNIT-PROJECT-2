import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  outputDir: 'verification/test-results',
  workers: 1,
  timeout: 45_000,
  reporter: 'list',
  use: {
    baseURL: process.env.ATLAS_BASE_URL || 'http://127.0.0.1:8765',
    browserName: 'chromium',
    trace: 'retain-on-failure',
    launchOptions: {
      args: ['--enable-webgl', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
    },
  },
});
