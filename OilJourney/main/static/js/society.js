function initSocietyPage() {

    const revealElements = document.querySelectorAll(".sc-reveal");

    if ("IntersectionObserver" in window) {

        try {

            const revealObserver = new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach((entry) => {

                        if (entry.isIntersecting) {

                            entry.target.classList.add("sc-visible");

                            observer.unobserve(entry.target);
                        }

                    });

                },
                {
                    threshold: 0.01,
                    rootMargin: "0px 0px 0px 0px"
                }
            );

            revealElements.forEach((element) => {

                element.classList.add("sc-reveal-pending");

                revealObserver.observe(element);

            });

        } catch (error) {

            revealElements.forEach((element) => {

                element.classList.remove("sc-reveal-pending");

                element.classList.add("sc-visible");

            });

        }

    } else {

        revealElements.forEach((element) => {

            element.classList.add("sc-visible");

        });

    }


    const internalLinks = document.querySelectorAll(
        '.society-page a[href^="#"]'
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

    document.addEventListener("DOMContentLoaded", initSocietyPage);

} else {

    initSocietyPage();

}
