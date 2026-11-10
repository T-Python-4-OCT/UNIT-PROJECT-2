(() => {
  const root = document.documentElement;
  const isEnglish = root.lang === 'en';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const storage = {
    get(key) {
      try { return localStorage.getItem(key); } catch { return null; }
    },
    set(key, value) {
      try { localStorage.setItem(key, value); } catch { /* Storage may be disabled. */ }
    },
  };

  // Mobile navigation closes when the visitor chooses a page or taps outside it.
  const nav = document.querySelector('.main-nav');
  const menuButton = document.querySelector('.menu-toggle');
  const currentPath = window.location.pathname;
  nav?.querySelectorAll('a').forEach((link) => {
    const targetPath = new URL(link.href, window.location.origin).pathname;
    const isSectionPage = (targetPath === '/industries/' && currentPath.startsWith('/industry/'));
    if (targetPath === currentPath || isSectionPage) link.setAttribute('aria-current', 'page');
  });
  const closeMenu = () => {
    if (!nav?.classList.contains('open')) return;
    nav.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
    menuButton?.setAttribute('aria-label', isEnglish ? 'Open menu' : 'فتح القائمة');
    if (menuButton) menuButton.textContent = '☰';
  };
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('click', (event) => {
    if (nav?.classList.contains('open') && !nav.contains(event.target) && !menuButton?.contains(event.target)) closeMenu();
  });

  // Fast Arabic-friendly search and category filters on the sectors directory.
  const search = document.querySelector('#sector-search');
  const cards = [...document.querySelectorAll('#sector-grid .industry-card')];
  const chips = [...document.querySelectorAll('[data-sector-filter]')];
  const resultCount = document.querySelector('#sector-result-count');
  const emptyState = document.querySelector('#sector-empty');
  document.querySelector('#random-sector')?.addEventListener('click', () => {
    const choice = cards[Math.floor(Math.random() * cards.length)];
    if (choice) window.location.assign(choice.href);
  });

  const normalize = (value) => value
    .normalize('NFKD')
    .replace(/[\u064B-\u065F\u0670\u0640]/g, '')
    .replace(/[أإآ]/g, 'ا')
    .replace(/ى/g, 'ي')
    .toLocaleLowerCase('ar');
  const categories = {
    energy: ['energy'],
    materials: ['petrochemicals', 'mining'],
    essential: ['pharma', 'food'],
    future: ['mobility', 'defense'],
  };
  let activeFilter = 'all';
  const applySectorFilters = () => {
    if (!cards.length) return;
    const query = normalize(search?.value.trim() || '');
    let visible = 0;
    cards.forEach((card) => {
      const slug = card.getAttribute('href').split('/').filter(Boolean).at(-1);
      const text = normalize(card.innerText || card.textContent || '');
      const matchesCategory = activeFilter === 'all' || categories[activeFilter]?.includes(slug);
      const matchesSearch = !query || text.includes(query);
      const show = matchesCategory && matchesSearch;
      card.hidden = !show;
      if (show) visible += 1;
    });
    if (resultCount) resultCount.textContent = isEnglish ? `${new Intl.NumberFormat('en').format(visible)} sectors` : `${new Intl.NumberFormat('ar-SA').format(visible)} قطاعات`;
    if (emptyState) emptyState.hidden = visible > 0;
  };
  search?.addEventListener('input', applySectorFilters);
  chips.forEach((chip) => chip.addEventListener('click', () => {
    activeFilter = chip.dataset.sectorFilter;
    chips.forEach((item) => {
      const selected = item === chip;
      item.classList.toggle('is-active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    applySectorFilters();
  }));
  document.querySelector('#sector-reset')?.addEventListener('click', () => {
    if (search) search.value = '';
    chips.find((chip) => chip.dataset.sectorFilter === 'all')?.click();
    search?.focus();
  });

  // Keep theme choice between visits, even when browser storage is unavailable.
  const themeButton = document.querySelector('.theme-toggle');
  const setTheme = (theme) => {
    root.dataset.theme = theme;
    const dark = theme === 'dark';
    if (themeButton) {
      const icon = themeButton.querySelector('.theme-icon');
      const label = themeButton.querySelector('.theme-label');
      if (icon) icon.textContent = dark ? '☀' : '☾';
      if (label) label.textContent = isEnglish ? (dark ? 'Light mode' : 'Dark mode') : (dark ? 'الوضع النهاري' : 'الوضع الليلي');
      themeButton.setAttribute('aria-label', isEnglish ? (dark ? 'Switch to light mode' : 'Switch to dark mode') : (dark ? 'تفعيل الوضع النهاري' : 'تفعيل الوضع الليلي'));
    }
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#172b26' : '#f6f4ed');
    storage.set('senaa-theme', theme);
  };
  setTheme(storage.get('senaa-theme') || 'light');
  themeButton?.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));

  // Presentation mode enlarges small copy and remembers the choice.
  const presentationButton = document.querySelector('.presentation-toggle');
  const setPresentationMode = (enabled) => {
    root.classList.toggle('presentation-mode', enabled);
    presentationButton?.setAttribute('aria-pressed', String(enabled));
    if (presentationButton) {
      const label = isEnglish ? (enabled ? 'Exit presentation mode' : 'Presentation mode') : (enabled ? 'إيقاف وضع العرض' : 'تفعيل وضع العرض');
      presentationButton.querySelector('.presentation-label').textContent = isEnglish ? (enabled ? 'Exit' : 'Present') : (enabled ? 'إيقاف' : 'عرض');
      presentationButton.setAttribute('aria-label', label);
    }
    storage.set('senaa-presentation-mode', enabled ? 'on' : 'off');
  };
  setPresentationMode(storage.get('senaa-presentation-mode') === 'on');
  presentationButton?.addEventListener('click', () => setPresentationMode(!root.classList.contains('presentation-mode')));


  // Share a sector with the native share sheet or copy its link as a fallback.
  document.querySelectorAll('.share-sector').forEach((button) => button.addEventListener('click', async () => {
    const title = `${button.dataset.shareTitle || (isEnglish ? 'Saudi Industries' : 'الصناعة السعودية')} | ${isEnglish ? 'Senaa' : 'صناعة'}`;
    const payload = { title, text: isEnglish ? 'Read about this Saudi industrial sector.' : 'اقرأ عن هذا القطاع الصناعي السعودي', url: window.location.href };
    try {
      if (navigator.share) await navigator.share(payload);
      else if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(payload.url);
      else throw new Error('Sharing is unavailable');
      const status = button.querySelector('.share-status');
      if (status) status.textContent = isEnglish ? (navigator.share ? 'Sharing options opened' : 'Link copied') : (navigator.share ? 'تم فتح خيارات المشاركة' : 'نُسخ الرابط');
      button.classList.add('share-complete');
      window.setTimeout(() => {
        button.classList.remove('share-complete');
        if (status) status.textContent = '';
      }, 2400);
    } catch (error) {
      if (error.name !== 'AbortError') {
        const status = button.querySelector('.share-status');
        if (status) status.textContent = 'تعذرت المشاركة، انسخ الرابط من المتصفح';
      }
    }
  }));

  // Selecting a mapped city updates its details and keeps a shareable URL hash.
  const mapDetail = document.querySelector('#map-detail');
  const mapSelectors = [...document.querySelectorAll('.city-index-item[data-city-id]')];
  const renderMapCity = (cityId, updateAddress = false) => {
    if (!mapDetail || !mapSelectors.length) return;
    const marker = mapSelectors.find((item) => item.dataset.cityId === cityId);
    if (!marker) return;
    mapSelectors.forEach((item) => {
      const selected = item.dataset.cityId === cityId;
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    document.querySelectorAll('.geo-city-marker').forEach((item) => item.classList.toggle('is-selected', item.dataset.cityId === cityId));
    document.querySelector('#map-region').textContent = marker.dataset.region;
    document.querySelector('#map-city').textContent = marker.dataset.city;
    document.querySelector('#map-description').textContent = marker.dataset.description;
    document.querySelector('#map-coordinates').textContent = `${Number(marker.dataset.lat).toFixed(5)}, ${Number(marker.dataset.lon).toFixed(5)}`;
    const sectorList = document.querySelector('#map-sectors');
    sectorList.replaceChildren();
    marker.dataset.sectors.split('|').forEach((sector) => {
      const tag = document.createElement('span');
      tag.textContent = sector;
      sectorList.append(tag);
    });
    const source = document.querySelector('#map-source');
    source.href = marker.dataset.url;
    source.innerHTML = '';
    source.append(document.createTextNode(marker.dataset.source));
    const arrow = document.createElement('b');
    arrow.textContent = ' ↗';
    source.append(arrow);
    mapDetail.classList.remove('is-changing');
    window.requestAnimationFrame(() => mapDetail.classList.add('is-changing'));
    if (updateAddress) history.replaceState(null, '', `#${cityId}`);
  };
  mapSelectors.forEach((item) => item.addEventListener('click', () => renderMapCity(item.dataset.cityId, true)));
  window.addEventListener('industrialmap:select', (event) => renderMapCity(event.detail.cityId, Boolean(event.detail.updateAddress)));
  if (mapDetail) {
    const initialCity = window.location.hash.slice(1) || mapSelectors[0]?.dataset.cityId;
    if (initialCity) renderMapCity(initialCity, false);
  }

  // Reading progress, back-to-top control, and subtle reveal effects.
  const progress = document.createElement('div');
  progress.className = 'reading-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.append(progress);
  const topButton = document.createElement('button');
  topButton.className = 'back-to-top';
  topButton.type = 'button';
  topButton.setAttribute('aria-label', isEnglish ? 'Back to top' : 'العودة إلى أعلى الصفحة');
  topButton.innerHTML = '<span aria-hidden="true">↑</span>';
  document.body.append(topButton);
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' }));

  let scrollQueued = false;
  const updateScrollUI = () => {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = maxScroll > 0 ? window.scrollY / maxScroll : 0;
    progress.style.transform = `scaleX(${Math.min(1, Math.max(0, ratio))})`;
    topButton.classList.toggle('is-visible', window.scrollY > 500);
    scrollQueued = false;
  };
  window.addEventListener('scroll', () => {
    if (!scrollQueued) {
      scrollQueued = true;
      window.requestAnimationFrame(updateScrollUI);
    }
  }, { passive: true });
  updateScrollUI();

  if (!reducedMotion && 'IntersectionObserver' in window) {
    root.classList.add('js-enhanced');
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -28px 0px' });
    document.querySelectorAll('.industry-card,.achievement-card,.sector-achievement-card,.winner-card,.milestone,.award-row,.sector-story,.sector-impact,.outlook-column,.sector-sources').forEach((item) => {
      item.classList.add('reveal-item');
      observer.observe(item);
    });
  }

  // Defer decorative background footage until the page is idle and the hero is near view.
  const backgroundVideos = [...document.querySelectorAll('video[data-background-video]')];
  const saveData = Boolean(navigator.connection?.saveData);
  const smallScreen = window.matchMedia('(max-width: 700px)').matches;
  const startBackgroundVideo = (video) => {
    const source = video.querySelector('source[data-src]');
    if (!source || reducedMotion || saveData || smallScreen) {
      video.hidden = true;
      return;
    }
    source.src = source.dataset.src;
    source.removeAttribute('data-src');
    video.load();
    video.play().catch(() => {});
  };
  if (backgroundVideos.length) {
    const queueVideo = (video) => {
      const start = () => startBackgroundVideo(video);
      if ('requestIdleCallback' in window) window.requestIdleCallback(start, { timeout: 2200 });
      else window.setTimeout(start, 900);
    };
    if ('IntersectionObserver' in window) {
      const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            queueVideo(entry.target);
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '240px 0px' });
      backgroundVideos.forEach((video) => videoObserver.observe(video));
    } else {
      backgroundVideos.forEach(queueVideo);
    }
  }

  // Keyboard shortcuts: / or Ctrl/Cmd+K focuses sector search; Escape clears/closes.
  document.addEventListener('keydown', (event) => {
    const editing = ['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if (search && !editing && (event.key === '/' || ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k'))) {
      event.preventDefault();
      search.focus();
    }
    if (event.key === 'Escape') {
      closeMenu();
      if (search && document.activeElement === search) {
        search.value = '';
        search.blur();
        applySectorFilters();
      }
    }
  });
})();
