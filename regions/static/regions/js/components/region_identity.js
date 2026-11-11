
(() => {
    const page = document.getElementById("region-page");

    if (!page) return;

    const fallbackSlug = window.location.pathname
        .split("/")
        .filter(Boolean)
        .pop();

    const slug = page.dataset.regionSlug || fallbackSlug;

    const patterns = {
        "al-ahsa": {
            name: "الأحساء",
            shape: `
                <path d="M90 25 V160" />
                <path d="M90 50 Q45 12 23 55" />
                <path d="M90 70 Q40 36 18 80" />
                <path d="M90 95 Q43 65 23 110" />
                <path d="M90 120 Q50 92 35 140" />
                <path d="M90 50 Q135 12 157 55" />
                <path d="M90 70 Q140 36 162 80" />
                <path d="M90 95 Q137 65 157 110" />
                <path d="M90 120 Q130 92 145 140" />
                <path d="M90 25 Q72 9 90 1 Q108 9 90 25" />
                <circle cx="90" cy="163" r="4" fill="currentColor" stroke="none"/>
            `
        },

        "taif": {
            name: "الطائف",
            shape: `
                <g transform="translate(90 90)">
                    <ellipse cx="0" cy="-29" rx="20" ry="34"/>
                    <ellipse cx="0" cy="-29" rx="20" ry="34" transform="rotate(72)"/>
                    <ellipse cx="0" cy="-29" rx="20" ry="34" transform="rotate(144)"/>
                    <ellipse cx="0" cy="-29" rx="20" ry="34" transform="rotate(216)"/>
                    <ellipse cx="0" cy="-29" rx="20" ry="34" transform="rotate(288)"/>
                    <circle cx="0" cy="0" r="16"/>
                    <circle cx="0" cy="0" r="6" fill="currentColor" stroke="none"/>
                    <circle cx="0" cy="-75" r="3" fill="currentColor" stroke="none"/>
                    <circle cx="71" cy="-23" r="3" fill="currentColor" stroke="none"/>
                    <circle cx="44" cy="60" r="3" fill="currentColor" stroke="none"/>
                    <circle cx="-44" cy="60" r="3" fill="currentColor" stroke="none"/>
                    <circle cx="-71" cy="-23" r="3" fill="currentColor" stroke="none"/>
                </g>
            `
        },

        "al-qassim": {
            name: "القصيم",
            shape: `
                <path d="M90 10 L125 45 L90 80 L55 45 Z"/>
                <path d="M90 100 L125 135 L90 170 L55 135 Z"/>
                <path d="M10 90 L45 55 L80 90 L45 125 Z"/>
                <path d="M100 90 L135 55 L170 90 L135 125 Z"/>
                <path d="M90 30 L105 45 L90 60 L75 45 Z"/>
                <path d="M90 120 L105 135 L90 150 L75 135 Z"/>
                <path d="M30 90 L45 75 L60 90 L45 105 Z"/>
                <path d="M120 90 L135 75 L150 90 L135 105 Z"/>
                <path d="M10 10 L35 10 L10 35 Z"/>
                <path d="M170 10 L145 10 L170 35 Z"/>
                <path d="M10 170 L35 170 L10 145 Z"/>
                <path d="M170 170 L145 170 L170 145 Z"/>
            `
        },

        "al-jouf": {
            name: "الجوف",
            shape: `
                <path d="M45 157 Q100 100 135 25"/>
                <path d="M62 137 Q22 115 35 86 Q72 91 78 116 Z"/>
                <path d="M82 113 Q120 110 132 80 Q102 72 88 98 Z"/>
                <path d="M101 82 Q68 55 82 31 Q111 45 113 69 Z"/>
                <path d="M118 56 Q151 60 161 34 Q134 25 123 45 Z"/>
                <ellipse cx="46" cy="143" rx="10" ry="15" transform="rotate(-35 46 143)" fill="currentColor"/>
                <ellipse cx="110" cy="104" rx="9" ry="14" transform="rotate(35 110 104)" fill="currentColor"/>
                <ellipse cx="122" cy="43" rx="8" ry="13" transform="rotate(35 122 43)" fill="currentColor"/>
            `
        },

        "abha": {
            name: "أبها",
            shape: `
                <path d="M10 35 L35 10 L60 35 Z"/>
                <path d="M60 35 L90 5 L120 35 Z"/>
                <path d="M120 35 L145 10 L170 35 Z"/>
                <path d="M10 145 L35 170 L60 145 Z"/>
                <path d="M60 145 L90 175 L120 145 Z"/>
                <path d="M120 145 L145 170 L170 145 Z"/>
                <path d="M90 50 L130 90 L90 130 L50 90 Z"/>
                <path d="M90 68 L112 90 L90 112 L68 90 Z"/>
                <path d="M90 80 L100 90 L90 100 L80 90 Z" fill="currentColor"/>
                <path d="M10 65 L30 90 L10 115 Z"/>
                <path d="M170 65 L150 90 L170 115 Z"/>
                <path d="M35 55 V125"/>
                <path d="M145 55 V125"/>
                <circle cx="35" cy="45" r="5" fill="currentColor"/>
                <circle cx="145" cy="45" r="5" fill="currentColor"/>
                <circle cx="35" cy="135" r="5" fill="currentColor"/>
                <circle cx="145" cy="135" r="5" fill="currentColor"/>
            `
        }
    };

    const identity = patterns[slug];

    if (!identity) return;

    page.dataset.regionIdentity = slug;

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    const layer = document.createElement("div");
    layer.className = "region-identity-layer";
    layer.setAttribute("aria-hidden", "true");

    layer.innerHTML = `
        <svg
            class="region-identity-pattern"
            xmlns="http://www.w3.org/2000/svg"
            preserveAspectRatio="xMidYMin slice"
        >
            <defs>
                <pattern
                    id="region-ornament-pattern"
                    width="180"
                    height="180"
                    patternUnits="userSpaceOnUse"
                >
                    <g
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        ${identity.shape}
                    </g>
                </pattern>
            </defs>

            <rect
                width="100%"
                height="100%"
                fill="url(#region-ornament-pattern)"
            />
        </svg>

        <div class="region-identity-halo region-identity-halo-one"></div>
        <div class="region-identity-halo region-identity-halo-two"></div>
        <div class="region-identity-halo region-identity-halo-three"></div>

        <div class="region-identity-emblem">
            <svg
                viewBox="0 0 180 180"
                xmlns="http://www.w3.org/2000/svg"
            >
                <circle
                    cx="90"
                    cy="90"
                    r="85"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.5"
                />

                <circle
                    cx="90"
                    cy="90"
                    r="73"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="0.8"
                    stroke-dasharray="4 8"
                />

                <g
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    ${identity.shape}
                </g>
            </svg>
        </div>
    `;

    page.prepend(layer);

    if (reducedMotion) return;

    let pointerX = 0;
    let pointerY = 0;
    let scrollShift = 0;
    let scheduled = false;

    function renderMovement() {
        page.style.setProperty(
            "--identity-shift-x",
            `${pointerX}px`
        );

        page.style.setProperty(
            "--identity-shift-y",
            `${pointerY}px`
        );

        page.style.setProperty(
            "--identity-scroll-shift",
            `${scrollShift}px`
        );

        scheduled = false;
    }

    function scheduleMovement() {
        if (scheduled) return;

        scheduled = true;
        requestAnimationFrame(renderMovement);
    }

    function updateScroll() {
        const bounds = page.getBoundingClientRect();
        const total = Math.max(
            1,
            page.offsetHeight - window.innerHeight
        );

        const progress = Math.min(
            1,
            Math.max(0, -bounds.top / total)
        );

        scrollShift = progress * 35;
        scheduleMovement();
    }

    if (window.matchMedia("(pointer: fine)").matches) {
        page.addEventListener("pointermove", (event) => {
            const bounds = page.getBoundingClientRect();

            const x = (
                event.clientX - bounds.left
            ) / bounds.width - 0.5;

            const y = (
                event.clientY - bounds.top
            ) / bounds.height - 0.5;

            pointerX = x * 22;
            pointerY = y * 18;

            scheduleMovement();
        }, { passive: true });

        page.addEventListener("pointerleave", () => {
            pointerX = 0;
            pointerY = 0;
            scheduleMovement();
        });
    }

    window.addEventListener(
        "scroll",
        updateScroll,
        { passive: true }
    );

    updateScroll();
})();
