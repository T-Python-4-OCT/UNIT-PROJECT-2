document.addEventListener("DOMContentLoaded", function () {

    const revealElements = document.querySelectorAll(
        ".home-page .oj-reveal"
    );

    const observer = new IntersectionObserver(
        function (entries, observer) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.classList.add("is-visible");

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.15
        }
    );

    revealElements.forEach(function (element) {
        observer.observe(element);
    });

});


