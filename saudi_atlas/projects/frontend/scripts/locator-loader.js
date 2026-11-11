const locator = document.querySelector('[data-locator]');

if (locator && 'IntersectionObserver' in window) {
  const stage = locator.querySelector('[data-locator-stage]');
  const mount = locator.querySelector('[data-locator-canvas]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const anchor = locator.dataset.x ? [Number(locator.dataset.x), Number(locator.dataset.y)] : null;
  let generation = 0;
  let relief;

  function stop() {
    generation += 1;
    relief?.dispose();
    relief = undefined;
    mount.replaceChildren();
    stage.removeAttribute('data-locator-ready');
  }

  async function start() {
    if (relief || motion.matches || navigator.connection?.saveData) return;
    const attempt = ++generation;
    try {
      const { mountLocator, loadTerrain } = await import('./locator-scene.js');
      if (attempt !== generation) return;
      await loadTerrain();
      if (attempt !== generation) return;
      relief = mountLocator({
        stage,
        mount,
        anchor,
        accent: locator.dataset.accent,
        onReady: () => stage.setAttribute('data-locator-ready', ''),
        onError: stop,
      });
    } catch {
      if (attempt === generation) stop();
    }
  }

  const nearby = new IntersectionObserver(
    ([entry]) => {
      if (!entry.isIntersecting) return;
      nearby.disconnect();
      start();
    },
    { rootMargin: '200px 0px' },
  );

  const watch = () => {
    if (!motion.matches) nearby.observe(stage);
  };
  motion.addEventListener('change', () => {
    stop();
    nearby.disconnect();
    watch();
  });
  window.addEventListener('pagehide', stop);
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) watch();
  });
  watch();
}
