"""Check that a community report is serious before we publish it (like the mobile app)."""

import re

from main import ai_client

JOKE_WORDS = re.compile(r"(ههه|هههه|تجربه|تجربة|تجريب|test|testing|asdf|لول)", re.IGNORECASE)


def local_review(title: str, description: str) -> str | None:
    """Return a reason if the report is clearly not serious, else None."""
    if JOKE_WORDS.search(title) or JOKE_WORDS.search(description):
        return "البلاغ فيه كلمات تجربة أو مزاح."
    if len(set(description.replace(" ", ""))) < 6:
        return "الوصف ما فيه تفاصيل مفهومة."
    return None


def ai_review(report: dict) -> str | None:
    """Ask the AI if the report is clear and useful. Return a reason if rejected, else None."""
    prompt = f"""
You review Arabic community reports about scam messages. Do NOT judge whether it is a scam,
only whether the report is serious, clear and useful for other people.
Return JSON: {{"accepted": true/false, "reason": "short Arabic reason if rejected, else empty"}}

Report:
- Title: {report["title"]}
- Type: {report["type_title"]}
- Contact (number / email / account): {report["contact"]}
- Description: {report["description"]}
- Scam message text: {report["message"]}
""".strip()
    try:
        answer = ai_client.ask_json("You are a careful content moderator. Answer ONLY with JSON.", prompt, 150)
    except ai_client.AIError:
        return None  # AI not available: we trust the local review
    if answer.get("accepted") is False:
        return str(answer.get("reason") or "البلاغ غير واضح أو غير مكتمل.")
    return None
