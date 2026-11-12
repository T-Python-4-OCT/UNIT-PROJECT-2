const form = document.querySelector('[data-pages-search]');
const input = form.elements.q;
const results = document.querySelector('[data-search-results]');
const status = document.querySelector('[data-search-status]');
const { cards, empty, missing, heading, counts } = JSON.parse(
  document.getElementById('pages-search-index').textContent,
);

function fold(text) {
  return text.toLowerCase().normalize('NFKD')
    .replace(/\p{M}|ـ/gu, '').replaceAll('ى', 'ي').replaceAll('ة', 'ه').replaceAll('ß', 'ss');
}

function highlight(container, terms) {
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);

  for (const node of nodes) {
    const text = node.data;
    const owners = [];
    let folded = '';
    for (const { segment, index } of new Intl.Segmenter().segment(text)) {
      const part = fold(segment);
      folded += part;
      for (let i = 0; i < part.length; i++) owners.push([index, index + segment.length]);
    }
    const spans = [];
    for (const term of terms) {
      for (let start = folded.indexOf(term); start !== -1; start = folded.indexOf(term, start + 1)) {
        spans.push([owners[start][0], owners[start + term.length - 1][1]]);
      }
    }
    const merged = [];
    for (const [start, end] of spans.sort((a, b) => a[0] - b[0])) {
      const last = merged.at(-1);
      if (last && start <= last[1]) last[1] = Math.max(last[1], end);
      else merged.push([start, end]);
    }
    if (!merged.length) continue;

    const fragment = document.createDocumentFragment();
    let cursor = 0;
    for (const [start, end] of merged) {
      const mark = document.createElement('mark');
      mark.textContent = text.slice(start, end);
      fragment.append(text.slice(cursor, start), mark);
      cursor = end;
    }
    fragment.append(text.slice(cursor));
    node.replaceWith(fragment);
  }
}

function update() {
  const query = input.value.trim().replace(/\s+/gu, ' ').slice(0, 80);
  const terms = fold(query).split(/\s+/u).filter(Boolean);
  const hit = (text) => terms.every((term) => fold(text).includes(term));
  const matches = terms.length ? cards.map((card) => ({
    card,
    named: hit(card.name),
    headline: hit(card.headline),
    passages: card.passages.map(hit),
  })).filter(({ headline, passages }) => headline || passages.some(Boolean)) : [];
  const count = (match) => match.passages.filter(Boolean).length;
  matches.sort((a, b) => b.named - a.named || b.headline - a.headline || count(b) - count(a));

  if (!matches.length) {
    results.innerHTML = query ? missing : empty;
  } else {
    results.innerHTML = matches[0].card.html;
    const title = results.querySelector('#results-title');
    const quote = document.createElement('q');
    quote.textContent = query;
    title.replaceChildren(heading + ' ', quote);
    results.querySelector('[data-search-outcome]').textContent = counts[matches.length];

    const list = results.querySelector('.result-list');
    list.replaceChildren();
    const template = document.createElement('template');
    for (const { card, passages } of matches) {
      template.innerHTML = card.html;
      const row = template.content.querySelector('.result');
      const snippets = row.querySelector('.result-matches');
      [...(snippets?.children ?? [])].forEach((item, index) => {
        if (!passages[index]) item.remove();
      });
      if (!snippets?.children.length) {
        snippets?.remove();
        const summary = row.querySelector('.result-summary') ?? document.createElement('p');
        summary.className = 'result-summary';
        summary.textContent = card.summary;
        row.append(summary);
      }
      highlight(row, terms);
      list.append(row);
    }
  }

  const outcome = results.querySelector('[data-search-outcome]');
  status.textContent = outcome?.dataset.announce || outcome?.textContent.trim() || '';
  const url = new URL(form.action);
  if (query) url.searchParams.set('q', query);
  history.replaceState(history.state, '', url);
  for (const link of document.querySelectorAll('.language-switch')) {
    const alternate = new URL(link.href);
    alternate.search = url.search;
    link.href = alternate.href;
  }
}

let timer;
input.addEventListener('input', () => {
  clearTimeout(timer);
  timer = setTimeout(update, 200);
});
form.addEventListener('submit', (event) => {
  event.preventDefault();
  clearTimeout(timer);
  update();
});
input.value = (new URL(location.href).searchParams.get('q') ?? '').slice(0, 80);
if (input.value) update();
