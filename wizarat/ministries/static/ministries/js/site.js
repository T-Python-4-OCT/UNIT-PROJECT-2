(() => {
  const nav = document.querySelector(".site-nav");
  const progress = document.querySelector(".reading-progress span");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const updateScrollEffects = () => {
    if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 12);
    if (progress) {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const percentage = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
      progress.style.width = `${Math.min(100, Math.max(0, percentage))}%`;
    }
  };
  window.addEventListener("scroll", updateScrollEffects, { passive: true });
  updateScrollEffects();

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reducedMotion) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => revealObserver.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  document.querySelectorAll("img").forEach((image) => {
    image.addEventListener("error", () => {
      image.hidden = true;
      image.parentElement.classList.add("image-fallback");
    }, { once: true });
  });

  // Same Arabic normalisation as the server-side search: drop diacritics, unify alef/ya/ta marbuta.
  const normalizeArabic = (value) => String(value || "")
    .replace(/[\u064B-\u065F\u0670\u0640]/g, "")
    .toLocaleLowerCase("ar")
    .replace(/[\u0623\u0625\u0622\u0671]/g, "\u0627")
    .replace(/\u0649/g, "\u064A")
    .replace(/\u0629/g, "\u0647")
    .trim();

  // Live text search + category filter for a grid of cards (home page and directory page).
  const setupCardFilter = ({ input, select, cards, count, empty }) => {
    const searchInput = document.querySelector(input);
    const categorySelect = document.querySelector(select);
    const cardItems = [...document.querySelectorAll(cards)];
    const countElement = document.querySelector(count);
    const emptyElement = document.querySelector(empty);
    if (!searchInput || !categorySelect || !cardItems.length) return;
    const filterCards = () => {
      const term = normalizeArabic(searchInput.value);
      const category = categorySelect.value;
      let visible = 0;
      cardItems.forEach((card) => {
        const show = normalizeArabic(card.dataset.search).includes(term)
          && (!category || card.dataset.category === category);
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (countElement) countElement.textContent = `${visible}`;
      if (emptyElement) emptyElement.classList.toggle("is-visible", visible === 0);
    };
    searchInput.addEventListener("input", filterCards);
    categorySelect.addEventListener("change", filterCards);
  };
  setupCardFilter({
    input: ".js-ministry-search", select: ".js-category-filter", cards: ".js-ministry-card",
    count: ".js-result-count", empty: ".js-empty-state",
  });
  setupCardFilter({
    input: ".js-directory-search", select: ".js-directory-category", cards: ".js-directory-card",
    count: ".js-directory-count", empty: ".js-directory-empty",
  });

  const counterItems = document.querySelectorAll("[data-count-target]");
  const animateCounter = (element) => {
    const target = Number(element.dataset.countTarget);
    if (!Number.isFinite(target)) return;
    if (reducedMotion) {
      element.textContent = new Intl.NumberFormat("ar-SA").format(target);
      return;
    }
    const start = performance.now();
    const duration = 1100;
    const draw = (now) => {
      const progressValue = Math.min(1, (now - start) / duration);
      const eased = 1 - ((1 - progressValue) ** 3);
      element.textContent = new Intl.NumberFormat("ar-SA").format(Math.round(target * eased));
      if (progressValue < 1) requestAnimationFrame(draw);
    };
    requestAnimationFrame(draw);
  };
  if ("IntersectionObserver" in window) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counterItems.forEach((item) => counterObserver.observe(item));
  } else {
    counterItems.forEach(animateCounter);
  }

  document.querySelectorAll(".js-share-page").forEach((button) => {
    button.addEventListener("click", async () => {
      const feedback = document.querySelector(button.dataset.feedbackTarget);
      const successMessage = button.dataset.success;
      const errorMessage = button.dataset.error;
      try {
        await navigator.clipboard.writeText(window.location.href);
        if (feedback) feedback.textContent = successMessage;
      } catch (error) {
        try {
          const temporaryInput = document.createElement("textarea");
          temporaryInput.value = window.location.href;
          temporaryInput.setAttribute("readonly", "");
          temporaryInput.style.position = "fixed";
          temporaryInput.style.opacity = "0";
          let copied = false;
          try {
            document.body.append(temporaryInput);
            temporaryInput.select();
            copied = document.execCommand("copy");
          } finally {
            temporaryInput.remove();
          }
          if (feedback) feedback.textContent = copied ? successMessage : errorMessage;
        } catch (fallbackError) {
          if (feedback) feedback.textContent = errorMessage;
        }
      }
    });
  });

  document.querySelectorAll("[data-gallery-index]").forEach((button) => {
    button.addEventListener("click", () => {
      const carousel = document.querySelector("#galleryCarousel");
      if (!carousel || !window.bootstrap) return;
      window.bootstrap.Carousel.getOrCreateInstance(carousel).to(Number(button.dataset.galleryIndex));
    });
  });

  const searchModal = document.getElementById("searchModal");
  const searchDataElement = document.getElementById("chatbot-ministries");
  if (searchModal && searchDataElement) {
    const searchInput = searchModal.querySelector("[data-site-search-input]");
    const searchResults = searchModal.querySelector("[data-site-search-results]");
    const searchStatus = searchModal.querySelector("[data-site-search-status]");
    const searchAll = searchModal.querySelector("[data-site-search-all]");
    const searchIndex = JSON.parse(searchDataElement.textContent).map((ministry) => ({
      ministry,
      name: normalizeArabic(ministry.name),
      text: normalizeArabic([
        ministry.name, ministry.tagline, ministry.category, ministry.summary, ministry.minister,
        ...(ministry.tasks || []),
      ].join(" ")),
    }));

    const renderResults = () => {
      const query = searchInput.value.trim();
      const terms = normalizeArabic(query).split(/\s+/).filter(Boolean);
      searchResults.replaceChildren();
      searchAll.hidden = true;
      if (!terms.length) {
        searchStatus.textContent = searchStatus.dataset.hint;
        return;
      }
      const matches = searchIndex
        .filter((entry) => terms.every((term) => entry.text.includes(term)))
        .sort((a, b) => Number(!terms.every((t) => b.name.includes(t))) - Number(!terms.every((t) => a.name.includes(t))));
      searchStatus.textContent = matches.length
        ? `${new Intl.NumberFormat("ar-SA").format(matches.length)} ${searchStatus.dataset.countLabel}`
        : searchStatus.dataset.empty;
      matches.slice(0, 8).forEach(({ ministry }) => {
        const link = document.createElement("a");
        link.className = "search-result";
        link.href = ministry.url;
        const icon = document.createElement("span");
        icon.className = "search-result-icon";
        icon.innerHTML = `<i class="bi ${ministry.icon.replace(/[^a-z0-9-]/gi, "")}" aria-hidden="true"></i>`;
        const body = document.createElement("span");
        body.className = "search-result-body";
        const name = document.createElement("strong");
        name.textContent = ministry.name;
        const tagline = document.createElement("small");
        tagline.textContent = ministry.tagline;
        body.append(name, tagline);
        const category = document.createElement("span");
        category.className = "search-result-category";
        category.textContent = ministry.category;
        link.append(icon, body, category);
        searchResults.append(link);
      });
      if (matches.length > 8) {
        searchAll.href = `${searchAll.pathname}?q=${encodeURIComponent(query)}`;
        searchAll.hidden = false;
      }
    };
    searchInput.addEventListener("input", renderResults);
    searchModal.addEventListener("shown.bs.modal", () => searchInput.focus());
    document.addEventListener("keydown", (event) => {
      const typing = event.target.closest("input, textarea, select, [contenteditable]");
      if (event.key === "/" && !typing && window.bootstrap) {
        event.preventDefault();
        window.bootstrap.Modal.getOrCreateInstance(searchModal).show();
      }
    });
  }

  const quizElement = document.getElementById("quizData");
  const quizRoot = document.getElementById("quizApp");
  if (!quizElement || !quizRoot) return;
  const questions = JSON.parse(quizElement.textContent);
  const quizCopy = JSON.parse(document.getElementById("quizCopy").textContent);
  const questionElement = quizRoot.querySelector(".js-question");
  const choicesElement = quizRoot.querySelector(".js-choices");
  const numberElement = quizRoot.querySelector(".js-question-number");
  const progressBar = quizRoot.querySelector(".js-quiz-progress");
  const nextButton = quizRoot.querySelector(".js-quiz-next");
  const resultElement = quizRoot.querySelector(".js-quiz-result");
  let questionIndex = 0;
  let score = 0;
  let answered = false;

  const renderQuestion = () => {
    const question = questions[questionIndex];
    answered = false;
    questionElement.textContent = question.question;
    numberElement.textContent = quizCopy.question_counter
      .replace("{current}", questionIndex + 1)
      .replace("{total}", questions.length);
    progressBar.style.width = `${(questionIndex / questions.length) * 100}%`;
    choicesElement.replaceChildren();
    nextButton.disabled = true;
    nextButton.textContent = questionIndex === questions.length - 1
      ? quizCopy.show_result
      : quizCopy.next_question;
    question.choices.forEach((choice) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "quiz-choice";
      button.textContent = choice.name;
      button.addEventListener("click", () => {
        if (answered) return;
        answered = true;
        if (choice.slug === question.answer) {
          score += 1;
          button.classList.add("is-correct");
        } else {
          button.classList.add("is-wrong");
          const correctChoice = [...choicesElement.children].find(
            (item) => item.textContent === question.choices.find(
              (option) => option.slug === question.answer,
            ).name,
          );
          if (correctChoice) correctChoice.classList.add("is-correct");
        }
        choicesElement.querySelectorAll("button").forEach((item) => { item.disabled = true; });
        nextButton.disabled = false;
      });
      choicesElement.append(button);
    });
  };

  nextButton.addEventListener("click", () => {
    if (!answered) return;
    questionIndex += 1;
    if (questionIndex < questions.length) {
      renderQuestion();
      return;
    }
    quizRoot.querySelector(".js-quiz-content").hidden = true;
    resultElement.hidden = false;
    resultElement.querySelector(".js-score").textContent = `${score} / ${questions.length}`;
    resultElement.querySelector(".js-result-message").textContent = quizCopy.result_message;
    progressBar.style.width = "100%";
  });
  quizRoot.querySelector(".js-quiz-restart").addEventListener("click", () => {
    questionIndex = 0;
    score = 0;
    quizRoot.querySelector(".js-quiz-content").hidden = false;
    resultElement.hidden = true;
    renderQuestion();
  });
  renderQuestion();
})();
