
// =========================
// DARK / LIGHT MODE
// =========================

const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.querySelector(".theme-icon");

function applyTheme(theme) {

    document.body.classList.toggle(
        "light-mode",
        theme === "light"
    );

    if (themeIcon) {
        themeIcon.textContent = theme === "light" ? "☀" : "☾";
    }

    localStorage.setItem("theme", theme);
}

// Restore saved theme
const savedTheme = localStorage.getItem("theme") || "dark";

applyTheme(savedTheme);

// Toggle theme
if (themeToggle) {

    themeToggle.addEventListener("click", () => {

        const isLight = document.body.classList.contains("light-mode");

        applyTheme(isLight ? "dark" : "light");

    });

}


// =========================
// SMOOTH SECTION NAVIGATION
// =========================

document.querySelectorAll('a[href^="#"]').forEach(link => {

    link.addEventListener("click", function (event) {

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

    });

});


// =========================
// SCROLL REVEAL
// =========================

const sections = document.querySelectorAll(".experience-section");

if ("IntersectionObserver" in window) {

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }

        });

    }, {
        threshold: 0.2
    });

    sections.forEach(section => {
        observer.observe(section);
    });

}


// =========================
// ACTIVE SECTION NAVIGATION
// =========================

const sideDots = document.querySelectorAll(".side-dot");

const trackedSections = document.querySelectorAll(
    "#home, .experience-section"
);

if ("IntersectionObserver" in window) {

    const sectionObserver = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                const currentSection = entry.target.id;

                sideDots.forEach(dot => {

                    dot.classList.remove("active");

                    if (dot.dataset.section === currentSection) {
                        dot.classList.add("active");
                    }

                });

            }

        });

    }, {
        threshold: 0.5
    });

    trackedSections.forEach(section => {
        sectionObserver.observe(section);
    });

}


// =========================
// MOBILE NAVIGATION
// =========================

const menuToggle = document.getElementById("menu-toggle");
const mainNav = document.querySelector(".main-nav");

if (menuToggle && mainNav) {

    menuToggle.addEventListener("click", () => {

        mainNav.classList.toggle("open");

    });

    document.querySelectorAll(".nav-link").forEach(link => {

        link.addEventListener("click", () => {

            mainNav.classList.remove("open");

        });

    });

}


/* =========================
   KINGDOM STATS COUNTER
========================= */

const statsSection = document.querySelector(".kingdom-stats");
const statNumbers = document.querySelectorAll(".stat-number");

let statsStarted = false;

function animateCounter(element) {
    const target = Number(element.dataset.target);
    const decimals = Number(element.dataset.decimals || 0);
    const duration = 2000;
    const startTime = performance.now();

    function updateCounter(currentTime) {
        const progress = Math.min(
            (currentTime - startTime) / duration,
            1
        );

        const easedProgress = 1 - Math.pow(1 - progress, 4);
        const currentValue = target * easedProgress;

        element.textContent = currentValue.toFixed(decimals);

        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }

    requestAnimationFrame(updateCounter);
}

if (statsSection && statNumbers.length) {
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !statsStarted) {
                statsStarted = true;

                statNumbers.forEach(number => {
                    animateCounter(number);
                });

                statsObserver.disconnect();
            }
        });
    }, {
        threshold: 0.4
    });

    statsObserver.observe(statsSection);
}





/* =========================
   INTERACTIVE SAUDI MAP
========================= */

const saudiMap = document.getElementById("saudi-map");

