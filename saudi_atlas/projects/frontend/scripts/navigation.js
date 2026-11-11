const nav = document.querySelector('[data-site-nav]');
const toggle = document.querySelector('[data-menu-toggle]');
const menus = [...document.querySelectorAll('[data-projects-menu]')];
const compact = matchMedia('(max-width: 52rem)');

function setOpen(open) {
  if (!nav || !toggle) return;
  toggle.setAttribute('aria-expanded', String(open));
  nav.toggleAttribute('data-open', open);
}

if (nav && toggle) {
  toggle.hidden = false;
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  compact.addEventListener('change', () => setOpen(false));
}

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  for (const menu of menus) {
    if (menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
      return;
    }
  }
  if (toggle?.getAttribute('aria-expanded') === 'true') {
    setOpen(false);
    toggle.focus();
  }
});

document.addEventListener('click', (event) => {
  for (const menu of menus) {
    if (menu.open && !menu.contains(event.target) && !compact.matches) menu.open = false;
  }
});
