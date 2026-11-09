"""Views of the reports app: community reports list and report details."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from main import json_store
from reports import store
from reports.report_types import REPORT_TYPES


def report_list(request: HttpRequest) -> HttpResponse:
    all_reports = json_store.newest_first(store.load_reports())
    selected = request.GET.get("type", "")
    reports = all_reports

    if selected in REPORT_TYPES:
        reports = [report for report in reports if report["type"] == selected]

    for report in reports:
        report["type_info"] = REPORT_TYPES[report["type"]]

    context = {"reports": reports, "types": REPORT_TYPES, "selected": selected, "total": len(all_reports),
               "auto_count": len([report for report in all_reports if report["auto"]])}
    return render(request, "reports/report_list.html", context)


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
