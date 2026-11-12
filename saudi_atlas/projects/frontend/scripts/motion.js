const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const texts = [
  '.section-head',
  '.atlas-stage',
  '.project-row-figure',
  '.project-row-body',
  '.explore-card',
  '.timeline > li',
  '.attraction-list > li',
  '.story-grid > *',
  '.glance',
  '.chronology-year',
  '.film-caption',
  '.result',
  '[data-locator-stage]',
].join(',');
const photos = '.gallery-photo, .project-video-player, .next-plate-image';
const scrubbed = typeof CSS !== 'undefined' && CSS.supports?.('animation-timeline: view()');

if (!reduced.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      let order = 0;
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const element = entry.target;
        element.style.setProperty('--reveal-order', String(Math.min(order++, 5)));
        element.setAttribute(element.hasAttribute('data-mask') ? 'data-mask' : 'data-reveal', 'in');
        observer.unobserve(element);
      }
    },
    { rootMargin: '0px 0px -8% 0px' },
  );

  const watch = (selector, attribute) => {
    for (const element of document.querySelectorAll(selector)) {
      if (element.closest('[data-expedition]')) continue;
      if (element.getBoundingClientRect().top < innerHeight) continue;
      element.setAttribute(attribute, '');
      observer.observe(element);
    }
  };
  watch(texts, 'data-reveal');
  if (!scrubbed) watch(photos, 'data-mask');

  reduced.addEventListener(
    'change',
    () => {
      observer.disconnect();
      for (const element of document.querySelectorAll('[data-reveal], [data-mask]')) {
        element.removeAttribute('data-reveal');
        element.removeAttribute('data-mask');
      }
    },
    { once: true },
  );
}
