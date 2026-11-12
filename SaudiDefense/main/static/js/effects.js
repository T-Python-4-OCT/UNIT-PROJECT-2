
const header = document.getElementById("siteHeader");
const progressBar = document.getElementById("scrollProgress");
const backToTop = document.getElementById("backToTop");

function onScroll() {
    const scrolled = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

    header.classList.toggle("scrolled", scrolled > 40);

    if (maxScroll > 0) {
        progressBar.style.width = (scrolled / maxScroll) * 100 + "%";
    }

    backToTop.classList.toggle("show", scrolled > 600);
}

window.addEventListener("scroll", onScroll);
onScroll();

backToTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
