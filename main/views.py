"""Views of the main app: home, guide, FAQ and feedback."""

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from main import json_store
from main.content import CHANNELS, FAQ, FEEDBACK_TAGS, SCAM_TYPES, TIPS


def home(request: HttpRequest) -> HttpResponse:
    # The context is a dictionary: every key becomes a variable in the template
    context = {"name": "احذر", "slogan": "قبل ما تضغط… احذر."}
    return render(request, "main/home.html", context)


def guide(request: HttpRequest) -> HttpResponse:
    context = {"tips": TIPS, "scam_types": SCAM_TYPES, "channels": CHANNELS}
    return render(request, "main/guide.html", context)


def faq(request: HttpRequest) -> HttpResponse:
    return render(request, "main/faq.html", {"faq": FAQ})


def feedback(request: HttpRequest) -> HttpResponse:
    form = {"rating": "", "tag": "", "text": ""}
    errors = []

    if request.method == "POST":
        form = {
            "rating": request.POST.get("rating", ""),
            "tag": request.POST.get("tag", ""),
            "text": request.POST.get("text", "").strip(),
        }
        if form["rating"] not in ("1", "2", "3", "4", "5"):
            errors.append("اختر تقييمك من 1 إلى 5 نجوم.")
        if form["tag"] not in FEEDBACK_TAGS:
            errors.append("اختر الشيء اللي تبي نحسّنه.")
        if len(form["text"]) < 5:
            errors.append("اكتب رأيك في 5 أحرف على الأقل.")

        if not errors:
            json_store.add("feedback", {"rating": int(form["rating"]), "tag": form["tag"], "text": form["text"]})
            messages.success(request, "وصلنا رأيك، شكراً لك.")
            return redirect("main:feedback")

    all_feedback = json_store.load("feedback")
    average = round(sum(item["rating"] for item in all_feedback) / len(all_feedback), 1) if all_feedback else 0
    context = {
        "form": form,
        "errors": errors,
        "tags": FEEDBACK_TAGS,
        "stars": [5, 4, 3, 2, 1],
        "average": average,
        "feedback_count": len(all_feedback),
        "latest_feedback": json_store.newest_first(all_feedback)[:4],
    }
    return render(request, "main/feedback.html", context)
