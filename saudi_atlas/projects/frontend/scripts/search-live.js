const form = document.querySelector('[data-live-search]');
const results = document.querySelector('[data-search-results]');
const status = document.querySelector('[data-search-status]');

if (form && results && status) {
  const input = form.elements.q;
  const languageLinks = [...document.querySelectorAll('.language-switch')];
  const normalise = (value) => value.trim().split(/\s+/).filter(Boolean).join(' ').slice(0, 80);
  let shown = normalise(input.value);
  let timer = 0;
  let controller = null;
  let broken = false;

  const address = (query) => {
    const url = new URL(form.action, location.href);
    if (query) url.searchParams.set('q', query);
    return url;
  };

  function announce() {
    const outcome = results.querySelector('[data-search-outcome]');
    const text = outcome ? outcome.dataset.announce || outcome.textContent.trim() : '';

    status.textContent = '';
    setTimeout(() => {
      status.textContent = text;
    }, 50);
  }

  async function update(query, submitting) {
    controller?.abort();
    controller = new AbortController();
    const { signal } = controller;
    const url = address(query);
    try {
      const response = await fetch(url, { headers: { 'X-Atlas-Partial': 'results' }, signal });
      if (!response.ok) throw new Error(`Search returned ${response.status}`);
      const html = await response.text();
      if (signal.aborted) return;
      const template = document.createElement('template');
      template.innerHTML = html;
      results.replaceChildren(template.content);
      shown = query;
      history.replaceState(history.state, '', url.pathname + url.search);
      for (const link of languageLinks) {
        const target = new URL(link.href);
        target.search = url.search;
        link.href = target.pathname + target.search;
      }
      announce();
    } catch (error) {
      if (error.name === 'AbortError') return;

      broken = true;
      if (submitting) form.submit();
    }
  }

  input.addEventListener('input', () => {
    clearTimeout(timer);
    if (broken) return;
    timer = setTimeout(() => {
      const query = normalise(input.value);
      if (query !== shown) update(query, false);
    }, 200);
  });

  form.addEventListener('submit', (event) => {
    if (broken) return;
    event.preventDefault();
    clearTimeout(timer);
    update(normalise(input.value), true);
  });
}
