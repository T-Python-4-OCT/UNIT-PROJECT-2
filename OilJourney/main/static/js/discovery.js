document.addEventListener("DOMContentLoaded", function () {

    const revealElements = document.querySelectorAll(
        ".discovery-section-heading, " +
        ".discovery-intro-content, " +
        ".discovery-concession, " +
        ".exploration-card, " +
        ".discovery-timeline-item, " +
        ".discovery-shipment, " +
        ".discovery-ending"
    );

    revealElements.forEach(function (element) {
        element.classList.add("dis-reveal");
    });

    if (!("IntersectionObserver" in window)) {
        revealElements.forEach(function (element) {
            element.classList.add("dis-visible");
        });
        return;
    }

    const observer = new IntersectionObserver(
        function (entries, observer) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.classList.add("dis-visible");

                    observer.unobserve(entry.target);
                }

            });

        },
        {
            threshold: 0.15
        }
    );

    revealElements.forEach(function (element) {
        observer.observe(element);
    });

});
