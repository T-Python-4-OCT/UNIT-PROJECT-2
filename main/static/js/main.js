const progress = document.getElementById("scrollProgress");
const backToTop = document.getElementById("backToTop");

window.addEventListener("scroll", () => {
    const scrolled = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (progress && height > 0) {
        progress.style.width = (scrolled / height) * 100 + "%";
    }
    if (backToTop) {
        backToTop.classList.toggle("show", scrolled > 400);
    }
});

if (backToTop) {
    backToTop.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0, rootMargin: "0px 0px -40px 0px" });
document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

function animateCounter(el) {
    const target = Number(el.dataset.target);
    const duration = 1800;
    const start = performance.now();

    function update(now) {
        const progress = Math.min((now - start) / duration, 1);
        el.textContent = Math.floor(progress * target).toLocaleString("en-US");
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            el.textContent = target.toLocaleString("en-US");
        }
    }
    requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.6 });

document.querySelectorAll(".stat-num").forEach((el) => counterObserver.observe(el));

const copyBtn = document.getElementById("copyLink");

if (copyBtn) {
    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
            const label = copyBtn.querySelector("span");
            label.textContent = "تم النسخ ✓";
            setTimeout(() => {
                label.textContent = "نسخ الرابط";
            }, 2000);
        });
    });
}