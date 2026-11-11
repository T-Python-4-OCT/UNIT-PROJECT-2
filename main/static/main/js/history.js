document.addEventListener('DOMContentLoaded', () => {
    const timeline = document.querySelector('.heritage-history-timeline');

    if (!timeline) return;

    const stops = timeline.querySelectorAll('.heritage-history-stop');

    const reducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    ).matches;

    if (reducedMotion || !('IntersectionObserver' in window)) {
        return;
    }

    document.documentElement.classList.add('history-motion');

    const observer = new IntersectionObserver((entries, activeObserver) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            entry.target.classList.add('is-visible');
            activeObserver.unobserve(entry.target);
        });
    }, {
        threshold: 0.01,
        rootMargin: '0px 0px -2% 0px'
    });

    stops.forEach((stop) => {
        const rect = stop.getBoundingClientRect();

        if (rect.top < window.innerHeight && rect.bottom > 0) {
            stop.classList.add('is-visible');
        } else {
            observer.observe(stop);
        }
    });

    let ticking = false;

    function updateTimeline() {
        const rect = timeline.getBoundingClientRect();
        const start = window.innerHeight * 0.55;

        const progress = Math.min(
            1,
            Math.max(0, (start - rect.top) / rect.height)
        );

        timeline.style.setProperty(
            '--timeline-progress',
            progress.toFixed(3)
        );

        ticking = false;
    }

    function onScroll() {
        if (ticking) return;

        ticking = true;
        window.requestAnimationFrame(updateTimeline);
    }

    window.addEventListener('scroll', onScroll, {
        passive: true
    });

    window.addEventListener('resize', onScroll);

    updateTimeline();
});
