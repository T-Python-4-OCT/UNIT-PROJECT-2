document.addEventListener("DOMContentLoaded", () => {

    const video = document.querySelector(".home-hero-video");

    if (!video) return;

    video.muted = true;

    const playBackground = () => {
        if (!document.hidden) {
            video.play().catch(() => {});
        }
    };

    playBackground();

    document.addEventListener("visibilitychange", () => {

        if (document.hidden) {
            video.pause();
        } else {
            playBackground();
        }

    });

});