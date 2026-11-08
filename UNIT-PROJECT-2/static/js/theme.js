const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeLabel = document.querySelector(".theme-label");

const languageToggle = document.getElementById("languageToggle");
const languageLabel = document.getElementById("languageLabel");

const bootstrapCSS = document.getElementById("bootstrap-css");

const translations = {
    ar: {
        brand: "حكاية وطن",
        home: "الرئيسية",
        cities: "المدن",
        history: "تاريخ المملكة",
        heritage: "التراث",
        stories: "قصص الأنبياء",
        about: "عن المشروع",
        darkMode: "الوضع الليلي",
        lightMode: "الوضع النهاري",
        footerDescription: "رحلة بين تاريخ المملكة وكنوزها الثقافية والإنسانية."
    },

    en: {
        brand: "Hikayat Watan",
        home: "Home",
        cities: "Cities",
        history: "Saudi History",
        heritage: "Heritage",
        stories: "Prophets' Stories",
        about: "About Project",
        darkMode: "Dark Mode",
        lightMode: "Light Mode",
        footerDescription: "A journey through Saudi Arabia's history and its cultural and human treasures."
    }
};

function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }

    return null;
}

function setCookie(name, value) {
    document.cookie =
        name + "=" + encodeURIComponent(value) +
        "; max-age=31536000; path=/; SameSite=Lax";
}

function updateThemeLabel() {
    const isDark = document.body.classList.contains("dark-mode");
    const language = getCookie("language") || "ar";

    themeIcon.textContent = isDark ? "☀" : "☾";

    themeLabel.textContent = isDark
        ? translations[language].lightMode
        : translations[language].darkMode;
}

function updateLanguage(language) {
    const isEnglish = language === "en";

    document.documentElement.lang = language;
    document.documentElement.dir = isEnglish ? "ltr" : "rtl";

    bootstrapCSS.href = isEnglish
        ? "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        : "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css";

    document.querySelectorAll("[data-i18n]").forEach(element => {
        const key = element.dataset.i18n;

        if (translations[language][key]) {
            element.textContent = translations[language][key];
        }
    });

    document.body.classList.toggle("english-font", isEnglish);

    languageLabel.textContent = isEnglish ? "ع" : "EN";

    setCookie("language", language);

    updateThemeLabel();
}

if (getCookie("theme") === "dark") {
    document.body.classList.add("dark-mode");
}

updateLanguage(getCookie("language") || "ar");

themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    const isDark = document.body.classList.contains("dark-mode");

    setCookie("theme", isDark ? "dark" : "light");

    updateThemeLabel();
});

languageToggle.addEventListener("click", () => {
    const currentLanguage = getCookie("language") || "ar";
    updateLanguage(currentLanguage === "ar" ? "en" : "ar");
});