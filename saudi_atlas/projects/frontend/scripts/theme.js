const root = document.documentElement;
const toggles = [...document.querySelectorAll('[data-theme-toggle]')];
const reduced = matchMedia('(prefers-reduced-motion: reduce)');

let wanted = root.dataset.theme;
let running = null;

const sync = () => {
  for (const toggle of toggles) toggle.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
};
const apply = (theme) => {
  root.dataset.theme = theme;
  try {
    localStorage.setItem('atlas-theme', theme);
  } catch {}
  sync();
};
const token = (name, fallback) => getComputedStyle(root).getPropertyValue(name).trim() || fallback;
const milliseconds = (value) => (value.endsWith('ms') ? parseFloat(value) : parseFloat(value) * 1000);

function reveal(toggle, theme) {
  const box = toggle.getBoundingClientRect();
  const x = box.left + box.width / 2;
  const y = box.top + box.height / 2;
  const radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
  root.style.setProperty('--theme-x', `${x}px`);
  root.style.setProperty('--theme-y', `${y}px`);
  root.classList.add('theme-shift');
  const transition = document.startViewTransition(() => apply(theme));
  running = transition;
  transition.ready.then(
    () => {
      root.animate(
        { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`] },
        {
          duration: milliseconds(token('--dur-theme', '600ms')),
          easing: token('--ease-out', 'ease-out'),
          pseudoElement: '::view-transition-new(root)',
        },
      );
    },
    () => {},
  );
  transition.finished.finally(() => {
    if (running !== transition) return;
    running = null;
    root.classList.remove('theme-shift');
    root.style.removeProperty('--theme-x');
    root.style.removeProperty('--theme-y');
  });
}

for (const toggle of toggles) {
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    wanted = wanted === 'dark' ? 'light' : 'dark';
    if (typeof document.startViewTransition !== 'function' || reduced.matches) {
      running?.skipTransition();
      apply(wanted);
      return;
    }

    reveal(toggle, wanted);
  });
}
sync();
