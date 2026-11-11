
document.addEventListener("DOMContentLoaded", () => {

  // Smooth Hero Entrance
const hero = document.querySelector(".space-hero");

if (hero) {
    requestAnimationFrame(() => {
        hero.classList.add("space-page-ready");
    });
}
    // Background video
    const video = document.querySelector(".space-background-video");

    if (video) {
        video.muted = true;
        video.play().catch(() => {});
    }

    // Reveal mission sections
    const elements = document.querySelectorAll(`
        .mission-heading,
        .mission-content,
        .mission-gallery,
        .mission-video,
        .missions-footer
    `);

    elements.forEach(element => {
        element.classList.add("space-reveal");
    });

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("space-visible");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12
    });

    elements.forEach(element => observer.observe(element));

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener("click", event => {
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
