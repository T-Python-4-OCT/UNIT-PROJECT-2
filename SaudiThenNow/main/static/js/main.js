const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isArabic = document.documentElement.lang === "ar";

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
const progress = document.getElementById("progress");

function onScroll() {
  header.classList.toggle("scrolled", window.scrollY > 10);

  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const percent = maxScroll > 0 ? (window.scrollY / maxScroll) * 100 : 0;
  progress.style.setProperty("--progress", percent + "%");
}

window.addEventListener("scroll", onScroll, { passive: true });
window.addEventListener("resize", onScroll);
onScroll();

const compareSlider = document.getElementById("compare-slider");

if (compareSlider) {
  const range = compareSlider.querySelector("input");

  range.addEventListener("input", () => {
    compareSlider.style.setProperty("--pos", range.value + "%");
  });
}

const stories = document.querySelector(".stories");

if (stories) {
  const pin = stories.querySelector(".stories-pin");
  const track = stories.querySelector(".stories-track");
  const wideScreen = window.matchMedia("(min-width: 961px)");
  let distance = 0;

  function moveStories() {
    if (!distance) {
      return;
    }

    const pinTop = parseFloat(getComputedStyle(pin).top);
    const scrolled = pinTop - stories.getBoundingClientRect().top;
    const done = Math.min(Math.max(scrolled / distance, 0), 1);
    const shift = done * distance * (isArabic ? 1 : -1);
    track.style.transform = "translateX(" + shift + "px)";
  }

  function measureStories() {
    track.style.transform = "";

    if (wideScreen.matches) {
      distance = Math.max(0, track.scrollWidth - pin.clientWidth);
      stories.style.height = pin.offsetHeight + distance + "px";
    } else {
      distance = 0;
      stories.style.height = "";
    }

    moveStories();
  }

  window.addEventListener("scroll", moveStories, { passive: true });
  window.addEventListener("resize", measureStories);
  window.addEventListener("load", measureStories);
  measureStories();
}

const callbacks = new Map();

const watcher = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      watcher.unobserve(entry.target);
      callbacks.get(entry.target).forEach((callback) => callback());
    }
  });
}, { threshold: 0.15 });

function whenVisible(element, callback) {
  const list = callbacks.get(element) || [];
  list.push(callback);
  callbacks.set(element, list);
  watcher.observe(element);
}

if (!reduceMotion) {
  const revealItems = document.querySelectorAll(
    ".section-head, .intro-text, .stats, .frame, .moment, .future-card, .more-topic"
  );

  revealItems.forEach((item) => {
    const index = Array.from(item.parentElement.children).indexOf(item);
    const step = item.classList.contains("moment") ? 0.18 : 0.1;
    item.style.setProperty("--delay", (index % 6) * step + "s");
    item.classList.add("reveal");
    whenVisible(item, () => item.classList.add("shown"));
  });

  document.querySelectorAll(".future-line rect").forEach((rect) => {
    rect.addEventListener("transitionend", () => {
      rect.closest(".future-card").classList.add("drawn");
    }, { once: true });
  });
}

function formatNumber(value, sample) {
  const decimals = (sample.split(".")[1] || "").length;

  return value.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
    useGrouping: sample.includes(","),
  });
}

document.querySelectorAll(".stat-now").forEach((stat) => {
  const textNode = stat.firstChild;
  const original = textNode.textContent;
  const numbers = original.match(/\d[\d,]*(\.\d+)?/g);

  if (reduceMotion || !numbers || numbers.length !== 1) {
    return;
  }

  const sample = numbers[0];
  const target = parseFloat(sample.replace(/,/g, ""));
  textNode.textContent = original.replace(sample, formatNumber(0, sample));

  whenVisible(stat, () => {
    const start = performance.now();

    function step(now) {
      const done = Math.min((now - start) / 1600, 1);
      const eased = 1 - Math.pow(1 - done, 3);
      textNode.textContent = original.replace(sample, formatNumber(target * eased, sample));

      if (done < 1) {
        requestAnimationFrame(step);
      }
    }

    requestAnimationFrame(step);
  });
});

const doors = document.querySelector(".doors");

if (doors && !reduceMotion) {
  doors.classList.add("closed");

  const loading = Array.from(doors.querySelectorAll("img")).map((img) => {
    if (img.complete) {
      return Promise.resolve();
    }

    return new Promise((resolve) => {
      img.addEventListener("load", resolve, { once: true });
      img.addEventListener("error", resolve, { once: true });
    });
  });

  const timeout = new Promise((resolve) => setTimeout(resolve, 2500));

  Promise.race([Promise.all(loading), timeout]).then(() => {
    setTimeout(() => doors.classList.add("open"), 400);
  });
}

const dayWords = ["يوم واحد", "يومان", "أيام", "يومًا", "يوم"];
const yearWords = ["سنة", "سنتان", "سنوات", "سنة", "سنة"];

function arabicCount(count, words) {
  const rest = count % 100;

  if (count === 1) return words[0];
  if (count === 2) return words[1];
  if (rest >= 3 && rest <= 10) return count + " " + words[2];
  if (rest >= 11) return count + " " + words[3];
  return count + " " + words[4];
}

function countdownText(element) {
  const pad = (number) => String(number).padStart(2, "0");
  let seconds = Math.floor((new Date(element.dataset.date) - new Date()) / 1000);

  if (seconds > 0) {
    const days = Math.floor(seconds / 86400);
    seconds %= 86400;
    const clock = pad(Math.floor(seconds / 3600)) + ":" + pad(Math.floor((seconds % 3600) / 60)) + ":" + pad(seconds % 60);

    if (isArabic) {
      return "باقي " + arabicCount(days, dayWords) + " و" + clock;
    }

    return days.toLocaleString("en-US") + " days " + clock + " to go";
  }

  const years = Number(element.dataset.year) - new Date().getFullYear();

  if (years < 0) return "";
  if (years === 0) return isArabic ? "هذه السنة" : "This year";
  if (isArabic) return "باقي " + arabicCount(years, yearWords) + " تقريبًا";
  return years === 1 ? "In about a year" : "In about " + years + " years";
}

const countdowns = document.querySelectorAll(".countdown");

function updateCountdowns() {
  countdowns.forEach((element) => {
    element.textContent = countdownText(element);
  });
}

if (countdowns.length) {
  updateCountdowns();
  setInterval(updateCountdowns, 1000);
}
