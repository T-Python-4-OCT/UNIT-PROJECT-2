
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");

function updateThemeIcon() {
    const theme = document.documentElement.getAttribute("data-bs-theme");

    if (theme === "dark") {
        themeIcon.textContent = "☀";
        themeToggle.setAttribute("aria-label", "Switch to light mode");
    } else {
        themeIcon.textContent = "☾";
        themeToggle.setAttribute("aria-label", "Switch to dark mode");
    }
}

if (themeToggle && themeIcon) {
    updateThemeIcon();

    themeToggle.addEventListener("click", function () {
        const current = document.documentElement.getAttribute("data-bs-theme");
        const next = current === "dark" ? "light" : "dark";

        document.documentElement.setAttribute("data-bs-theme", next);

        try {
            localStorage.setItem("theme", next);
        } catch (error) {
            // The theme still changes if storage is unavailable.
        }

        updateThemeIcon();
    });
}
