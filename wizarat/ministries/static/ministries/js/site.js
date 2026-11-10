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

  const search = document.querySelector(".js-ministry-search");
  const categoryFilter = document.querySelector(".js-category-filter");
  const ministryCards = [...document.querySelectorAll(".js-ministry-card")];
  const resultCount = document.querySelector(".js-result-count");
  const emptyState = document.querySelector(".js-empty-state");
  if (search && categoryFilter && ministryCards.length) {
    const normalizeText = (value) => value
      .toLocaleLowerCase("ar")
      .replace(/[\u064B-\u065F\u0670\u0640]/g, "")
      .trim();
    const filterCards = () => {
      const term = normalizeText(search.value);
      const category = categoryFilter.value;
      let visible = 0;
      ministryCards.forEach((card) => {
        const matchesText = normalizeText(card.dataset.search).includes(term);
        const matchesCategory = !category || card.dataset.category === category;
        const showCard = matchesText && matchesCategory;
        card.hidden = !showCard;
        if (showCard) visible += 1;
      });
      if (resultCount) resultCount.textContent = `${visible}`;
      if (emptyState) emptyState.classList.toggle("is-visible", visible === 0);
    };
    search.addEventListener("input", filterCards);
    categoryFilter.addEventListener("change", filterCards);
  }

  const directorySearch = document.querySelector(".js-directory-search");
  const directoryCategory = document.querySelector(".js-directory-category");
  const directoryCards = [...document.querySelectorAll(".js-directory-card")];
  const directoryCount = document.querySelector(".js-directory-count");
  const directoryEmpty = document.querySelector(".js-directory-empty");
  if (directorySearch && directoryCategory && directoryCards.length) {
    const normalizeText = (value) => value
      .toLocaleLowerCase("ar")
      .replace(/[\u064B-\u065F\u0670\u0640]/g, "")
      .trim();
    const filterDirectory = () => {
      const term = normalizeText(directorySearch.value);
      const category = directoryCategory.value;
      let visible = 0;
      directoryCards.forEach((card) => {
        const matchesText = normalizeText(card.dataset.search).includes(term);
        const matchesCategory = !category || card.dataset.category === category;
        const showCard = matchesText && matchesCategory;
        card.hidden = !showCard;
        if (showCard) visible += 1;
      });
      if (directoryCount) directoryCount.textContent = `${visible}`;
      if (directoryEmpty) directoryEmpty.classList.toggle("is-visible", visible === 0);
    };
    directorySearch.addEventListener("input", filterDirectory);
    directoryCategory.addEventListener("change", filterDirectory);
  }

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
