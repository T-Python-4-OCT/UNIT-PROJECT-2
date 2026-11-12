/* old_riyadh.js — مقارنة قديم/حديث + خريطة البوابات التفاعلية */
(function () {
  "use strict";
  var M = window.Masmak;

  /* ---------- مقارنة الصور (قديم / حديث) ---------- */
  var cmp = M.$("[data-compare]");
  if (cmp) {
    var range = M.$("[data-compare-range]", cmp);
    var presets = M.$$("[data-compare-set]");
    var setPos = function (v, animate) {
      v = Math.max(0, Math.min(100, Number(v)));
      if (animate && !M.reduceMotion) {
        var from = parseFloat(getComputedStyle(cmp).getPropertyValue("--pos")) || 50, t0 = null;
        var step = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 500), e = 1 - Math.pow(1 - p, 3);
          cmp.style.setProperty("--pos", from + (v - from) * e + "%");
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      } else {
        cmp.style.setProperty("--pos", v + "%");
      }
      range.value = v;
      presets.forEach(function (b) { b.classList.toggle("is-active", Number(b.getAttribute("data-compare-set")) === Math.round(v)); });
    };
    range.addEventListener("input", function () { setPos(range.value); });
    presets.forEach(function (b) {
      b.addEventListener("click", function () { setPos(b.getAttribute("data-compare-set"), true); });
    });
    /* حركة تعريفية عند الظهور الأول */
    if ("IntersectionObserver" in window && !M.reduceMotion) {
      var io = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) {
          io.disconnect();
          setPos(70, true);
          setTimeout(function () { setPos(30, true); }, 650);
          setTimeout(function () { setPos(50, true); }, 1300);
        }
      }, { threshold: 0.5 });
      io.observe(cmp);
    }
  }

  /* ---------- خريطة البوابات ---------- */
  var gates = M.data("gates-data") || [];
  var panel = M.$("[data-gate-panel]");
  if (!gates.length || !panel) return;
  var byId = {};
  gates.forEach(function (g) { byId[g.id] = g; });
  var nodes = M.$$(".gm-gate");
  var chips = M.$$("[data-gate-btn]");

  function show(id) {
    var g = byId[id];
    if (!g) return;
    M.$("[data-gate-name]", panel).textContent = g.name;
    M.$("[data-gate-dir]", panel).textContent = "الجهة: " + g.dir + " · " + (g.kind === "نقبة" ? "نقبة (بوابة صغيرة للمشاة)" : "بوابة " + g.kind);
    M.$("[data-gate-aka]", panel).textContent = g.aka ? "وتُعرف أيضاً: " + g.aka : "";
    M.$("[data-gate-note]", panel).textContent = g.note;
    nodes.forEach(function (n) { n.classList.toggle("is-active", n.getAttribute("data-gate") === id); });
    chips.forEach(function (c) { c.classList.toggle("is-active", c.getAttribute("data-gate-btn") === id); });
  }
  nodes.forEach(function (n) {
    var id = n.getAttribute("data-gate");
    n.addEventListener("click", function () { show(id); });
    n.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(id); }
    });
  });
  chips.forEach(function (c) { c.addEventListener("click", function () { show(c.getAttribute("data-gate-btn")); }); });
  show("dhuhaira");
})();
