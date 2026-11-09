"""Views of the detector app: check a message, check a PDF, and the checks history."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from main import ai_client, json_store
from detector.analyzer import VERDICTS, analyze
from detector.pdf_reader import PDFError, analyze_pdf, extract_text

MIN_LENGTH = 10
MAX_LENGTH = 2000


def detector_home(request: HttpRequest) -> HttpResponse:
    """GET: show the form. POST: analyze the message and show the result."""
    context = {
        "mode": "text",
        "text": request.GET.get("text", ""),
        "ai_ready": ai_client.is_ready(),
        "save_on": True,
    }

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        save = request.POST.get("save") == "on"
        context["text"] = text
        context["save_on"] = save

        if len(text) < MIN_LENGTH:
            context["error"] = f"النص قصير، الصق الرسالة كاملة ({MIN_LENGTH} أحرف على الأقل)."
        elif len(text) > MAX_LENGTH:
            context["error"] = f"النص طويل، الحد الأقصى {MAX_LENGTH} حرف. للمستندات الطويلة استخدم فحص PDF."
        else:
            result = analyze(text)

            if save:
                saved = json_store.add("checks", {
                    key: result[key] for key in ("text", "score", "verdict", "scam_type", "reasons", "steps",
                                                 "if_clicked", "advice", "flags", "ai_flags", "segments", "source")
                })
                result["id"] = saved["id"]
            context["result"] = result
            context["verdict"] = VERDICTS[result["verdict"]]

    return render(request, "detector/detector.html", context)


def check_pdf(request: HttpRequest) -> HttpResponse:
    context = {"mode": "pdf", "ai_ready": ai_client.is_ready(), "question": ""}

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        uploaded = request.FILES.get("pdf")
        context["question"] = question

        if uploaded is None:
            context["pdf_error"] = "اختر ملف PDF أولاً."
        elif not uploaded.name.lower().endswith(".pdf"):
            context["pdf_error"] = "الملف لازم يكون بصيغة PDF."
        elif len(question) < 5:
            context["pdf_error"] = "اكتب سؤالك عن الملف (5 أحرف على الأقل)."
        else:
            try:
                text = extract_text(uploaded)
            except PDFError as error:
                context["pdf_error"] = str(error)
            else:
                result = analyze_pdf(text, question)
                result["file_name"] = uploaded.name
                context["pdf_result"] = result
                context["verdict"] = VERDICTS[result["verdict"]]

    return render(request, "detector/detector.html", context)


def history(request: HttpRequest) -> HttpResponse:
    checks = json_store.newest_first(json_store.load("checks"))
    selected = request.GET.get("verdict", "")
    filters = []
    for key, info in VERDICTS.items():
        count = len([check for check in checks if check["verdict"] == key])
        filters.append({"key": key, "title": info["title"], "css": info["css"], "count": count})
    if selected in VERDICTS:
        checks = [check for check in checks if check["verdict"] == selected]

    for check in checks:
        check["verdict_info"] = VERDICTS[check["verdict"]]

    context = {"checks": checks, "selected": selected, "filters": filters}
    return render(request, "detector/history.html", context)


def check_detail(request: HttpRequest, check_id: int) -> HttpResponse:
    check = json_store.get("checks", check_id)
    if check is None:
        raise Http404("Check not found")
    context = {"result": check, "verdict": VERDICTS[check["verdict"]], "from_history": True}
    return render(request, "detector/check_detail.html", context)
