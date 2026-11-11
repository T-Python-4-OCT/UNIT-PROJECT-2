"""Views of the reports app: community reports list, new report, report details."""

import re
from urllib.parse import quote, unquote

from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from main import contacts, json_store
from reports import store
from reports.moderation import ai_review, local_review
from reports.report_types import REPORT_TYPES

PHONE = re.compile(r"^\+?[0-9 ]{7,15}$")
EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

# Cookie with the last 5 searches of this visitor (kept for 30 days)
RECENT_COOKIE = "recent_searches"
RECENT_MAX = 5
RECENT_AGE = 60 * 60 * 24 * 30


def read_recent(request: HttpRequest) -> list[str]:
    """The cookie looks like 0551234567|bit.ly%2Fabc (each value is quoted, then joined with |)."""
    raw = request.COOKIES.get(RECENT_COOKIE, "")
    return [unquote(value) for value in raw.split("|") if value][:RECENT_MAX]


def validate(form: dict) -> list[str]:
    errors = []
    if len(form["title"]) < 5:
        errors.append("اكتب عنوان واضح للبلاغ (5 أحرف على الأقل).")
    if form["type"] not in REPORT_TYPES:
        errors.append("اختر نوع البلاغ.")
    if not form["contact"]:
        errors.append("اكتب رقم أو بريد أو حساب المحتال.")
    elif form["type"] in ("sms", "call") and not PHONE.match(form["contact"]) and not form["contact"].isalpha():
        errors.append("رقم الهاتف غير صحيح (من 7 إلى 15 رقم).")
    elif form["type"] == "email" and not EMAIL.match(form["contact"]):
        errors.append("البريد الإلكتروني غير صحيح.")
    if len(form["description"]) < 20:
        errors.append("اكتب وصف للحالة لا يقل عن 20 حرف، حتى يستفيد غيرك.")
    return errors


def report_list(request: HttpRequest) -> HttpResponse:
    all_reports = json_store.newest_first(store.load_reports())
    selected = request.GET.get("type", "")
    query = request.GET.get("q", "").strip()
    reports = all_reports
    lookup = None

    if selected in REPORT_TYPES:
        reports = [report for report in reports if report["type"] == selected]
    if query:
        # 1) the same phone / email / link, written in any format
        matches = store.find_matches([query], reports)
        # 2) or the words inside the title, description or message
        words = [report for report in reports if report not in matches and
                 (query in report["title"] or query in report["description"] or query in report["message"])]
        reports = matches + words
        lookup = {"value": contacts.clean(query), "times": store.times_reported(matches), "found": bool(matches)}

    for report in reports:
        report["type_info"] = REPORT_TYPES[report["type"]]

    # Put the new search first, without repeating it, and keep only the last 5
    recent = read_recent(request)
    if query:
        value = contacts.clean(query)
        recent = ([value] + [item for item in recent if item != value])[:RECENT_MAX]

    context = {"reports": reports, "types": REPORT_TYPES, "selected": selected, "query": query,
               "lookup": lookup, "total": len(all_reports), "recent": recent,
               "auto_count": len([report for report in all_reports if report["auto"]])}
    response = render(request, "reports/report_list.html", context)
    if query:
        response.set_cookie(RECENT_COOKIE, "|".join(quote(item, safe="") for item in recent),
                            max_age=RECENT_AGE, httponly=True, samesite="Lax")
    return response


def clear_searches(request: HttpRequest) -> HttpResponse:
    """Delete the recent searches cookie, then go back to the reports list."""
    response = redirect("reports:list")
    if request.method == "POST":
        response.delete_cookie(RECENT_COOKIE)
        messages.success(request, "مسحنا آخر عمليات البحث من متصفحك.")
    return response


def new_report(request: HttpRequest) -> HttpResponse:
    form = {"title": "", "type": "sms", "contact": "", "description": "", "message": request.GET.get("message", "")}
    errors = []

    if request.method == "POST":
        form = {key: request.POST.get(key, "").strip() for key in form}
        errors = validate(form)
        if not errors:
            form["type_title"] = REPORT_TYPES[form["type"]]["title"]
            reason = local_review(form["title"], form["description"]) or ai_review(form)
            if reason:
                errors.append(f"ما قدرنا ننشر البلاغ: {reason} عدّله وحاول مرة ثانية.")
            else:
                report = store.add_manual(form)
                messages.success(request, "تم نشر بلاغك، شكراً لأنك تحمي غيرك.")
                return redirect("reports:detail", report_id=report["id"])

    context = {"form": form, "errors": errors, "types": REPORT_TYPES}
    return render(request, "reports/new_report.html", context)


def report_detail(request: HttpRequest, report_id: int) -> HttpResponse:
    reports = store.load_reports()
    report = next((item for item in reports if item["id"] == report_id), None)
    if report is None:
        raise Http404("Report not found")
    report["type_info"] = REPORT_TYPES[report["type"]]
    others = [item for item in store.find_matches(report["contacts"], reports) if item["id"] != report["id"]]
    for item in others:
        item["type_info"] = REPORT_TYPES[item["type"]]
    context = {"report": report, "others": others, "times": report["count"] + store.times_reported(others)}
    return render(request, "reports/report_detail.html", context)
