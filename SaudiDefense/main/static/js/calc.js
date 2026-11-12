
const CURRENT_RATE = 0.20;
const TARGET_RATE = 0.50;

const calcInput = document.getElementById("calcInput");
const calcRange = document.getElementById("calcRange");

function formatNumber(value) {
    return value.toLocaleString("en-US", { maximumFractionDigits: 1 });
}

function calculate() {
    const spending = Math.max(Number(calcInput.value) || 0, 0);

    const now = spending * CURRENT_RATE;
    const target = spending * TARGET_RATE;
    const gap = target - now;

    document.getElementById("calcNow").textContent = formatNumber(now);
    document.getElementById("calcTarget").textContent = formatNumber(target);
    document.getElementById("calcGap").textContent = formatNumber(gap);

    const sentence = document.getElementById("calcSentence");
    sentence.innerHTML = sentence.dataset.template
        .replace("{total}", "<strong>" + formatNumber(spending) + "</strong>")
        .replace("{now}", "<strong>" + formatNumber(now) + "</strong>")
        .replace("{target}", "<strong>" + formatNumber(target) + "</strong>")
        .replace("{gap}", "<strong class='gap'>" + formatNumber(gap) + "</strong>");
}

function toWesternDigits(text) {
    return text
        .replace(/[٠-٩]/g, function (d) { return d.charCodeAt(0) - 1632; })
        .replace(/[۰-۹]/g, function (d) { return d.charCodeAt(0) - 1776; })
        .replace("٫", ".")
        .replace(/[^0-9.]/g, "");
}

calcInput.addEventListener("input", function () {
    const cleaned = toWesternDigits(calcInput.value);
    if (cleaned !== calcInput.value) {
        calcInput.value = cleaned;
    }
    calcRange.value = calcInput.value;
    calculate();
});

calcRange.addEventListener("input", function () {
    calcInput.value = calcRange.value;
    calculate();
});

calculate();
