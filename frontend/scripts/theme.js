const root = document.documentElement;
const toggle = document.querySelector('[data-theme-toggle]');

if (toggle) {
  const syncToggle = () => toggle.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
  toggle.hidden = false;
  syncToggle();

  toggle.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = theme;
    try { localStorage.setItem('atlas-theme', theme); } catch {}
    syncToggle();
  });
}