const regions = {
    "SA-01": {
        name: "الرياض",
        description: "عاصمة المملكة ومركزها السياسي والاقتصادي. تجمع بين المعالم التاريخية والمشاريع المستقبلية."
    },
    "SA-02": {
        name: "مكة المكرمة",
        description: "تحتضن المسجد الحرام والكعبة المشرفة، وهي قبلة المسلمين ووجهة ملايين الحجاج والمعتمرين."
    },
    "SA-03": {
        name: "المدينة المنورة",
        description: "مدينة رسول الله ﷺ، وتتميز بمسجد النبوي ومعالمها الإسلامية والتاريخية."
    },
    "SA-04": {
        name: "المنطقة الشرقية",
        description: "تتميز بثرواتها الطبيعية وسواحل الخليج العربي، وتضم مدنًا مهمة مثل الدمام والخبر والأحساء."
    },
    "SA-05": {
        name: "القصيم",
        description: "تشتهر بمزارع النخيل وإنتاج التمور وأسواقها التراثية."
    },
    "SA-06": {
        name: "حائل",
        description: "تتميز بجبالها ومواقعها الأثرية ونقوشها الصخرية المسجلة ضمن التراث العالمي."
    },
    "SA-07": {
        name: "تبوك",
        description: "منطقة تجمع بين الجبال والسواحل والطبيعة المتنوعة، وتضم مشاريع سياحية كبرى."
    },
    "SA-08": {
        name: "الحدود الشمالية",
        description: "تقع شمال المملكة وتتميز بطبيعتها الصحراوية ومواقعها التاريخية."
    },
    "SA-09": {
        name: "جازان",
        description: "تشتهر بجزرها البحرية وجبالها الخضراء ومحاصيلها الزراعية."
    },
    "SA-10": {
        name: "نجران",
        description: "تتميز بتراثها العمراني وقصورها التاريخية وموقع الأخدود الأثري."
    },
    "SA-11": {
        name: "الباحة",
        description: "تشتهر بغاباتها وجبال السروات وأجوائها المعتدلة وقراها التراثية."
    },
    "SA-12": {
        name: "الجوف",
        description: "تشتهر بواحات الزيتون وآثارها التاريخية وقلاعها القديمة."
    },
    "SA-14": {
        name: "عسير",
        description: "تتميز بجبالها الشاهقة وقراها التراثية وطبيعتها الخضراء."
    }
};

let selectedRegion = null;
let mapRegions = [];
let mapLabels = [];

function getMapColors() {
    const isLight = document.body.classList.contains("light-mode");

    return isLight
        ? {
            normal: "#DCE8DE",
            hover: "#A9C9AE",
            selected: "#7FA98A",
            border: "#B18B35",
            text: "#263C30"
        }
        : {
            normal: "#234B38",
            hover: "#376B4D",
            selected: "#376B4D",
            border: "#D4AF37",
            text: "#FFFFFF"
        };
}

// =========================
// UPDATE MAP COLORS
// =========================

function updateSaudiMapTheme() {

    const mapColors = getMapColors();

    mapRegions.forEach(region => {

        region.style.fill =
            region.id === selectedRegion
                ? mapColors.selected
                : mapColors.normal;

        region.style.stroke = mapColors.border;
        region.style.strokeWidth = "1.5";

    });

    mapLabels.forEach(label => {
        label.setAttribute("fill", mapColors.text);
    });
}

// =========================
// DISPLAY REGION INFORMATION
// =========================

function showRegionInfo(regionId) {

    const region = regions[regionId];

    if (!region) return;

    const nameElement = document.getElementById("region-name");
    const descriptionElement = document.getElementById("region-description");
    const labelElement = document.querySelector(".region-label");

    if (nameElement) {
        nameElement.textContent = region.name;
    }

    if (descriptionElement) {
        descriptionElement.textContent = region.description;
    }

    if (labelElement) {
        labelElement.textContent = "اكتشف المنطقة";
    }
}

// =========================
// RESET REGION INFORMATION
// =========================

function resetRegionInfo() {

    const nameElement = document.getElementById("region-name");
    const descriptionElement = document.getElementById("region-description");
    const labelElement = document.querySelector(".region-label");

    if (nameElement) {
        nameElement.textContent = "اختر منطقة";
    }

    if (descriptionElement) {
        descriptionElement.textContent =
            "مرر المؤشر على إحدى المناطق الإدارية في الخريطة لاستكشاف معلوماتها.";
    }

    if (labelElement) {
        labelElement.textContent = "اكتشف المملكة";
    }
}

