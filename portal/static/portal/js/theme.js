/* ===== Dark / light mode toggle =====
   The saved theme is applied in base.html before the page paints;
   this script only updates the button and saves the new choice. */
document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("themeToggle");
  const root = document.documentElement;

  if (!themeToggle) {
    return;
  }

  // Show the icon and label for the mode the button will switch TO
  function updateThemeButton(theme) {
    const isDark = theme === "dark";

    const label = isDark
      ? themeToggle.dataset.lightLabel
      : themeToggle.dataset.darkLabel;

    const ariaLabel = isDark
      ? themeToggle.dataset.lightAria
      : themeToggle.dataset.darkAria;

    const icon = themeToggle.querySelector(".theme-icon");

    if (icon) {
      icon.textContent = isDark ? "☀" : "☾";
    }

    themeToggle.setAttribute("aria-label", ariaLabel);
    themeToggle.setAttribute("title", label);
  }

  const currentTheme = root.getAttribute("data-bs-theme") || "light";
  updateThemeButton(currentTheme);

  themeToggle.addEventListener("click", function () {
    const current = root.getAttribute("data-bs-theme");
    const newTheme = current === "dark" ? "light" : "dark";

    root.setAttribute("data-bs-theme", newTheme);
    localStorage.setItem("site-theme", newTheme); // remembered on the next visit

    updateThemeButton(newTheme);
  });
});


/* ===== Scroll reveal: sections fade in the first time they enter the screen ===== */
document.addEventListener("DOMContentLoaded", function () {
  const revealElements = document.querySelectorAll(
    ".cinematic-journey .journey-heading, .bento-item, .cinematic-about, .gallery-item, .comparison-row"
  );

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  revealElements.forEach(function (element) {
    element.classList.add("reveal-item");
  });

  const revealObserver = new IntersectionObserver(
    function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.12,
      rootMargin: "0px 0px -40px 0px"
    }
  );

  revealElements.forEach(function (element) {
    revealObserver.observe(element);
  });
});


/* ===== Navbar scroll state + reading progress ===== */
document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".site-navbar");

  if (!navbar) {
    return;
  }

  let ticking = false;

  function updateNavbar() {
    const scrollTop = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const progress = maxScroll > 0 ? scrollTop / maxScroll : 0;

    navbar.classList.toggle("is-scrolled", scrollTop > 24);
    navbar.style.setProperty("--scroll-progress", progress.toFixed(3));
    ticking = false;
  }

  // requestAnimationFrame: update at most once per frame, not on every scroll event
  window.addEventListener("scroll", function () {
    if (!ticking) {
      window.requestAnimationFrame(updateNavbar);
      ticking = true;
    }
  }, { passive: true });

  updateNavbar();
});


/* ===== Count-up for stat numbers ===== */
document.addEventListener("DOMContentLoaded", function () {
  const statValues = document.querySelectorAll(".stat-value");

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  // Animate only values like "280", "4,438", "18.3 million", "460+", "+28 مليون".
  // Skip dates and rankings such as "25 April 2016" or "2nd of 197".
  const pattern = /^(\+?)(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(\D*)$/;

  function countUp(element, target, decimals, prefix, suffix, grouped) {
    const duration = 1200;
    const start = performance.now();

    // Only the digits change while counting. They sit in their own box, sized to the
    // final number, so words like "million" / "مليون" and the "+" sign do not move.
    const digits = document.createElement("span");
    digits.className = "count-digits";
    digits.textContent = element.textContent.trim().slice(prefix.length, element.textContent.trim().length - suffix.length);
    element.textContent = "";
    element.append(prefix, digits, suffix);
    digits.style.minWidth = digits.getBoundingClientRect().width + "px";

    function frame(now) {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      const value = target * eased;
      // Keep the commas while counting when the original value had them
      const text = grouped
        ? Math.round(value).toLocaleString("en-US")
        : value.toFixed(decimals);
      digits.textContent = text;

      if (t < 1) {
        requestAnimationFrame(frame);
      }
    }

    requestAnimationFrame(frame);
  }

  const observer = new IntersectionObserver(function (entries, obs) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) {
        return;
      }

      const element = entry.target;
      const match = element.textContent.trim().match(pattern);
      obs.unobserve(element);

      if (!match) {
        return;
      }

      const prefix = match[1];
      const grouped = match[2].includes(",");
      const number = match[2].replace(/,/g, "");
      const suffix = match[3];
      const decimals = (number.split(".")[1] || "").length;
      countUp(element, parseFloat(number), decimals, prefix, suffix, grouped);
    });
  }, { threshold: 0.6 });

  statValues.forEach(function (element) {
    observer.observe(element);
  });
});


/* ===== Character counter for textareas with data-char-counter ===== */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-char-counter]").forEach(function (field) {
    const counter = document.getElementById(field.dataset.charCounter);
    const max = Number(field.getAttribute("maxlength"));

    if (!counter || !max) {
      return;
    }

    function update() {
      const length = field.value.trim().length;
      counter.textContent = length + " / " + max;
      counter.classList.toggle("is-over", length > max);
    }

    field.addEventListener("input", update);
    update();
  });
});


/* ===== Before/after slider: the range value becomes the --pos CSS variable ===== */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-compare]").forEach(function (compare) {
    const range = compare.querySelector(".compare-range");

    if (!range) {
      return;
    }

    range.addEventListener("input", function () {
      compare.style.setProperty("--pos", range.value + "%");
    });
  });
});

/* ===== Quiz progress: count answered questions and fill the bar ===== */
document.addEventListener("DOMContentLoaded", function () {
  const quiz = document.querySelector("[data-quiz]");
  if (!quiz) {
    return;
  }

  const total = quiz.querySelectorAll("fieldset").length;
  const count = quiz.querySelector("[data-quiz-count]");
  const fill = quiz.querySelector("[data-quiz-fill]");

  function update() {
    const answered = quiz.querySelectorAll("input[type=radio]:checked").length;
    count.textContent = answered;
    fill.style.width = (answered / total) * 100 + "%";
  }

  quiz.addEventListener("change", update);
  update(); // answers kept after a failed submit are counted straight away
});

/* ===== Spotlight: pass the pointer position to CSS so a glow follows it ===== */
document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".spotlight, .info-card, .stat-card");

  cards.forEach(function (card) {
    card.addEventListener("pointermove", function (event) {
      const box = card.getBoundingClientRect();
      card.style.setProperty("--mx", event.clientX - box.left + "px");
      card.style.setProperty("--my", event.clientY - box.top + "px");
    });
  });
});
