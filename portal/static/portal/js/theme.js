document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("themeToggle");
  const root = document.documentElement;

  if (!themeToggle) {
    return;
  }


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
    localStorage.setItem("site-theme", newTheme);

    updateThemeButton(newTheme);
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const revealElements = document.querySelectorAll(
    ".cinematic-journey .journey-heading, .cinematic-journey .col, .cinematic-about"
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