// =========================
// LOAD SAUDI MAP
// =========================

if (saudiMap) {

    saudiMap.addEventListener("load", () => {

        const svgDoc = saudiMap.contentDocument;

        if (!svgDoc) return;

        const svg = svgDoc.querySelector("svg");

        if (!svg) return;

        mapRegions = Object.keys(regions)
            .map(id => svgDoc.getElementById(id))
            .filter(Boolean);

        // =========================
        // REGION INTERACTIONS
        // =========================

        mapRegions.forEach(region => {

            region.style.cursor = "pointer";
            region.style.transition = "fill 0.3s ease";

            // Hover
            region.addEventListener("mouseenter", () => {

                region.style.fill = mapColors.hover;

                showRegionInfo(region.id);

            });

            // Mouse leaves region
            region.addEventListener("mouseleave", () => {

                updateSaudiMapTheme();

                if (selectedRegion) {
                    showRegionInfo(selectedRegion);
                } else {
                    resetRegionInfo();
                }

            });

            // Click to select
            region.addEventListener("click", () => {

                selectedRegion = region.id;

                updateSaudiMapTheme();

                showRegionInfo(region.id);

            });

        });

        // =========================
        // REGION LABELS
        // =========================

        const labelsGroup = svgDoc.createElementNS(
            "http://www.w3.org/2000/svg",
            "g"
        );

        labelsGroup.setAttribute("class", "region-labels");

        mapRegions.forEach(region => {

            const box = region.getBBox();

            const label = svgDoc.createElementNS(
                "http://www.w3.org/2000/svg",
                "text"
            );

            let labelX = box.x + box.width / 2;
            let labelY = box.y + box.height / 2;
            
            // Custom position for Tabuk
            if (region.id === "SA-07") {
                labelX = box.x + box.width * 0.55;
                labelY = box.y + box.height * 0.35;
            }
            
            label.setAttribute("x", labelX);
            label.setAttribute("y", labelY);

            label.setAttribute("text-anchor", "middle");
            label.setAttribute("dominant-baseline", "middle");

            label.setAttribute(
                "font-size",
                Math.max(8, Math.min(13, box.width / 5))
            );

            label.setAttribute("font-weight", "bold");
            label.setAttribute("font-family", "Arial, sans-serif");
            label.setAttribute("fill", mapColors.text);
            label.setAttribute("pointer-events", "none");

            label.textContent = regions[region.id].name;

            labelsGroup.appendChild(label);

            mapLabels.push(label);

        });

        svg.appendChild(labelsGroup);

        // Initial map appearance
        updateSaudiMapTheme();

        resetRegionInfo();

    });

}


/* =========================
   HISTORY STORY ANIMATIONS
========================= */

const historyScenes = document.querySelectorAll(".history-scene");

if (historyScenes.length) {



    function animateHistoryYear(element, target) {

        const digits = String(target).split("");
        const duration = 1600;
    
        element.innerHTML = "";
    
        element.style.display = "inline-flex";
        element.style.direction = "ltr";
        element.style.overflow = "hidden";
        element.style.verticalAlign = "middle";
    
        digits.forEach((digit, index) => {
    
            const column = document.createElement("span");
            column.style.display = "inline-block";
            column.style.overflow = "hidden";
            column.style.height = "1.15em";
    
            const reel = document.createElement("span");
    
            reel.style.display = "flex";
            reel.style.flexDirection = "column";
            reel.style.transform = "translateY(0)";
            reel.style.transition =
                `transform ${duration}ms cubic-bezier(.16, 1, .3, 1)`;
    
            for (let number = 0; number <= 9; number++) {
                const item = document.createElement("span");
                item.textContent = number;
                item.style.display = "block";
                item.style.height = "1.15em";
                item.style.lineHeight = "1.15em";
                reel.appendChild(item);
            }
    
            column.appendChild(reel);
            element.appendChild(column);
    
            const delay = index * 140;
    
            setTimeout(() => {
                reel.style.transform = `translateY(-${Number(digit) * 1.15}em)`;
            }, delay);
        });
    }
    
    

    const historyObserver = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                const scene = entry.target;
                const counter = scene.querySelector(".year-counter");

                scene.classList.add("is-visible");

                // تشغيل العداد مرة واحدة لكل محطة
                if (counter && !counter.dataset.animated) {

                    counter.dataset.animated = "true";

                    const target = Number(counter.dataset.target);

                    animateHistoryYear(counter, target);
                }
            }

        });

    }, {
        threshold: 0.55
    });

    historyScenes.forEach(scene => {
        historyObserver.observe(scene);
    });

}



