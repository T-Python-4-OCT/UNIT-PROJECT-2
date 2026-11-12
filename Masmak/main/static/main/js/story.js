/* story.js — تسلسل فصول القصة مرتبطاً بخريطة المسار التفاعلية */
(function () {
  "use strict";
  var M = window.Masmak;
  var data = M.data("story-data");
  var root = M.$("[data-story]");
  if (!data || !root) return;

  var chapters = data.chapters, route = data.route;
  var routeIndex = {};
  route.forEach(function (r, i) { routeIndex[r.id] = i; });

  var articles = M.$$("[data-chapter]", root);
  var points = M.$$(".mp-point", root);
  var pathEl = M.$("[data-route]", root);
  var pathBg = M.$("[data-route-bg]", root);
  var callout = M.$("[data-callout]", root);
  var fill = M.$("[data-progress]", root);
  var countEl = M.$("[data-step-count]", root);
  var playBtn = M.$("[data-play]");
  var current = 0, timer = null;

  /* ---------- رسم المسار بمنحنى ناعم (Catmull-Rom → Bézier) ---------- */
  function segment(p0, p1, p2, p3) {
    var t = 0.5;
    var c1x = p1.x + (p2.x - p0.x) / 6 * t * 2, c1y = p1.y + (p2.y - p0.y) / 6 * t * 2;
    var c2x = p2.x - (p3.x - p1.x) / 6 * t * 2, c2y = p2.y - (p3.y - p1.y) / 6 * t * 2;
    return " C" + c1x.toFixed(1) + " " + c1y.toFixed(1) + " " + c2x.toFixed(1) + " " + c2y.toFixed(1) + " " + p2.x + " " + p2.y;
  }
  function buildPath(n) {
    var d = "M" + route[0].x + " " + route[0].y;
    for (var i = 0; i < n; i++) {
      var p0 = route[Math.max(0, i - 1)], p1 = route[i], p2 = route[i + 1], p3 = route[Math.min(route.length - 1, i + 2)];
      d += segment(p0, p1, p2, p3);
    }
    return d;
  }
  var full = buildPath(route.length - 1);
  pathEl.setAttribute("d", full);
  pathBg.setAttribute("d", full);
  var total = pathEl.getTotalLength();
  /* الطول التراكمي حتى كل محطة */
  var probe = document.createElementNS("http://www.w3.org/2000/svg", "path");
  probe.style.visibility = "hidden";
  pathEl.parentNode.appendChild(probe);
  var cum = route.map(function (_, i) {
    if (i === 0) return 0;
    probe.setAttribute("d", buildPath(i));
    return probe.getTotalLength();
  });
  probe.remove();
  pathEl.style.strokeDasharray = total;
  pathEl.style.strokeDashoffset = total;
  if (!M.reduceMotion) pathEl.style.transition = "stroke-dashoffset 1.1s cubic-bezier(.2,.7,.2,1)";

  /* ---------- تفعيل فصل ---------- */
  function setStep(i, opts) {
    opts = opts || {};
    current = Math.max(0, Math.min(chapters.length - 1, i));
    var ch = chapters[current];
    var ri = routeIndex[ch.point] || 0;

    articles.forEach(function (a, k) {
      a.classList.toggle("is-active", k === current);
      a.setAttribute("aria-current", k === current ? "step" : "false");
    });
    fill.style.width = ((current + 1) / chapters.length) * 100 + "%";
    countEl.textContent = (current + 1) + " من " + chapters.length;

    pathEl.style.strokeDashoffset = total - cum[ri];
    points.forEach(function (p, k) {
      p.classList.toggle("is-done", k < ri);
      p.classList.toggle("is-active", k === ri);
    });
    var r = route[ri];
    callout.innerHTML = "";
    var b = document.createElement("b");
    b.textContent = (ri + 1) + ". " + r.name + " — " + r.date;
    callout.appendChild(b);
    callout.appendChild(document.createTextNode(r.note));

    if (opts.scroll) {
      var el = articles[current];
      var rect = el.getBoundingClientRect();
      if (rect.top < 80 || rect.top > window.innerHeight * 0.6) {
        window.scrollTo({ top: window.scrollY + rect.top - 150, behavior: M.reduceMotion ? "auto" : "smooth" });
      }
    }
    if (opts.hash !== false && history.replaceState) history.replaceState(null, "", "#ch-" + ch.slug);
  }

  /* ---------- التشغيل التلقائي ---------- */
  function stop() {
    clearInterval(timer); timer = null;
    playBtn.querySelector("use").setAttribute("href", "#i-play");
    playBtn.querySelector("span").textContent = "تشغيل المسار";
  }
  function play() {
    if (current >= chapters.length - 1) setStep(0);
    playBtn.querySelector("use").setAttribute("href", "#i-pause");
    playBtn.querySelector("span").textContent = "إيقاف";
    timer = setInterval(function () {
      if (current >= chapters.length - 1) { stop(); M.toast("وصلنا إلى بوابة المصمك"); return; }
      setStep(current + 1, { scroll: false });
    }, 2600);
  }
  playBtn.addEventListener("click", function () { timer ? stop() : play(); });
  M.$("[data-restart]").addEventListener("click", function () { stop(); setStep(0, { scroll: true }); });

  /* ---------- أحداث ---------- */
  M.$("[data-step-next]", root).addEventListener("click", function () { stop(); setStep(current + 1, { scroll: true }); });
  M.$("[data-step-prev]", root).addEventListener("click", function () { stop(); setStep(current - 1, { scroll: true }); });
  articles.forEach(function (a, k) {
    a.addEventListener("click", function (e) {
      if (k === current || e.target.closest("a")) return;
      stop(); setStep(k, { scroll: true });
    });
    a.addEventListener("keydown", function (e) {
      if ((e.key === "Enter" || e.key === " ") && k !== current && e.target === a) { e.preventDefault(); stop(); setStep(k, { scroll: true }); }
    });
  });
  points.forEach(function (p) {
    function go() {
      var id = p.getAttribute("data-point");
      var k = chapters.findIndex(function (c) { return c.point === id; });
      if (k !== -1) { stop(); setStep(k, { scroll: true }); }
    }
    p.addEventListener("click", go);
    p.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
  });
  document.addEventListener("keydown", function (e) {
    if (/input|textarea|select/i.test(e.target.tagName)) return;
    if (e.key === "ArrowLeft") { stop(); setStep(current + 1, { scroll: true }); }   /* RTL */
    if (e.key === "ArrowRight") { stop(); setStep(current - 1, { scroll: true }); }
  });

  /* ---------- البداية (مع دعم الرابط المباشر #ch-slug) ---------- */
  var start = 0;
  if (location.hash.indexOf("#ch-") === 0) {
    var slug = location.hash.slice(4);
    var k = chapters.findIndex(function (c) { return c.slug === slug; });
    if (k !== -1) start = k;
  }
  setStep(start, { hash: start !== 0, scroll: start !== 0 });
})();
