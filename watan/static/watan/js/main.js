/* حكاية وطن — السلوك التفاعلي */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- أدوات الكوكيز ---- */
  function getCookie(name) {
    var prefix = name + '=';
    var parts = document.cookie ? document.cookie.split(';') : [];
    for (var i = 0; i < parts.length; i++) {
      var part = parts[i].trim();
      if (part.indexOf(prefix) === 0) return decodeURIComponent(part.substring(prefix.length));
    }
    return null;
  }
  function setCookie(name, value, maxAge) {
    document.cookie = name + '=' + encodeURIComponent(value) + '; path=/; max-age=' + maxAge + '; SameSite=Lax';
  }
  function deleteCookie(name) {
    document.cookie = name + '=; path=/; max-age=0; SameSite=Lax';
  }
  function setGoogleTranslateCookie(language) {
    var value = language === 'en' ? '/ar/en' : '/ar';
    document.cookie = 'googtrans=' + value + '; path=/; max-age=' + (60 * 60 * 24 * 365) + '; SameSite=Lax';
  }
  function clearGoogleTranslateCookies() {
    // Google Translate may create host-only and domain cookies. Clear both so Arabic is restored reliably.
    var expires = '; expires=Thu, 01 Jan 1970 00:00:00 GMT; max-age=0; path=/; SameSite=Lax';
    document.cookie = 'googtrans=' + expires;
    var host = window.location.hostname;
    var labels = host.split('.');
    for (var i = 0; i < labels.length - 1; i++) {
      var domain = labels.slice(i).join('.');
      document.cookie = 'googtrans=' + expires + '; domain=' + domain;
      document.cookie = 'googtrans=' + expires + '; domain=.' + domain;
    }
  }

  /* ---- الوضع الداكن / الفاتح: يُحفظ في Cookie لمدة سنة ---- */
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-bs-theme', next);
      setCookie('watan-theme', next, 60 * 60 * 24 * 365);
      toggle.setAttribute('aria-label', next === 'dark' ? 'تفعيل الوضع الفاتح' : 'تفعيل الوضع الداكن');
    });
  }

  /* ---- التبديل بين العربية والإنجليزية عبر Google Translate مع حفظ الاختيار في Cookie ---- */
  var languageButton = document.getElementById('languageToggle');
  var languageLabel = document.getElementById('languageToggleLabel');
  var currentLanguage = getCookie('watan-language') || root.getAttribute('lang') || 'ar';
  if (currentLanguage !== 'en') currentLanguage = 'ar';
  var pendingLanguage = null;

  function updateLanguageUi(language) {
    currentLanguage = language;
    root.setAttribute('lang', language);
    root.setAttribute('dir', language === 'en' ? 'ltr' : 'rtl');
    if (languageLabel) languageLabel.textContent = language === 'ar' ? 'EN' : 'عربي';
    if (languageButton) {
      languageButton.setAttribute('aria-label', language === 'ar' ? 'Switch language to English' : 'التبديل إلى العربية');
      languageButton.setAttribute('title', language === 'ar' ? 'Switch to English' : 'التبديل إلى العربية');
    }
  }

  function applyGoogleLanguage(language, attemptsLeft) {
    var combo = document.querySelector('#google_translate_element select.goog-te-combo');
    if (!combo) {
      if (attemptsLeft > 0) {
        window.setTimeout(function () { applyGoogleLanguage(language, attemptsLeft - 1); }, 180);
      } else {
        pendingLanguage = language;
        if (languageButton && languageButton.dataset.userRequested === 'true') {
          languageButton.dataset.userRequested = 'false';
          pendingLanguage = null;
          setCookie('watan-language', currentLanguage, 60 * 60 * 24 * 365);
          window.alert('تعذّر تحميل خدمة الترجمة. تأكد من اتصال الإنترنت ثم حاول مرة أخرى.');
        } else if (language === 'en') {
          pendingLanguage = null;
          updateLanguageUi('ar');
          setCookie('watan-language', 'ar', 60 * 60 * 24 * 365);
        }
      }
      return;
    }
    if (language === 'en') {
      setGoogleTranslateCookie('en');
      combo.value = 'en';
    } else {
      clearGoogleTranslateCookies();
      combo.value = '';
    }
    combo.dispatchEvent(new Event('change', { bubbles: true }));
    pendingLanguage = null;
    updateLanguageUi(language);
  }

  updateLanguageUi(currentLanguage);
  if (currentLanguage === 'en') {
    pendingLanguage = 'en';
    applyGoogleLanguage('en', 50);
  }
  window.addEventListener('watan-translate-ready', function () {
    if (pendingLanguage) applyGoogleLanguage(pendingLanguage, 50);
  });
  if (languageButton) {
    languageButton.addEventListener('click', function () {
      var next = currentLanguage === 'ar' ? 'en' : 'ar';
      languageButton.dataset.userRequested = 'true';
      setCookie('watan-language', next, 60 * 60 * 24 * 365);

      if (next === 'en') {
        // Switch to English immediately and persist Google Translate's preference.
        setGoogleTranslateCookie('en');
        pendingLanguage = 'en';
        applyGoogleLanguage('en', 50);
      } else {
        // Google Translate changes the live DOM. Clear its cookies, then reload the original Arabic HTML.
        clearGoogleTranslateCookies();
        pendingLanguage = null;
        languageButton.dataset.userRequested = 'false';
        updateLanguageUi('ar');
        window.setTimeout(function () {
          window.location.reload();
        }, 100);
      }
    });
  }

  /* ---- شريط التنقل + التقدم + زر الأعلى ---- */
  var nav = document.getElementById('mainNav');
  var bar = document.querySelector('.scroll-progress span');
  var toTop = document.getElementById('toTop');
  function onScroll() {
    var y = window.pageYOffset || root.scrollTop;
    var h = root.scrollHeight - root.clientHeight;
    if (nav) nav.classList.toggle('scrolled', y > 30);
    if (bar && h > 0) bar.style.width = (y / h * 100) + '%';
    if (toTop) toTop.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });

  /* ---- ظهور العناصر عند التمرير ---- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- عدّاد الإحصاءات ---- */
  var counters = document.querySelectorAll('[data-count]');
  function runCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;
    if (reduce) { el.textContent = target; return; }
    var dur = 1600, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window && counters.length) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { runCounter(en.target); co.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  } else {
    counters.forEach(runCounter);
  }

  /* ---- فلترة المدن حسب المنطقة ---- */
  var filterBtns = document.querySelectorAll('[data-filter]');
  var cityCols = document.querySelectorAll('[data-region]');
  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var key = btn.getAttribute('data-filter');
      filterBtns.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      cityCols.forEach(function (c) {
        c.classList.toggle('is-hidden', key !== 'all' && c.getAttribute('data-region') !== key);
      });
    });
  });

  /* ---- معرض الصور: مزامنة الصور المصغّرة مع الشريط ---- */
  var carousel = document.getElementById('cityGallery');
  if (carousel) {
    var thumbs = document.querySelectorAll('.gallery-thumbs button');
    carousel.addEventListener('slid.bs.carousel', function (e) {
      thumbs.forEach(function (t, i) { t.classList.toggle('active', i === e.to); });
    });
  }

  /* ---- فيديو الهيرو: إيقاف عند تفضيل تقليل الحركة + زر الصوت ---- */
  var heroVideo = document.querySelector('.hero-media video');
  if (heroVideo) {
    if (reduce) { heroVideo.removeAttribute('autoplay'); heroVideo.pause(); }
    var soundBtn = document.getElementById('heroSound');
    if (soundBtn) soundBtn.addEventListener('click', function () {
      heroVideo.muted = !heroVideo.muted;
      soundBtn.querySelector('i').className = heroVideo.muted ? 'bi bi-volume-mute-fill' : 'bi bi-volume-up-fill';
    });
  }
})();
