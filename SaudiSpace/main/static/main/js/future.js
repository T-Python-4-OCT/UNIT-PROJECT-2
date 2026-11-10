
document.addEventListener("DOMContentLoaded", () => {

    // Scroll reveal
    const revealElements = document.querySelectorAll(".future-reveal");

    const revealObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("future-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.12
        }
    );

    revealElements.forEach((element) => {
        revealObserver.observe(element);
    });


    // Background video
    const heroVideo = document.querySelector(".future-hero-video");

    if (heroVideo) {
        const reducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );

        if (reducedMotion.matches) {
            heroVideo.pause();
        }

        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                heroVideo.pause();
            } else if (!reducedMotion.matches) {
                heroVideo.play().catch(() => {});
            }
        });
    }


    // Smooth section navigation
    document.querySelectorAll('.future-page a[href^="#"]').forEach((link) => {
        link.addEventListener("click", (event) => {
            const target = document.querySelector(link.getAttribute("href"));

            if (target) {
                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });

});
