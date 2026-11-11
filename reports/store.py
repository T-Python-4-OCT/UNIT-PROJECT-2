"""Community reports: save, match and auto-publish (all in data/reports.json)."""

from datetime import datetime

from main import contacts, json_store

FILE = "reports"


def load_reports() -> list[dict]:
    reports = json_store.load(FILE)
    for report in reports:  # older reports may miss these fields
        report.setdefault("contacts", [contacts.clean(report["contact"])] if report.get("contact") else [])
        report.setdefault("count", 1)
        report.setdefault("auto", False)
    return reports


def find_matches(values: list[str], reports: list[dict] | None = None) -> list[dict]:
    """Reports that share at least one phone / email / link with the given values."""
    wanted = {contacts.clean(value) for value in values if value}
    if not wanted:
        return []
    reports = load_reports() if reports is None else reports
    return [report for report in reports if wanted & set(report["contacts"])]


def times_reported(matches: list[dict]) -> int:
    return sum(report["count"] for report in matches)


def guess_type(found: dict) -> str:
    if found["emails"] and not found["phones"]:
        return "email"
    return "sms"


def auto_report(result: dict) -> dict:
    """Publish a warning from a detector result, or add +1 to an existing report of the same scammer."""
    found = contacts.find_contacts(result["text"])
    values = contacts.all_contacts(found)
    reports = load_reports()

    same = [report for report in reports
            if report["message"] == result["text"] or (values and set(values) & set(report["contacts"]))]
    if same:
        report = same[0]
        report["count"] += 1
        report["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        report["contacts"] = list(dict.fromkeys(report["contacts"] + values))
        json_store.save(FILE, reports)
        report["is_new"] = False
        return report

    flags = "، ".join(flag["title"] for flag in result["flags"][:4]) or "علامات احتيال"
    report = json_store.add(FILE, {
        "title": result.get("report_title") or result["scam_type"],
        "type": guess_type(found),
        "contact": values[0] if values else "بدون رقم أو رابط",
        "contacts": values,
        "description": f"رسالة رصدها كاشف احذر بنسبة أمان {result['score']}٪. العلامات: {flags}.",
        "message": result["text"],
        "count": 1,
        "auto": True,
        "verdict": result["verdict"],
    })
    report["is_new"] = True
    return report


def add_manual(form: dict) -> dict:
    values = [contacts.clean(form["contact"])] + contacts.all_contacts(contacts.find_contacts(form["message"]))
    return json_store.add(FILE, {
        "title": form["title"], "type": form["type"], "contact": form["contact"],
        "contacts": list(dict.fromkeys(value for value in values if value)),
        "description": form["description"], "message": form["message"], "count": 1, "auto": False,
    })
