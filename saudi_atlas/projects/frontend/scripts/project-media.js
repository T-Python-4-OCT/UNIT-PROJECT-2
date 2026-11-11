const gallery = document.querySelector('[data-project-gallery]');
const dialog = gallery?.querySelector('dialog');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const scrollBehavior = () => (reducedMotion.matches ? 'auto' : 'smooth');

if (gallery && typeof dialog?.showModal === 'function') {
  const links = [...gallery.querySelectorAll('[data-project-photo]')];
  const stage = dialog.querySelector('[data-photo-stage]');
  const counter = dialog.querySelector('[data-photo-counter]');
  const steps = [...dialog.querySelectorAll('[data-photo-step]')];
  const template = dialog.dataset.labelCounter;
  let index = 0;
  let opener;
  let touchX = null;

  const preload = (link) => {
    if (link) new Image().src = link.href;
  };

  function show(next) {
    index = (next + links.length) % links.length;
    const link = links[index];
    const source = link.querySelector('img');
    const image = new Image();
    image.src = link.href;
    image.alt = source.alt;
    image.width = source.width;
    image.height = source.height;
    const caption = document.createElement('figcaption');
    caption.className = 'media-caption';
    caption.textContent = link.closest('figure').querySelector('figcaption').textContent;
    stage.replaceChildren(image, caption);
    counter.textContent = template.replace('%(current)s', index + 1).replace('%(total)s', links.length);
    preload(links[(index + 1) % links.length]);
    preload(links[(index - 1 + links.length) % links.length]);
  }

  for (const step of steps) {
    step.hidden = links.length < 2;
    step.addEventListener('click', () => show(index + Number(step.dataset.photoStep)));
  }

  gallery.addEventListener('click', (event) => {
    const link = event.target.closest('[data-project-photo]');
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    show(links.indexOf(link));
    dialog.showModal();
  });

  dialog.addEventListener('keydown', (event) => {
    if (links.length < 2) return;
    const forward = document.dir === 'rtl' ? 'ArrowLeft' : 'ArrowRight';
    const backward = document.dir === 'rtl' ? 'ArrowRight' : 'ArrowLeft';
    if (event.key === forward) show(index + 1);
    if (event.key === backward) show(index - 1);
  });

  dialog.addEventListener(
    'touchstart',
    (event) => {
      touchX = event.touches[0].clientX;
    },
    { passive: true },
  );
  dialog.addEventListener('touchend', (event) => {
    if (touchX === null || links.length < 2) return;
    const delta = event.changedTouches[0].clientX - touchX;
    touchX = null;
    if (Math.abs(delta) < 48) return;
    const forward = document.dir === 'rtl' ? delta > 0 : delta < 0;
    show(index + (forward ? 1 : -1));
  });

  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    stage.replaceChildren();
    opener?.focus();
  });
}

const strip = gallery?.querySelector('[data-gallery-strip]');
const stripSteps = gallery?.querySelector('[data-gallery-steps]');

