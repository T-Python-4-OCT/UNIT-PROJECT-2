const menuBtn = document.getElementById("menu-btn");
const nav = document.getElementById("nav");

menuBtn.addEventListener("click", () => {
  const isOpen = nav.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", isOpen);
});

nav.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    nav.classList.remove("open");
    menuBtn.setAttribute("aria-expanded", false);
  });
});

const header = document.getElementById("site-header");

window.addEventListener("scroll", () => {
  header.classList.toggle("scrolled", window.scrollY > 10);
});

const compareSlider = document.getElementById("compare-slider");

if (compareSlider) {
  const range = compareSlider.querySelector("input");

  range.addEventListener("input", () => {
    compareSlider.style.setProperty("--pos", range.value + "%");
  });
}