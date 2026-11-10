function initAramcoPage() {

    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;


    const revealElements = document.querySelectorAll(".ar-reveal");

    const showAll = () => {
        revealElements.forEach((element) => {
            element.classList.remove("ar-reveal-pending");
            element.classList.add("ar-visible");
        });
    };

    if (!("IntersectionObserver" in window) || prefersReducedMotion) {

        showAll();

    } else {

        try {

            const revealObserver = new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach((entry) => {

                        if (!entry.isIntersecting) {
                            return;
                        }

                        entry.target.classList.add("ar-visible");
                        observer.unobserve(entry.target);

                    });

                },
                {
                    threshold: 0.01,
                    rootMargin: "0px"
                }
            );

            revealElements.forEach((element) => {

                element.classList.add("ar-reveal-pending");
                revealObserver.observe(element);

            });

        } catch (error) {

            showAll();

        }

    }


    const internalLinks = document.querySelectorAll(
        '.aramco-page a[href^="#"]'
    );

    internalLinks.forEach((link) => {

        link.addEventListener("click", (event) => {

            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (!target) {
                return;
            }

            event.preventDefault();

            target.scrollIntoView({
                behavior: prefersReducedMotion ? "auto" : "smooth",
                block: "start"
            });

            history.pushState(null, "", targetId);

            if (!target.hasAttribute("tabindex")) {
                target.setAttribute("tabindex", "-1");
            }

            target.focus({ preventScroll: true });

        });

    });

}


if (document.readyState === "loading") {

    document.addEventListener("DOMContentLoaded", initAramcoPage);

} else {

    initAramcoPage();

}