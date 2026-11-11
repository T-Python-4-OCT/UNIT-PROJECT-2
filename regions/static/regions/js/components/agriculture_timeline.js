
(() => {
    const timeline = document.querySelector(".agri-timeline");

    if (!timeline) return;

    const stages = [
        {
            year: "1947",
            title: "بداية التنظيم الزراعي",
            description: "تأسست المديرية العامة للزراعة في المملكة، لتبدأ مرحلة مهمة في تنظيم العمل الزراعي وتطوير خدماته."
        },
        {
            year: "السبعينيات",
            title: "التوسع وتحديث الزراعة",
            description: "شهد القطاع الزراعي توسعًا في أساليب الإنتاج، مع تطوير شبكات الري والمرافق الداعمة للزراعة ووسائلها الحديثة."
        },
        {
            year: "2016",
            title: "البيئة والمياه والزراعة",
            description: "توحّدت مسؤوليات البيئة والمياه والزراعة ضمن وزارة واحدة، في خطوة تعكس أهمية إدارة الموارد الطبيعية بصورة متكاملة."
        },
        {
            year: "2024",
            title: "إنتاج زراعي متنوع",
            description: "أظهرت الإحصاءات الزراعية أن إنتاج التمور في المملكة بلغ نحو 1.923 مليون طن، إلى جانب منتجات زراعية أخرى متنوعة."
        }
    ];

    const buttons = timeline.querySelectorAll(".timeline-step");
    const scene = timeline.querySelector("#timeline-scene");
    const layers = timeline.querySelectorAll(".scene-layer");
    const progress = timeline.querySelector("#timeline-progress");
    const yearLabel = timeline.querySelector("#timeline-year-label");
    const title = timeline.querySelector("#timeline-title");
    const description = timeline.querySelector("#timeline-description");
    const nextButton = timeline.querySelector("#timeline-next");
    const resetButton = timeline.querySelector("#timeline-reset");

    let currentStage = 0;

    function updateTimeline(index) {
        currentStage = index;

        buttons.forEach((button, buttonIndex) => {
            button.setAttribute(
                "aria-pressed",
                String(buttonIndex === index)
            );
        });

        layers.forEach((layer, layerIndex) => {
            layer.classList.toggle(
                "is-active",
                layerIndex === index
            );
        });

        scene.dataset.stage = String(index);
        yearLabel.textContent = stages[index].year;
        title.textContent = stages[index].title;
        description.textContent = stages[index].description;

        progress.style.width = `${
            (index / (stages.length - 1)) * 100
        }%`;

        nextButton.textContent = index === stages.length - 1
            ? "العودة للبداية ↺"
            : "المحطة التالية ←";
    }

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            updateTimeline(Number(button.dataset.stage));
        });
    });

    nextButton.addEventListener("click", () => {
        updateTimeline((currentStage + 1) % stages.length);
    });

    resetButton.addEventListener("click", () => {
        updateTimeline(0);
    });

    updateTimeline(0);

    const canvas = timeline.querySelector("#agriculture-chart");
    const chartButtons = timeline.querySelectorAll(".chart-switch");

    if (!canvas || typeof Chart === "undefined") return;

    const agriculturalData = {
        labels: [
            "التمور",
            "الزيتون",
            "خضروات البيوت المحمية"
        ],
        datasets: [{
            label: "الإنتاج (ألف طن)",
            data: [1923, 351.7, 797],
            backgroundColor: [
                "#356B4E",
                "#C6A46C",
                "#B45E49"
            ],
            borderRadius: 10,
            borderWidth: 0
        }]
    };

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    let chart = null;

    function createChart(type) {
        if (chart) {
            chart.destroy();
        }

        const darkMode = document.documentElement.classList.contains("dark");
        const textColor = darkMode ? "#F5F0E6" : "#173C30";
        const secondaryColor = darkMode ? "#C1D0C4" : "#56685D";

        chart = new Chart(canvas, {
            type,
            data: agriculturalData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: reducedMotion ? 0 : 800
                },
                plugins: {
                    legend: {
                        display: type === "doughnut",
                        position: "bottom",
                        rtl: true,
                        labels: {
                            color: textColor,
                            font: {
                               family: "Tajawal"
                            }
                        }
                    },
                    tooltip: {
                        rtl: true,
                        callbacks: {
                            label: (context) => {
                                const value = typeof context.parsed === "number"
                                    ? context.parsed
                                    : context.parsed.y;

                                return `${context.label}: ${value} ألف طن`;
                            }
                        }
                    }
                },
                scales: type === "bar" ? {
                    x: {
                        ticks: {
                            color: textColor,
                            font: {
                               family: "Tajawal"
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: secondaryColor
                        }
                    }
                } : {}
            }
        });

        chartButtons.forEach((button) => {
            button.setAttribute(
                "aria-pressed",
                String(button.dataset.chartType === type)
            );
        });
    }

    chartButtons.forEach((button) => {
        button.addEventListener("click", () => {
            createChart(button.dataset.chartType);
        });
    });

    createChart("bar");

    const themeObserver = new MutationObserver(() => {
        if (chart) {
            createChart(chart.config.type);
        }
    });

    themeObserver.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"]
    });
})();
