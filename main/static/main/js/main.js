// الطريق إلى 2034 – shared behaviour for every page

document.addEventListener("DOMContentLoaded", function () {
    // Navbar shadow after scrolling
    var nav = document.querySelector(".site-nav");
    function onScroll() {
        if (nav) nav.classList.toggle("scrolled", window.scrollY > 10);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    // Reveal sections when they enter the screen
    var items = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });
        items.forEach(function (el) { observer.observe(el); });
    } else {
        items.forEach(function (el) { el.classList.add("visible"); });
    }
});

// =========================================================
// Home page: countdown + number counters
// =========================================================
document.addEventListener("DOMContentLoaded", function () {

    // ----- Countdown -----
    var box = document.getElementById("countdown");
    if (box) {
        var target = new Date(box.dataset.target).getTime();
        var els = {
            days: document.getElementById("cd-days"),
            hours: document.getElementById("cd-hours"),
            minutes: document.getElementById("cd-minutes"),
            seconds: document.getElementById("cd-seconds"),
        };
        function setValue(el, value) {
            if (el.textContent !== String(value)) {
                el.textContent = value;
                el.classList.remove("tick");
                void el.offsetWidth;          // restart the CSS animation
                el.classList.add("tick");
            }
        }
        function update() {
            var diff = Math.max(0, target - Date.now());
            setValue(els.days, Math.floor(diff / 86400000));
            setValue(els.hours, Math.floor(diff / 3600000) % 24);
            setValue(els.minutes, Math.floor(diff / 60000) % 60);
            setValue(els.seconds, Math.floor(diff / 1000) % 60);
        }
        update();
        setInterval(update, 1000);
    }

    // ----- Count-up numbers when they appear on screen -----
    var counters = document.querySelectorAll(".counter");
    if (counters.length && "IntersectionObserver" in window) {
        var obs = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target, end = Number(el.dataset.target), start = null;
                function step(ts) {
                    if (!start) start = ts;
                    var p = Math.min((ts - start) / 1400, 1);
                    el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
                    if (p < 1) requestAnimationFrame(step);
                }
                el.textContent = "0";
                requestAnimationFrame(step);
                obs.unobserve(el);
            });
        }, { threshold: 0.6 });
        counters.forEach(function (c) { obs.observe(c); });
    }
});
