document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("themeToggle");
  const root = document.documentElement;

  if (!themeToggle) {
    return;
  }

  function updateThemeButton(theme) {
    const isDark = theme === "dark";

    themeToggle.textContent = isDark ? "Light mode" : "Dark mode";
    themeToggle.setAttribute(
      "aria-label",
      isDark ? "Switch to light mode" : "Switch to dark mode"
    );
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
