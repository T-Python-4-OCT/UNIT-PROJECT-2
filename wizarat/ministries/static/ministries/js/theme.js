(() => {
  const root = document.documentElement;
  const toggle = document.getElementById("themeToggle");
  const icon = document.getElementById("themeIcon");
  if (!toggle || !icon) return;

  const updateThemeButton = () => {
    const isDark = root.dataset.bsTheme === "dark";
    icon.className = isDark ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
    toggle.setAttribute("aria-label", isDark ? "تفعيل الوضع الفاتح" : "تفعيل الوضع الداكن");
  };

  toggle.addEventListener("click", () => {
    const nextTheme = root.dataset.bsTheme === "dark" ? "light" : "dark";
    root.dataset.bsTheme = nextTheme;
    try {
      localStorage.setItem("theme", nextTheme);
    } catch (error) {
      toggle.dataset.storageError = "true";
    }
    updateThemeButton();
  });

  updateThemeButton();
})();
