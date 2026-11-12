/* participants.js — معرض الشخصيات (شريط + نافذة) وقائمة الرواد مع البحث والتصفية */
(function () {
  "use strict";
  var M = window.Masmak;
  var people = M.data("people-data") || [];
  var urlTpl = window.MASMAK_PERSON_URL || "/participants/SLUG/";

  /* ---------- الشريط (carousel) ---------- */
  var track = M.$("[data-carousel]");
  function scrollByCard(dir) {
    if (!track) return;
    var card = track.querySelector(".person-card:not([hidden])");
    var w = card ? card.getBoundingClientRect().width + 18 : 280;
    /* في RTL: التالي = التمرير نحو اليسار (قيمة سالبة) */
    track.scrollBy({ left: dir * -w, behavior: M.reduceMotion ? "auto" : "smooth" });
  }
  var nextBtn = M.$("[data-carousel-next]"), prevBtn = M.$("[data-carousel-prev]");
  if (nextBtn) nextBtn.addEventListener("click", function () { scrollByCard(1); });
  if (prevBtn) prevBtn.addEventListener("click", function () { scrollByCard(-1); });

  /* ---------- تصفية الشريط حسب المجموعة ---------- */
  var cards = M.$$(".person-card[data-person]");
  M.$$("[data-group-filter]").forEach(function (chip, _, all) {
    chip.addEventListener("click", function () {
      var g = chip.getAttribute("data-group-filter");
      all.forEach(function (c) { c.classList.toggle("is-active", c === chip); });
      cards.forEach(function (card) { card.hidden = !(g === "all" || card.getAttribute("data-group") === g); });
      if (track) track.scrollTo({ left: 0 });
    });
  });

  /* ---------- النافذة المنبثقة ---------- */
  var modal = M.$("[data-modal]");
  var current = 0, lastFocus = null;
  function visiblePeople() {
    var slugs = cards.filter(function (c) { return !c.hidden; }).map(function (c) { return c.getAttribute("data-person"); });
    return people.filter(function (p) { return slugs.indexOf(p.slug) !== -1; });
  }
  function fill(p) {
    M.$("[data-m-role]", modal).textContent = p.role;
    M.$("[data-m-name]", modal).textContent = p.name;
    M.$("[data-m-years]", modal).textContent = p.years || "";
    M.$("[data-m-group]", modal).textContent = p.group;
    M.$("[data-m-summary]", modal).textContent = p.summary;
    M.$("[data-m-link]", modal).setAttribute("href", urlTpl.replace("SLUG", p.slug));
  }
  function open(slug) {
    var list = visiblePeople();
    current = Math.max(0, list.findIndex(function (p) { return p.slug === slug; }));
    fill(list[current]);
    lastFocus = document.activeElement;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    setTimeout(function () { M.$("[data-modal-close]", modal).focus(); }, 50);
  }
  function close() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  function move(d) {
    var list = visiblePeople();
    if (!list.length) return;
    current = (current + d + list.length) % list.length;
    fill(list[current]);
  }
  if (modal) {
    cards.forEach(function (c) { c.addEventListener("click", function () { open(c.getAttribute("data-person")); }); });
    M.$("[data-modal-close]", modal).addEventListener("click", close);
    M.$("[data-m-next]", modal).addEventListener("click", function () { move(1); });
    M.$("[data-m-prev]", modal).addEventListener("click", function () { move(-1); });
    modal.addEventListener("click", function (e) { if (e.target === modal) close(); });
    document.addEventListener("keydown", function (e) {
      if (!modal.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") move(1);   /* RTL: اليسار = التالي */
      if (e.key === "ArrowRight") move(-1);
      if (e.key === "Tab") {               /* حصر التركيز داخل النافذة */
        var f = M.$$("a, button", modal);
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    });
  }

  /* ---------- قائمة الرواد: بحث + تصفية ---------- */
  var items = M.$$("[data-roster] .roster__item");
  var search = M.$("[data-roster-search]");
  var empty = M.$("[data-roster-empty]");
  var countEl = M.$("[data-roster-count]");
  var origin = "all";
  /* توحيد الحروف العربية لبحث أذكى (أ/إ/آ → ا، ة → ه، ى → ي) */
  function norm(s) {
    return (s || "").replace(/[ً-ْ]/g, "").replace(/[أإآ]/g, "ا").replace(/ة/g, "ه").replace(/ى/g, "ي").toLowerCase().trim();
  }
  function apply() {
    var q = norm(search ? search.value : "");
    var shown = 0;
    items.forEach(function (it) {
      var okOrigin = origin === "all" || it.getAttribute("data-origin") === origin;
      var hay = norm(it.getAttribute("data-name") + " " + it.getAttribute("data-origin"));
      var ok = okOrigin && (!q || hay.indexOf(q) !== -1);
      it.hidden = !ok;
      if (ok) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
    if (countEl) countEl.textContent = shown;
  }
  if (search) search.addEventListener("input", apply);
  M.$$("[data-origin].chip").forEach(function (chip, _, all) {
    chip.addEventListener("click", function () {
      origin = chip.getAttribute("data-origin");
      all.forEach(function (c) { c.classList.toggle("is-active", c === chip); });
      apply();
    });
  });
})();
