
(function () {
  "use strict";

  var root = document.documentElement;

  
  var themeBtn = document.getElementById("theme-toggle");
  var themeLabel = document.getElementById("theme-label");
  var themeColor = document.querySelector('meta[name="theme-color"]');

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var isDark = theme === "dark";
    if (themeBtn) themeBtn.setAttribute("aria-pressed", String(isDark));
    if (themeLabel && themeBtn) themeLabel.textContent = themeBtn.getAttribute(isDark ? "data-label-on-dark" : "data-label-on-light");
    if (themeBtn) themeBtn.setAttribute("aria-label", themeBtn.getAttribute(isDark ? "data-aria-on-dark" : "data-aria-on-light"));
    if (themeColor) themeColor.setAttribute("content", isDark ? "#0D122C" : "#16644A");
  }

  applyTheme(root.getAttribute("data-theme") || "light");

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem("theme", next); } catch (e) {  }
    });
  }

  
  var menuBtn = document.getElementById("menu-toggle");
  var nav = document.getElementById("site-nav");

  function setMenu(open) {
    document.body.classList.toggle("nav-open", open);
    if (menuBtn) {
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", menuBtn.getAttribute(open ? "data-label-open" : "data-label-closed"));
    }
  }

  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      setMenu(!document.body.classList.contains("nav-open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  
  document.addEventListener("click", function (e) {
    var link = e.target.closest("a[href]");
    if (!link) return;
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (link.target && link.target !== "_self") return;
    if (link.hasAttribute("download")) return;

    var url;
    try { url = new URL(link.href, window.location.href); } catch (err) { return; }
    if (url.origin !== window.location.origin) return;
    if (url.pathname === window.location.pathname && url.search === window.location.search) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    e.preventDefault();
    document.body.classList.add("is-leaving");
    window.setTimeout(function () { window.location.href = url.href; }, 180);
  });
  window.addEventListener("pageshow", function () {
    document.body.classList.remove("is-leaving");
  });

  
  var chips = document.querySelectorAll(".chip[data-filter]");
  var cards = document.querySelectorAll("#gallery .card");

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var filter = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      cards.forEach(function (card) {
        var show = filter === "all" || card.getAttribute("data-kind") === filter;
        card.hidden = !show;
      });
    });
  });
})();
