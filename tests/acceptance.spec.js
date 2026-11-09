import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const projects = [
  { slug: 'neom', en: 'NEOM', ar: 'نيوم' },
  { slug: 'qiddiya', en: 'Qiddiya', ar: 'القدية' },
  { slug: 'diriyah', en: 'Diriyah', ar: 'الدرعية' },
  { slug: 'roshn', en: 'ROSHN', ar: 'روشن' },
  { slug: 'the-red-sea', en: 'The Red Sea', ar: 'البحر الأحمر' },
  { slug: 'amaala', en: 'AMAALA', ar: 'أمالا' },
];

const routes = [{ en: 'Saudi Arabia’s giga-projects', ar: 'المشاريع السعودية الكبرى' }, ...projects];
const labels = {
  en: {
    language: 'العربية',
    skip: 'Skip to content',
    theme: 'Dark mode',
    scene: '3D map',
    exploreMap: 'Explore the map',
    missing: 'Page not found',
    return: 'Return to the atlas',
    fallback: 'The 3D map is unavailable. Explore using the project links.',
  },
  ar: {
    language: 'English',
    skip: 'انتقل إلى المحتوى',
    theme: 'الوضع الداكن',
    scene: 'خريطة ثلاثية الأبعاد',
    exploreMap: 'استكشف الخريطة',
    missing: 'الصفحة غير موجودة',
    return: 'العودة إلى الأطلس',
    fallback: 'الخريطة ثلاثية الأبعاد غير متاحة. يمكنك استكشاف المشاريع عبر الروابط.',
  },
};

const wcagTags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'];

function pathFor(locale, slug) {
  const prefix = locale === 'ar' ? '/ar' : '';
  return slug ? `${prefix}/projects/${slug}/` : `${prefix}/`;
}

async function loadImages(page) {
  await page.evaluate(async () => {
    for (const image of document.images) {
      image.loading = 'eager';
      image.decoding = 'sync';
    }
    await Promise.all(Array.from(document.images, image => image.decode()));
    await document.fonts.ready;
  });
}

