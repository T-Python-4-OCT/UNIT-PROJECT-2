// تكبير الصور (Lightbox)
// تضغط على أي صورة في المعارض والبطاقات، فتفتح كبيرة بملء الشاشة

const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const lightboxCaption = document.getElementById("lightboxCaption");

// الصور اللي نسمح بتكبيرها
const zoomImages = document.querySelectorAll(".gallery img, .card-img img, .upcoming-img img");

function openLightbox(img) {
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightboxCaption.textContent = img.alt;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";   // نوقف تمرير الصفحة وراها
}

function closeLightbox() {
    lightbox.hidden = true;
    lightboxImg.src = "";
    document.body.style.overflow = "";
}

zoomImages.forEach(function (img) {
    img.classList.add("zoomable");
    img.title = lightbox.dataset.hint;

    img.addEventListener("click", function (event) {
        // لو الصورة داخل رابط (مثل بطاقة القطاع) نخلي الرابط يشتغل عادي
        if (img.closest("a")) return;
        event.preventDefault();
        openLightbox(img);
    });
});

// نقفلها بزر X، أو بالضغط على الخلفية، أو بزر Esc
document.getElementById("lightboxClose").addEventListener("click", closeLightbox);

lightbox.addEventListener("click", function (event) {
    if (event.target === lightbox) closeLightbox();
});

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !lightbox.hidden) closeLightbox();
});
