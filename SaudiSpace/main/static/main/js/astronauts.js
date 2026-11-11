
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

    // Reveal elements
    const elements = document.querySelectorAll(`
        .astronauts-heading,
        .astronaut-card,
        .astronauts-banner
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
        threshold: 0.15
    });

    elements.forEach(element => observer.observe(element));

    // Stagger astronaut cards
    document.querySelectorAll(".astronaut-card").forEach((card, index) => {
        card.style.transitionDelay = `${index * 150}ms`;
    });

});