if (strip && stripSteps) {
  const [back, forward] = stripSteps.querySelectorAll('[data-gallery-step]');
  const items = [...strip.children];
  const photos = [...strip.querySelectorAll('[data-project-photo]')];
  const rtl = () => getComputedStyle(strip).direction === 'rtl';
  const travelled = () => Math.abs(strip.scrollLeft);
  const room = () => strip.scrollWidth - strip.clientWidth;
  const offset = (item) => {
    const view = strip.getBoundingClientRect();
    const box = item.getBoundingClientRect();
    return rtl() ? view.right - box.right : box.left - view.left;
  };
  const scrollAlong = (distance) =>
    strip.scrollBy({ left: rtl() ? -distance : distance, behavior: scrollBehavior() });
  let frame = 0;

  function update() {
    frame = 0;
    stripSteps.hidden = room() <= 1;
    back.disabled = travelled() <= 1;
    forward.disabled = travelled() >= room() - 1;
  }
  const schedule = () => {
    if (!frame) frame = requestAnimationFrame(update);
  };

  forward.addEventListener('click', () => {
    const next = items.find((item) => offset(item) > 2);
    if (next) scrollAlong(offset(next));
  });
  back.addEventListener('click', () => {
    const previous = items.findLast((item) => offset(item) < -2);
    if (previous) scrollAlong(offset(previous));
  });

  strip.addEventListener('scroll', schedule, { passive: true });

  if ('ResizeObserver' in window) new ResizeObserver(schedule).observe(strip);
  else update();

  let drag = null;
  let suppressClick = false;
  const move = (event) => {
    const distance = event.clientX - drag.x;
    if (!drag.moved && Math.abs(distance) < 6) return;
    if (!drag.moved) {
      drag.moved = true;
      strip.setAttribute('data-dragging', '');
    }
    strip.scrollLeft = drag.left - distance;
  };
  const release = () => {
    removeEventListener('pointermove', move);
    removeEventListener('pointerup', release);
    removeEventListener('pointercancel', release);
    if (drag?.moved) {
      suppressClick = true;
      setTimeout(() => {
        suppressClick = false;
      }, 0);
      strip.removeAttribute('data-dragging');
    }
    drag = null;
  };
  strip.addEventListener('pointerdown', (event) => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    drag = { x: event.clientX, left: strip.scrollLeft, moved: false };
    addEventListener('pointermove', move);
    addEventListener('pointerup', release);
    addEventListener('pointercancel', release);
  });
  strip.addEventListener(
    'click',
    (event) => {
      if (!suppressClick) return;
      suppressClick = false;
      event.preventDefault();
      event.stopPropagation();
    },
    true,
  );
  strip.addEventListener('dragstart', (event) => event.preventDefault());

  strip.addEventListener('keydown', (event) => {
    const link = event.target.closest('[data-project-photo]');
    if (!link || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const keys = rtl() ? { ArrowLeft: 1, ArrowRight: -1 } : { ArrowRight: 1, ArrowLeft: -1 };
    let target = photos.indexOf(link);
    if (event.key in keys) target += keys[event.key];
    else if (event.key === 'Home') target = 0;
    else if (event.key === 'End') target = photos.length - 1;
    else return;
    event.preventDefault();
    const photo = photos[Math.max(0, Math.min(photos.length - 1, target))];
    photo.focus({ preventScroll: true });
    photo.closest('li').scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: scrollBehavior() });
  });
}

const rail = document.querySelector('[data-plate-rail]');

if (rail && 'IntersectionObserver' in window) {
  const sections = new Map();
  for (const link of rail.querySelectorAll('a[href^="#"]')) {
    const section = document.getElementById(decodeURIComponent(link.hash.slice(1)))?.closest('section');
    if (section) sections.set(section, link);
  }
  const order = [...sections.keys()];
  let current = null;

  const mark = (link) => {
    if (link === current) return;
    current?.removeAttribute('aria-current');
    current = link;
    current?.setAttribute('aria-current', 'location');
  };

  const update = () => {
    const line = innerHeight * 0.35;
    const passed = order.filter((section) => section.getBoundingClientRect().top <= line + 1);
    mark(passed.length ? sections.get(passed.at(-1)) : null);
  };
  const observer = new IntersectionObserver(update, { rootMargin: '-35% 0px -64% 0px' });

  for (const section of order) observer.observe(section);

  addEventListener('scrollend', update, { passive: true });
}

const film = document.querySelector('[data-film]');
const filmVideo = film?.querySelector('[data-film-video]');
const filmPlay = film?.querySelector('[data-film-play]');

if (film && filmVideo && filmPlay) {
  const showCover = () => {
    filmVideo.controls = false;
    filmPlay.hidden = false;
  };

  showCover();

  filmPlay.addEventListener('click', () => {
    filmPlay.hidden = true;
    filmVideo.controls = true;
    filmVideo.focus({ preventScroll: true });
    filmVideo.play().catch(showCover);
  });

  filmVideo.addEventListener('play', () => {
    film.dataset.playing = '';
  });
  filmVideo.addEventListener('pause', () => {
    delete film.dataset.playing;
  });
  filmVideo.addEventListener('ended', () => {
    delete film.dataset.playing;
    filmVideo.currentTime = 0;
    showCover();
    filmPlay.focus({ preventScroll: true });
  });
}
