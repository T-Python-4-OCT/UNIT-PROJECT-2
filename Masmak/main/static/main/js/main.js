/* ==========================================================================
   main.js — سلوك مشترك لكل الصفحات
   الوضع الداكن/الفاتح، قائمة الجوال، شريط التقدم، ظهور العناصر، العدّادات، غبار الصحراء.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- أدوات صغيرة مشتركة ---------- */
  var Masmak = (window.Masmak = {
    reduceMotion: reduceMotion,
    $: function (sel, ctx) { return (ctx || document).querySelector(sel); },
    $$: function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); },
    data: function (id) {
      var el = document.getElementById(id);
      if (!el) return null;
      try { return JSON.parse(el.textContent); } catch (e) { return null; }
    },
    store: {
      get: function (k, fallback) {
        try { var v = localStorage.getItem("masmak-" + k); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
      },
      set: function (k, v) { try { localStorage.setItem("masmak-" + k, JSON.stringify(v)); } catch (e) {} }
    },
    toast: function (msg) {
      var t = document.querySelector("[data-toast]");
      if (!t) return;
      t.textContent = msg;
      t.classList.add("is-shown");
      clearTimeout(t._timer);
      t._timer = setTimeout(function () { t.classList.remove("is-shown"); }, 2400);
    }
  });

  /* ---------- صور ويكيميديا: الرجوع إلى الرسم التوضيحي إن تعذّر التحميل ---------- */
  function useFallback(img) {
    var fb = img.getAttribute("data-fallback");
    if (!fb || img.getAttribute("data-fell-back")) return;
    img.setAttribute("data-fell-back", "1");
    img.src = fb;
    var fig = img.closest(".media");
    if (fig && !fig.querySelector(".media__badge")) {
      var b = document.createElement("span");
      b.className = "media__badge";
      b.textContent = "رسم توضيحي — تعذّر تحميل الصورة من ويكيميديا";
      fig.appendChild(b);
    }
  }
  Masmak.$$("img[data-fallback]").forEach(function (img) {
    if (img.complete && img.naturalWidth === 0) useFallback(img);
    else img.addEventListener("error", function () { useFallback(img); });
  });

  /* ---------- الوضع الداكن / الفاتح ---------- */
  Masmak.$$("[data-theme-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("masmak-theme", next); } catch (e) {}
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute("content", next === "light" ? "#f4eee2" : "#121110");
      Masmak.toast(next === "light" ? "الوضع الفاتح" : "الوضع الداكن");
    });
  });

  /* ---------- قائمة الجوال ---------- */
  var nav = document.getElementById("site-nav");
  var menuBtn = Masmak.$("[data-menu-toggle]");
  function setMenu(open) {
    if (!nav || !menuBtn) return;
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? "إغلاق القائمة" : "فتح القائمة");
    menuBtn.querySelector("use").setAttribute("href", open ? "#i-close" : "#i-menu");
  }
  if (menuBtn) {
    menuBtn.addEventListener("click", function () { setMenu(!nav.classList.contains("is-open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    Masmak.$$(".nav__link").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  }

  /* ---------- الترويسة فوق الواجهة الرئيسية + شريط القراءة ---------- */
  var header = document.getElementById("site-header");
  var heroMode = header && header.classList.contains("is-hero");
  var bar = Masmak.$("[data-read-progress]");
  function onScroll() {
    var y = window.scrollY;
    if (heroMode) header.classList.toggle("is-hero", y < window.innerHeight * 0.6);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- ظهور العناصر عند التمرير ---------- */
  var reveals = Masmak.$$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- العدّادات ---------- */
  var counters = Masmak.$$("[data-count]");
  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (isNaN(target) || reduceMotion) return;
    var start = target > 1000 ? target - 120 : 0;
    var t0 = null, dur = 1400;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(start + (target - start) * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { animateCount(en.target); cio.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- غبار الصحراء في الواجهة (canvas) ---------- */
  var canvas = Masmak.$("[data-dust]");
  if (canvas && canvas.getContext && !reduceMotion) {
    var ctx = canvas.getContext("2d");
    var parts = [], W = 0, H = 0, raf = null, visible = true;
    function resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(90, W / 14));
      parts = [];
      for (var i = 0; i < n; i++) {
        parts.push({ x: Math.random() * W, y: H * (0.35 + Math.random() * 0.65), r: Math.random() * 1.8 + 0.4,
          vx: -(Math.random() * 0.35 + 0.08), vy: -(Math.random() * 0.12), a: Math.random() * 0.5 + 0.15 });
      }
    }
    function tick() {
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < -10) { p.x = W + 10; p.y = H * (0.35 + Math.random() * 0.65); }
        if (p.y < H * 0.25) p.y = H;
        ctx.beginPath();
        ctx.fillStyle = "rgba(240, 200, 140," + p.a + ")";
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
      raf = visible ? requestAnimationFrame(tick) : null;
    }
    resize();
    window.addEventListener("resize", resize);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) {
        visible = en[0].isIntersecting;
        if (visible && !raf) raf = requestAnimationFrame(tick);
      }).observe(canvas);
    }
    raf = requestAnimationFrame(tick);
  }
})();
