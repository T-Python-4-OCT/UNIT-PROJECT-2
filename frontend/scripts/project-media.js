const gallery = document.querySelector('[data-project-gallery]');
const dialog = gallery?.querySelector('dialog');

if (gallery && typeof dialog?.showModal === 'function') {
  const links = [...gallery.querySelectorAll('[data-project-photo]')];
  const stage = dialog.querySelector('[data-photo-stage]');
  const counter = dialog.querySelector('[data-photo-counter]');
  const steps = [...dialog.querySelectorAll('[data-photo-step]')];
  const template = dialog.dataset.labelCounter;
  let index = 0;
  let opener;
  let touchX = null;

  const preload = (link) => { if (link) new Image().src = link.href; };

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

  dialog.addEventListener('touchstart', (event) => { touchX = event.touches[0].clientX; }, { passive: true });
  dialog.addEventListener('touchend', (event) => {
    if (touchX === null || links.length < 2) return;
    const delta = event.changedTouches[0].clientX - touchX;
    touchX = null;
    if (Math.abs(delta) < 48) return;
    const forward = document.dir === 'rtl' ? delta > 0 : delta < 0;
    show(index + (forward ? 1 : -1));
  });

  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    stage.replaceChildren();
    opener?.focus();
  });
}
