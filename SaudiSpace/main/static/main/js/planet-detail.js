document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll(
        ".planet-cinematic .pc-section, .planet-cinematic .pc-surface, .planet-cinematic .pc-orbit-section"
    );

    if (!("IntersectionObserver" in window)) {
        sections.forEach(section => {
            section.classList.add("pc-visible");
        });

        return;
    }

    const observer = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("pc-visible");

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.12
        }
    );

    sections.forEach(section => {
        section.classList.add("pc-reveal");
        observer.observe(section);
    });

});