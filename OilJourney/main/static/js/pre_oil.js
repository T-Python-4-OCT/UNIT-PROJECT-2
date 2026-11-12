document.addEventListener("DOMContentLoaded", function () {

    const page = document.querySelector(".pre-oil-page");

    if (!page) return;

    const elements = page.querySelectorAll(
        ".pre-intro-content, " +
        ".pre-lifestyle-card, " +
        ".pre-timeline-item, " +
        ".pre-transition-content, " +
        ".pre-transition-image"
    );

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (reduceMotion || !("IntersectionObserver" in window)) {
        elements.forEach(function (element) {
            element.classList.add("is-visible");
        });

        return;
    }

    elements.forEach(function (element) {
        element.classList.add("pre-reveal");
    });

    const observer = new IntersectionObserver(
        function (entries, observer) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.classList.add("is-visible");

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.15
        }
    );

    elements.forEach(function (element) {
        observer.observe(element);
    });

});