"""Read the text of an uploaded PDF and analyze it with the user's question."""

import re

import pymupdf

from main import ai_client
from detector.analyzer import DEFAULT_ADVICE, local_scan, verdict_for

MAX_CHARS = 4000
ARABIC = re.compile(r"[\u0600-\u06FF]")
# PDFs often break the "لأ" letters into the wrong order (األ instead of الأ)
LAM_ALEF_FIX = {"األ": "الأ", "اإل": "الإ", "اآل": "الآ"}


class PDFError(Exception):
    pass


def page_lines(page) -> list[str]:
    """Rebuild every line from its words, right-to-left for Arabic lines.

    PDF files store Arabic in "visual" order, so reading them directly gives
    the words backwards. We use each word's position to put them back in order.
    """
    lines = {}
    for x0, y0, x1, y1, word, block, line, _ in page.get_text("words"):
        lines.setdefault((block, line), []).append((x1, word))

    result = []
    for words in lines.values():
        is_arabic = any(ARABIC.search(word) for _, word in words)
        words.sort(key=lambda item: item[0], reverse=is_arabic)
        result.append(" ".join(word for _, word in words))
    return result


def extract_text(uploaded_file) -> str:
    try:
        document = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
    except (pymupdf.FileDataError, RuntimeError, ValueError) as error:
        raise PDFError("تعذّر قراءة الملف. تأكد إنه ملف PDF سليم.") from error

    if document.needs_pass:
        raise PDFError("الملف محمي بكلمة مرور، افتح الحماية وارفعه مرة ثانية.")

    text = ""
    for page in document:
        text += "\n".join(page_lines(page)) + "\n"
        if len(text) >= MAX_CHARS:
            break
    document.close()

    for wrong, right in LAM_ALEF_FIX.items():
        text = text.replace(wrong, right)
    text = text.strip()
    if not text:
        raise PDFError("الملف ما فيه نص قابل للقراءة (ممكن يكون صور ممسوحة ضوئياً).")
    return text[:MAX_CHARS]


def analyze_pdf(text: str, question: str, page_count_note: str = "") -> dict:
    local = local_scan(text)
    try:
        answer = ai_client.ask_json(
            "You are a professional forensic document analyst. Answer ONLY with a JSON object, Arabic text inside.",
            f"""
The user asks about this document: "{question}"

Rate how TRUSTWORTHY / SAFE the document is for the user's question, 0-100
(85-100 legitimate, 50-84 needs review, 0-49 suspicious or fraudulent).

Return JSON:
{{"safety_score": 0-100,
 "answer": "direct Arabic answer to the user's question in 1-2 sentences",
 "evidence": ["2 or 3 specific Arabic points from the document"],
 "recommendation": "one practical Arabic recommendation"}}

Document:
\"\"\"{text}\"\"\"
""".strip(),
            max_tokens=600,
        )
        score = max(0, min(100, int(float(answer.get("safety_score", 50)))))
        source = "ai"
        reply = str(answer.get("answer", "")).strip()
        evidence = [str(item).strip() for item in answer.get("evidence", []) if str(item).strip()][:3]
        recommendation = str(answer.get("recommendation", "")).strip()
    except ai_client.AIError:
        score = local["safety"]
        source = "rules"
        reply = "تم فحص نص المستند بالقواعد المحلية فقط، لأن خدمة الذكاء الاصطناعي غير متاحة الآن."
        evidence = [rule["explain"] for rule in local["rules"][:3]] or ["لم نجد في النص علامات احتيال معروفة."]
        recommendation = DEFAULT_ADVICE[verdict_for(score)]

    if local["has_signature"]:
        score = min(score, 30)

    return {
        "score": score,
        "verdict": verdict_for(score),
        "answer": reply,
        "evidence": evidence,
        "recommendation": recommendation,
        "flags": [{"key": rule["key"], "title": rule["title"]} for rule in local["rules"]],
        "source": source,
        "excerpt": text[:600],
    }
