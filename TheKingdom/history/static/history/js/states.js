
"use strict";

/* ================================================
   تاريخ المملكة — تفاعلات الدولة السعودية الأولى
================================================ */

document.addEventListener("DOMContentLoaded", () => {

    const page = document.querySelector("#originsPage");
    if (!page) return;

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    /* ==========================================
       الأرقام العربية
    ========================================== */

    const arabicDigits = "٠١٢٣٤٥٦٧٨٩";

    function toArabic(value) {
        return String(value).replace(/[0-9]/g, digit => {
            return arabicDigits[Number(digit)];
        });
    }

    function formatNumber(value) {
        return toArabic(String(value).padStart(2, "0"));
    }

    function translateVisibleNumbers(root) {

        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT
        );

        const nodes = [];

        while (walker.nextNode()) {
            nodes.push(walker.currentNode);
        }

        nodes.forEach(node => {

            const parent = node.parentElement;
            if (!parent) return;

            if (["SCRIPT", "STYLE", "NOSCRIPT"].includes(
                parent.tagName
            )) {
                return;
            }

            node.nodeValue = toArabic(node.nodeValue);
        });
    }

    translateVisibleNumbers(page);

    /* ==========================================
       ظهور الأقسام أثناء التمرير
    ========================================== */

    const revealElements = page.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window && !reducedMotion) {

        const revealObserver = new IntersectionObserver(
            (entries, observer) => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) return;

                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                });
            },
            {
                threshold: 0.1,
                rootMargin: "0px 0px -25px 0px"
            }
        );

        revealElements.forEach(element => {
            revealObserver.observe(element);
        });

    } else {

        revealElements.forEach(element => {
            element.classList.add("is-visible");
        });
    }

    /* ==========================================
       شريط تقدم القراءة
    ========================================== */

    const progress = page.querySelector("#originsProgress");
    let scrollScheduled = false;

    function updateScrollProgress() {

        const maxScroll = Math.max(
            document.documentElement.scrollHeight -
            window.innerHeight,
            1
        );

        const percent = Math.min(
            Math.max(window.scrollY / maxScroll * 100, 0),
            100
        );

        if (progress) {
            progress.style.width = `${percent}%`;
        }

        scrollScheduled = false;
    }

    window.addEventListener("scroll", () => {

        if (scrollScheduled) return;

        scrollScheduled = true;

        requestAnimationFrame(updateScrollProgress);

    }, { passive: true });

    window.addEventListener(
        "resize",
        updateScrollProgress
    );

    updateScrollProgress();

    /* ==========================================
       الخط الزمني — البيانات من Django / JSON
    ========================================== */

    const timelineButtons = [
        ...page.querySelectorAll(".origins-time-btn")
    ];

    const timelineEvents = timelineButtons.map(button => ({
        year: button.dataset.year || "",
        title: button.dataset.title || "",
        description: button.dataset.description || "",
        image: button.dataset.image || "",
        alt: button.dataset.alt || ""
    }));

    const timelineYear = page.querySelector("#timelineYear");
    const timelineTitle = page.querySelector("#timelineTitle");
    const timelineDescription = page.querySelector(
        "#timelineDescription"
    );

    const timelineCounter = page.querySelector(
        "#timelineCounter"
    );

    const timelinePosition = page.querySelector(
        "#timelinePosition"
    );

    const timelinePrev = page.querySelector("#timelinePrev");
    const timelineNext = page.querySelector("#timelineNext");

    const timelineImage = page.querySelector("#timelineImage");
    const timelineStage = page.querySelector(
        ".origins-timeline-stage"
    );

    let currentTimelineIndex = 0;
    let imageRequestId = 0;

    function updateTimelineImage(src, alt) {

        if (!timelineImage || !src) return;

        // Avoid changing the image unnecessarily.
        if (timelineImage.getAttribute("src") === src) {
            timelineImage.alt = alt;
            return;
        }

        const requestId = ++imageRequestId;

        timelineImage.classList.add("is-changing");

        const preloadedImage = new Image();

        preloadedImage.onload = () => {

            // Ignore a stale image if the user has
            // already selected another event.
            if (requestId !== imageRequestId) return;

            timelineImage.src = src;
            timelineImage.alt = alt;

            requestAnimationFrame(() => {
                timelineImage.classList.remove("is-changing");
            });
        };

        preloadedImage.onerror = () => {

            if (requestId !== imageRequestId) return;

            timelineImage.classList.remove("is-changing");
        };

        preloadedImage.src = src;
    }

    function scrollTimelineSelector(activeButton) {

        if (!activeButton) return;

        const selector = activeButton.closest(
            ".origins-timeline-selector"
        );

        if (!selector) return;

        if (selector.scrollWidth <= selector.clientWidth) {
            return;
        }

        const selectorRect = selector.getBoundingClientRect();
        const buttonRect = activeButton.getBoundingClientRect();

        const distance =
            buttonRect.left +
            buttonRect.width / 2 -
            selectorRect.left -
            selectorRect.width / 2;

        selector.scrollBy({
            left: distance,
            behavior: reducedMotion ? "instant" : "smooth"
        });
    }

    function showTimelineEvent(
        index,
        userInteraction = false
    ) {

        if (
            !Number.isInteger(index) ||
            index < 0 ||
            index >= timelineEvents.length
        ) {
            return;
        }

        currentTimelineIndex = index;

        const event = timelineEvents[index];
        const total = timelineEvents.length;

        if (timelineYear) {
            timelineYear.textContent =
                `${toArabic(event.year)}م`;
        }

        if (timelineTitle) {
            timelineTitle.textContent = event.title;
        }

        if (timelineDescription) {
            timelineDescription.textContent =
                toArabic(event.description);
        }

        if (timelineCounter) {
            timelineCounter.textContent =
                `الحدث ${formatNumber(index + 1)} من ${formatNumber(total)}`;
        }

        if (timelinePosition) {
            timelinePosition.textContent =
                `${formatNumber(index + 1)} / ${formatNumber(total)}`;
        }

        updateTimelineImage(event.image, event.alt);

        // Brief transition for the event card.
        if (timelineStage && userInteraction) {

            timelineStage.classList.remove("is-updating");

            // Reflow so consecutive clicks restart the effect.
            void timelineStage.offsetWidth;

            timelineStage.classList.add("is-updating");
        }

        timelineButtons.forEach((button, buttonIndex) => {

            const active = buttonIndex === index;

            button.classList.toggle("is-active", active);

            button.setAttribute(
                "aria-pressed",
                String(active)
            );
        });

        if (timelinePrev) {
            timelinePrev.disabled = index === 0;
        }

        if (timelineNext) {
            timelineNext.disabled = index === total - 1;
        }

        // Do not scroll the entire page!
        // Only move the selector when a user interacts.
        if (userInteraction) {
            scrollTimelineSelector(timelineButtons[index]);
        }
    }

    timelineButtons.forEach(button => {

        button.addEventListener("click", () => {

            const index = Number(button.dataset.time);

            if (!Number.isInteger(index)) return;

            showTimelineEvent(index, true);
        });
    });

    if (timelinePrev) {

        timelinePrev.addEventListener("click", () => {
            showTimelineEvent(
                currentTimelineIndex - 1,
                true
            );
        });
    }

    if (timelineNext) {

        timelineNext.addEventListener("click", () => {
            showTimelineEvent(
                currentTimelineIndex + 1,
                true
            );
        });
    }

    // Keyboard arrows, only when a timeline
    // selector button has keyboard focus.
    timelineButtons.forEach(button => {

        button.addEventListener("keydown", event => {

            const current = Number(button.dataset.time);

            if (event.key === "ArrowLeft") {

                event.preventDefault();

                const next = Math.min(
                    current + 1,
                    timelineButtons.length - 1
                );

                showTimelineEvent(next, true);
                timelineButtons[next].focus();

            } else if (event.key === "ArrowRight") {

                event.preventDefault();

                const previous = Math.max(current - 1, 0);

                showTimelineEvent(previous, true);
                timelineButtons[previous].focus();
            }
        });
    });

    // First event, WITHOUT automatic page scrolling.
    if (timelineEvents.length > 0) {
        showTimelineEvent(0, false);
    }

    /* ==========================================
       فيديو الافتتاحية
    ========================================== */

    const heroVideo = page.querySelector("#originsHeroVideo");

    if (heroVideo) {

        heroVideo.muted = true;

        const smallScreenQuery = window.matchMedia(
            "(max-width: 768px)"
        );

        function playHeroVideo() {

            if (
                reducedMotion ||
                smallScreenQuery.matches ||
                document.hidden
            ) {
                return;
            }

            const playPromise = heroVideo.play();

            if (
                playPromise &&
                typeof playPromise.catch === "function"
            ) {
                playPromise.catch(() => {
                    // The background poster remains available.
                });
            }
        }

        function pauseHeroVideo() {
            heroVideo.pause();
        }

        if ("IntersectionObserver" in window) {

            const videoObserver = new IntersectionObserver(
                entries => {

                    entries.forEach(entry => {

                        if (entry.isIntersecting) {
                            playHeroVideo();
                        } else {
                            pauseHeroVideo();
                        }
                    });
                },
                { threshold: 0.15 }
            );

            videoObserver.observe(heroVideo);

        } else {

            playHeroVideo();
        }

        if (reducedMotion || smallScreenQuery.matches) {
            pauseHeroVideo();
        }

        smallScreenQuery.addEventListener("change", () => {

            if (smallScreenQuery.matches) {
                pauseHeroVideo();
            } else {
                const rect = heroVideo.getBoundingClientRect();

                if (
                    rect.bottom > 0 &&
                    rect.top < window.innerHeight
                ) {
                    playHeroVideo();
                }
            }
        });

        document.addEventListener("visibilitychange", () => {

            if (document.hidden) {

                pauseHeroVideo();

            } else {

                const rect = heroVideo.getBoundingClientRect();

                if (
                    rect.bottom > 0 &&
                    rect.top < window.innerHeight
                ) {
                    playHeroVideo();
                }
            }
        });
    }

    /* ==========================================
       عارض الصور والخريطة
    ========================================== */

    const mapOpen = page.querySelector("#originsMapOpen");
    const timelineImageOpen = page.querySelector(
        "#timelineImageOpen"
    );

    const lightbox = page.querySelector(
        "#originsMapLightbox"
    );

    const lightboxClose = page.querySelector(
        "#originsMapClose"
    );

    const lightboxImage = page.querySelector(
        "#originsLightboxImage"
    );

    const lightboxCaption = page.querySelector(
        "#originsLightboxCaption"
    );

    let previousFocus = null;

    function openLightbox(src, alt, caption) {

        if (!lightbox || !lightboxImage || !src) return;

        previousFocus = document.activeElement;

        lightboxImage.src = src;
        lightboxImage.alt = alt || "صورة تاريخية";

        if (lightboxCaption) {
            lightboxCaption.textContent = caption || "";
        }

        lightbox.hidden = false;

        lightbox.setAttribute("aria-hidden", "false");

        document.body.classList.add("origins-map-open");

        lightboxClose?.focus();
    }

    function closeLightbox() {

        if (!lightbox || lightbox.hidden) return;

        lightbox.hidden = true;

        lightbox.setAttribute("aria-hidden", "true");

        document.body.classList.remove("origins-map-open");

        if (
            previousFocus &&
            previousFocus.isConnected &&
            typeof previousFocus.focus === "function"
        ) {
            previousFocus.focus();
        }
    }

    if (mapOpen) {

        mapOpen.addEventListener("click", () => {

            const image = mapOpen.querySelector("img");

            if (!image) return;

            openLightbox(
                image.src,
                image.alt,
                "خريطة الامتداد التاريخي للدولة السعودية الأولى"
            );
        });
    }

    if (timelineImageOpen && timelineImage) {

        timelineImageOpen.addEventListener("click", () => {

            const event = timelineEvents[currentTimelineIndex];

            // Use the actual displayed image in case a
            // newer image is still loading.
            openLightbox(
                timelineImage.src,
                timelineImage.alt,
                event?.title || "مشهد من التاريخ"
            );
        });
    }

    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    if (lightbox) {

        lightbox.addEventListener("click", event => {

            if (event.target === lightbox) {
                closeLightbox();
            }
        });

        document.addEventListener("keydown", event => {

            if (lightbox.hidden) return;

            if (event.key === "Escape") {

                event.preventDefault();
                closeLightbox();

            } else if (event.key === "Tab") {

                // Only the close button receives focus.
                event.preventDefault();
                lightboxClose?.focus();
            }
        });
    }

});
