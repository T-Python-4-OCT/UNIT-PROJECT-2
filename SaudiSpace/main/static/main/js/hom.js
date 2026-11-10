document.addEventListener("DOMContentLoaded", () => {

    const hero = document.querySelector(".saudi-hero");
    const video = document.querySelector(".saudi-hero-video");

    // Fade in hero text
    if (hero) {
        requestAnimationFrame(() => {
            hero.classList.add("hero-loaded");
        });
    }

    // Play background video
    if (video) {

        video.muted = true;

        video.play().catch(() => {});

        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                video.pause();
            } else {
                video.play().catch(() => {});
            }
        });

    }

});