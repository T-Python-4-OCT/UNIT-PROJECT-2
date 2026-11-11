
(() => {
    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    const homeVideo = document.getElementById("home-hero-video");

    if (homeVideo) {
        homeVideo.addEventListener("error", () => {
            homeVideo.hidden = true;
        }, true);

        if (prefersReducedMotion) {
            homeVideo.pause();
            homeVideo.hidden = true;
        }
    }

    if (typeof Swiper !== "undefined") {
        new Swiper(".crops-swiper", {
            slidesPerView: 1,
            spaceBetween: 24,
            loop: true,
            speed: 700,
            grabCursor: true,
            navigation: {
                nextEl: ".crop-next",
                prevEl: ".crop-prev"
            },
            breakpoints: {
                640: {
                    slidesPerView: 2
                },
                1024: {
                    slidesPerView: 3
                }
            }
        });
    }

    if (!prefersReducedMotion && typeof gsap !== "undefined") {
        gsap.from(".hero-reveal", {
            opacity: 0,
            y: 55,
            duration: 1,
            stagger: 0.18,
            ease: "power3.out"
        });

        if (typeof ScrollTrigger !== "undefined") {
            gsap.registerPlugin(ScrollTrigger);

            gsap.utils.toArray(".reveal-item").forEach((element) => {
                gsap.from(element, {
                    opacity: 0,
                    y: 65,
                    duration: 0.9,
                    ease: "power3.out",
                    scrollTrigger: {
                        trigger: element,
                        start: "top 92%",
                        once: true
                    }
                });
            });
        }
    }
})();
