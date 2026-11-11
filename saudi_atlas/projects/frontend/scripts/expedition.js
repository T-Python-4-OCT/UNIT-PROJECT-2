const section = document.querySelector('[data-expedition]');

if (section && 'IntersectionObserver' in window) {
  const stage = section.querySelector('[data-atlas-stage]');
  const mount = section.querySelector('[data-atlas-canvas]');
  const toggle = section.querySelector('[data-atlas-toggle]');
  const status = section.querySelector('[data-atlas-status]');
  const controls = section.querySelector('.atlas-controls');
  const ring = section.querySelector('[data-atlas-ring]');
  const links = new Map(
    [...section.querySelectorAll('[data-atlas-link]')].map((link) => [link.dataset.project, link]),
  );
  const rows = [...section.querySelectorAll('li.project-row[data-project]')];
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const KEY = 'atlas-3d';
  const SLOW_FRAME = 120;
  const SLOW_RUN = 40;
  const WARM_UP = 12;

  let running = false;
  let active = null;
  let scene = null;
  let generation = 0;
  let near = false;
  let scrolled = false;
  let onScreen = false;
  let queued = 0;
  let tooSlow = false;
  let pointerAt = -Infinity;
  let observers = [];

  function stored() {
    try {
      return localStorage.getItem(KEY);
    } catch {
      return null;
    }
  }

  function remember(value) {
    try {
      localStorage.setItem(KEY, value);
    } catch {}
  }

  const saveData = () => navigator.connection?.saveData === true;
  const webgl2Likely = () => 'WebGL2RenderingContext' in window;

  function wanted() {
    const choice = stored();
    if (choice === 'on') return true;
    if (choice === 'off') return false;
    return !saveData();
  }

  const pressed = () => toggle.getAttribute('aria-pressed') === 'true';
  const setPressed = (value) => toggle.setAttribute('aria-pressed', String(value));

  function setActive(row) {
    if (row === active) return;
    active = row;
    for (const item of rows) item.toggleAttribute('data-active', item === row);
    for (const [slug, link] of links)
      link.toggleAttribute('data-active', !!row && slug === row.dataset.project);
    const link = row && links.get(row.dataset.project);
    if (link?.dataset.anchorX) {
      ring.style.setProperty('--ring-x', link.dataset.anchorX);
      ring.style.setProperty('--ring-y', link.dataset.anchorY);
      ring.setAttribute('data-visible', '');
    } else {
      ring.removeAttribute('data-visible');
    }
  }

  function layout() {
    return getComputedStyle(section).getPropertyValue('--journey').trim();
  }

  function focusLine() {
    const kind = layout();
    const top = parseFloat(getComputedStyle(stage).top) || 0;
    if (kind === 'wide') return (top + innerHeight) / 2;
    if (kind === 'narrow') return (top + stage.offsetHeight + innerHeight) / 2;
    return innerHeight / 2;
  }

  const crossing = new Set();
  let line = 0;
  let middle = null;
  function onCrossing(entries) {
    for (const entry of entries) {
      if (entry.isIntersecting) crossing.add(entry.target);
      else crossing.delete(entry.target);
    }
    if (crossing.size) {
      const distance = (row) => {
        const box = row.getBoundingClientRect();
        return Math.abs(box.top + box.height / 2 - line);
      };
      setActive([...crossing].sort((a, b) => distance(a) - distance(b))[0]);
      return;
    }
    const before = rows[0].getBoundingClientRect().top > line;
    const after = rows.at(-1).getBoundingClientRect().bottom < line;
    if (before || after) setActive(null);
  }

  function observeLine() {
    const next = Math.round(focusLine());
    if (middle && Math.abs(next - line) < 2) return;
    middle?.disconnect();
    crossing.clear();
    line = next;
    middle = new IntersectionObserver(onCrossing, {
      rootMargin: `${-line}px 0px ${line - innerHeight}px 0px`,
    });
    rows.forEach((row) => middle.observe(row));
  }

  function measure() {
    const focus = line || focusLine();
    const centres = rows.map((row) => {
      const r = row.getBoundingClientRect();
      return r.top + r.height / 2;
    });
    const lastIndex = centres.length - 1;
    if (focus <= centres[0]) return (focus - centres[0]) / (centres[1] - centres[0]);
    if (focus >= centres[lastIndex])
      return lastIndex + (focus - centres[lastIndex]) / (centres[lastIndex] - centres[lastIndex - 1]);
    let index = 0;
    while (index < lastIndex - 1 && focus >= centres[index + 1]) index++;
    return index + (focus - centres[index]) / (centres[index + 1] - centres[index]);
  }

  function update() {
    queued = 0;
    if (scene && onScreen) scene.setProgress(measure());
  }

  function onScroll() {
    if (!queued) queued = requestAnimationFrame(update);
  }

  let resizing = 0;
  function onResize() {
    if (resizing) return;
    resizing = requestAnimationFrame(() => {
      resizing = 0;
      if (running) observeLine();
      onScroll();
    });
  }

  function watchFrames(attempt) {
    if (stored() === 'on') return;
    let previous = 0;
    let count = 0;
    let average = 0;
    let slowRun = 0;
    const tick = (now) => {
      if (attempt !== generation || !scene) return;
      if (!onScreen || document.hidden) {
        previous = 0;
        requestAnimationFrame(tick);
        return;
      }
      if (previous) {
        count += 1;
        const interval = now - previous;
        if (count > WARM_UP) {
          average = average ? average * 0.85 + interval * 0.15 : interval;
          slowRun = average > SLOW_FRAME ? slowRun + 1 : 0;
          if (slowRun >= SLOW_RUN) {
            tooSlow = true;
            stop3D();
            setPressed(false);
            return;
          }
        }
      }
      previous = now;
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  function stop3D() {
    generation += 1;
    scene?.dispose();
    scene = null;
    mount.replaceChildren();
    stage.removeAttribute('data-scene-ready');
    controls.inert = false;
    toggle.removeAttribute('aria-busy');
  }

  function unavailable() {
    stop3D();
    setPressed(false);
    status.textContent = status.dataset.unavailableLabel;
  }

  function probe() {
    try {
      const context = document.createElement('canvas').getContext('webgl2');
      if (!context) return false;
      context.getExtension('WEBGL_lose_context')?.loseContext();
      return true;
    } catch {
      return false;
    }
  }

  function stops() {
    return rows.map((row) => {
      const link = links.get(row.dataset.project);
      const anchor = link?.dataset.anchorX
        ? [Number(link.dataset.anchorX), Number(link.dataset.anchorY)]
        : null;
      return {
        slug: row.dataset.project,
        anchor,
        accent: row.style.getPropertyValue('--accent-dark').trim() || '#e6c27c',
      };
    });
  }

  async function start3D() {
    if (scene || toggle.hasAttribute('aria-busy') || !running) return;
    status.textContent = '';
    if (!webgl2Likely() || !probe()) {
      unavailable();
      return;
    }
    const attempt = ++generation;
    toggle.setAttribute('aria-busy', 'true');
    try {
      const { mountExpedition, loadTerrain } = await import('./expedition-scene.js');
      if (attempt !== generation) return;
      await loadTerrain();
      if (attempt !== generation) return;
      scene = mountExpedition({
        stage,
        mount,
        stops: stops(),
        direction: document.documentElement.dir === 'rtl' ? 'rtl' : 'ltr',
        onReady: () => {
          if (attempt !== generation) return;
          toggle.removeAttribute('aria-busy');
          if (controls.contains(document.activeElement)) toggle.focus();
          controls.inert = true;
          stage.setAttribute('data-scene-ready', '');
          watchFrames(attempt);
        },
        onError: () => {
          if (attempt === generation) unavailable();
        },
      });
      scene.setProgress(measure());
    } catch {
      if (attempt === generation) unavailable();
    }
  }

  function maybeStart() {
    if (running && near && scrolled && !tooSlow && pressed() && !scene) start3D();
  }

  function onFirstScroll() {
    if (scrollY <= 0) return;
    scrolled = true;
    removeEventListener('scroll', onFirstScroll);
    maybeStart();
  }

  toggle.addEventListener('click', () => {
    if (!running) return;
    status.textContent = '';
    if (pressed()) {
      remember('off');
      setPressed(false);
      stop3D();
      return;
    }
    remember('on');
    setPressed(true);
    tooSlow = false;
    const box = stage.getBoundingClientRect();
    if (box.bottom <= 0 || box.top >= innerHeight) stage.scrollIntoView({ block: 'nearest' });
    start3D();
  });

  section.addEventListener('pointerdown', () => {
    pointerAt = performance.now();
  });
  section.addEventListener('focusin', (event) => {
    const row = event.target.closest('li.project-row');
    if (!row || !layout() || performance.now() - pointerAt < 600) return;
    const align = () => row.scrollIntoView({ block: 'end', behavior: 'instant' });
    align();

    requestAnimationFrame(() => {
      if (row.contains(document.activeElement)) align();
    });
  });

  function begin() {
    if (running) return;
    running = true;
    toggle.hidden = false;
    setPressed(!tooSlow && wanted() && webgl2Likely());
    observeLine();
    addEventListener('resize', onResize, { passive: true });
    const nearby = new IntersectionObserver(
      ([entry]) => {
        near = entry.isIntersecting;
        maybeStart();
      },
      { rootMargin: '100% 0px' },
    );
    nearby.observe(stage);
    const visible = new IntersectionObserver(([entry]) => {
      onScreen = entry.isIntersecting;
      if (onScreen) {
        addEventListener('scroll', onScroll, { passive: true });
        onScroll();
      } else {
        removeEventListener('scroll', onScroll);
      }
    });
    visible.observe(section);
    observers = [nearby, visible];
    if (scrollY > 0) scrolled = true;
    else addEventListener('scroll', onFirstScroll, { passive: true });
  }

  function end() {
    if (document.activeElement === toggle) rows[0]?.querySelector('h3 a')?.focus();
    running = false;
    stop3D();
    observers.forEach((observer) => observer.disconnect());
    observers = [];
    middle?.disconnect();
    middle = null;
    crossing.clear();
    removeEventListener('scroll', onScroll);
    removeEventListener('resize', onResize);
    removeEventListener('scroll', onFirstScroll);
    onScreen = false;
    near = false;
    setActive(null);
    status.textContent = '';
    toggle.hidden = true;
  }

  function sync() {
    if (motion.matches) end();
    else begin();
  }

  motion.addEventListener('change', sync);
  window.addEventListener('pagehide', end);
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) sync();
  });
  sync();
}
