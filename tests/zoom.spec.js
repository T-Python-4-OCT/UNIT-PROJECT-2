import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { chromium, expect, test } from '@playwright/test';

const projects = ['neom', 'qiddiya', 'diriyah', 'roshn', 'the-red-sea', 'amaala'];

test('Edge reflows the full atlas at 200% browser zoom', async ({ baseURL }, testInfo) => {
  const profile = testInfo.outputPath('zoom-profile');
  const settings = join(profile, 'Default');
  await mkdir(settings, { recursive: true });
  await writeFile(join(settings, 'Preferences'), JSON.stringify({
    partition: { default_zoom_level: { x: Math.log(2) / Math.log(1.2) } },
  }));

  const context = await chromium.launchPersistentContext(profile, {
    channel: 'msedge',
    viewport: null,
    args: ['--window-size=1000,800'],
  });
  try {
    const page = context.pages()[0];
    for (const prefix of ['', '/ar']) {
      for (const path of ['/', '/timeline/', '/compare/', ...projects.map((slug) => `/projects/${slug}/`)]) {
        const response = await page.goto(`${baseURL}${prefix}${path}`);
        expect(response.status()).toBe(200);
        await page.evaluate(() => document.fonts.ready);
        await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
        const widths = await page.evaluate(() => ({
          layout: document.documentElement.clientWidth,
          content: document.documentElement.scrollWidth,
          window: outerWidth,
        }));
        expect(widths.layout / widths.window).toBeGreaterThan(0.45);
        expect(widths.layout / widths.window).toBeLessThanOrEqual(0.51);
        expect(widths.content, `${prefix}${path} at 200% zoom`).toBeLessThanOrEqual(widths.layout + 1);
      }
    }
    await page.screenshot({ path: 'verification/zoom-ar-detail.png', fullPage: true });
  } finally {
    await context.close();
  }
});
