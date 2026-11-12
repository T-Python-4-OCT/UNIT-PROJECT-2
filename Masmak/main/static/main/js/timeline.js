/* timeline.js — خط زمني تفاعلي: تصفية بالحقبة، تنقّل، ومقياس زمني نسبي قابل للسحب */
(function () {
  "use strict";
  var M = window.Masmak;
  var root = M.$("[data-tl]");
  if (!root) return;

  var marks = M.$$("[data-event]", root);
  var cards = M.$$("[data-event-card]", root);
  var scroller = M.$("[data-tl-scroller]", root);
  var bar = M.$("[data-scale]");
  var dots = bar ? M.$$("[data-tl-jump]", bar) : [];
  var handle = bar ? M.$("[data-scale-handle]", bar) : null;
  var bubble = bar ? M.$("[data-scale-bubble]", bar) : null;
  var activeId = (M.$(".tl__mark.is-active", root) || marks[0]).getAttribute("data-event");

  function markOf(id) { return marks.find(function (m) { return m.getAttribute("data-event") === id; }); }
  function dotOf(id) { return dots.find(function (d) { return d.getAttribute("data-tl-jump") === id; }); }
  function visibleMarks() { return marks.filter(function (m) { return !m.hidden; }); }

  /* ---------- مؤشر المقياس ---------- */
  function moveHandle(id, pos) {
    if (!handle) return;
    var dot = dotOf(id);
    if (!dot) return;
    var p = pos != null ? pos : parseFloat(dot.getAttribute("data-pos"));
    handle.style.insetInlineStart = p + "%";
    bubble.textContent = dot.getAttribute("data-label");
    bubble.classList.toggle("edge-start", p < 12);
    bubble.classList.toggle("edge-end", p > 88);
    bar.setAttribute("aria-valuenow", dot.getAttribute("data-year"));
    bar.setAttribute("aria-valuetext", dot.getAttribute("data-label"));
  }

  function select(id, opts) {
    opts = opts || {};
    activeId = id;
    marks.forEach(function (m) {
      var on = m.getAttribute("data-event") === id;
      m.classList.toggle("is-active", on);
      m.setAttribute("aria-selected", on ? "true" : "false");
      m.tabIndex = on ? 0 : -1;
      if (on && opts.scroll !== false) {
        var sr = scroller.getBoundingClientRect(), mr = m.getBoundingClientRect();
        scroller.scrollBy({ left: (mr.left + mr.width / 2) - (sr.left + sr.width / 2), behavior: M.reduceMotion ? "auto" : "smooth" });
      }
      if (on && opts.focus) m.focus({ preventScroll: true });
    });
    cards.forEach(function (c) { c.hidden = c.getAttribute("data-event-card") !== id; });
    dots.forEach(function (d) { d.classList.toggle("is-active", d.getAttribute("data-tl-jump") === id); });
    if (!opts.keepHandle) moveHandle(id);
  }

  function step(dir, focus) {
    var vis = visibleMarks();
    var i = vis.findIndex(function (m) { return m.getAttribute("data-event") === activeId; });
    var n = vis[Math.max(0, Math.min(vis.length - 1, i + dir))];
    if (n) select(n.getAttribute("data-event"), { focus: focus });
  }

  /* ---------- أحداث الخط الزمني ---------- */
  marks.forEach(function (m) {
    m.addEventListener("click", function () { select(m.getAttribute("data-event")); });
    m.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); step(1, true); }    /* RTL */
      if (e.key === "ArrowRight") { e.preventDefault(); step(-1, true); }
      if (e.key === "Home") { e.preventDefault(); select(visibleMarks()[0].getAttribute("data-event"), { focus: true }); }
      if (e.key === "End") { e.preventDefault(); var v = visibleMarks(); select(v[v.length - 1].getAttribute("data-event"), { focus: true }); }
    });
  });
  M.$("[data-tl-next]").addEventListener("click", function () { step(1); });
  M.$("[data-tl-prev]").addEventListener("click", function () { step(-1); });

  /* ---------- السحب والنقر على المقياس ---------- */
  if (bar) {
    /* النسبة من بداية الشريط (اليمين في RTL) */
    function posFromEvent(e) {
      var r = bar.getBoundingClientRect();
      var rtl = getComputedStyle(bar).direction === "rtl";
      var x = e.touches ? e.touches[0].clientX : e.clientX;
      var p = rtl ? (r.right - x) / r.width : (x - r.left) / r.width;
      return Math.max(0, Math.min(1, p)) * 100;
    }
    function nearest(p) {
      var best = null, bd = Infinity;
      dots.forEach(function (d) {
        if (d.classList.contains("is-dim")) return;
        var dist = Math.abs(parseFloat(d.getAttribute("data-pos")) - p);
        if (dist < bd) { bd = dist; best = d; }
      });
      return best ? best.getAttribute("data-tl-jump") : null;
    }
    var dragging = false;
    function update(e, final) {
      var p = posFromEvent(e);
      var id = nearest(p);
      if (!id) return;
      if (dragging && !final) {
        handle.style.insetInlineStart = p + "%";
        if (id !== activeId) select(id, { keepHandle: true, scroll: true });
        moveHandleLabel(id, p);
      } else {
        select(id);
      }
    }
    function moveHandleLabel(id, p) {
      var dot = dotOf(id);
      bubble.textContent = dot.getAttribute("data-label");
      bubble.classList.toggle("edge-start", p < 12);
      bubble.classList.toggle("edge-end", p > 88);
    }
    bar.addEventListener("pointerdown", function (e) {
      dragging = true;
      bar.classList.add("is-dragging");
      if (bar.setPointerCapture) bar.setPointerCapture(e.pointerId);
      update(e);
    });
    bar.addEventListener("pointermove", function (e) { if (dragging) update(e); });
    function end(e) {
      if (!dragging) return;
      dragging = false;
      bar.classList.remove("is-dragging");
      update(e, true);   /* يستقر المؤشر على أقرب محطة */
    }
    bar.addEventListener("pointerup", end);
    bar.addEventListener("pointercancel", function () { dragging = false; bar.classList.remove("is-dragging"); moveHandle(activeId); });
    bar.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft" || e.key === "ArrowDown") { e.preventDefault(); step(1); }
      if (e.key === "ArrowRight" || e.key === "ArrowUp") { e.preventDefault(); step(-1); }
      if (e.key === "Home") { e.preventDefault(); select(visibleMarks()[0].getAttribute("data-event")); }
      if (e.key === "End") { e.preventDefault(); var v = visibleMarks(); select(v[v.length - 1].getAttribute("data-event")); }
    });
  }

  /* ---------- التصفية بالحقبة ---------- */
  var chips = M.$$("[data-era].chip");
  function setEra(id) {
    chips.forEach(function (c) { c.classList.toggle("is-active", c.getAttribute("data-era") === id); });
    marks.forEach(function (m) { m.hidden = !(id === "all" || m.getAttribute("data-era") === id); });
    dots.forEach(function (d) {
      var mark = markOf(d.getAttribute("data-tl-jump"));
      d.classList.toggle("is-dim", !!(mark && mark.hidden));
    });
    var vis = visibleMarks();
    if (!vis.some(function (m) { return m.getAttribute("data-event") === activeId; }) && vis.length) {
      select(vis[0].getAttribute("data-event"));
    }
    scroller.scrollTo({ left: 0 });
  }
  chips.forEach(function (c) { c.addEventListener("click", function () { setEra(c.getAttribute("data-era")); }); });

  select(activeId, { scroll: true });
})();
