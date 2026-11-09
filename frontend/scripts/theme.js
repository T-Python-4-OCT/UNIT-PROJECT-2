const root = document.documentElement;
const toggles = [...document.querySelectorAll('[data-theme-toggle]')];

const sync = () => {
  for (const toggle of toggles) toggle.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
};

for (const toggle of toggles) {
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = theme;
    try { localStorage.setItem('atlas-theme', theme); } catch {}
    sync();
  });
}
sync();
