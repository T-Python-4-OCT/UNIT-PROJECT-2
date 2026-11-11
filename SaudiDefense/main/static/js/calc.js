// حاسبة التوطين (صفحة رؤية 2030)
// تكتب مبلغ الإنفاق، فنحسب: المحلي اليوم، والمطلوب في 2030، والفرق

const CURRENT_RATE = 0.20;   // نسبة التوطين الحالية تقريباً
const TARGET_RATE = 0.50;    // مستهدف رؤية 2030

const calcInput = document.getElementById("calcInput");
const calcRange = document.getElementById("calcRange");

// نكتب الرقم بفواصل وبخانة عشرية وحدة، مثل 1,250.5
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

    // الجملة اللي تشرح النتيجة: نبدّل {total} و {now} ... بالأرقام
    // (الأرقام بخط عريض عشان تبان)
    const sentence = document.getElementById("calcSentence");
    sentence.innerHTML = sentence.dataset.template
        .replace("{total}", "<strong>" + formatNumber(spending) + "</strong>")
        .replace("{now}", "<strong>" + formatNumber(now) + "</strong>")
        .replace("{target}", "<strong>" + formatNumber(target) + "</strong>")
        .replace("{gap}", "<strong class='gap'>" + formatNumber(gap) + "</strong>");
}

// نحوّل الأرقام العربية (٠١٢٣…) والفارسية (۰۱۲۳…) لأرقام عادية (0123…)
// ونشيل أي حرف مو رقم أو فاصلة عشرية
function toWesternDigits(text) {
    return text
        .replace(/[٠-٩]/g, function (d) { return d.charCodeAt(0) - 1632; })
        .replace(/[۰-۹]/g, function (d) { return d.charCodeAt(0) - 1776; })
        .replace("٫", ".")
        .replace(/[^0-9.]/g, "");
}

// لما يكتب في المربع نحدّث الشريط، ولما يحرّك الشريط نحدّث المربع
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
