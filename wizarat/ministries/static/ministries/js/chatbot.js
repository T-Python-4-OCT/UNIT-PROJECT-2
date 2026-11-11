(() => {
  const widget = document.querySelector("[data-assistant]");
  const copyElement = document.getElementById("chatbot-copy");
  const ministriesElement = document.getElementById("chatbot-ministries");
  if (!widget || !copyElement || !ministriesElement) return;

  const copy = JSON.parse(copyElement.textContent);
  const ministries = JSON.parse(ministriesElement.textContent);
  const panel = widget.querySelector(".assistant-panel");
  const toggle = widget.querySelector("[data-assistant-toggle]");
  const closeButton = widget.querySelector("[data-assistant-close]");
  const messages = widget.querySelector("[data-assistant-messages]");
  const suggestions = widget.querySelector("[data-assistant-suggestions]");
  const form = widget.querySelector("[data-assistant-form]");
  const input = widget.querySelector("[data-assistant-input]");
  let greeted = false;

  const normalize = (value) => value
    .toLocaleLowerCase("ar")
    .replace(/[\u064B-\u065F\u0670\u0640]/g, "")
    .replace(/[؟?!،,.:;؛]/g, " ")
    .trim();

  const appendMessage = (text, sender, links = []) => {
    const message = document.createElement("article");
    message.className = `assistant-message assistant-message-${sender}`;
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    message.append(paragraph);
    if (links.length) {
      const linkList = document.createElement("div");
      linkList.className = "assistant-links";
      links.forEach(({ label, url }) => {
        const link = document.createElement("a");
        link.href = url;
        link.textContent = label;
        if (url.startsWith("https://")) {
          link.target = "_blank";
          link.rel = "noopener noreferrer";
        }
        linkList.append(link);
      });
      message.append(linkList);
    }
    messages.append(message);
    messages.scrollTop = messages.scrollHeight;
  };

  const addSuggestions = () => {
    suggestions.replaceChildren();
    copy.questions.forEach((question) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = question;
      button.addEventListener("click", () => submitQuestion(question));
      suggestions.append(button);
    });
  };

  const categoryAnswer = (question) => {
    const categories = [...new Set(ministries.map((ministry) => ministry.category))];
    const category = categories.find((item) => normalize(question).includes(normalize(item)));
    if (!category) return null;
    const names = ministries
      .filter((ministry) => ministry.category === category)
      .map((ministry) => ministry.name);
    return `${copy.category_label} ${names.join("، ")}`;
  };

  const findMinistry = (question) => {
    const query = normalize(question);
    let bestMatch = null;
    let bestScore = 0;
    ministries.forEach((ministry) => {
      const name = normalize(ministry.name);
      const specificName = name.replace(/^وزارة\s*/, "");
      const tokens = specificName
        .split(/\s+/)
        .map((token) => token.replace(/^و/, ""))
        .filter((token) => token.length > 1);
      const matchedTokens = tokens.filter((token) => query.includes(token)).length;
      const score = query.includes(name)
        ? tokens.length + 2
        : matchedTokens;
      if (score > bestScore) {
        bestScore = score;
        bestMatch = ministry;
      }
    });
    return bestMatch;
  };

  const answerQuestion = (question) => {
    const category = categoryAnswer(question);
    if (category) {
      appendMessage(category, "bot");
      return;
    }

    const ministry = findMinistry(question);
    if (!ministry) {
      appendMessage(copy.no_match, "bot");
      addSuggestions();
      return;
    }

    const normalizedQuestion = normalize(question);
    const asksAboutTasks = /مهام|مسؤوليات|اختصاص|دور/.test(normalizedQuestion);
    const asksAboutFoundation = /تأسس|تأسيس|تاريخ|متى/.test(normalizedQuestion);
    const asksAboutWebsite = /موقع|رابط|رسمي|الكتروني|إلكتروني/.test(normalizedQuestion);
    let answer = ministry.summary;
    if (asksAboutFoundation && ministry.founded) {
      answer = `${copy.founded_label} ${ministry.founded}`;
    } else if (asksAboutTasks && ministry.tasks.length) {
      answer = `${copy.tasks_label} ${ministry.tasks.slice(0, 3).join("، ")}`;
    } else if (asksAboutWebsite && ministry.website) {
      answer = copy.website_label;
    } else if (ministry.founded) {
      answer = `${answer} ${copy.founded_label} ${ministry.founded}`;
    }

    const links = [{ label: copy.details_label, url: ministry.url }];
    if (asksAboutWebsite && ministry.website) {
      links.unshift({ label: copy.website_label, url: ministry.website });
    }
    appendMessage(answer, "bot", links);
  };

  function submitQuestion(value) {
    const question = value.trim();
    if (!question) return;
    appendMessage(question, "user");
    input.value = "";
    suggestions.replaceChildren();
    answerQuestion(question);
    input.focus();
  }

  const openPanel = () => {
    panel.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    if (!greeted) {
      appendMessage(copy.greeting, "bot");
      addSuggestions();
      greeted = true;
    }
    input.focus();
  };

  const closePanel = () => {
    panel.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.focus();
  };

  toggle.addEventListener("click", () => {
    if (panel.hidden) openPanel();
    else closePanel();
  });
  closeButton.addEventListener("click", closePanel);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    submitQuestion(input.value);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) closePanel();
  });
})();
