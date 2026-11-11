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
  header.style.setProperty("--scroll", percent / 100);
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
    ".section-head, .intro-text, .stats, .numbers, .frame, .moment, .future-card, .more-topic"
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

document.querySelectorAll(".stat-now, .count-up").forEach((stat) => {
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

const timeMachine = document.getElementById("time-machine");

if (timeMachine) {
  const range = document.getElementById("time-range");
  const yearLabel = document.getElementById("time-year");
  const eventLink = document.getElementById("time-event");
  const hero = document.querySelector(".hero-inner");
  const moments = JSON.parse(document.getElementById("time-moments").textContent);
  const first = Number(range.min);
  const last = Number(range.max);
  let playing = null;

  function travel(year) {
    range.value = year;
    yearLabel.textContent = year;
    hero.style.setProperty("--time", (year - first) / (last - first));

    const moment = moments.filter((item) => item.year <= year).pop();

    if (moment) {
      const icon = document.createElement("span");
      icon.className = "material-symbols-outlined";
      icon.textContent = moment.icon;
      eventLink.replaceChildren(icon, moment.year + ": " + moment.text);
      eventLink.href = moment.url;
    }
  }

  function stopPlaying() {
    cancelAnimationFrame(playing);
  }

  range.addEventListener("input", () => {
    stopPlaying();
    travel(Number(range.value));
  });

  range.addEventListener("pointerdown", stopPlaying);

  if (reduceMotion) {
    travel(last);
  } else {
    travel(first);

    setTimeout(() => {
      const start = performance.now();

      function step(now) {
        const done = Math.min((now - start) / 4000, 1);
        const eased = done < 0.5 ? 2 * done * done : 1 - Math.pow(-2 * done + 2, 2) / 2;
        travel(Math.round(first + (last - first) * eased));

        if (done < 1) {
          playing = requestAnimationFrame(step);
        }
      }

      playing = requestAnimationFrame(step);
    }, 1800);
  }
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
  const seconds = (new Date(element.dataset.date) - new Date()) / 1000;

  if (seconds > 0) {
    const days = Math.ceil(seconds / 86400);

    if (isArabic) return "باقي " + arabicCount(days, dayWords);
    return days === 1 ? "1 day to go" : days + " days to go";
  }

  const years = Number(element.dataset.year) - new Date().getFullYear();

  if (years < 0) return "";
  if (years === 0) return isArabic ? "هذه السنة" : "This year";
  if (isArabic) return "باقي " + arabicCount(years, yearWords) + " تقريبًا";
  return years === 1 ? "In about a year" : "In about " + years + " years";
}

document.querySelectorAll(".countdown").forEach((element) => {
  element.textContent = countdownText(element);
});

const timeIntro = document.getElementById("time-intro");

if (timeIntro) {
  if (!reduceMotion) {
    const yearLabel = document.getElementById("intro-year");
    const skipButton = document.getElementById("intro-skip");
    const first = 1902;
    const last = new Date().getFullYear();
    const start = performance.now();
    let finished = false;

    function closeIntro() {
      finished = true;
      timeIntro.hidden = true;
      document.documentElement.classList.remove("intro-open");
    }

    function count(now) {
      const done = Math.min(Math.max((now - start - 400) / 2000, 0), 1);
      const eased = 1 - Math.pow(1 - done, 3);
      yearLabel.textContent = Math.round(first + (last - first) * eased);

      if (done < 1 && !finished) {
        requestAnimationFrame(count);
      }
    }

    timeIntro.hidden = false;
    timeIntro.classList.add("play");
    document.documentElement.classList.add("intro-open");
    skipButton.addEventListener("click", closeIntro);
    skipButton.focus();
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeIntro();
    });
    requestAnimationFrame(count);
    setTimeout(closeIntro, 4300);
  }
}

const stage = document.getElementById("stage");

