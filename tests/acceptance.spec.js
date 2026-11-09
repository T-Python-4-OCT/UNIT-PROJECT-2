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

const pages = [
  { path: '', en: 'Six projects across Saudi Arabia', ar: 'ستة مشاريع في أنحاء السعودية' },
  { path: 'timeline/', en: 'Every milestone in one sequence', ar: 'كل المحطات في تسلسل واحد' },
  { path: 'compare/', en: 'The six side by side', ar: 'المشاريع الستة جنبًا إلى جنب' },
  ...projects.map(project => ({ ...project, path: `projects/${project.slug}/` })),
];

const labels = {
  en: {
    language: 'العربية',
    skip: 'Skip to content',
    theme: 'Dark mode',
    scene: '3D map',
    exploreMap: 'Explore the map',
    browse: 'Browse the projects',
    projects: 'Projects',
    missing: 'Page not found',
    return: 'Return to the atlas',
    viewer: 'Photo viewer',
    close: 'Close',
    next: 'Next photo',
    fallback: 'The 3D map is unavailable. Explore using the project links.',
  },
  ar: {
    language: 'English',
    skip: 'انتقل إلى المحتوى',
    theme: 'الوضع الداكن',
    scene: 'خريطة ثلاثية الأبعاد',
    exploreMap: 'استكشف الخريطة',
    browse: 'تصفح المشاريع',
    projects: 'المشاريع',
    missing: 'الصفحة غير موجودة',
    return: 'العودة إلى الأطلس',
    viewer: 'عارض الصور',
    close: 'إغلاق',
    next: 'الصورة التالية',
    fallback: 'الخريطة ثلاثية الأبعاد غير متاحة. يمكنك استكشاف المشاريع عبر الروابط.',
  },
};

const wcagTags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'];
const at = (locale, path = '') => `${locale === 'ar' ? '/ar' : ''}/${path}`;
const header = page => page.locator('.site-header');
const mapLink = (page, name) => page.locator('.atlas-controls').getByRole('link', { name, exact: true });

async function loadImages(page) {
  await page.evaluate(async () => {
    for (const image of document.images) {
      image.loading = 'eager';
      image.decoding = 'sync';
    }
    await Promise.all(Array.from(document.images, image => image.decode().catch(() => {})));
    await document.fonts.ready;
  });
}

async function capturePage(page, path) {
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
    const controls = Array.from(document.querySelectorAll('a, button, summary')).filter(
      element => element.getClientRects().length && getComputedStyle(element).visibility !== 'hidden',
    );
    const clipped = controls.filter(element => {
      if (element.classList.contains('skip-link')) return false;
      const bounds = element.getBoundingClientRect();
      return bounds.left < -1 || bounds.right > viewport + 1;
    }).map(element => element.textContent.trim() || element.getAttribute('aria-label'));
    const header = document.querySelector('.header-bar').getBoundingClientRect().height;
    return { overflow: document.documentElement.scrollWidth - viewport, clipped, oneRowHeader: header < 80 };
  });
  expect(layout, `Reflow at ${width}px`).toEqual({ overflow: 0, clipped: [], oneRowHeader: true });
}

