/* quiz.js — اختبار تاريخي: ترتيب عشوائي، شرح فوري، نتيجة ومراجعة، وحفظ أفضل نتيجة محلياً */
(function () {
  "use strict";
  var M = window.Masmak;
  var all = M.data("quiz-data") || [];
  var root = M.$("[data-quiz]");
  if (!root || !all.length) return;

  var $ = function (s) { return M.$(s, root); };
  var startEl = $("[data-quiz-start]"), runEl = $("[data-quiz-run]"), resultEl = $("[data-quiz-result]");
  var qEl = $("[data-quiz-q]"), optsEl = $("[data-quiz-options]"), fbEl = $("[data-quiz-feedback]");
  var nextBtn = $("[data-quiz-next]");
  var KEYS = ["أ", "ب", "ج", "د"];
  var qs = [], i = 0, score = 0, answers = [];

  function shuffle(a) {
    a = a.slice();
    for (var k = a.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)); var t = a[k]; a[k] = a[j]; a[j] = t; }
    return a;
  }
  function showBest() {
    var best = M.store.get("quiz-best", null);
    var el = $("[data-best]");
    if (best !== null) { el.hidden = false; el.textContent = "أفضل نتيجة سابقة لك: " + best + " من " + all.length; }
  }

  function begin() {
    var doShuffle = $("[data-shuffle]").checked;
    qs = (doShuffle ? shuffle(all) : all.slice()).map(function (q) {
      /* خلط الخيارات مع الاحتفاظ بالإجابة الصحيحة */
      var opts = q.options.map(function (t, k) { return { t: t, ok: k === q.answer }; });
      return { q: q.q, opts: doShuffle ? shuffle(opts) : opts, explain: q.explain, page: q.page };
    });
    i = 0; score = 0; answers = [];
    startEl.hidden = true; resultEl.hidden = true; runEl.hidden = false;
    render();
  }

  function render() {
    var q = qs[i];
    $("[data-quiz-count]").textContent = (i + 1) + " من " + qs.length;
    $("[data-quiz-progress]").style.width = (i / qs.length) * 100 + "%";
    $("[data-quiz-score]").textContent = score + " نقطة";
    $("[data-quiz-page]").textContent = "القاعة: " + q.page;
    qEl.textContent = q.q;
    optsEl.innerHTML = "";
    fbEl.className = "quiz__feedback"; fbEl.innerHTML = "";
    nextBtn.disabled = true;
    nextBtn.firstChild.textContent = i === qs.length - 1 ? "عرض النتيجة " : "السؤال التالي ";
    q.opts.forEach(function (o, k) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "option";
      b.innerHTML = '<span class="option__key"></span><span></span>';
      b.children[0].textContent = KEYS[k];
      b.children[1].textContent = o.t;
      b.addEventListener("click", function () { choose(k); });
      optsEl.appendChild(b);
    });
    qEl.focus({ preventScroll: true });
  }

  function choose(k) {
    var q = qs[i], btns = M.$$(".option", optsEl);
    if (btns[0].disabled) return;
    var ok = q.opts[k].ok;
    if (ok) score++;
    answers.push({ q: q.q, ok: ok, right: q.opts.find(function (o) { return o.ok; }).t });
    btns.forEach(function (b, j) {
      b.disabled = true;
      if (q.opts[j].ok) b.classList.add("is-correct");
      else if (j === k) b.classList.add("is-wrong");
    });
    fbEl.innerHTML = "";
    var title = document.createElement("b");
    title.className = ok ? "ok" : "no";
    title.textContent = ok ? "إجابة صحيحة ✓" : "ليست هذه — الإجابة الصحيحة مظلّلة بالأخضر";
    var p = document.createElement("span");
    p.textContent = q.explain;
    fbEl.appendChild(title); fbEl.appendChild(p);
    fbEl.classList.add("is-shown");
    $("[data-quiz-score]").textContent = score + " نقطة";
    nextBtn.disabled = false;
    nextBtn.focus({ preventScroll: true });
  }

  function finish() {
    runEl.hidden = true; resultEl.hidden = false;
    var pct = Math.round((score / qs.length) * 100);
    $("[data-final]").textContent = score;
    var ring = $("[data-ring]");
    ring.style.setProperty("--p", 0);
    requestAnimationFrame(function () {
      var t0 = null;
      (function anim(ts) {
        if (!t0) t0 = ts;
        var pr = Math.min(1, (ts - t0) / 900);
        ring.style.setProperty("--p", pct * pr);
        if (pr < 1) requestAnimationFrame(anim);
      })(performance.now());
    });
    var v = pct >= 90 ? ["مؤرّخ المصمك!", "معرفتك بقصة الاسترداد دقيقة جداً."]
      : pct >= 70 ? ["أحسنت", "تعرف القصة جيداً، وبقيت تفاصيل قليلة."]
      : pct >= 50 ? ["بداية جيدة", "راجع قصة الاسترداد وجولة المصمك ثم أعد المحاولة."]
      : ["الرحلة تستحق جولة أخرى", "ابدأ من قصة الاسترداد، وستجد الإجابات كلها هناك."];
    $("[data-verdict]").textContent = v[0];
    $("[data-verdict-text]").textContent = v[1] + " (" + pct + "٪)";
    var best = M.store.get("quiz-best", 0);
    if (score > best) { M.store.set("quiz-best", score); M.toast("نتيجة جديدة هي الأفضل لك!"); }
    var rev = $("[data-review]");
    rev.innerHTML = "";
    answers.forEach(function (a) {
      var d = document.createElement("div");
      d.className = "review__item " + (a.ok ? "ok" : "no");
      d.innerHTML = '<svg class="icon" aria-hidden="true"><use href="#i-' + (a.ok ? "check" : "x") + '"/></svg><div><b></b><br><span class="muted"></span></div>';
      d.querySelector("b").textContent = a.q;
      d.querySelector(".muted").textContent = "الإجابة: " + a.right;
      rev.appendChild(d);
    });
  }

  $("[data-quiz-begin]").addEventListener("click", begin);
  $("[data-quiz-again]").addEventListener("click", function () { resultEl.hidden = true; startEl.hidden = false; showBest(); });
  nextBtn.addEventListener("click", function () {
    if (i < qs.length - 1) { i++; render(); } else { finish(); }
  });
  root.addEventListener("keydown", function (e) {
    if (runEl.hidden) return;
    var n = parseInt(e.key, 10);
    if (n >= 1 && n <= 4) { var b = M.$$(".option", optsEl)[n - 1]; if (b) b.click(); }
  });
  showBest();
})();
