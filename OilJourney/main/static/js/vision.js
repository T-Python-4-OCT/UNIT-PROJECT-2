function initVisionPage() {
    const revealElements = document.querySelectorAll(".vp-reveal");

    if ("IntersectionObserver" in window) {
        try {
            const revealObserver = new IntersectionObserver(
                (entries, observer) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add("vp-visible");
                            observer.unobserve(entry.target);
                        }
                    });
                },
                {
                    threshold: 0.15,
                    rootMargin: "0px 0px -30px 0px"
                }
            );

            revealElements.forEach((element) => {
                element.classList.add("vp-reveal-pending");
                revealObserver.observe(element);
            });

        } catch (error) {
            revealElements.forEach((element) => {
                element.classList.remove("vp-reveal-pending");
                element.classList.add("vp-visible");
            });
        }

    } else {
        revealElements.forEach((element) => {
            element.classList.add("vp-visible");
        });
    }



    const internalLinks = document.querySelectorAll(
        '.vision-page a[href^="#"]'
    );

    internalLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {
                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });
}


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initVisionPage);
} else {
    initVisionPage();
}