async function assertMapLabels(page) {
  const issues = await page.locator('[data-atlas-stage]').evaluate(element => {
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
    for (const route of pages) {
      test(`${locale} ${theme} ${route.path || 'home'}`, async ({ page, baseURL }, testInfo) => {
        await page.emulateMedia({ colorScheme: 'light', reducedMotion: 'no-preference' });
        await page.addInitScript(value => localStorage.setItem('atlas-theme', value), theme);
        const problems = [];
        const appOrigin = new URL(baseURL).origin;
        const staticResponses = [];
        page.on('pageerror', error => problems.push(error.message));
        page.on('response', response => {
          if (response.url().startsWith(`${appOrigin}/static/`)) {
            staticResponses.push(response.url());
            if (!response.ok() && response.status() !== 304 && response.status() !== 206) problems.push(`${response.status()} ${response.url()}`);
          }
        });

        const response = await page.goto(at(locale, route.path));
        expect(response?.status()).toBe(200);
        await expect(page.locator('html')).toHaveAttribute('lang', locale);
        await expect(page.locator('html')).toHaveAttribute('dir', locale === 'ar' ? 'rtl' : 'ltr');
        await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
        await expect(page.getByRole('heading', { level: 1 })).toHaveText(route[locale]);
        await expect(page).toHaveTitle(new RegExp(route[locale]));
        const description = await page.locator('meta[name="description"]').getAttribute('content');
        expect(description).toMatch(locale === 'ar' ? /\p{Script=Arabic}/u : /^[A-Za-z]/);
        await expect(header(page).getByRole('link', { name: labels[locale].language })).toHaveAttribute('href', at(alternate, route.path));
        await expect(page.locator(`link[rel="alternate"][hreflang="${alternate}"]`)).toHaveAttribute('href', `${appOrigin}${at(alternate, route.path)}`);
        await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `${appOrigin}${at(locale, route.path)}`);
        await expect(header(page).getByRole('button', { name: labels[locale].theme })).toHaveAttribute('aria-pressed', String(theme === 'dark'));

        if (route.slug) {
          const index = projects.findIndex(project => project.slug === route.slug);
          const next = projects[(index + 1) % projects.length];
          const previous = projects[(index + projects.length - 1) % projects.length];
          await expect(page.locator('.pager-next')).toHaveAttribute('href', at(locale, `projects/${next.slug}/`));
          await expect(page.locator('.pager-previous')).toHaveAttribute('href', at(locale, `projects/${previous.slug}/`));
          await expect(page.locator('.detail-hero img')).toHaveAttribute('alt', locale === 'ar' ? /\p{Script=Arabic}/u : /^[A-Za-z]/);
          await expect(page.locator('#sources-title')).toHaveCount(0);
          await expect(page.locator('.story-grid article')).toHaveCount(3);
          await expect(page.locator('.attraction-list li')).toHaveCount(3);
          await expect(page.locator('.glance-list > div')).toHaveCount(3);
          expect(await page.locator('.milestones .timeline li').count()).toBeGreaterThanOrEqual(3);
          expect(await page.locator('[data-project-photo]').count()).toBeGreaterThan(0);
          await expect(page.locator('.project-video video')).toHaveAttribute('poster', /-poster\.webp$/);
          await expect(header(page).locator(`a[aria-current="page"][href="${at(locale, route.path)}"]`)).toHaveCount(1);
        } else if (!route.path) {
          await expect(page.locator('.project-row')).toHaveCount(6);
          await expect(page.locator('.hero-mosaic a')).toHaveCount(6);
          await expect(page.locator('.atlas-poster')).toBeVisible();
          for (const project of projects) {
            await expect(mapLink(page, project[locale])).toHaveAttribute('href', at(locale, `projects/${project.slug}/`));
          }
        }

        for (const width of [320, 390, 768, 1024, 1440]) {
          await assertReflow(page, width);
          if (!route.path) await assertMapLabels(page);
        }
        await loadImages(page);
        const audit = await new AxeBuilder({ page }).withTags(wcagTags).analyze();
        expect(audit.violations.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }))).toEqual([]);
        expect(staticResponses.some(url => /\/static\/build\/assets\/.+-[\w-]+\.css$/.test(url))).toBe(true);
        expect(staticResponses.some(url => /\/static\/build\/assets\/.+-[\w-]+\.js$/.test(url))).toBe(true);
        expect(staticResponses.some(url => /\.(woff2?)$/.test(url))).toBe(true);
        expect(problems).toEqual([]);
        await capturePage(page, testInfo.outputPath('desktop.png'));
        await page.setViewportSize({ width: 390, height: 844 });
        await capturePage(page, testInfo.outputPath('mobile.png'));
      });
    }
  }

  test(`${locale} keyboard navigation and persistent preferences`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'light', reducedMotion: 'no-preference' });
    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(at(locale));
    const skip = page.getByRole('link', { name: labels[locale].skip });
    const theme = header(page).getByRole('button', { name: labels[locale].theme });
    const switcher = header(page).getByRole('link', { name: labels[locale].language });
    await page.keyboard.press('Tab');
    await assertFocusRing(skip);
    await page.keyboard.press('Enter');
    await expect(page.getByRole('main')).toBeFocused();
    await page.keyboard.press('Tab');
    await assertFocusRing(page.getByRole('link', { name: labels[locale].exploreMap }));
    await page.keyboard.press('Tab');
    await assertFocusRing(page.getByRole('link', { name: labels[locale].browse }));
    await page.keyboard.press('Tab');
    await assertFocusRing(page.locator('.hero-mosaic a').first());
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(new RegExp(`${at(locale, 'projects/neom/')}$`));

    await page.keyboard.press('Tab');
    await assertFocusRing(skip);
    await page.keyboard.press('Tab');
    await assertFocusRing(header(page).locator('.brand'));
    await page.keyboard.press('Tab');
    const summary = header(page).locator('.projects-menu summary');
    await assertFocusRing(summary);
    await page.keyboard.press('Enter');
    await expect(header(page).locator('.projects-menu')).toHaveAttribute('open', '');
    await page.keyboard.press('Escape');
    await expect(header(page).locator('.projects-menu')).not.toHaveAttribute('open', '');
    await expect(summary).toBeFocused();
    await switcher.focus();
    await page.keyboard.press('Tab');
    await assertFocusRing(theme);
    await page.keyboard.press('Space');
    await expect(theme).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.reload();
    await expect(theme).toHaveAttribute('aria-pressed', 'true');

    await switcher.focus();
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(new RegExp(`${at(alternate, 'projects/neom/')}$`));
    await expect(page.locator('html')).toHaveAttribute('lang', alternate);
    const alternateTheme = header(page).getByRole('button', { name: labels[alternate].theme });
    await expect(alternateTheme).toHaveAttribute('aria-pressed', 'true');
    await alternateTheme.press('Space');
    await page.locator('.pager-next').click();
    await expect(page).toHaveURL(new RegExp(`${at(alternate, 'projects/qiddiya/')}$`));
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  });

  test(`${locale} compact menu opens, closes and returns focus`, async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(at(locale));
    const toggle = header(page).locator('[data-menu-toggle]');
    await expect(toggle).toBeVisible();
    await expect(header(page).locator('.site-nav')).toBeHidden();
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(header(page).locator('.site-nav')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(toggle).toBeFocused();
    await toggle.click();
    await header(page).locator('.projects-menu summary').click();
    await header(page).locator('.projects-menu-list').getByRole('link', { name: new RegExp(projects[2][locale]) }).click();
    await expect(page.getByRole('heading', { level: 1 })).toHaveText(projects[2][locale]);
  });

  test(`${locale} unknown project has a localized recovery link`, async ({ page }) => {
    const response = await page.goto(at(locale, 'projects/missing-project/'));
    expect(response?.status()).toBe(404);
    await expect(page.getByRole('heading', { name: labels[locale].missing })).toBeVisible();
    await page.getByRole('link', { name: labels[locale].return }).click();
    await expect(page.getByRole('heading', { level: 1 })).toHaveText(pages[0][locale]);
  });

  test(`${locale} reduced motion keeps the poster and project links`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(at(locale));
    await expect(page.locator('.atlas-poster')).toBeVisible();
    await expect(page.getByRole('button', { name: labels[locale].scene })).toHaveCount(0);
    await expect(page.locator('[data-atlas-canvas] canvas')).toHaveCount(0);
    await mapLink(page, projects[0][locale]).click();
    await expect(page.getByRole('heading', { level: 1 })).toHaveText(projects[0][locale]);
  });

  test(`${locale} the photo viewer steps through photos and returns focus`, async ({ page }) => {
    await page.goto(at(locale, 'projects/diriyah/'));
    const photos = page.locator('[data-project-photo]');
    const dialog = page.getByRole('dialog', { name: labels[locale].viewer });
    await photos.first().press('Enter');
    await expect(dialog).toBeVisible();
    await expect(dialog.getByRole('button', { name: labels[locale].close })).toBeFocused();
    await expect(dialog.locator('figcaption')).toHaveText(await page.locator('.gallery-grid figcaption').first().innerText());
    await expect(dialog.locator('[data-photo-counter]')).toContainText('1');
    await dialog.getByRole('button', { name: labels[locale].next }).click();
    await expect(dialog.locator('figcaption')).toHaveText(await page.locator('.gallery-grid figcaption').nth(1).innerText());
    await page.keyboard.press('Escape');
    await expect(dialog).toBeHidden();
    await expect(photos.first()).toBeFocused();
  });
}