/* =========================
   FIRST SAUDI STATE RULERS
========================= */

const rulerData = {
    mohammed: {
        name: "الإمام محمد بن سعود",
        period: "1727 – 1765",
        image: "/static/SaudiApp/images/History/ImamMohammed.webp",
        description:
            "مؤسس الدولة السعودية الأولى وإمام الدرعية. تولى الحكم عام 1727، ووضع الأساس لقيام دولة قامت على الاستقرار والوحدة، وجعل الدرعية مركزًا للحكم."
    },

    abdulaziz: {
        name: "الإمام عبدالعزيز بن محمد",
        period: "1765 – 1803",
        image: "/static/SaudiApp/images/History/ImamAbdulaziz.webp",
        description:
            "الإمام الثاني للدولة السعودية الأولى. واصل مسيرة والده في توحيد مناطق الجزيرة العربية، وشهد عهده توسع الدولة وتعزيز مكانتها."
    },

    saud: {
        name: "الإمام سعود بن عبدالعزيز",
        period: "1803 – 1814",
        image: "/static/SaudiApp/images/History/ImamSaud.webp",
        description:
            "الإمام الثالث للدولة السعودية الأولى. عُرف في المصادر التاريخية بسعود الكبير، وامتد نفوذ الدولة في عهده إلى مناطق واسعة."
    },

    abdullah: {
        name: "الإمام عبدالله بن سعود",
        period: "1814 – 1818",
        image: "/static/SaudiApp/images/History/ImamAbdullah.webp",
        description:
            "الإمام الرابع والأخير للدولة السعودية الأولى. شهد عهده الحملات العسكرية التي انتهت بسقوط الدرعية عام 1818."
    }
};

const rulerButtons = document.querySelectorAll(
    ".scene-one .ruler-thumb"
);

const mainRulerImage = document.getElementById("ruler-main-image");
const rulerName = document.getElementById("ruler-name");
const rulerPeriod = document.getElementById("ruler-period");
const rulerDescription = document.getElementById("ruler-description");

function selectRuler(button) {
    const ruler = rulerData[button.dataset.ruler];

    if (
        !ruler ||
        !mainRulerImage ||
        !rulerName ||
        !rulerPeriod ||
        !rulerDescription
    ) return;

    mainRulerImage.classList.add("changing");
    rulerName.classList.add("changing");
    rulerPeriod.classList.add("changing");
    rulerDescription.classList.add("changing");

    setTimeout(() => {
        mainRulerImage.src = ruler.image;
        mainRulerImage.alt = ruler.name;

        rulerName.textContent = ruler.name;
        rulerPeriod.textContent = ruler.period;
        rulerDescription.textContent = ruler.description;

        mainRulerImage.classList.remove("changing");
        rulerName.classList.remove("changing");
        rulerPeriod.classList.remove("changing");
        rulerDescription.classList.remove("changing");
    }, 180);

    rulerButtons.forEach(item => {
        item.classList.toggle("active", item === button);
    });
}

rulerButtons.forEach(button => {
    button.addEventListener("mouseenter", () => {
        selectRuler(button);
    });

    button.addEventListener("focus", () => {
        selectRuler(button);
    });

    button.addEventListener("click", () => {
        selectRuler(button);
    });
});



