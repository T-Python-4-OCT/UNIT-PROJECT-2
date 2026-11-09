const gallery = document.querySelector('[data-project-gallery]');
const dialog = gallery?.querySelector('dialog');

if (typeof dialog?.showModal === 'function') {
  const figure = dialog.querySelector('figure');
  let opener;
  document.addEventListener('click', (event) => {
    const link = event.target.closest('[data-project-photo]');
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const image = link.querySelector('img').cloneNode();
    image.src = link.href;
    image.loading = 'eager';
    const caption = link.closest('figure').querySelector('figcaption').cloneNode(true);
    figure.replaceChildren(image, caption);
    opener = link;
    dialog.showModal();
  });
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    figure.replaceChildren();
    opener?.focus();
  });
}