async function capturePage(page, path) {
  await page.getByRole('main').scrollIntoViewIfNeeded();
  await page.evaluate(async () => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
  await page.screenshot({ path, fullPage: true, animations: 'disabled' });
}

async function assertFocusRing(control) {
  await expect(control).toBeFocused();
  const outline = await control.evaluate(element => getComputedStyle(element).outlineStyle);
  expect(outline).not.toBe('none');
}

async function assertReflow(page, width) {
  await page.setViewportSize({ width, height: 900 });
  const layout = await page.evaluate(() => {
    const viewport = document.documentElement.clientWidth;
    const controls = Array.from(document.querySelectorAll('a, button')).filter(
      element => element.getClientRects().length && getComputedStyle(element).visibility !== 'hidden',
    );
    const clipped = controls.filter(element => {
      const bounds = element.getBoundingClientRect();
      if (element.classList.contains('skip-link')) return false;
      return bounds.left < -1 || bounds.right > viewport + 1;
    }).map(element => element.textContent.trim() || element.getAttribute('aria-label'));
    return { overflow: document.documentElement.scrollWidth - viewport, clipped };
  });
  expect(layout, `Reflow at ${width}px`).toEqual({ overflow: 0, clipped: [] });
}

async function assertMapLabels(page) {
  const stage = page.locator('[data-atlas-stage]');
  const issues = await stage.evaluate(element => {
    const bounds = element.getBoundingClientRect();
    const labels = [...element.querySelectorAll('[data-atlas-link]')];
    return labels.flatMap((label, index) => {
      const { left, right, top, bottom } = label.getBoundingClientRect();
      const clipped = left < bounds.left || right > bounds.right || top < bounds.top || bottom > bounds.bottom;
      const overlapping = labels.slice(index + 1).some(other => {
        const rect = other.getBoundingClientRect();
        return left < rect.right && right > rect.left && top < rect.bottom && bottom > rect.top;
      });
      return clipped || overlapping ? [label.textContent] : [];
    });
  });
  expect(issues, 'Map labels fit without overlapping').toEqual([]);
}

for (const locale of ['en', 'ar']) {
  const alternate = locale === 'en' ? 'ar' : 'en';
  for (const theme of ['light', 'dark']) {
    for (const route of routes) {
      test(`${locale} ${theme} ${route.slug || 'home'}`, async ({ page, baseURL }, testInfo) => {
        await page.emulateMedia({ colorScheme: 'light', reducedMotion: 'no-preference' });
        await page.addInitScript(value => localStorage.setItem('atlas-theme', value), theme);
        const problems = [];
        const appOrigin = new URL(baseURL).origin;
        const staticResponses = [];
        page.on('pageerror', error => problems.push(error.message));
        page.on('response', response => {
          if (response.url().startsWith(`${appOrigin}/static/`)) {
            staticResponses.push(response.url());
            if (!response.ok() && response.status() !== 304) problems.push(`${response.status()} ${response.url()}`);
          }
        });
        page.on('requestfailed', request => {
          if (request.url().startsWith(`${appOrigin}/`)) problems.push(`${request.failure()?.errorText} ${request.url()}`);
        });

        const response = await page.goto(pathFor(locale, route.slug));
        expect(response?.status()).toBe(200);
        await expect(page.locator('html')).toHaveAttribute('lang', locale);
        await expect(page.locator('html')).toHaveAttribute('dir', locale === 'ar' ? 'rtl' : 'ltr');
        await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
        await expect(page.getByRole('heading', { level: 1 })).toHaveText(route[locale]);
        await expect(page).toHaveTitle(new RegExp(route[locale]));
        const description = await page.locator('meta[name="description"]').getAttribute('content');
        expect(description).toMatch(locale === 'ar' ? /\p{Script=Arabic}/u : /^[A-Za-z]/);
        await expect(page.getByRole('link', { name: labels[locale].language })).toHaveAttribute(
          'href', pathFor(alternate, route.slug),
        );
        await expect(page.locator(`link[rel="alternate"][hreflang="${alternate}"]`)).toHaveAttribute(
          'href', pathFor(alternate, route.slug),
        );
        await expect(page.getByRole('button', { name: labels[locale].theme })).toHaveAttribute(
          'aria-pressed', String(theme === 'dark'),
        );

        if (route.slug) {
          const next = projects[(projects.indexOf(route) + 1) % projects.length];
          await expect(page.locator('.next-project a')).toHaveAttribute('href', pathFor(locale, next.slug));
          await expect(page.locator('.detail-media img')).toHaveAttribute('alt', locale === 'ar' ? /\p{Script=Arabic}/u : /^[A-Za-z]/);
          await expect(page.locator('.detail-media figcaption a')).toHaveCount(0);
          await expect(page.locator('#sources-title')).toHaveCount(0);
          await expect(page.locator('.timeline li')).toHaveCount(3);
          await expect(page.locator('.story-grid article')).toHaveCount(3);
          await expect(page.locator('[data-project-viewer]')).toHaveCount(0);
          expect(await page.locator('[data-project-photo] img').count()).toBeGreaterThan(0);
        } else {
          await expect(page.locator('.project-card')).toHaveCount(6);
          await expect(page.locator('.atlas-poster')).toBeVisible();
          for (const project of projects) {
            await expect(page.getByRole('link', { name: project[locale], exact: true })).toHaveAttribute(
              'href', pathFor(locale, project.slug),
            );
          }
        }

        for (const width of [320, 390, 768, 1440]) {
          await assertReflow(page, width);
          if (!route.slug) await assertMapLabels(page);
        }
        await loadImages(page);
        const audit = await new AxeBuilder({ page }).withTags(wcagTags).analyze();
        expect(audit.violations.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }))).toEqual([]);
        expect(staticResponses.some(url => /\/static\/build\/assets\/.+-[\w-]+\.css$/.test(url))).toBe(true);
        expect(staticResponses.some(url => /\/static\/build\/assets\/.+-[\w-]+\.js$/.test(url))).toBe(true);
        expect(staticResponses.some(url => /\.(woff2?)$/.test(url))).toBe(true);
        expect(problems).toEqual([]);
        await capturePage(page, testInfo.outputPath('desktop.png'));

        if (!route.slug || route.slug === 'diriyah') {
          await page.setViewportSize({ width: 390, height: 844 });
          await capturePage(page, testInfo.outputPath('mobile.png'));
        }
      });
    }
  }

  test(`${locale} keyboard navigation and persistent preferences`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'light', reducedMotion: 'no-preference' });
    await page.goto(pathFor(locale));
    const skip = page.getByRole('link', { name: labels[locale].skip });
    const theme = page.getByRole('button', { name: labels[locale].theme });
    const switcher = page.getByRole('link', { name: labels[locale].language });
    const neom = page.getByRole('link', { name: projects[0][locale], exact: true });
    await page.keyboard.press('Tab');
    await assertFocusRing(skip);
    await page.keyboard.press('Enter');
    await expect(page.getByRole('main')).toBeFocused();
    await page.keyboard.press('Tab');
    await assertFocusRing(page.getByRole('link', { name: labels[locale].exploreMap }));
    await page.keyboard.press('Tab');
    await assertFocusRing(page.getByRole('button', { name: labels[locale].scene }));
    await page.keyboard.press('Tab');
    await assertFocusRing(neom);
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(new RegExp(`${pathFor(locale, 'neom')}$`));

    await page.keyboard.press('Tab');
    await assertFocusRing(skip);
    await page.keyboard.press('Tab');
    await assertFocusRing(page.locator('.brand'));
    await page.keyboard.press('Tab');
    await assertFocusRing(page.locator('.site-nav a'));
    await page.keyboard.press('Tab');
    await assertFocusRing(switcher);
    await page.keyboard.press('Tab');
    await assertFocusRing(theme);
    await page.keyboard.press('Space');
    await expect(theme).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.reload();
    await expect(theme).toHaveAttribute('aria-pressed', 'true');

    await switcher.focus();
    await page.keyboard.press('Enter');
    const alternate = locale === 'en' ? 'ar' : 'en';
    await expect(page).toHaveURL(new RegExp(`${pathFor(alternate, 'neom')}$`));
    await expect(page.locator('html')).toHaveAttribute('lang', alternate);
    await expect(page.getByRole('button', { name: labels[alternate].theme })).toHaveAttribute('aria-pressed', 'true');
    const tree = await page.locator('.site-header').ariaSnapshot();
    expect(tree).toContain(`button "${labels[alternate].theme}" [pressed]`);
    await page.getByRole('button', { name: labels[alternate].theme }).press('Space');
    await page.locator('.next-project a').click();
    await expect(page).toHaveURL(new RegExp(`${pathFor(alternate, 'qiddiya')}$`));
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  });

  test(`${locale} unknown project has a localized recovery link`, async ({ page }) => {
    const response = await page.goto(pathFor(locale, 'missing-project'));
    expect(response?.status()).toBe(404);
    await expect(page.getByRole('heading', { name: labels[locale].missing })).toBeVisible();
    await page.getByRole('link', { name: labels[locale].return }).click();
    await expect(page.getByRole('heading', { name: routes[0][locale] })).toBeVisible();
  });

  test(`${locale} reduced motion keeps the poster and project links`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(pathFor(locale));
    await expect(page.locator('.atlas-poster')).toBeVisible();
    await expect(page.getByRole('button', { name: labels[locale].scene })).toHaveCount(0);
    await expect(page.locator('[data-atlas-canvas] canvas')).toHaveCount(0);
    await page.getByRole('link', { name: projects[0][locale], exact: true }).click();
    await expect(page.getByRole('heading', { name: projects[0][locale] })).toBeVisible();
  });
}

