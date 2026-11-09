"""Views of the detector app: check a message and show the result."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main import ai_client
from detector.analyzer import VERDICTS, analyze

MIN_LENGTH = 10
MAX_LENGTH = 2000


def detector_home(request: HttpRequest) -> HttpResponse:
    """GET: show the form. POST: analyze the message and show the result."""
    context = {
        "mode": "text",
        "text": "",
        "ai_ready": ai_client.is_ready(),
    }

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        context["text"] = text

        if len(text) < MIN_LENGTH:
            context["error"] = f"النص قصير، الصق الرسالة كاملة ({MIN_LENGTH} أحرف على الأقل)."
        elif len(text) > MAX_LENGTH:
            context["error"] = f"النص طويل، الحد الأقصى {MAX_LENGTH} حرف."
        else:
            result = analyze(text)
            context["result"] = result
            context["verdict"] = VERDICTS[result["verdict"]]

    return render(request, "detector/detector.html", context)
