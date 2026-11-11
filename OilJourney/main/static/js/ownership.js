if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(({ target, isIntersecting }) => {
            if (!isIntersecting) return;

            target.classList.add("ow-visible");
            obs.unobserve(target);
        });
    }, { threshold: 0.01 });

    document.querySelectorAll(".ow-reveal").forEach((element) => {
        element.classList.add("ow-reveal-pending");
        observer.observe(element);
    });
}

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

document.addEventListener("click", (event) => {
    const link = event.target.closest('.ownership-page a[href^="#"]');
    if (!link) return;

    const id = link.getAttribute("href").slice(1);
    const target = id && document.getElementById(id);
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({
        behavior: reducedMotion.matches ? "auto" : "smooth",
        block: "start"
    });
});