(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (!menuButton || !nav) return;

  menuButton.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? (document.documentElement.lang === 'en' ? 'Close menu' : 'إغلاق القائمة') : (document.documentElement.lang === 'en' ? 'Open menu' : 'فتح القائمة'));
    menuButton.textContent = open ? '×' : '☰';
  });
})();
