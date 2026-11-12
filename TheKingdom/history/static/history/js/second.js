
"use strict";

/* =================================================
   THE KINGDOM — SECOND SAUDI STATE
   Realistic historical flipbook using StPageFlip
================================================= */

document.addEventListener("DOMContentLoaded", async () => {

    const page = document.querySelector("#revivalPage");
    if (!page) return;

    const viewer = page.querySelector("#revivalDocumentViewer");

    const archiveButtons = [
        ...page.querySelectorAll(".revival-archive-item")
    ];

    if (!viewer || archiveButtons.length === 0) return;

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    const arabicDigits = "٠١٢٣٤٥٦٧٨٩";

    function toArabic(value) {
        return String(value).replace(/[0-9]/g, digit =>
            arabicDigits[Number(digit)]
        );
    }

    function formatNumber(value) {
        return toArabic(String(value).padStart(2, "0"));
    }

    /* ==========================================
       ١. تحميل بيانات الوثائق من Django
    ========================================== */

    const documents = archiveButtons.map(button => ({
        year: button.dataset.year || "",
        label: button.dataset.label || "",
        title: button.dataset.title || "",
        description: button.dataset.description || "",
        image: button.dataset.image || "",
        alt: button.dataset.alt || "",
        imageNote: button.dataset.imageNote || ""
    }));

    // الختم الأصلي الموجود في second.html.
    const emblemImage = viewer.querySelector(
        ".revival-paper-seal img"
    );

    const emblemSrc = emblemImage?.getAttribute("src") || "";

    /* ==========================================
       ٢. تحميل CSS والمكتبة الجاهزة
    ========================================== */

    const script = document.querySelector(
        'script[src*="second.js"]'
    );

    if (script) {
        const cssURL = new URL(
            "../css/second-book.css",
            script.src
        ).href;

        if (!document.querySelector(
            'link[data-revival-book-style]'
        )) {
            const link = document.createElement("link");

            link.rel = "stylesheet";
            link.href = cssURL;
            link.dataset.revivalBookStyle = "true";

            document.head.appendChild(link);
        }
    }

    function loadPageFlipLibrary() {
        return new Promise((resolve, reject) => {

            if (window.St?.PageFlip) {
                resolve(window.St.PageFlip);
                return;
            }

            const externalScript = document.createElement("script");

            externalScript.src =
                "https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.min.js";

            externalScript.onload = () => {
                if (window.St?.PageFlip) {
                    resolve(window.St.PageFlip);
                } else {
                    reject(new Error(
                        "مكتبة تقليب الصفحات لم تُحمّل بشكل صحيح."
                    ));
                }
            };

            externalScript.onerror = () => {
                reject(new Error(
                    "تعذر تحميل مكتبة تقليب الصفحات."
                ));
            };

            document.head.appendChild(externalScript);
        });
    }

    /* ==========================================
       ٣. إنشاء عناصر HTML بأمان
    ========================================== */

    function element(tag, className = "", value = null) {
        const node = document.createElement(tag);

        if (className) node.className = className;

        if (value !== null) {
            node.textContent = toArabic(value);
        }

        return node;
    }

    function appendText(parent, tag, className, value) {
        const node = element(tag, className, value);
        parent.appendChild(node);
        return node;
    }

    function createSeal() {
        if (!emblemSrc) return null;

        const seal = element("div", "rb-document-seal");
        seal.setAttribute("aria-hidden", "true");

        const image = document.createElement("img");
        image.src = emblemSrc;
        image.alt = "";

        seal.appendChild(image);
        return seal;
    }

    /* ==========================================
       ٤. ورقة الوثيقة اليمنى
    ========================================== */

    function createDocumentPage(data, index) {

        const sheet = element("div", "rb-flip-page");
        const paper = element("article", "rb-paper-content");

        const header = element("div", "rb-document-header");

        appendText(
            header,
            "span",
            "",
            "وثيقة تاريخية"
        );

        appendText(
            header,
            "span",
            "",
            `${data.year}م`
        );

        paper.appendChild(header);

        const seal = createSeal();
        if (seal) paper.appendChild(seal);

        appendText(
            paper,
            "span",
            "rb-document-category",
            data.label
        );

        appendText(
            paper,
            "h3",
            "rb-document-title",
            data.title
        );

        paper.appendChild(
            element("div", "rb-document-rule")
        );

        appendText(
            paper,
            "p",
            "rb-document-description",
            data.description
        );

        const footer = element("div", "rb-document-footer");

        appendText(
            footer,
            "span",
            "",
            "الدولة السعودية الثانية"
        );

        appendText(
            footer,
            "span",
            "",
            formatNumber(index + 1)
        );

        paper.appendChild(footer);
        sheet.appendChild(paper);

        return sheet;
    }

    /* ==========================================
       ٥. صفحة المشهد الأيسر
       لكل حدث صفحتان متقابلتان
    ========================================== */

    function createVisualPage(data, index) {

        const sheet = element(
            "div",
            "rb-flip-page rb-visual-page"
        );

        const paper = element(
            "article",
            "rb-paper-content rb-visual-content"
        );

        const header = element("div", "rb-document-header");

        appendText(
            header,
            "span",
            "",
            "من السجل التاريخي"
        );

        appendText(
            header,
            "span",
            "",
            formatNumber(index + 1)
        );

        paper.appendChild(header);

        const seal = createSeal();
        if (seal) paper.appendChild(seal);

        appendText(
            paper,
            "span",
            "rb-visual-kicker",
            "الدولة السعودية الثانية"
        );

        if (data.image) {

            const figure = element("figure", "rb-visual-image");

            const image = document.createElement("img");

            image.src = data.image;
            image.alt = data.alt || "صورة تاريخية توضيحية";
            image.loading = "lazy";

            figure.appendChild(image);

            if (data.imageNote) {

                appendText(
                    figure,
                    "figcaption",
                    "",
                    data.imageNote
                );
            }

            paper.appendChild(figure);

        } else {

            const ornament = element(
                "div",
                "rb-visual-year",
                data.year
            );

            ornament.setAttribute(
                "aria-hidden",
                "true"
            );

            paper.appendChild(ornament);
        }

        appendText(
            paper,
            "h3",
            "rb-visual-title",
            data.label
        );

        appendText(
            paper,
            "p",
            "rb-visual-description",
            `محطة من تاريخ الدولة السعودية الثانية عام ${data.year}م.`
        );

        const footer = element("div", "rb-document-footer");

        appendText(
            footer,
            "span",
            "",
            "الأرشيف التاريخي"
        );

        appendText(
            footer,
            "span",
            "",
            `${data.year}م`
        );

        paper.appendChild(footer);
        sheet.appendChild(paper);

        return sheet;
    }

    /* ==========================================
       ٦. واجهة الكتاب
    ========================================== */

    const book = element("div", "rb-book");
    book.dir = "rtl";

    const heading = element("div", "rb-book-heading");

    appendText(
        heading,
        "span",
        "",
        "سجل الوثائق التاريخية"
    );

    appendText(
        heading,
        "span",
        "",
        "الدولة السعودية الثانية"
    );

    book.appendChild(heading);

    const stage = element("div", "rb-flip-stage");

    // اتجاه الحاوية LTR لأن المكتبة ترتب الصفحات
    // وفق تسلسلها الهندسي، بينما كل صفحة RTL.
    stage.dir = "ltr";

    const bookRoot = element("div", "rb-flip-root");

    stage.appendChild(bookRoot);
    book.appendChild(stage);

    const toolbar = element("div", "rb-book-toolbar");

    const previousButton = element(
        "button",
        "rb-book-control"
    );

    previousButton.type = "button";
    previousButton.textContent = "السابقة";

    const counter = element(
        "span",
        "rb-book-counter",
        `٠١ / ${formatNumber(documents.length)}`
    );

    counter.dir = "ltr";
    counter.setAttribute("aria-live", "polite");

    const nextButton = element(
        "button",
        "rb-book-control"
    );

    nextButton.type = "button";
    nextButton.textContent = "التالية";

    toolbar.append(
        previousButton,
        counter,
        nextButton
    );

    book.appendChild(toolbar);

    const hint = element(
        "p",
        "rb-book-hint",
        "اقلب الصفحات بالسحب أو اختر وثيقة من القائمة."
    );

    book.appendChild(hint);

    // صفحتان لكل حدث.
    // المكتبة تضع الأولى يسارًا والثانية يمينًا.
    // محتوى الصفحات نفسه يبقى عربيًا من اليمين.
    const pages = [];

    documents.forEach((data, index) => {

        pages.push(createVisualPage(data, index));
        pages.push(createDocumentPage(data, index));

    });

    bookRoot.append(...pages);

    /* ==========================================
       ٧. تهيئة مكتبة StPageFlip
    ========================================== */

    let PageFlipClass;

    try {
        PageFlipClass = await loadPageFlipLibrary();
    } catch (error) {

        console.error(error);

        // لا نخفي عارض الوثائق القديم
        // إذا فشل تحميل المكتبة.
        const warning = element(
            "p",
            "rb-library-warning",
            "تعذر تحميل الكتاب التفاعلي. تحقق من اتصال الإنترنت."
        );

        viewer.prepend(warning);
        return;
    }

    viewer.appendChild(book);

    let pageFlip;

    try {

        pageFlip = new PageFlipClass(bookRoot, {
            width: 360,
            height: 520,

            size: "stretch",

            minWidth: 230,
            maxWidth: 480,

            minHeight: 332,
            maxHeight: 693,

            drawShadow: true,
            maxShadowOpacity: 0.55,

            flippingTime: 600,

            usePortrait: true,
            showCover: false,

            autoSize: true,
            mobileScrollSupport: false
        });

        pageFlip.loadFromHTML(pages);

    } catch (error) {

        console.error(error);
        book.remove();
        return;
    }

    // نخفي الورقة القديمة بعد نجاح التهيئة.
    viewer.classList.add("revival-book-ready");

    /* ==========================================
       ٨. التحكم بالتنقل
    ========================================== */

    let desiredDocumentIndex = 0;
    let sequenceRunning = false;

    let currentDocumentIndex = 0;

    function getCurrentDocumentIndex() {
        return Math.min(
            Math.floor(pageFlip.getCurrentPageIndex() / 2),
            documents.length - 1
        );
    }

    function updateNavigation() {

        currentDocumentIndex = getCurrentDocumentIndex();

        counter.textContent =
            `${formatNumber(currentDocumentIndex + 1)} / ${formatNumber(documents.length)}`;

        archiveButtons.forEach((button, index) => {

            const active = index === currentDocumentIndex;

            button.classList.toggle("is-active", active);

            button.setAttribute(
                "aria-pressed",
                String(active)
            );
        });

        previousButton.disabled =
            currentDocumentIndex === 0;

        nextButton.disabled =
            currentDocumentIndex === documents.length - 1;
    }

    pageFlip.on("flip", updateNavigation);

    function sleep(milliseconds) {
        return new Promise(resolve =>
            setTimeout(resolve, milliseconds)
        );
    }

    /* ==========================================
       ٩. تقليب متسلسل
       مثال: ١ إلى ٤ = ٣ مراحل
    ========================================== */

    async function runSequence() {

        if (sequenceRunning) return;

        sequenceRunning = true;

        try {

            while (
                getCurrentDocumentIndex() !== desiredDocumentIndex
            ) {

                const currentPage =
                    pageFlip.getCurrentPageIndex();

                const targetPage =
                    desiredDocumentIndex * 2;

                if (reducedMotion.matches) {

                    pageFlip.turnToPage(targetPage);
                    updateNavigation();
                    break;
                }

                if (targetPage > currentPage) {
                    pageFlip.flipNext();
                } else {
                    pageFlip.flipPrev();
                }

                // نترك لكل ورقة فرصة إكمال الحركة
                // قبل إصدار أمر التقليب التالي.
                await sleep(750);

                updateNavigation();
            }

        } finally {

            sequenceRunning = false;

            hint.textContent =
                "اقلب الصفحات بالسحب أو اختر وثيقة من القائمة.";
        }
    }

    function goToDocument(index) {

        if (
            !Number.isInteger(index) ||
            index < 0 ||
            index >= documents.length
        ) {
            return;
        }

        desiredDocumentIndex = index;

        hint.textContent =
            "جارٍ تقليب صفحات الأرشيف...";

        runSequence();
    }

    /* ==========================================
       ١٠. الأحداث
    ========================================== */

    archiveButtons.forEach(button => {

        button.addEventListener("click", () => {

            goToDocument(
                Number(button.dataset.index)
            );
        });

        button.addEventListener("keydown", event => {

            if (
                event.key !== "ArrowUp" &&
                event.key !== "ArrowDown"
            ) {
                return;
            }

            event.preventDefault();

            const index = Number(button.dataset.index);

            const nextIndex = event.key === "ArrowDown"
                ? Math.min(index + 1, documents.length - 1)
                : Math.max(index - 1, 0);

            archiveButtons[nextIndex].focus();

            goToDocument(nextIndex);
        });
    });

    previousButton.addEventListener("click", () => {
        goToDocument(
            Math.max(0, desiredDocumentIndex - 1)
        );
    });

    nextButton.addEventListener("click", () => {
        goToDocument(
            Math.min(
                documents.length - 1,
                desiredDocumentIndex + 1
            )
        );
    });

    pageFlip.on("changeState", event => {

        // يعيد مزامنة القائمة عند التقليب اليدوي.
        if (event.data === "read") {

            updateNavigation();

            if (!sequenceRunning) {
                desiredDocumentIndex =
                    getCurrentDocumentIndex();
            }
        }
    });

    updateNavigation();

    /* ==========================================
       ١١. ظهور الأقسام أثناء التمرير
    ========================================== */

    const revealElements = page.querySelectorAll(
        ".revival-reveal"
    );

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (!entry.isIntersecting) return;

            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
        });

    }, { threshold: 0.08 });

    revealElements.forEach(item => {

        if (reducedMotion.matches) {
            item.classList.add("is-visible");
        } else {
            observer.observe(item);
        }
    });

    /* ==========================================
       ١٢. تقدم القراءة
    ========================================== */

    const progress = page.querySelector("#revivalProgress");

    function updateProgress() {

        if (!progress) return;

        const scrollHeight = Math.max(
            document.documentElement.scrollHeight -
            window.innerHeight,
            1
        );

        progress.style.width =
            `${Math.min(100, window.scrollY / scrollHeight * 100)}%`;
    }

    window.addEventListener(
        "scroll",
        updateProgress,
        { passive: true }
    );

    updateProgress();

});
