
"use strict";

/* =====================================================
   المملكة — الدولة السعودية الثالثة
   الخط الزمني + الفيديوهات السينمائية
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const page = document.querySelector("#unityPage");

    if (!page) return;

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    const arabicDigits = "٠١٢٣٤٥٦٧٨٩";

    let milestones = [];
    let currentIndex = 0;
    let changeTimer = null;
    let scrollScheduled = false;

    /* ==========================================
       ١. الأدوات المشتركة
    ========================================== */

    function arabic(value) {
        return String(value).replace(
            /[0-9]/g,
            digit => arabicDigits[Number(digit)]
        );
    }

    function formatNumber(value) {
        return arabic(String(value).padStart(2, "0"));
    }

    function createElement(
        tag,
        className = "",
        content = null
    ) {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        if (content !== null) {
            element.textContent = arabic(content);
        }

        return element;
    }

    function translateNumbers(root) {

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

            if (
                ["SCRIPT", "STYLE", "NOSCRIPT"].includes(
                    parent.tagName
                )
            ) {
                return;
            }

            node.nodeValue = arabic(node.nodeValue);
        });
    }

    translateNumbers(page);

    /* ==========================================
       ٢. إظهار العناصر عند التمرير
    ========================================== */

    const revealElements = page.querySelectorAll(
        ".unity-reveal"
    );

    if (
        "IntersectionObserver" in window &&
        !reducedMotion.matches
    ) {

        const revealObserver = new IntersectionObserver(
            (entries, observer) => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) return;

                    entry.target.classList.add("is-visible");

                    observer.unobserve(entry.target);
                });

            },
            {
                threshold: 0.06,
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
       ٣. شريط تقدم القراءة
    ========================================== */

    const progress = page.querySelector("#unityProgress");

    function updateProgress() {

        const total = Math.max(
            document.documentElement.scrollHeight -
                window.innerHeight,
            1
        );

        const percentage = Math.max(
            0,
            Math.min(
                100,
                window.scrollY / total * 100
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

            requestAnimationFrame(updateProgress);
        },
        { passive: true }
    );

    window.addEventListener("resize", updateProgress);

    updateProgress();

    /* ==========================================
       ٤. فيديو افتتاحية الدولة الثالثة
    ========================================== */

    const hero = page.querySelector(".unity-hero");

    const heroVideo = page.querySelector(
        "#unityHeroVideo"
    );

    let heroVisible = true;

    function safePlay(video) {

        if (!video || !video.paused) return;

        const result = video.play();

        if (result && typeof result.catch === "function") {
            result.catch(error => {
                console.debug(
                    "تعذر تشغيل الفيديو تلقائيًا:",
                    error
                );
            });
        }
    }

    function manageHeroPlayback() {

        if (!heroVideo) return;

        if (
            document.hidden ||
            reducedMotion.matches ||
            !heroVisible
        ) {
            heroVideo.pause();
            return;
        }

        heroVideo.muted = true;

        safePlay(heroVideo);
    }

    if (heroVideo) {

        heroVideo.muted = true;
        heroVideo.defaultMuted = true;

        // إظهار صورة البنر عند تعذر تحميل الفيديو.
        heroVideo.addEventListener("error", () => {
            heroVideo.classList.add("has-error");
        });

        if (
            hero &&
            "IntersectionObserver" in window
        ) {

            const heroObserver = new IntersectionObserver(
                entries => {

                    heroVisible = entries[0].isIntersecting;

                    manageHeroPlayback();

                },
                {
                    threshold: 0.08
                }
            );

            heroObserver.observe(hero);

        } else if (hero) {

            const checkHeroVisibility = () => {

                const rect = hero.getBoundingClientRect();

                heroVisible =
                    rect.bottom > 0 &&
                    rect.top < window.innerHeight;

                manageHeroPlayback();
            };

            window.addEventListener(
                "scroll",
                checkHeroVisibility,
                { passive: true }
            );

            checkHeroVisibility();
        }

        manageHeroPlayback();
    }

    /* ==========================================
       ٥. فيلم مسيرة المملكة (٥٩ ثانية)
    ========================================== */

    const legacyFilm = page.querySelector(
        "#unityLegacyFilm"
    );

    const legacyVideo = page.querySelector(
        "#unityLegacyVideo"
    );

    const legacyPlayButton = page.querySelector(
        "#unityLegacyPlay"
    );

    function updateLegacyButton() {

        if (!legacyFilm || !legacyVideo) return;

        const playing =
            !legacyVideo.paused &&
            !legacyVideo.ended;

        legacyFilm.classList.toggle(
            "is-playing",
            playing
        );

        if (legacyPlayButton) {

            legacyPlayButton.hidden = playing;

            legacyPlayButton.setAttribute(
                "aria-label",
                playing
                    ? "الفيديو قيد التشغيل"
                    : "تشغيل فيلم مسيرة المملكة"
            );
        }
    }

    if (legacyVideo) {

        // لا يبدأ هذا المقطع تلقائيًا.
        legacyVideo.autoplay = false;
        legacyVideo.loop = false;

        // يسمح للمشاهد بتشغيل الصوت.
        legacyVideo.muted = false;

        legacyVideo.addEventListener(
            "play",
            updateLegacyButton
        );

        legacyVideo.addEventListener(
            "pause",
            updateLegacyButton
        );

        legacyVideo.addEventListener(
            "ended",
            updateLegacyButton
        );

        legacyVideo.addEventListener(
            "error",
            () => {

                if (legacyPlayButton) {
                    legacyPlayButton.hidden = true;
                }

                console.error(
                    "تعذر تحميل فيديو مسيرة المملكة."
                );
            }
        );

        if (legacyPlayButton) {

            legacyPlayButton.addEventListener(
                "click",
                () => {

                    if (legacyVideo.paused) {

                        safePlay(legacyVideo);

                    } else {

                        legacyVideo.pause();
                    }
                }
            );
        }

        // إذا خرج المشاهد من قسم الفيديو
        // يتوقف التشغيل دون إعادة المقطع للبداية.
        if (
            legacyFilm &&
            "IntersectionObserver" in window
        ) {

            const legacyObserver =
                new IntersectionObserver(
                    entries => {

                        const visible =
                            entries[0].isIntersecting;

                        if (!visible) {
                            legacyVideo.pause();
                        }

                    },
                    {
                        threshold: 0.04
                    }
                );

            legacyObserver.observe(legacyFilm);
        }

        updateLegacyButton();
    }

    /* ==========================================
       ٦. التوقف عند إخفاء التبويب
    ========================================== */

    document.addEventListener(
        "visibilitychange",
        () => {

            if (document.hidden) {

                heroVideo?.pause();
                legacyVideo?.pause();

            } else {

                manageHeroPlayback();
            }
        }
    );

    if (typeof reducedMotion.addEventListener === "function") {

        reducedMotion.addEventListener(
            "change",
            manageHeroPlayback
        );
    }

    /* ==========================================
       ٧. عناصر مسيرة التوحيد
    ========================================== */

    const journeyNav = page.querySelector(
        "#unityJourneyNav"
    );

    const stage = page.querySelector(
        "#unityJourneyStage"
    );

    const stageImage = page.querySelector(
        "#unityJourneyImage"
    );

    const stageYear = page.querySelector(
        "#unityStageYear"
    );

    const stageTitle = page.querySelector(
        "#unityStageTitle"
    );

    const stageDescription = page.querySelector(
        "#unityStageDescription"
    );

    const stageLocation = page.querySelector(
        "#unityStageLocation"
    );

    const stageCategory = page.querySelector(
        "#unityStageCategory"
    );

    const stageWatermark = page.querySelector(
        "#unityJourneyWatermark"
    );

    const stageCounter = page.querySelector(
        "#unityStageCounter"
    );

    const stageDots = page.querySelector(
        "#unityStageDots"
    );

    const previousButton = page.querySelector(
        "#unityPrevious"
    );

    const nextButton = page.querySelector(
        "#unityNext"
    );

    const modernTrack = page.querySelector(
        "#unityModernTrack"
    );

    /* ==========================================
       ٨. معالجة مسارات الصور
    ========================================== */

    function resolveImage(path) {

        const fallback = page.dataset.heroImage || "";

        if (!path) return fallback;

        const staticRoot = page.dataset.staticRoot;

        if (!staticRoot) return fallback;

        let relativePath = String(path);

        if (relativePath.startsWith("history/")) {

            relativePath = relativePath.slice(
                "history/".length
            );
        }

        try {

            return new URL(
                relativePath,
                new URL(staticRoot, window.location.href)
            ).href;

        } catch (error) {

            console.error(
                "تعذر معالجة مسار الصورة:",
                path
            );

            return fallback;
        }
    }

    /* ==========================================
       ٩. قائمة المحطات
    ========================================== */

    function buildNavigation() {

        if (!journeyNav) return;

        const fragment = document.createDocumentFragment();

        milestones.forEach((event, index) => {

            const button = createElement(
                "button",
                "unity-journey-item"
            );

            button.type = "button";

            button.dataset.index = String(index);

            button.setAttribute(
                "aria-pressed",
                String(index === currentIndex)
            );

            const label = createElement(
                "span",
                "",
                event.label
            );

            const year = createElement(
                "strong",
                "",
                event.year
            );

            year.dir = "ltr";

            button.append(label, year);

            button.addEventListener(
                "click",
                () => selectMilestone(index)
            );

            button.addEventListener(
                "keydown",
                handleKeyboard
            );

            fragment.appendChild(button);
        });

        journeyNav.replaceChildren(fragment);
    }

    /* ==========================================
       ١٠. نقاط تقدم المحطات
    ========================================== */

    function buildDots() {

        if (!stageDots) return;

        const fragment = document.createDocumentFragment();

        milestones.forEach((_, index) => {

            const dot = createElement(
                "span",
                index === 0 ? "is-active" : ""
            );

            fragment.appendChild(dot);
        });

        stageDots.replaceChildren(fragment);
    }

    /* ==========================================
       ١١. عرض المحطة المختارة
    ========================================== */

    function renderMilestone(index) {

        const event = milestones[index];

        if (!event) return;

        currentIndex = index;

        if (stageYear) {
            stageYear.textContent = arabic(event.year);
        }

        if (stageWatermark) {
            stageWatermark.textContent = arabic(
                event.year
            );
        }

        if (stageTitle) {
            stageTitle.textContent = event.title;
        }

        if (stageDescription) {
            stageDescription.textContent = arabic(
                event.description
            );
        }

        if (stageLocation) {
            stageLocation.textContent = event.location;
        }

        if (stageCategory) {
            stageCategory.textContent = event.label;
        }

        if (stageCounter) {

            stageCounter.textContent =
                `${formatNumber(index + 1)} / ${formatNumber(milestones.length)}`;
        }

        if (stageImage) {

            const imageURL = resolveImage(
                event.image
            );

            stageImage.style.backgroundImage =
                `url(${JSON.stringify(imageURL)})`;
        }

        if (journeyNav) {

            const buttons = journeyNav.querySelectorAll(
                ".unity-journey-item"
            );

            buttons.forEach((button, buttonIndex) => {

                const active = buttonIndex === index;

                button.classList.toggle(
                    "is-active",
                    active
                );

                button.setAttribute(
                    "aria-pressed",
                    String(active)
                );
            });
        }

        if (stageDots) {

            const dots = stageDots.querySelectorAll(
                "span"
            );

            dots.forEach((dot, dotIndex) => {

                dot.classList.toggle(
                    "is-active",
                    dotIndex === index
                );
            });
        }

        if (previousButton) {
            previousButton.disabled = index === 0;
        }

        if (nextButton) {

            nextButton.disabled =
                index === milestones.length - 1;
        }
    }

    /* ==========================================
       ١٢. التنقل بين المحطات
    ========================================== */

    function selectMilestone(index) {

        if (
            !Number.isInteger(index) ||
            index < 0 ||
            index >= milestones.length
        ) {
            return;
        }

        if (changeTimer !== null) {

            window.clearTimeout(changeTimer);

            changeTimer = null;
        }

        if (!stage || reducedMotion.matches) {

            stage?.classList.remove(
                "is-switching"
            );

            renderMilestone(index);

            return;
        }

        stage.classList.add("is-switching");

        changeTimer = window.setTimeout(
            () => {

                renderMilestone(index);

                stage.classList.remove(
                    "is-switching"
                );

                changeTimer = null;

            },
            170
        );
    }

    /* ==========================================
       ١٣. لوحة المفاتيح
    ========================================== */

    function handleKeyboard(event) {

        const validKeys = [
            "ArrowDown",
            "ArrowUp",
            "ArrowLeft",
            "ArrowRight"
        ];

        if (!validKeys.includes(event.key)) return;

        if (!journeyNav) return;

        const buttons = [
            ...journeyNav.querySelectorAll(
                ".unity-journey-item"
            )
        ];

        const index = buttons.indexOf(
            event.currentTarget
        );

        if (index === -1) return;

        const forward =
            event.key === "ArrowDown" ||
            event.key === "ArrowLeft";

        const target = Math.max(
            0,
            Math.min(
                milestones.length - 1,
                index + (forward ? 1 : -1)
            )
        );

        event.preventDefault();

        selectMilestone(target);

        buttons[target]?.focus({
            preventScroll: true
        });
    }

    /* ==========================================
       ١٤. أزرار السابق والتالي
    ========================================== */

    previousButton?.addEventListener(
        "click",
        () => {
            selectMilestone(currentIndex - 1);
        }
    );

    nextButton?.addEventListener(
        "click",
        () => {
            selectMilestone(currentIndex + 1);
        }
    );

    /* ==========================================
       ١٥. محطات المملكة الحديثة
    ========================================== */

    function buildModernTimeline(events) {

        if (!modernTrack) return;

        const fragment = document.createDocumentFragment();

        events.forEach(event => {

            const card = createElement(
                "article",
                "unity-modern-card"
            );

            const year = createElement(
                "span",
                "unity-modern-card-year",
                event.year
            );

            year.dir = "ltr";

            const title = createElement(
                "h3",
                "",
                event.title
            );

            const description = createElement(
                "p",
                "",
                event.description
            );

            card.append(
                year,
                title,
                description
            );

            fragment.appendChild(card);
        });

        modernTrack.replaceChildren(fragment);
    }

    /* ==========================================
       ١٦. معالجة أخطاء البيانات
    ========================================== */

    function showLoadingError(message) {

        console.error(
            "تعذر تحميل بيانات الدولة الثالثة:",
            message
        );

        if (journeyNav) {

            journeyNav.replaceChildren(
                createElement(
                    "p",
                    "unity-loading",
                    "تعذر تحميل المحطات التاريخية. تحقق من بيانات الصفحة."
                )
            );
        }

        if (modernTrack) {

            modernTrack.replaceChildren(
                createElement(
                    "p",
                    "unity-loading",
                    "تعذر تحميل محطات المملكة الحديثة."
                )
            );
        }

        if (previousButton) {
            previousButton.disabled = true;
        }

        if (nextButton) {
            nextButton.disabled = true;
        }
    }

    /* ==========================================
       ١٧. قراءة البيانات من Django
    ========================================== */

    function initializeTimeline() {

        try {

            const dataElement =
                document.getElementById(
                    "thirdEventsData"
                );

            if (!dataElement) {

                throw new Error(
                    "عنصر بيانات thirdEventsData غير موجود."
                );
            }

            const data = JSON.parse(
                dataElement.textContent
            );

            if (
                !Array.isArray(data.milestones) ||
                data.milestones.length === 0
            ) {

                throw new Error(
                    "بيانات المحطات التاريخية غير صالحة."
                );
            }

            milestones = data.milestones;

            currentIndex = 0;

            buildNavigation();
            buildDots();
            renderMilestone(0);

            if (Array.isArray(data.modern)) {

                buildModernTimeline(data.modern);

            } else if (modernTrack) {

                modernTrack.replaceChildren();
            }

            updateProgress();

        } catch (error) {

            showLoadingError(error.message);
        }
    }

    /* ==========================================
       ١٨. التشغيل
    ========================================== */

    initializeTimeline();

});
