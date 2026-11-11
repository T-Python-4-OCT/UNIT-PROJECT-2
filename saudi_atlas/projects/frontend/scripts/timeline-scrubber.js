const chart = document.querySelector('[data-scrubber]');
const chronology = document.querySelector('[data-chronology]');

if (chart && chronology) {
  const header = document.querySelector('[data-site-header]');
  const marker = chart.querySelector('[data-lane-marker]');
  const ticks = [...chart.querySelectorAll('[data-tick]')];
  const dots = [...chart.querySelectorAll('[data-dot]')];
  const groups = [...chronology.querySelectorAll('[data-year]')];
  const entryOf = new Map(
    dots.map((dot) => [dot, document.getElementById(decodeURIComponent(dot.hash.slice(1)))]),
  );
  const dotOf = new Map(dots.map((dot) => [entryOf.get(dot), dot]));

  const tip = document.createElement('div');
  tip.className = 'lane-tip';
  tip.setAttribute('aria-hidden', 'true');
  tip.hidden = true;
  chart.append(tip);

  let lit = [];
  const light = (...elements) => {
    for (const element of lit) element.removeAttribute('data-lit');
    lit = elements.filter(Boolean);
    for (const element of lit) element.setAttribute('data-lit', '');
  };

  const onScreen = (element) => {
    const box = element.getBoundingClientRect();
    const top = Math.max(
      header?.getBoundingClientRect().bottom ?? 0,
      getComputedStyle(chart).position === 'sticky' ? chart.getBoundingClientRect().bottom : 0,
    );
    return box.bottom > top && box.top < innerHeight;
  };

  function label(dot) {
    const entry = entryOf.get(dot);
    if (!entry) return;
    const when = document.createElement('span');
    when.className = 'lane-tip-when';
    when.textContent = entry.querySelector('time')?.textContent ?? entry.closest('[data-year]').dataset.year;
    tip.replaceChildren(when, entry.querySelector('p').textContent);
    tip.hidden = false;
    const area = chart.getBoundingClientRect();
    const box = dot.getBoundingClientRect();
    const gap = 6;
    const edge = 8;
    const width = tip.offsetWidth;
    const height = tip.offsetHeight;
    const left = Math.min(
      Math.max(box.left + box.width / 2 - area.left - chart.clientLeft - width / 2, edge),
      chart.clientWidth - width - edge,
    );
    let top = box.top - area.top - chart.clientTop - height - gap;
    if (top < edge || area.top + top < (header?.getBoundingClientRect().bottom ?? 0))
      top = box.bottom - area.top - chart.clientTop + gap;
    tip.style.left = `${left}px`;
    tip.style.top = `${top}px`;
  }

  function point(dot) {
    const entry = entryOf.get(dot);
    label(dot);
    light(dot, entry && onScreen(entry) ? entry : null);
  }

  function release() {
    const focused = dots.includes(document.activeElement) ? document.activeElement : null;
    if (focused) point(focused);
    else {
      tip.hidden = true;
      light();
    }
  }

  for (const dot of dots) {
    dot.addEventListener('pointerenter', () => point(dot));
    dot.addEventListener('focus', () => point(dot));
    dot.addEventListener('pointerleave', () => requestAnimationFrame(release));
    dot.addEventListener('blur', () => requestAnimationFrame(release));

    dot.addEventListener('click', () => {
      tip.hidden = true;
      light();
      entryOf.get(dot)?.focus({ preventScroll: true });
    });
  }

  for (const [entry, dot] of dotOf) {
    if (!entry) continue;
    entry.addEventListener('pointerenter', () => light(dot));
    entry.addEventListener('pointerleave', () => light());
    entry.addEventListener('focusin', () => light(dot));
    entry.addEventListener('focusout', () => light());
  }

  function place() {
    const stuck = getComputedStyle(chart).position === 'sticky';
    const line =
      (stuck ? chart.getBoundingClientRect().bottom : (header?.getBoundingClientRect().bottom ?? 0)) + 24;
    const current = groups.find((group) => {
      const box = group.getBoundingClientRect();
      return box.bottom > line && box.top < innerHeight;
    });
    if (!current) {
      chart.removeAttribute('data-marker');
      marker.hidden = true;
      for (const tick of ticks) tick.removeAttribute('data-covered');
      return;
    }
    if (chart.dataset.marker === current.dataset.year) return;
    chart.style.setProperty('--marker-at', current.dataset.at);
    chart.dataset.marker = current.dataset.year;
    marker.textContent = current.dataset.year;
    marker.hidden = false;

    for (const tick of ticks)
      tick.toggleAttribute(
        'data-covered',
        Math.abs(Number(tick.dataset.tick) - Number(current.dataset.year) - 0.5) < 2.5,
      );
  }

  let queued = false;
  const schedule = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      place();
    });
  };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule, { passive: true });
  place();
}
