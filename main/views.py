"""Views of the main app: home, guide, FAQ and feedback."""

from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from main import json_store
from detector.analyzer import build_segments, local_scan
from detector.rules import RULES
from reports import store
from reports.report_types import REPORT_TYPES
from main.content import CHANNELS, FAQ, FEEDBACK_TAGS, SCAM_TYPES, STORIES, TIPS, VIDEO_TRANSCRIPT


HERO_SAMPLE = "عميلنا العزيز، سيتم إيقاف حسابك خلال 24 ساعة. حدّث بياناتك عبر alrajhi-update.com وأرسل رمز التحقق."


def with_highlights(text: str) -> dict:
    """Run the real scanner on a sample text so the page shows real highlights."""
    scan = local_scan(text)
    return {"segments": build_segments(text, scan["spans"]), "flags": scan["rules"], "safety": scan["safety"]}


def home(request: HttpRequest) -> HttpResponse:
    samples = []
    for scam in SCAM_TYPES:
        samples.append({**scam, **with_highlights(scam["sample"])})

    checks = json_store.load("checks")
    reports = json_store.newest_first(store.load_reports())
    for report in reports:
        report["type_info"] = REPORT_TYPES[report["type"]]
    context = {
        "hero": with_highlights(HERO_SAMPLE),
        "samples": samples,
        "stories": STORIES,
        "transcript": VIDEO_TRANSCRIPT,
        "auto_count": len([report for report in reports if report["auto"]]),
        "channels": CHANNELS,
        "latest_reports": reports[:3],
        "checks_count": len(checks),
        "fraud_count": len([check for check in checks if check["verdict"] == "fraud"]),
        "reports_count": len(reports),
        "patterns_count": sum(len(rule["patterns"]) for rule in RULES),
    }
    return render(request, "main/home.html", context)


def guide(request: HttpRequest) -> HttpResponse:
    context = {"tips": TIPS, "scam_types": SCAM_TYPES, "channels": CHANNELS, "rules": RULES}
    return render(request, "main/guide.html", context)


def scam_detail(request: HttpRequest, scam_key: str) -> HttpResponse:
    """Path parameter: for /guide/bank/ Django sends scam_key = "bank" to this view."""
    scam = next((item for item in SCAM_TYPES if item["key"] == scam_key), None)
    if scam is None:
        raise Http404("Scam type not found")
    others = [item for item in SCAM_TYPES if item["key"] != scam_key]
    context = {"scam": scam, "others": others, **with_highlights(scam["sample"])}
    return render(request, "main/scam_detail.html", context)


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
