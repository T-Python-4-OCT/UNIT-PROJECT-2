
(() => {
    const heritage = document.querySelector(".region-heritage");

    if (!heritage) return;

    const tabs = [...heritage.querySelectorAll("[data-heritage-tab]")];
    const panels = [...heritage.querySelectorAll("[data-heritage-panel]")];
    const nextButton = heritage.querySelector("#heritage-next");
    const labels = ["الحكاية", "المواسم", "الأسواق والفعاليات"];

    let activeIndex = 0;

    function activateTab(index) {
        activeIndex = index;

        tabs.forEach((tab, i) => {
            const active = i === index;

            tab.setAttribute("aria-selected", String(active));
            tab.tabIndex = active ? 0 : -1;
        });

        panels.forEach((panel, i) => {
            panel.hidden = i !== index;
        });

        const nextIndex = (index + 1) % tabs.length;

        nextButton.textContent = nextIndex === 0
            ? "العودة للحكاية ↺"
            : `التالي: ${labels[nextIndex]} ←`;
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            activateTab(index);
        });

        tab.addEventListener("keydown", (event) => {
            let nextIndex;

            if (event.key === "ArrowLeft") {
                nextIndex = (index + 1) % tabs.length;
            } else if (event.key === "ArrowRight") {
                nextIndex = (index - 1 + tabs.length) % tabs.length;
            } else if (event.key === "Home") {
                nextIndex = 0;
            } else if (event.key === "End") {
                nextIndex = tabs.length - 1;
            } else {
                return;
            }

            event.preventDefault();

            activateTab(nextIndex);
            tabs[nextIndex].focus();
        });
    });

    nextButton.addEventListener("click", () => {
        activateTab((activeIndex + 1) % tabs.length);
    });

    activateTab(0);
})();
