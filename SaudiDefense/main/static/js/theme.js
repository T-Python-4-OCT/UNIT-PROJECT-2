const html = document.documentElement;
const themeButton = document.getElementById("themeToggle");

function updateIcon() {
    const icon = themeButton.querySelector("i");
    if (html.getAttribute("data-bs-theme") === "dark") {
        icon.className = "bi bi-sun-fill";
    } else {
        icon.className = "bi bi-moon-stars-fill";
    }
}

themeButton.addEventListener("click", function () {
    let newTheme = "dark";
    if (html.getAttribute("data-bs-theme") === "dark") {
        newTheme = "light";
    }

    html.setAttribute("data-bs-theme", newTheme);

    try {
        localStorage.setItem("theme", newTheme);
    } catch (e) {}

    updateIcon();
});

updateIcon();
