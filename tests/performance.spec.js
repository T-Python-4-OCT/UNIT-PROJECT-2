import { expect, test } from '@playwright/test';

const coreBudget = 1_000_000;
const sceneBudget = 3_000_000;

async function watchVitals(page) {
  await page.addInitScript(() => {
    window.atlasVitals = { lcp: 0, cls: 0, shifts: [] };
    new PerformanceObserver((list) => {
      window.atlasVitals.lcp = list.getEntries().at(-1).startTime;
    }).observe({ type: 'largest-contentful-paint', buffered: true });

    let sessionStart = 0;
    let previous = 0;
    let score = 0;
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.hadRecentInput) continue;
        window.atlasVitals.shifts.push({
          time: Math.round(entry.startTime),
          score: entry.value,
          elements: entry.sources.map(({ node }) => node?.id || node?.className || node?.nodeName),
        });
        if (entry.startTime - previous >= 1_000 || entry.startTime - sessionStart >= 5_000) {
          sessionStart = entry.startTime;
          score = 0;
        }
        score += entry.value;
        previous = entry.startTime;
        window.atlasVitals.cls = Math.max(score, window.atlasVitals.cls);
      }
    }).observe({ type: 'layout-shift', buffered: true });
  });
}

test.use({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, trace: 'off' });

for (const route of ['/', '/ar/', '/projects/neom/', '/ar/projects/diriyah/']) {
  test(`cold mobile performance ${route}`, async ({ page, context }) => {
    const cdp = await context.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
    await cdp.send('Network.emulateNetworkConditions', {
      offline: false, latency: 80, downloadThroughput: 1_250_000, uploadThroughput: 625_000,
    });
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await watchVitals(page);
    const samples = [];
    for (let sample = 0; sample < 3; sample++) {
      await page.goto(route, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await expect.poll(() => page.evaluate(() => window.atlasVitals.lcp)).toBeGreaterThan(0);
      const measurement = await page.evaluate(() => ({
        ...window.atlasVitals,
        transfer: performance.getEntriesByType('resource').reduce((sum, resource) => sum + resource.transferSize, 0)
          + performance.getEntriesByType('navigation')[0].transferSize,
        resources: performance.getEntriesByType('resource').length,
      }));
      samples.push(measurement);
    }
    const lcp = samples.map((sample) => Math.round(sample.lcp)).sort((a, b) => a - b);
    const cls = Math.max(...samples.map((sample) => sample.cls));
    const core = Math.max(...samples.map((sample) => sample.transfer));
    console.log(`${route} LCP ${lcp[1]} ms median (${lcp.join(', ')}), max CLS ${cls.toFixed(4)}, max core ${core} bytes`);
    if (cls > 0.1) console.log(JSON.stringify(samples.map((sample) => sample.shifts)));
    expect(lcp[1]).toBeLessThanOrEqual(2500);
    expect(cls).toBeLessThanOrEqual(0.1);
    expect(samples.every((sample) => sample.transfer > 0)).toBe(true);
    expect(core).toBeLessThanOrEqual(coreBudget);

    if (!route.includes('/projects/')) {
      const toggle = page.locator('[data-atlas-toggle]');
      await toggle.click();
      await expect(page.locator('[data-atlas-canvas] canvas')).toBeVisible();
      await page.waitForLoadState('networkidle');
      const scene = await page.evaluate((offset) => {
        const canvas = document.querySelector('[data-atlas-canvas] canvas');
        return {
          transfer: performance.getEntriesByType('resource').slice(offset).reduce((sum, item) => sum + item.transferSize, 0),
          pixelRatio: canvas.width / canvas.getBoundingClientRect().width,
        };
      }, samples.at(-1).resources);
      console.log(`${route} deferred scene ${scene.transfer} bytes, pixel ratio ${scene.pixelRatio.toFixed(2)}`);
      expect(scene.transfer).toBeGreaterThan(0);
      expect(scene.transfer).toBeLessThanOrEqual(sceneBudget);
      expect(scene.pixelRatio).toBeLessThanOrEqual(1.51);
    }
  });
}
