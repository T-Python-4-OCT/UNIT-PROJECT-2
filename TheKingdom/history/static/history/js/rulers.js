
"use strict";

/* =====================================================
   THE KINGDOM — RULER BIOGRAPHIES
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const page = document.querySelector("#bioPage");

    if (!page) return;

    const progress = document.querySelector(
        "#bioProgress"
    );

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    const arabicDigits = "٠١٢٣٤٥٦٧٨٩";

    /* ==========================================
       ١. تعريب الأرقام
    ========================================== */

    function toArabicDigits(value) {
        return String(value).replace(
            /[0-9]/g,
            digit => arabicDigits[Number(digit)]
        );
    }

    document.querySelectorAll(".bio-digits").forEach(
        element => {
            element.textContent = toArabicDigits(
                element.textContent
            );
        }
    );

    /* ==========================================
       ٢. تأثير ظهور الأقسام
    ========================================== */

    const revealElements = [
        ...page.querySelectorAll(".bio-reveal")
    ];

    if (
        "IntersectionObserver" in window &&
        !reducedMotion.matches
    ) {

        // لا نخفي العناصر إلا بعد التأكد
        // من دعم المتصفح للتأثير.
        const observer = new IntersectionObserver(
            (entries, instance) => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) return;

                    entry.target.classList.add(
                        "is-visible"
                    );

                    instance.unobserve(entry.target);
                });

            },
            {
                threshold: 0.05,
                rootMargin: "0px 0px -20px 0px"
            }
        );

        revealElements.forEach(element => {
            observer.observe(element);
        });

        page.classList.add("bio-motion-ready");

    } else {

        revealElements.forEach(element => {
            element.classList.add("is-visible");
        });
    }

    /* ==========================================
       ٣. شريط تقدم القراءة
    ========================================== */

    let scrollScheduled = false;

    function updateReadingProgress() {

        const scrollable = Math.max(
            document.documentElement.scrollHeight -
                window.innerHeight,
            1
        );

        const percentage = Math.min(
            100,
            Math.max(
                0,
                (window.scrollY / scrollable) * 100
            )
        );

        if (progress) {
            progress.style.width = `${percentage}%`;
        }

        scrollScheduled = false;
    }

    window.addEventListener(
        "scroll",
        () => {

            if (scrollScheduled) return;

            scrollScheduled = true;

            window.requestAnimationFrame(
                updateReadingProgress
            );
        },
        { passive: true }
    );

    window.addEventListener(
        "resize",
        updateReadingProgress
    );

    updateReadingProgress();

    /* ==========================================
       ٤. تنقل سلس داخل السيرة
    ========================================== */

    page.querySelectorAll('a[href^="#"]').forEach(
        link => {

            link.addEventListener("click", event => {

                const targetId = link.getAttribute(
                    "href"
                );

                if (!targetId || targetId === "#") {
                    return;
                }

                const target = page.querySelector(
                    targetId
                );

                if (!target) return;

                event.preventDefault();

                target.scrollIntoView({
                    behavior: reducedMotion.matches
                        ? "auto"
                        : "smooth",
                    block: "start"
                });

                history.replaceState(
                    null,
                    "",
                    targetId
                );
            });
        }
    );

});
