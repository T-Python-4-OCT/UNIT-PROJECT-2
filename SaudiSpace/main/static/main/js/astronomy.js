
document.addEventListener("DOMContentLoaded", () => {

    const elements = document.querySelectorAll(
        ".astronomy-page .reveal"
    );

    if (!("IntersectionObserver" in window)) {
        elements.forEach(element => {
            element.classList.add("show");
        });
        return;
    }

    const observer = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("show");

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.12
        }
    );

    elements.forEach(element => {
        observer.observe(element);
    });

});