/* =========================
   SECOND SAUDI STATE RULERS
========================= */

const secondRulerData = {
    turki: {
        name: "الإمام تركي بن عبدالله",
        period: "1824 – 1834",
        image: "/static/SaudiApp/images/History/ImamTurki.webp",
        description: "مؤسس الدولة السعودية الثانية. استعاد مدينة الرياض عام 1824، واتخذها عاصمة للدولة، وأعاد بناء الحكم السعودي بعد نهاية الدولة السعودية الأولى."
    },

    faisal: {
        name: "الإمام فيصل بن تركي",
        period: "1834 – 1838 و1843 – 1865",
        image: "/static/SaudiApp/images/History/ImamFaisal.webp",
        description: "تولى الحكم على فترتين، وعمل على استعادة قوة الدولة السعودية الثانية وتثبيت الاستقرار وتوسيع نفوذها."
    },

    abdullah2: {
        name: "الإمام عبدالله بن فيصل",
        period: "1865 – 1871",
        image: "/static/SaudiApp/images/History/ImamAbdullah2.webp",
        description: "تولى الحكم بعد وفاة والده الإمام فيصل بن تركي، وشهدت فترة حكمه تحديات وصراعات داخلية أثرت في استقرار الدولة."
    },

    abdulrahman: {
        name: "الإمام عبدالرحمن بن فيصل",
        period: "1875 – 1891",
        image: "/static/SaudiApp/images/History/ImamAbdulrahman.webp",
        description: "آخر أئمة الدولة السعودية الثانية، واجه تحديات سياسية وعسكرية انتهت بسقوط الدولة عام 1891."
    }
};

const secondRulerButtons = document.querySelectorAll(
    '.scene-two .ruler-thumb'
);

const secondMainImage = document.getElementById(
    "ruler-main-image-2"
);

const secondRulerName = document.getElementById(
    "ruler-name-2"
);

const secondRulerPeriod = document.getElementById(
    "ruler-period-2"
);

const secondRulerDescription = document.getElementById(
    "ruler-description-2"
);

function selectSecondRuler(button) {

    const ruler = secondRulerData[button.dataset.ruler];

    if (!ruler || !secondMainImage) return;

    secondMainImage.classList.add("changing");
    secondRulerName.classList.add("changing");
    secondRulerPeriod.classList.add("changing");
    secondRulerDescription.classList.add("changing");

    setTimeout(() => {

        secondMainImage.src = ruler.image;
        secondMainImage.alt = ruler.name;

        secondRulerName.textContent = ruler.name;
        secondRulerPeriod.textContent = ruler.period;
        secondRulerDescription.textContent = ruler.description;

        secondMainImage.classList.remove("changing");
        secondRulerName.classList.remove("changing");
        secondRulerPeriod.classList.remove("changing");
        secondRulerDescription.classList.remove("changing");

    }, 180);

    secondRulerButtons.forEach(item => {
        item.classList.remove("active");
    });

    button.classList.add("active");
}

secondRulerButtons.forEach(button => {

    button.addEventListener("mouseenter", () => {
        selectSecondRuler(button);
    });

    button.addEventListener("click", () => {
        selectSecondRuler(button);
    });

});