if (stage) {
  const slides = Array.from(stage.querySelectorAll(".slide"));
  const filterButtons = document.querySelectorAll(".filter");
  const yearsRow = document.getElementById("years");
  const counter = document.getElementById("stage-count");
  const playButton = document.getElementById("stage-play");
  const progressBar = document.getElementById("stage-progress");
  let list = slides;
  let index = 0;
  let timer = null;
  let lastEra = "";

  const yearButtons = slides.map((slide) => {
    const era = slide.querySelector(".slide-era").textContent;

    if (era !== lastEra) {
      lastEra = era;
      const label = document.createElement("span");
      label.className = "years-era";
      label.textContent = lastEra;
      yearsRow.append(label);
    }

    const button = document.createElement("button");
    button.type = "button";
    button.className = "year " + slide.classList[1];
    button.textContent = slide.dataset.year;
    button.addEventListener("click", () => {
      stop();
      show(list.indexOf(slide), true);
    });
    yearsRow.append(button);
    return button;
  });

  function restartProgress() {
    progressBar.classList.remove("run");
    void progressBar.offsetWidth;
    progressBar.classList.add("run");
  }

  function show(newIndex, scroll) {
    index = (newIndex + list.length) % list.length;
    const current = list[index];

    slides.forEach((slide, i) => {
      slide.classList.toggle("active", slide === current);
      yearButtons[i].classList.toggle("active", slide === current);
    });

    counter.textContent = index + 1 + (isArabic ? " من " : " / ") + list.length;

    if (scroll) {
      yearButtons[slides.indexOf(current)].scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "nearest",
        inline: "center",
      });
    }

    if (timer) {
      restartProgress();
    }
  }

  function play() {
    timer = setInterval(() => show(index + 1, true), 5000);
    playButton.children[0].textContent = "pause";
    playButton.children[1].textContent = playButton.dataset.pause;
    restartProgress();
  }

  function stop() {
    clearInterval(timer);
    timer = null;
    playButton.children[0].textContent = "play_arrow";
    playButton.children[1].textContent = playButton.dataset.play;
    progressBar.classList.remove("run");
  }

  function step(direction) {
    stop();
    show(index + direction, true);
  }

  function filter(topic) {
    list = slides.filter((slide) => topic === "all" || slide.dataset.topics.split(" ").includes(topic));
    let label = null;

    Array.from(yearsRow.children).forEach((child) => {
      if (child.classList.contains("years-era")) {
        label = child;
        label.hidden = true;
      } else {
        child.hidden = !list.includes(slides[yearButtons.indexOf(child)]);
        if (!child.hidden) label.hidden = false;
      }
    });

    filterButtons.forEach((button) => {
      const active = button.dataset.topic === topic;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active);
    });

    stop();
    show(0, false);
    yearsRow.scrollLeft = 0;
  }

  playButton.addEventListener("click", () => (timer ? stop() : play()));
  document.getElementById("stage-prev").addEventListener("click", () => step(-1));
  document.getElementById("stage-next").addEventListener("click", () => step(1));

  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") step(isArabic ? -1 : 1);
    if (event.key === "ArrowLeft") step(isArabic ? 1 : -1);
  });

  let startX = null;

  stage.addEventListener("pointerdown", (event) => {
    startX = event.clientX;
  });

  stage.addEventListener("pointerup", (event) => {
    const moved = event.clientX - startX;

    if (startX !== null && Math.abs(moved) > 50) {
      step((moved < 0) !== isArabic ? 1 : -1);
    }

    startX = null;
  });

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      filter(button.dataset.topic);
      history.replaceState(null, "", button.dataset.topic === "all" ? location.pathname : "#" + button.dataset.topic);
    });
  });

  const start = document.querySelector('.filter[data-topic="' + location.hash.slice(1) + '"]');
  filter(start ? start.dataset.topic : "all");

  if (start) {
    start.scrollIntoView({ block: "nearest", inline: "center" });
  }
}