test('English remains the default when the browser prefers Arabic', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ baseURL, locale: 'ar-SA' });
  try {
    const page = await context.newPage();
    await page.goto('/');
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    await expect(page.getByRole('heading', { name: routes[0].en })).toBeVisible();
  } finally {
    await context.close();
  }
});

test('project and language links work with JavaScript disabled', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ baseURL, javaScriptEnabled: false });
  try {
    const page = await context.newPage();
    await page.goto('/');
    await expect(page.locator('.atlas-poster')).toBeVisible();
    await expect(page.getByRole('button', { name: labels.en.theme })).toHaveCount(0);
    await expect(page.getByRole('button', { name: labels.en.scene })).toHaveCount(0);
    await page.getByRole('link', { name: 'AMAALA', exact: true }).click();
    await page.getByRole('link', { name: labels.en.language }).click();
    await expect(page).toHaveURL(/\/ar\/projects\/amaala\/$/);
    await expect(page.getByRole('heading', { name: 'أمالا', exact: true })).toBeVisible();
  } finally {
    await context.close();
  }
});

test('the photo viewer preserves the caption and returns focus on Escape', async ({ page }) => {
  await page.goto('/ar/projects/amaala/');
  const photo = page.locator('[data-project-gallery] [data-project-photo]');
  const dialog = page.getByRole('dialog', { name: 'عارض الصور' });
  await photo.press('Enter');
  await expect(dialog).toBeVisible();
  await expect(dialog.getByRole('button', { name: 'إغلاق الصورة' })).toBeFocused();
  await expect(dialog.locator('figcaption')).toHaveText(await photo.locator('..').locator('figcaption').innerText());
  await expect(dialog.locator('figcaption a')).toHaveCount(0);
  await page.keyboard.press('Escape');
  await expect(dialog).toBeHidden();
  await expect(photo).toBeFocused();
});

