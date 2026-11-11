import '../styles/view-cursor.css';

const strip = document.querySelector('[data-gallery-strip]');

if (strip) {
  const label = document.createElement('span');
  label.className = 'view-cursor';
  label.setAttribute('aria-hidden', 'true');
  label.textContent = strip.dataset.viewLabel || 'View';
  document.body.append(label);

  let x = 0;
  let y = 0;
  let over = false;
  let frame = 0;

  const render = () => {
    frame = 0;
    label.style.translate = `${x}px ${y}px`;
    label.toggleAttribute('data-visible', over && !strip.hasAttribute('data-dragging'));
  };
  const schedule = () => {
    if (!frame) frame = requestAnimationFrame(render);
  };
  const track = (event) => {
    if (event.pointerType !== 'mouse') {
      over = false;
    } else {
      x = event.clientX;
      y = event.clientY;
      over = Boolean(event.target.closest?.('[data-project-photo]'));
    }
    schedule();
  };
  const hide = () => {
    over = false;
    schedule();
  };

  strip.addEventListener('pointerover', track, { passive: true });
  strip.addEventListener('pointermove', track, { passive: true });
  strip.addEventListener('pointerleave', hide, { passive: true });

  strip.addEventListener('click', hide, { passive: true });
}
