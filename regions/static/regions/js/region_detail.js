
(() => {
    const intro = document.getElementById("region-intro");
    const skipButton = document.getElementById("skip-region-intro");
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    function closeIntro() {
        if (!intro || !intro.isConnected) return;

        if (typeof gsap === "undefined" || reducedMotion) {
            intro.remove();
            return;
        }

        gsap.to(intro, {
            opacity: 0,
            duration: 0.7,
            ease: "power2.inOut",
            onComplete: () => intro.remove()
        });
    }

    if (intro) {
        if (reducedMotion || typeof gsap === "undefined") {
            intro.remove();
        } else {
            const introTimeline = gsap.timeline({
                onComplete: closeIntro
            });

            introTimeline
                .from("#intro-background", {
                    scale: 1.16,
                    duration: 4,
                    ease: "power2.out"
                }, 0)
                .from(".intro-eyebrow", {
                    opacity: 0,
                    y: 25,
                    duration: 0.5
                }, 0.15)
                .from(".intro-title", {
                    opacity: 0,
                    y: 65,
                    scale: 0.92,
                    duration: 0.9,
                    ease: "power3.out"
                }, 0.4)
                .from(".intro-line", {
                    scaleX: 0,
                    duration: 0.5,
                    ease: "power2.out"
                }, 1)
                .from(".intro-subtitle", {
                    opacity: 0,
                    y: 30,
                    duration: 0.7
                }, 1.15)
                .from(".intro-description", {
                    opacity: 0,
                    y: 20,
                    duration: 0.7
                }, 1.6)
                .to({}, {
                    duration: 1.1
                });

            if (skipButton) {
                skipButton.addEventListener("click", () => {
                    introTimeline.kill();
                    closeIntro();
                });
            }
        }
    }

    const gallery = document.querySelector(".region-gallery");

    if (gallery && typeof Swiper !== "undefined") {
        const autoplayDelay = Number(
            gallery.dataset.autoplayDelay
        ) || 4000;

        new Swiper(gallery, {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            speed: 800,
            autoplay: reducedMotion ? false : {
                delay: autoplayDelay,
                disableOnInteraction: false,
                pauseOnMouseEnter: true
            },
            pagination: {
                el: ".region-gallery .swiper-pagination",
                clickable: true
            },
            keyboard: {
                enabled: true
            },
            grabCursor: true
        });
    }
})();
