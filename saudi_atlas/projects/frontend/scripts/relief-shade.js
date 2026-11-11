const shades = [...document.querySelectorAll('.atlas-shade[data-src]')];

function show(image) {
  if (!image.dataset.src) return;
  image.src = image.dataset.src;
  image.removeAttribute('data-src');
}

function watch(images, rootMargin) {
  const waiting = new Map(images.map((image) => [image.closest('.atlas-stage') ?? image, image]));
  const nearby = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        show(waiting.get(entry.target));
        nearby.unobserve(entry.target);
      }
    },
    { rootMargin },
  );
  waiting.forEach((_, stage) => nearby.observe(stage));
}

if (!('IntersectionObserver' in window)) {
  shades.forEach(show);
} else if (shades.length) {
  const journey = shades.filter((image) => image.closest('[data-expedition]'));
  const others = shades.filter((image) => !journey.includes(image));
  if (others.length) watch(others, '200px 0px');
  if (journey.length) {
    const intents = ['scroll', 'wheel', 'touchstart', 'keydown'];
    const begin = () => {
      intents.forEach((type) => removeEventListener(type, begin, true));
      watch(journey, '100% 0px');
    };
    if (scrollY > 0) begin();
    else intents.forEach((type) => addEventListener(type, begin, { capture: true, passive: true }));
  }
}
