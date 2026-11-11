
(() => {
    const journey = document.querySelector(".crop-journey");

    if (!journey) return;

    const buttons = [
        ...journey.querySelectorAll(".journey-stage")
    ];

    const contents = [
        ...journey.querySelectorAll(".journey-content")
    ];

    const visuals = [
        ...journey.querySelectorAll(".journey-visual-stage")
    ];

    const progress = journey.querySelector("#journey-progress");
    const progressTrack = journey.querySelector(
        ".journey-progress-track"
    );

    const counter = journey.querySelector("#journey-counter");
    const visualCounter = journey.querySelector(
        "#journey-visual-counter"
    );

    const nextButton = journey.querySelector("#journey-next");
    const prevButton = journey.querySelector("#journey-prev");
    const resetButton = journey.querySelector("#journey-reset");

    if (
        !buttons.length ||
        !progress ||
        !nextButton ||
        !prevButton ||
        !resetButton
    ) {
        return;
    }

    const total = buttons.length;
    let currentIndex = 0;

    function formatCount(value) {
        return String(value).padStart(2, "0");
    }

    function updateStage(index) {
        if (index < 0 || index >= total) return;

        currentIndex = index;

        buttons.forEach((button, buttonIndex) => {
            const active = buttonIndex === index;

            button.setAttribute(
                "aria-pressed",
                String(active)
            );
        });

        contents.forEach((content, contentIndex) => {
            const active = contentIndex === index;

            content.hidden = !active;
            content.classList.toggle("hidden", !active);
        });

        visuals.forEach((visual, visualIndex) => {
            const active = visualIndex === index;

            visual.hidden = !active;
            visual.classList.toggle("is-active", active);
        });

        const currentText = (
            `${formatCount(index + 1)} / ${formatCount(total)}`
        );

        if (counter) {
            counter.textContent = currentText;
        }

        if (visualCounter) {
            visualCounter.textContent = currentText;
        }

        progress.style.width = `${((index + 1) / total) * 100}%`;

        if (progressTrack) {
            progressTrack.setAttribute(
                "aria-valuenow",
                String(index + 1)
            );
        }

        prevButton.disabled = index === 0;

        nextButton.textContent = index === total - 1
            ? "العودة للبداية ↺"
            : "المرحلة التالية ←";
    }

    buttons.forEach((button, index) => {
        button.addEventListener("click", () => {
            updateStage(index);
        });
    });

    nextButton.addEventListener("click", () => {
        const nextIndex = currentIndex === total - 1
            ? 0
            : currentIndex + 1;

        updateStage(nextIndex);
    });

    prevButton.addEventListener("click", () => {
        updateStage(currentIndex - 1);
    });

    resetButton.addEventListener("click", () => {
        updateStage(0);
    });

    updateStage(0);
})();
