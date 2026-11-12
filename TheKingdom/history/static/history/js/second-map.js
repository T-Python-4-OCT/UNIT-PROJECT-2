
"use strict";

/* ==========================================
   الدولة السعودية الثانية
   تكبير الخريطة التاريخية
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    const page = document.querySelector("#revivalPage");

    if (!page) return;

    const mapOpen = page.querySelector(
        "#revivalMapOpen"
    );

    const mapDialog = page.querySelector(
        "#revivalMapDialog"
    );

    const mapClose = page.querySelector(
        "#revivalMapClose"
    );

    if (!mapOpen || !mapDialog || !mapClose) {
        return;
    }

    /* ======================================
       فتح الخريطة
    ====================================== */

    function openMap() {

        if (mapDialog.open) return;

        mapDialog.showModal();

        mapClose.focus();
    }

    /* ======================================
       إغلاق الخريطة
    ====================================== */

    function closeMap() {

        if (!mapDialog.open) return;

        mapDialog.close();
    }

    /* ======================================
       الضغط على صورة الخريطة
    ====================================== */

    mapOpen.addEventListener(
        "click",
        openMap
    );

    /* ======================================
       زر الإغلاق
    ====================================== */

    mapClose.addEventListener(
        "click",
        closeMap
    );

    /* ======================================
       الضغط خارج نافذة الخريطة
    ====================================== */

    mapDialog.addEventListener("click", event => {

        if (event.target !== mapDialog) {
            return;
        }

        const rect = mapDialog.getBoundingClientRect();

        const clickedInside =
            event.clientX >= rect.left &&
            event.clientX <= rect.right &&
            event.clientY >= rect.top &&
            event.clientY <= rect.bottom;

        if (!clickedInside) {
            closeMap();
        }
    });

    /* ======================================
       إعادة التركيز بعد الإغلاق
    ====================================== */

    mapDialog.addEventListener("close", () => {

        mapOpen.focus({
            preventScroll: true
        });
    });

});