/* =========================================
   SAUDI NATIONAL OCCASIONS COUNTDOWN
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    const daysElement = document.getElementById("countdown-days");
    const hoursElement = document.getElementById("countdown-hours");
    const minutesElement = document.getElementById("countdown-minutes");
    const secondsElement = document.getElementById("countdown-seconds");

    const nameElement = document.getElementById("next-occasion-name");
    const dateElement = document.getElementById("next-occasion-date");

    // Stop if countdown is not on this page
    if (
        !daysElement ||
        !hoursElement ||
        !minutesElement ||
        !secondsElement ||
        !nameElement ||
        !dateElement
    ) {
        return;
    }

    const occasions = [
        {
            name: "يوم التأسيس",
            date: "22 فبراير",
            month: 1,
            day: 22
        },
        {
            name: "يوم العلم",
            date: "11 مارس",
            month: 2,
            day: 11
        },
        {
            name: "اليوم الوطني",
            date: "23 سبتمبر",
            month: 8,
            day: 23
        }
    ];

    function getNextOccasion() {

        const now = new Date();

        const today = new Date(
            now.getFullYear(),
            now.getMonth(),
            now.getDate()
        );

        const upcoming = occasions
            .map(occasion => {

                let target = new Date(
                    now.getFullYear(),
                    occasion.month,
                    occasion.day
                );

                if (target < today) {
                    target = new Date(
                        now.getFullYear() + 1,
                        occasion.month,
                        occasion.day
                    );
                }

                return {
                    ...occasion,
                    target: target
                };

            })
            .sort((a, b) => a.target - b.target);

        return upcoming[0];
    }

    function updateCountdown() {

        const now = new Date();
        const next = getNextOccasion();

        let difference = next.target.getTime() - now.getTime();

        // If today is the occasion, show zero countdown
        const isOccasionDay =
            now.getFullYear() === next.target.getFullYear() &&
            now.getMonth() === next.target.getMonth() &&
            now.getDate() === next.target.getDate();

        if (isOccasionDay) {
            difference = 0;
            nameElement.textContent = "اليوم نحتفل بـ " + next.name;
            dateElement.textContent = "دام عزك يا وطن";
        } else {
            nameElement.textContent = next.name;
            dateElement.textContent = "الموعد القادم: " + next.date;
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((difference / (1000 * 60)) % 60);
        const seconds = Math.floor((difference / 1000) % 60);

        daysElement.textContent = String(days).padStart(2, "0");
        hoursElement.textContent = String(hours).padStart(2, "0");
        minutesElement.textContent = String(minutes).padStart(2, "0");
        secondsElement.textContent = String(seconds).padStart(2, "0");
    }

    updateCountdown();

    setInterval(updateCountdown, 1000);

});


/* ========================================
   INTERACTIVE TOURISM DESTINATIONS
======================================== */

const tourismHero = document.querySelector(".tourism-hero");

if (tourismHero) {

    const destinationOptions = tourismHero.querySelectorAll(".destination-option");
    const tourismTitle = document.getElementById("tourism-title");
    const tourismDescription = document.getElementById("tourism-description");
    const tourismLink = document.getElementById("tourism-link");

    const destinations = {

        "red-sea": {
            title: "البحر الأحمر",
            description: "حيث تلتقي زرقة البحر بسحر الطبيعة. اكتشف عالماً من الجزر الساحرة والشعاب المرجانية والتجارب البحرية الاستثنائية."
        },

        "diriyah": {
            title: "الدرعية",
            description: "هنا بدأت الحكاية. عِش عبق التاريخ بين أزقة الطريف العريقة وعمارة الطين الأصيلة، واكتشف مهد الدولة السعودية."
        },

        "alula": {
            title: "العُلا",
            description: "رحلة بين عجائب الطبيعة وأسرار التاريخ. تأمل التكوينات الصخرية المذهلة واكتشف حضارات تركت أثرها عبر الزمن."
        },

        "alahsa": {
            title: "الأحساء",
            description: "واحة تنبض بالحياة وسط الرمال. استكشف سحر النخيل والعيون الطبيعية والقرى التراثية في واحدة من أجمل واحات العالم."
        }

    };

    const destinationVideos = {
        "red-sea": document.getElementById("redsea-video"),
        "diriyah": document.getElementById("diriyah-video"),
        "alula": document.getElementById("alula-video"),
        "alahsa": document.getElementById("alahsa-video")
    };

    function selectDestination(option) {

        const destinationKey = option.dataset.destination;
        const destination = destinations[destinationKey];
    
        if (!destination) return;
        if (destinationKey === "red-sea") {
            tourismLink.href = "/red-sea/";
        }
    
        // Update selected destination
        destinationOptions.forEach(item => {
            item.classList.remove("active");
        });
    
        option.classList.add("active");
        tourismHero.dataset.activeDestination = destinationKey;
    
        // Switch background videos
        Object.entries(destinationVideos).forEach(([key, video]) => {
    
            if (!video) return;
    
            if (key === destinationKey) {
    
                video.muted = true;
                video.loop = true;
                video.playsInline = true;
    
                video.classList.add("is-visible");
    
                const startVideo = () => {
                    video.play().catch(error => {
                        console.error("Video playback error:", error);
                    });
                };
    
                if (video.readyState >= 2) {
                    startVideo();
                } else {
                    video.addEventListener("loadeddata", startVideo, {
                        once: true
                    });
                    video.load();
                }
    
            } else {
    
                video.classList.remove("is-visible");
                video.pause();
                video.currentTime = 0;
    
            }
    
        });
    
        // Update destination text
        tourismTitle.style.opacity = "0";
        tourismDescription.style.opacity = "0";
    
        setTimeout(() => {
    
            tourismTitle.textContent = destination.title;
            tourismDescription.textContent = destination.description;
    
            tourismTitle.style.opacity = "1";
            tourismDescription.style.opacity = "1";
    
        }, 180);
    }

    destinationOptions.forEach(option => {

        option.addEventListener("mouseenter", () => {
            selectDestination(option);
        });

        option.addEventListener("focus", () => {
            selectDestination(option);
        });

        option.addEventListener("click", () => {
            selectDestination(option);
        });

    });

}


