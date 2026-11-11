// ============================================================
// لمسات جافا سكربت خفيفة
// 1) القائمة العلوية شفافة فوق الصورة، وتصير بلون الصفحة لما ننزل
// 2) شريط تقدم القراءة فوق الصفحة
// 3) زر الرجوع للأعلى
// ============================================================

const header = document.getElementById("siteHeader");
const progressBar = document.getElementById("scrollProgress");
const backToTop = document.getElementById("backToTop");

function onScroll() {
    const scrolled = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

    // 1) نضيف كلاس "scrolled" للهيدر بعد ما ننزل 40 بكسل
    header.classList.toggle("scrolled", scrolled > 40);

    // 2) طول الشريط = نسبة اللي نزلناه من الصفحة
    if (maxScroll > 0) {
        progressBar.style.width = (scrolled / maxScroll) * 100 + "%";
    }

    // 3) زر الرجوع يظهر بعد ما ننزل شوي
    backToTop.classList.toggle("show", scrolled > 600);
}

window.addEventListener("scroll", onScroll);
onScroll();

backToTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