test('English remains the default when the browser prefers Arabic', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ baseURL, locale: 'ar-SA' });
  try {
    const page = await context.newPage();
    await page.goto('/');
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  } finally {
    await context.close();
  }
});

test('project, menu and language links work with JavaScript disabled', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ baseURL, javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  try {
    const page = await context.newPage();
    await page.goto('/');
    await expect(page.locator('.atlas-poster')).toBeVisible();
    await expect(page.locator('.site-nav')).toBeVisible();
    await expect(page.getByRole('button', { name: labels.en.theme })).toHaveCount(0);
    await expect(page.getByRole('button', { name: labels.en.scene })).toHaveCount(0);
    await mapLink(page, 'AMAALA').click();
    await page.locator('.site-header').getByRole('link', { name: labels.en.language }).click();
    await expect(page).toHaveURL(/\/ar\/projects\/amaala\/$/);
    await expect(page.getByRole('heading', { level: 1 })).toHaveText('أمالا');
    await page.goto('/timeline/?project=qiddiya');
    await expect(page.locator('.chronology-year li')).toHaveCount(3);
  } finally {
    await context.close();
  }
});

test('project films have posters, captions in the page language and no autoplay', async ({ page }) => {
  for (const locale of ['en', 'ar']) {
    for (const project of projects) {
      await page.goto(at(locale, `projects/${project.slug}/`));
      const player = page.locator('.project-video video');
      await expect(player).toHaveAttribute('controls', '');
      await expect(player).not.toHaveAttribute('autoplay', '');
      await expect(player.locator('source')).toHaveAttribute('src', new RegExp(`/static/atlas/videos/${project.slug}\\.mp4$`));
      const defaults = await player.locator('track[default]').evaluateAll(tracks => tracks.map(track => track.srclang));
      expect(defaults.every(lang => lang === locale)).toBe(true);
      if (locale === 'en') {
        await player.evaluate(video => { video.muted = true; return video.play(); });
        await expect.poll(() => player.evaluate(video => video.currentTime)).toBeGreaterThan(0);
        await player.evaluate(video => video.pause());
      }
    }
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
  await mapLink(page, 'The Red Sea').click();
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
    await mapLink(page, projects[2].ar).click();
    await expect(page.getByRole('heading', { level: 1 })).toHaveText(projects[2].ar);
  });
}
