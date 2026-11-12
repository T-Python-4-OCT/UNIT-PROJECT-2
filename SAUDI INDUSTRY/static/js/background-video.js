
const backgroundVideos = document.querySelectorAll(
    "video[data-background-video]"
);

if (backgroundVideos.length > 0) {
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    function updateBackgroundVideos() {
        backgroundVideos.forEach((video) => {
            const source = video.querySelector(
                "source[data-src]"
            );

            if (!source) return;

            if (reducedMotion.matches) {
                video.pause();

                if (source.hasAttribute("src")) {
                    source.removeAttribute("src");
                    video.load();
                }

                return;
            }

            if (!source.hasAttribute("src")) {
                source.src = source.dataset.src;
                video.load();
            }

            if (video.paused) {
                video.play().catch(() => {
                    // Show the poster if playback fails.
                });
            }
        });
    }

    updateBackgroundVideos();

    reducedMotion.addEventListener(
        "change",
        updateBackgroundVideos
    );
}
