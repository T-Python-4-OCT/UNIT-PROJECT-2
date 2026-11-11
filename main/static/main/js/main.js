// Small helpers. The site still works if JavaScript is turned off.

// 1) Show "checking..." while the server analyzes the message
document.querySelectorAll("form[data-loading]").forEach(function (form) {
  form.addEventListener("submit", function () {
    if (form.checkValidity()) {
      document.getElementById("loading").classList.add("is-on");
    }
  });
});

// 2) Live character counter under the message box
document.querySelectorAll("textarea[data-counter]").forEach(function (box) {
  var counter = document.getElementById(box.dataset.counter);
  box.addEventListener("input", function () {
    counter.textContent = box.value.length;
  });
});

// 3) "Paste" button: paste the copied message into the box
document.querySelectorAll("[data-paste]").forEach(function (button) {
  var box = document.getElementById(button.dataset.paste);
  if (!navigator.clipboard) {
    button.hidden = true;
    return;
  }
  button.addEventListener("click", function () {
    navigator.clipboard.readText().then(function (text) {
      box.value = text;
      box.dispatchEvent(new Event("input"));
      box.focus();
    });
  });
});

// 4) Show the chosen PDF file name
document.querySelectorAll(".drop-zone input[type=file]").forEach(function (input) {
  input.addEventListener("change", function () {
    var label = input.closest(".drop-zone").querySelector("[data-file-name]");
    if (input.files.length) {
      label.textContent = input.files[0].name;
    }
  });
});

// 5) Hide the loading layer if the user comes back with the browser "back" button
window.addEventListener("pageshow", function () {
  document.getElementById("loading").classList.remove("is-on");
});
