(() => {
  if (!('onpageswap' in window && 'onpagereveal' in window)) return;
  const name = 'plate-image';
  const named = new Set();
  let pressed = null;

  const slugOf = (url) => {
    try {
      return new URL(url, location.href).pathname.match(/\/projects\/([^/]+)\/$/)?.[1] || null;
    } catch {
      return null;
    }
  };
  const set = (element, value) => {
    element.style.setProperty('view-transition-name', value);
    named.add(element);
  };
  const reset = () => {
    for (const element of named) element.style.removeProperty('view-transition-name');
    named.clear();
  };
  const onScreen = (element) => {
    const box = element.getBoundingClientRect();
    return box.width > 0 && box.bottom > 0 && box.right > 0 && box.top < innerHeight && box.left < innerWidth;
  };
  const pictureFor = (slug, preferred) => {
    const holders = [preferred?.closest('[data-plate]'), ...document.querySelectorAll('[data-plate]')];
    for (const holder of holders) {
      const image = holder?.dataset.plate === slug && holder.querySelector('img');
      if (image && onScreen(image)) return image;
    }
    return null;
  };
  const pair = (url, preferred) => {
    reset();
    const slug = slugOf(url);
    const image = slug && pictureFor(slug, preferred);
    if (!image) return;
    for (const part of document.querySelectorAll('.detail-hero-image, .detail-hero-copy')) {
      if (!part.contains(image)) set(part, 'none');
    }
    set(image, name);
  };

  addEventListener(
    'click',
    (event) => {
      pressed = event.target.closest?.('a[href]') || null;
    },
    true,
  );
  addEventListener('pageswap', (event) => {
    const to = event.activation?.entry?.url;
    if (event.viewTransition && to) pair(to, pressed);
  });
  addEventListener('pagereveal', (event) => {
    reset();
    if (!event.viewTransition) return;
    const from = window.navigation?.activation?.from?.url;
    if (from) pair(from);
    event.viewTransition.finished.then(reset, reset);
  });
})();