test('project films play directly without autoplay', async ({ page }) => {
  for (const project of projects) {
    await page.goto(pathFor('en', project.slug));
    const player = page.locator('.project-video video');
    await expect(player).toHaveAttribute('controls', '');
    await expect(player).not.toHaveAttribute('autoplay', '');
    await expect(player.locator('source')).toHaveAttribute('src', new RegExp(`/static/atlas/videos/${project.slug}-web\\.mp4$`));
    await player.evaluate(video => { video.muted = true; return video.play(); });
    await expect.poll(() => player.evaluate(video => video.currentTime)).toBeGreaterThan(0);
    await player.evaluate(video => video.pause());
  }
});

test('the deferred scene opens on demand and releases its canvas on close', async ({ page }, testInfo) => {
  const chunkRequests = [];
  page.on('request', request => {
    if (/\/atlas-scene-[\w-]+\.js$/.test(request.url())) chunkRequests.push(request.url());
  });
  await page.goto('/');
  const scene = page.getByRole('button', { name: labels.en.scene });
  await expect(scene).toBeVisible();
  await expect(scene).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('[data-atlas-canvas] canvas')).toHaveCount(0);
  expect(chunkRequests).toHaveLength(0);
  await scene.press('Space');
  await expect(scene).toHaveAttribute('aria-pressed', 'true', { timeout: 15000 });
  await expect(page.locator('[data-atlas-canvas] canvas')).toBeVisible();
  expect(chunkRequests).toHaveLength(1);
  await loadImages(page);
  await capturePage(page, testInfo.outputPath('3d-map.png'));
  const audit = await new AxeBuilder({ page }).withTags(wcagTags).analyze();
  expect(audit.violations.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }))).toEqual([]);
  await scene.press('Space');
  await expect(scene).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('[data-atlas-canvas] canvas')).toHaveCount(0);
  await expect(page.locator('.atlas-poster')).toBeVisible();

  await page.setViewportSize({ width: 320, height: 900 });
  await scene.press('Space');
  await expect(page.locator('[data-atlas-canvas] canvas')).toBeVisible();
  await assertMapLabels(page);
  await page.getByRole('link', { name: 'The Red Sea', exact: true }).click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('The Red Sea');
});

for (const fallback of ['WebGL2 unavailable', 'scene import failed']) {
  test(`${fallback} preserves the Arabic poster and navigation`, async ({ page }) => {
    if (fallback === 'WebGL2 unavailable') {
      await page.addInitScript(() => {
        const context = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function (type, ...args) {
          return type === 'webgl2' ? null : context.call(this, type, ...args);
        };
      });
    } else {
      await page.route(/\/atlas-scene-[\w-]+\.js$/, route => route.abort('failed'));
    }
    await page.goto('/ar/');
    const scene = page.getByRole('button', { name: labels.ar.scene });
    await scene.click();
    await expect(page.getByRole('status')).toHaveText(labels.ar.fallback, { timeout: 15000 });
    await expect(scene).toHaveAttribute('aria-pressed', 'false');
    await expect(page.locator('[data-atlas-canvas] canvas')).toHaveCount(0);
    await expect(page.locator('.atlas-poster')).toBeVisible();
    await page.getByRole('link', { name: projects[2].ar, exact: true }).click();
    await expect(page.getByRole('heading', { name: projects[2].ar })).toBeVisible();
  });
}
