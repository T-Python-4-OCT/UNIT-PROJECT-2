/* tour.js — جولة تفاعلية في مخطط المصمك + بانوراما قابلة للسحب */
(function () {
  "use strict";
  var M = window.Masmak;
  var stops = M.data("tour-data") || [];
  var root = M.$("[data-tour]");

  if (root && stops.length) {
    var hotspots = M.$$("[data-hotspot]", root);
    var panels = M.$$("[data-stop]", root);
    var visitedEl = M.$("[data-visited]", root);
    var autoBtn = M.$("[data-tour-auto]", root);
    var ids = stops.map(function (s) { return s.id; });
    var visited = M.store.get("tour-visited", []).filter(function (v) { return ids.indexOf(v) !== -1; });
    var current = 0, timer = null;

    function render(i, focusPanel) {
      current = (i + stops.length) % stops.length;
      var id = stops[current].id;
      if (visited.indexOf(id) === -1) { visited.push(id); M.store.set("tour-visited", visited); }
      panels.forEach(function (p) { p.hidden = p.getAttribute("data-stop") !== id; });
      hotspots.forEach(function (h) {
        var hid = h.getAttribute("data-hotspot");
        h.classList.toggle("is-active", hid === id);
        h.classList.toggle("is-visited", visited.indexOf(hid) !== -1 && hid !== id);
        h.setAttribute("aria-pressed", hid === id ? "true" : "false");
      });
      visitedEl.textContent = "زرت " + Math.min(visited.length, stops.length) + " من " + stops.length;
      if (visited.length === stops.length && !render.done) {
        render.done = true;
        M.toast("أكملت الجولة في المصمك كاملة!");
      }
      if (focusPanel && window.innerWidth < 960) {
        var panel = M.$(".tour-panel", root);
        window.scrollTo({ top: window.scrollY + panel.getBoundingClientRect().top - 90, behavior: M.reduceMotion ? "auto" : "smooth" });
      }
    }
    function stopAuto() {
      clearInterval(timer); timer = null;
      autoBtn.querySelector("use").setAttribute("href", "#i-play");
      autoBtn.querySelector("span").textContent = "جولة موجّهة";
    }
    autoBtn.addEventListener("click", function () {
      if (timer) { stopAuto(); return; }
      autoBtn.querySelector("use").setAttribute("href", "#i-pause");
      autoBtn.querySelector("span").textContent = "إيقاف الجولة";
      render(0);
      timer = setInterval(function () {
        if (current === stops.length - 1) { stopAuto(); return; }
        render(current + 1);
      }, 4500);
    });
    hotspots.forEach(function (h) {
      var idx = stops.findIndex(function (s) { return s.id === h.getAttribute("data-hotspot"); });
      h.addEventListener("click", function () { stopAuto(); render(idx, true); });
      h.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); stopAuto(); render(idx, true); } });
    });
    M.$("[data-tour-next]", root).addEventListener("click", function () { stopAuto(); render(current + 1); });
    M.$("[data-tour-prev]", root).addEventListener("click", function () { stopAuto(); render(current - 1); });
    render(0);
  }

  /* ---------- بانوراما: سحب أفقي لا نهائي ---------- */
  var pano = M.$("[data-pano]");
  if (pano) {
    var x = 0, startX = 0, startPos = 0, dragging = false, vel = 0, last = 0, rafId = null;
    function apply() { pano.style.backgroundPosition = x + "px center"; }
    function down(e) {
      dragging = true; startX = (e.touches ? e.touches[0].clientX : e.clientX); startPos = x; last = startX; vel = 0;
      cancelAnimationFrame(rafId);
    }
    function moveEv(e) {
      if (!dragging) return;
      var cx = e.touches ? e.touches[0].clientX : e.clientX;
      vel = cx - last; last = cx;
      x = startPos + (cx - startX);
      apply();
    }
    function up() {
      if (!dragging) return;
      dragging = false;
      if (M.reduceMotion) return;
      (function glide() {                /* انزلاق بالقصور الذاتي */
        vel *= 0.94; x += vel; apply();
        if (Math.abs(vel) > 0.3) rafId = requestAnimationFrame(glide);
      })();
    }
    pano.addEventListener("mousedown", down);
    window.addEventListener("mousemove", moveEv);
    window.addEventListener("mouseup", up);
    pano.addEventListener("touchstart", down, { passive: true });
    pano.addEventListener("touchmove", moveEv, { passive: true });
    pano.addEventListener("touchend", up);
    pano.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { x += 60; apply(); }
      if (e.key === "ArrowRight") { x -= 60; apply(); }
    });
    /* دوران بطيء تلقائي حتى يلمسه المستخدم */
    if (!M.reduceMotion) {
      var idle = true;
      pano.addEventListener("mousedown", function () { idle = false; });
      pano.addEventListener("touchstart", function () { idle = false; }, { passive: true });
      (function drift() { if (idle) { x -= 0.25; apply(); } requestAnimationFrame(drift); })();
    }
  }
})();