/* ========================================
   RED SEA — FAVORITES
======================================== */

document.querySelectorAll(".red-sea-favorite").forEach(button => {

    button.setAttribute("aria-pressed", "false");

    button.addEventListener("click", () => {

        const isFavorite = button.classList.toggle("is-favorite");

        button.textContent = isFavorite ? "♥" : "♡";
        button.setAttribute("aria-pressed", String(isFavorite));

    });

});


/* ========================================
   RED SEA — GALLERY LIGHTBOX
======================================== */

const redSeaGallery = document.querySelector(".red-sea-gallery");

if (redSeaGallery) {

    const galleryItems = [...redSeaGallery.querySelectorAll(".red-sea-gallery-item")];

    const lightbox = document.getElementById("red-sea-lightbox");
    const lightboxImage = document.getElementById("red-sea-lightbox-image");
    const counter = document.getElementById("red-sea-lightbox-counter");

    const closeButton = lightbox.querySelector(".red-sea-lightbox-close");
    const prevButton = lightbox.querySelector(".prev");
    const nextButton = lightbox.querySelector(".next");

    let currentIndex = 0;

    function showImage(index) {
        currentIndex = (index + galleryItems.length) % galleryItems.length;

        const image = galleryItems[currentIndex].querySelector("img");

        lightboxImage.src = image.src;
        lightboxImage.alt = image.alt;

        counter.textContent = `${String(currentIndex + 1).padStart(2, "0")} / ${String(galleryItems.length).padStart(2, "0")}`;
    }

    function openLightbox(index) {
        showImage(index);
        lightbox.classList.add("active");
        lightbox.setAttribute("aria-hidden", "false");
        document.body.classList.add("lightbox-open");
    }

    function closeLightbox() {
        lightbox.classList.remove("active");
        lightbox.setAttribute("aria-hidden", "true");
        document.body.classList.remove("lightbox-open");
    }

    galleryItems.forEach((item, index) => {
        item.addEventListener("click", () => openLightbox(index));
    });

    closeButton.addEventListener("click", closeLightbox);

    prevButton.addEventListener("click", () => {
        showImage(currentIndex - 1);
    });

    nextButton.addEventListener("click", () => {
        showImage(currentIndex + 1);
    });

    lightbox.addEventListener("click", event => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });

    document.addEventListener("keydown", event => {
        if (!lightbox.classList.contains("active")) return;

        if (event.key === "Escape") closeLightbox();
        if (event.key === "ArrowLeft") showImage(currentIndex + 1);
        if (event.key === "ArrowRight") showImage(currentIndex - 1);
    });
}


