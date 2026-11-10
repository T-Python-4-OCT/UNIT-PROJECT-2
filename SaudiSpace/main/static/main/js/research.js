
document.addEventListener("DOMContentLoaded", () => {

    // Reveal sections when they enter the screen
    const revealElements = document.querySelectorAll(".research-reveal");

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("research-visible");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15
    });

    revealElements.forEach(element => {
        revealObserver.observe(element);
    });


    // Animate statistics counters
    const counters = document.querySelectorAll(".research-stat strong");

    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const counter = entry.target;
            const target = Number(counter.dataset.count);
            const duration = 1800;
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const progress = Math.min((currentTime - startTime) / duration, 1);
                const easedProgress = 1 - Math.pow(1 - progress, 4);
                const currentValue = Math.floor(easedProgress * target);

                counter.textContent = currentValue.toLocaleString("en-US");

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target.toLocaleString("en-US");
                }
            }

            requestAnimationFrame(updateCounter);
            observer.unobserve(counter);
        });
    }, {
        threshold: 0.5
    });

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });

});
