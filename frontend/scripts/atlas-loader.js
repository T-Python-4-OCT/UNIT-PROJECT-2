const atlas = document.querySelector('[data-atlas]');

if (atlas) {
  const stage = atlas.querySelector('[data-atlas-stage]');
  const mount = atlas.querySelector('[data-atlas-canvas]');
  const toggle = atlas.querySelector('[data-atlas-toggle]');
  const status = atlas.querySelector('[data-atlas-status]');
  const links = [...atlas.querySelectorAll('[data-atlas-link]')];
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let open = false;
  let generation = 0;
  let relief;

  function close() {
    generation += 1;
    open = false;
    relief?.dispose();
    relief = undefined;
    mount.replaceChildren();
    toggle.removeAttribute('aria-busy');
    toggle.setAttribute('aria-pressed', 'false');
  }

  function unavailable() {
    close();
    status.textContent = status.dataset.unavailableLabel;
  }

  function syncMotion() {
    if (motion.matches) {
      if (document.activeElement === toggle) links[0]?.focus();
      close();
      status.textContent = '';
    }
    toggle.hidden = motion.matches;
  }

  toggle.addEventListener('click', async () => {
    if (motion.matches) return;
    status.textContent = '';
    if (open) {
      close();
      return;
    }

    open = true;
    const attempt = ++generation;
    toggle.setAttribute('aria-busy', 'true');
    try {
      const { mountRelief } = await import('./atlas-scene.js');
      if (attempt !== generation) return;
      relief = mountRelief({ stage, mount, links, onError: unavailable });
      toggle.removeAttribute('aria-busy');
      toggle.setAttribute('aria-pressed', 'true');
    } catch {
      if (attempt === generation) unavailable();
    }
  });

  motion.addEventListener('change', syncMotion);
  window.addEventListener('pagehide', close);
  syncMotion();
}
