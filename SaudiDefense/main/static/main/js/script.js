
const themeToggle = document.getElementById("theme-toggle");
const languageToggle = document.getElementById("language-toggle");

function setCookie(name, value) {
    document.cookie = `${name}=${value}; max-age=2592000; path=/; SameSite=Lax`;
}

function getCookie(name) {
    const cookies = document.cookie.split("; ");

    const cookie = cookies.find(item => item.startsWith(name + "="));

    return cookie ? cookie.split("=")[1] : null;
}

function applyTheme(theme) {
    document.body.classList.toggle("dark-mode", theme === "dark");
    document.body.classList.toggle("light-mode", theme === "light");

    themeToggle.textContent = theme === "dark" ? "☀" : "☾";
}

function applyLanguage(language) {
    const isArabic = language === "ar";

    document.documentElement.lang = language;
    document.documentElement.dir = isArabic ? "rtl" : "ltr";

    document.querySelectorAll("[data-ar][data-en]").forEach(element => {
        element.textContent = isArabic
            ? element.dataset.ar
            : element.dataset.en;
    });

    languageToggle.textContent = isArabic ? "EN" : "عربي";
}

applyTheme(getCookie("theme") || "dark");
applyLanguage(getCookie("language") || "ar");

themeToggle.addEventListener("click", () => {
    const nextTheme = document.body.classList.contains("dark-mode")
        ? "light"
        : "dark";

    setCookie("theme", nextTheme);
    applyTheme(nextTheme);
});

languageToggle.addEventListener("click", () => {
    const nextLanguage = document.documentElement.lang === "ar"
        ? "en"
        : "ar";

    setCookie("language", nextLanguage);
    applyLanguage(nextLanguage);
});



document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById("defense-video");

    if (video) {
        video.muted = true;

        video.addEventListener("timeupdate", function () {

            if (video.currentTime >= 10) {
                video.currentTime = 0;
                video.play();
            }

        });

        video.play().catch(function () {
            console.log("Video autoplay was blocked.");
        });
    }

});