/* =========================
   ALULA EXPERIENCES CAROUSEL
========================= */

document.addEventListener("DOMContentLoaded", function () {

    const carousel = document.getElementById("alulaCarousel");

    if (!carousel) return;

    const slides = Array.from(
        carousel.querySelectorAll(".alula-slide")
    );

    const prevButton = document.getElementById("alulaPrev");
    const nextButton = document.getElementById("alulaNext");
    const counter = document.getElementById("alulaCounter");

    if (!slides.length) return;

    let currentIndex = 0;
    let startX = 0;
    let isDragging = false;
    let wheelLocked = false;

    function updateCarousel() {

        slides.forEach((slide, index) => {

            slide.classList.remove("active", "prev", "next");

            if (index === currentIndex) {
                slide.classList.add("active");
            }

            else if (
                index === (currentIndex - 1 + slides.length) % slides.length
            ) {
                slide.classList.add("prev");
            }

            else if (
                index === (currentIndex + 1) % slides.length
            ) {
                slide.classList.add("next");
            }

        });

        counter.textContent =
            String(currentIndex + 1).padStart(2, "0") +
            " / " +
            String(slides.length).padStart(2, "0");
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        updateCarousel();
    }

    function previousSlide() {
        currentIndex =
            (currentIndex - 1 + slides.length) % slides.length;

        updateCarousel();
    }

    nextButton.addEventListener("click", nextSlide);
    prevButton.addEventListener("click", previousSlide);

    /* Mouse and Touch Drag */

    carousel.addEventListener("pointerdown", function (event) {

        if (event.target.closest("a")) return;

        startX = event.clientX;
        isDragging = true;

        carousel.classList.add("dragging");

    });

    carousel.addEventListener("pointerup", function (event) {

        if (!isDragging) return;

        const difference = event.clientX - startX;

        if (Math.abs(difference) > 50) {

            if (difference < 0) {
                nextSlide();
            } else {
                previousSlide();
            }

        }

        isDragging = false;
        carousel.classList.remove("dragging");

    });

    carousel.addEventListener("pointercancel", function () {
        isDragging = false;
        carousel.classList.remove("dragging");
    });

    /* Trackpad Horizontal Scroll */

    carousel.addEventListener("wheel", function (event) {

        if (Math.abs(event.deltaX) < 20) return;

        if (wheelLocked) return;

        wheelLocked = true;

        if (event.deltaX > 0) {
            nextSlide();
        } else {
            previousSlide();
        }

        setTimeout(function () {
            wheelLocked = false;
        }, 650);

    }, { passive: true });

    /* Keyboard Navigation */

    carousel.setAttribute("tabindex", "0");

    carousel.addEventListener("keydown", function (event) {

        if (event.key === "ArrowRight") {
            previousSlide();
        }

        if (event.key === "ArrowLeft") {
            nextSlide();
        }

    });

    updateCarousel();

});


/* =========================
   MOBILE NAVIGATION MENU
========================= */

document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".main-header");
    const menuButton = document.getElementById("menu-toggle");
    const navigation = header?.querySelector(".main-nav");

    if (!header || !menuButton || !navigation) return;

    menuButton.setAttribute("aria-expanded", "false");

    menuButton.addEventListener("click", function () {
        const isOpen = header.classList.toggle("mobile-menu-open");
        menuButton.setAttribute("aria-expanded", String(isOpen));
    });

    navigation.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            header.classList.remove("mobile-menu-open");
            menuButton.setAttribute("aria-expanded", "false");
        });
    });

    document.addEventListener("click", function (event) {
        if (!header.contains(event.target)) {
            header.classList.remove("mobile-menu-open");
            menuButton.setAttribute("aria-expanded", "false");
        }
    });
});


