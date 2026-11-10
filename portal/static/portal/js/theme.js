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

    themeToggle.textContent = label;
    themeToggle.setAttribute("aria-label", ariaLabel);
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