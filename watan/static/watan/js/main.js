/* حكاية وطن — السلوك التفاعلي */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- إرسال تفضيلات المستخدم إلى Django لحفظها في Cookies ---- */
  function getCsrfToken() {
    var field = document.querySelector('#preferenceCsrfForm input[name="csrfmiddlewaretoken"]');
    return field ? field.value : '';
  }

  function savePreference(url, values) {
    var body = new URLSearchParams(values);
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: body.toString()
    }).then(function (response) {
      if (!response.ok) throw new Error('تعذر حفظ التفضيل');
      return response.json();
    }).then(function (data) {
      if (!data.ok) throw new Error('قيمة التفضيل غير صحيحة');
      return data;
    });
  }

  /* ---- الوضع الداكن / الفاتح: Django يقرأ Cookie ويعرض الوضع ---- */
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var previous = root.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
      var next = previous === 'dark' ? 'light' : 'dark';
      var endpoint = toggle.getAttribute('data-preference-url');

      // تطبيق فوري، ثم حفظ الاختيار من خلال View في Django.
      root.setAttribute('data-bs-theme', next);
      toggle.disabled = true;

      savePreference(endpoint, { theme: next }).then(function () {
        toggle.setAttribute('aria-label', next === 'dark' ? 'تفعيل الوضع الفاتح' : 'تفعيل الوضع الداكن');
      }).catch(function () {
        root.setAttribute('data-bs-theme', previous);
        window.alert('تعذر حفظ الوضع. حدّث الصفحة وحاول مرة أخرى.');
      }).finally(function () {
        toggle.disabled = false;
      });
    });
  }

  /* ---- اللغة: watan-language و googtrans Cookies تُدار من Django Views ---- */
  var languageButton = document.getElementById('languageToggle');
  var languageLabel = document.getElementById('languageToggleLabel');
  var currentLanguage = root.getAttribute('lang') === 'en' ? 'en' : 'ar';
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
        window.setTimeout(function () {
          applyGoogleLanguage(language, attemptsLeft - 1);
        }, 180);
      } else if (language === 'en') {
        pendingLanguage = null;
        window.alert('تم حفظ اللغة الإنجليزية، لكن خدمة Google Translate لم تُحمّل. تأكد من اتصال الإنترنت ثم أعد المحاولة.');
      }
      return;
    }

    combo.value = language === 'en' ? 'en' : '';
    combo.dispatchEvent(new Event('change', { bubbles: true }));
    pendingLanguage = null;
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
      var endpoint = languageButton.getAttribute('data-preference-url');
      languageButton.disabled = true;

      savePreference(endpoint, { language: next }).then(function () {
        // إعادة تحميل الصفحة تجعل Django يقرأ Cookie الجديدة، ويعيد Google Translate بناء اللغة.
        window.location.reload();
      }).catch(function () {
        languageButton.disabled = false;
        window.alert('تعذر حفظ اللغة. تأكد من اتصال الإنترنت ثم حاول مرة أخرى.');
      });
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
