(function () {
    "use strict";

    const body = document.body;
    const button = document.getElementById("themeToggle");
    const icon = document.getElementById("themeIcon");
    const label = document.querySelector(".theme-label");
    const isEnglish = document.documentElement.lang === "en";

    function setCookie(name, value, days) {
        const maxAge = days * 24 * 60 * 60;
        let cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; max-age=${maxAge}; path=/; SameSite=Lax`;
        if (window.location.protocol === "https:") cookie += "; Secure";
        document.cookie = cookie;
    }

    function getCookie(name) {
        const prefix = encodeURIComponent(name) + "=";
        const entry = document.cookie.split(";").map(item => item.trim()).find(item => item.startsWith(prefix));
        return entry ? decodeURIComponent(entry.slice(prefix.length)) : null;
    }

    function applyTheme(theme) {
        const selectedTheme = theme === "dark" ? "dark" : "light";
        body.dataset.theme = selectedTheme;

        const dark = selectedTheme === "dark";
        if (icon) icon.textContent = dark ? "☀" : "☾";
        if (label) label.textContent = dark
            ? (isEnglish ? "Light mode" : "الوضع النهاري")
            : (isEnglish ? "Dark mode" : "الوضع الليلي");

        if (button) {
            button.setAttribute("aria-pressed", String(dark));
            button.setAttribute("aria-label", dark
                ? (isEnglish ? "Enable light mode" : "تفعيل الوضع النهاري")
                : (isEnglish ? "Enable dark mode" : "تفعيل الوضع الليلي"));
        }
    }

    let savedTheme = "light";
    try {
        savedTheme = getCookie("saudi-heritage-theme") || "light";
    } catch (error) {
        // The site remains usable if cookies are unavailable.
    }
    applyTheme(savedTheme);

    if (button) {
        button.addEventListener("click", function () {
            const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
            try {
                setCookie("saudi-heritage-theme", nextTheme, 365);
            } catch (error) {
                // The theme still changes for the current page.
            }
            applyTheme(nextTheme);
        });
    }

    // Homepage city search: filters the six city cards without a page reload.
    const searchInput = document.getElementById("citySearch");
    const cityCards = Array.from(document.querySelectorAll("[data-city-card]"));
    const visibleCount = document.getElementById("visibleCities");
    const emptyState = document.getElementById("emptyCities");

    function normalizeText(value) {
        return (value || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u064B-\u065F\u0670]/g, "")
            .replace(/[أإآ]/g, "ا")
            .replace(/ة/g, "ه")
            .trim();
    }

    if (searchInput && cityCards.length) {
        searchInput.addEventListener("input", function () {
            const query = normalizeText(searchInput.value);
            let visible = 0;

            cityCards.forEach(function (card) {
                const searchableText = normalizeText(
                    (card.dataset.cityName || "") + " " + (card.dataset.cityRegion || "")
                );
                const matches = searchableText.includes(query);
                card.hidden = !matches;
                if (matches) visible += 1;
            });

            if (visibleCount) visibleCount.textContent = String(visible);
            if (emptyState) emptyState.hidden = visible !== 0;
        });
    }

    // Graceful fallback if an external photograph is temporarily unavailable.
    document.querySelectorAll("img").forEach(function (image) {
        image.addEventListener("error", function () {
            image.classList.add("image-unavailable");
            image.removeAttribute("src");
            image.setAttribute("aria-label", image.getAttribute("alt") || (isEnglish ? "Image unavailable" : "صورة غير متاحة"));
        }, { once: true });
    });

    const year = document.getElementById("currentYear");
    if (year) year.textContent = String(new Date().getFullYear());
})();
