const scroller = document.querySelector('[data-compare-scroll]');

if (scroller) {
  const frame = scroller.parentElement;
  const update = () => {
    const room = scroller.scrollWidth - scroller.clientWidth;
    const overflows = room > 1;
    if (overflows) scroller.setAttribute('tabindex', '0');
    else scroller.removeAttribute('tabindex');
    frame.toggleAttribute('data-fits', !overflows);

    frame.toggleAttribute('data-at-end', overflows && Math.abs(scroller.scrollLeft) >= room - 2);
  };
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(scroller);
  else addEventListener('resize', update, { passive: true });
  scroller.addEventListener('scroll', update, { passive: true });
  update();
}
