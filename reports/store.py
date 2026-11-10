"""Community reports: save and match (all in data/reports.json)."""

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


def add_manual(form: dict) -> dict:
    values = [contacts.clean(form["contact"])] + contacts.all_contacts(contacts.find_contacts(form["message"]))
    return json_store.add(FILE, {
        "title": form["title"], "type": form["type"], "contact": form["contact"],
        "contacts": list(dict.fromkeys(value for value in values if value)),
        "description": form["description"], "message": form["message"], "count": 1, "auto": False,
    })
