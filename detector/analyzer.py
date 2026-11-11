"""The fraud detector: local rules + AI opinion = one final result.

1) local_scan()  finds fraud signs with regex and marks them inside the message.
2) ask_ai()      asks the AI model (OpenRouter) for its opinion.
3) analyze()     mixes both into one safety score (0 = fraud, 100 = safe).
If the AI is not available (no key / no internet), the local result is used alone.
"""

import re

from main import ai_client
from detector.rules import DANGER_WEIGHT, DANGEROUS_PAIRS, RULES, SAFE_HINTS

TASHKEEL = re.compile(r"[ً-ْٰـ]")  # harakat + tatweel
LETTER_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي"})

SAFE_FROM = 75        # 75-100 safe
SUSPICIOUS_FROM = 40  # 40-74 suspicious, 0-39 fraud

VERDICTS = {
    "fraud": {"title": "احتيال", "headline": "هذه الرسالة احتيالية", "css": "fraud", "icon": "bi-shield-x"},
    "suspicious": {"title": "مشبوهة", "headline": "هذه الرسالة مشبوهة", "css": "suspicious", "icon": "bi-shield-exclamation"},
    "safe": {"title": "آمنة", "headline": "لم نرصد علامات احتيال", "css": "safe", "icon": "bi-shield-check"},
}

DEFAULT_ADVICE = {
    "fraud": "لا تضغط على أي رابط ولا ترد على المرسل، ولا تشارك أي رمز أو بيانات. احذف الرسالة واحظر الرقم، وإذا شاركت بياناتك تواصل مع بنكك فوراً.",
    "suspicious": "لا تتعامل مع الرسالة قبل ما تتأكد. تواصل مع الجهة من رقمها أو تطبيقها الرسمي، ولا تستخدم أي رابط أو رقم موجود في الرسالة.",
    "safe": "الرسالة لا تحمل علامات احتيال واضحة. مع ذلك لا تشارك رمز التحقق أو كلمة المرور مع أي أحد مهما كان.",
}


def normalize(text: str) -> tuple[str, list[int]]:
    """Make Arabic text easy to match, and remember where each letter came from.

    Returns the clean text and a list: position in clean text -> position in original text.
    """
    clean_chars = []
    positions = []
    for index, char in enumerate(text):
        if TASHKEEL.match(char):
            continue
        clean_chars.append(char.translate(LETTER_MAP).lower())
        positions.append(index)
    return "".join(clean_chars), positions


def is_word_char(char: str) -> bool:
    return char.isalnum() or bool(TASHKEEL.match(char))


def widen_to_word(text: str, start: int, end: int) -> tuple[int, int]:
    """Make the highlight cover whole words (e.g. 'بيانات' inside 'بياناتك')."""
    while start > 0 and is_word_char(text[start - 1]) and is_word_char(text[start]):
        start -= 1
    while end < len(text) and is_word_char(text[end]) and is_word_char(text[end - 1]):
        end += 1
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def verdict_for(score: int) -> str:
    if score >= SAFE_FROM:
        return "safe"
    if score >= SUSPICIOUS_FROM:
        return "suspicious"
    return "fraud"


def local_scan(text: str) -> dict:
    """Find fraud signs. Returns the found rules, the marked spans and a local safety score."""
    clean, positions = normalize(text)
    found = {}
    spans = []

    for rule in RULES:
        for pattern in rule["patterns"]:
            for match in re.finditer(pattern, clean, re.IGNORECASE):
                if match.start() == match.end():
                    continue
                start, end = widen_to_word(text, positions[match.start()], positions[match.end() - 1] + 1)
                spans.append((start, end, rule["key"]))
                found.setdefault(rule["key"], rule)

    # Reassuring words ("do not share it"): kept apart, they are shown in green only if the message is safe
    safe_spans = []
    for pattern in SAFE_HINTS:
        for match in re.finditer(pattern, clean, re.IGNORECASE):
            start, end = widen_to_word(text, positions[match.start()], positions[match.end() - 1] + 1)
            safe_spans.append((start, end, "safe"))

    # A real OTP message says "do not share it" and has no link: that is a warning, not a request
    is_warning_only = bool(safe_spans)
    if "credentials" in found and is_warning_only and not ({"link", "short_link", "fake_domain"} & found.keys()):
        del found["credentials"]
        spans = [span for span in spans if span[2] != "credentials"]

    # A link that is already "short" or "fake" should not also count as a normal link
    if "link" in found and ("short_link" in found or "fake_domain" in found):
        del found["link"]

    risk = sum(rule["weight"] for rule in found.values())
    for first, second in DANGEROUS_PAIRS:
        if first in found and second in found:
            risk += 15
    risk = min(risk, 100)

    return {
        "rules": sorted(found.values(), key=lambda rule: rule["weight"], reverse=True),
        "spans": spans,
        "safe_spans": safe_spans,
        "safety": 100 - risk,
        "has_signature": any(a in found and b in found for a, b in DANGEROUS_PAIRS),
    }


def build_segments(text: str, spans: list[tuple]) -> list[dict]:
    """Cut the message into pieces so the template can highlight the risky parts."""
    titles = {rule["key"]: rule["title"] for rule in RULES}
    titles["ai"] = "رصدها الذكاء الاصطناعي"
    titles["safe"] = "كلام يطمّن: الرسالة تحذّرك وما تطلب منك شيء"
    # How risky each key is: it decides the color when two highlights overlap
    weights = {rule["key"]: rule["weight"] for rule in RULES}
    weights["ai"] = DANGER_WEIGHT  # words the AI quoted are dangerous (red)
    weights["safe"] = 0            # a green word never hides a risky one

    spans = sorted(spans)
    merged = []
    for start, end, key in spans:
        if merged and start < merged[-1][1]:  # overlaps the previous one -> join them, keep the most risky color
            merged[-1][1] = max(merged[-1][1], end)
            if weights[key] > weights[merged[-1][2]]:
                merged[-1][2] = key
        else:
            merged.append([start, end, key])

    segments = []
    cursor = 0
    for start, end, key in merged:
        if start > cursor:
            segments.append({"text": text[cursor:start], "flag": None})
        segments.append({"text": text[start:end], "flag": key, "title": titles[key]})
        cursor = end
    if cursor < len(text):
        segments.append({"text": text[cursor:], "flag": None})
    return segments


AI_SYSTEM = (
    "You are «احذر», a senior fraud analyst for Saudi Arabia. You know the scams that target people in Saudi: "
    "fake bank alerts (Al Rajhi, SNB, Riyad Bank...), fake Absher / traffic fines / Saudi Post / Aramex / SMSA messages, "
    "fake prizes, job and investment scams, fake charity, romance and WhatsApp impersonation. "
    "You are careful: real banks DO send transaction alerts and OTP codes, and those are SAFE when they only inform "
    "and ask for nothing. You answer ONLY with one JSON object, all text in clear Gulf-friendly Modern Standard Arabic."
)

AI_EXAMPLES = """
Calibration examples (do not copy the text, copy the judgment):
1) "تم خصم 150 ريال من بطاقتك مدى المنتهية بـ 4321 لدى مطعم البيك" -> safety 95 (normal bank alert, no request).
2) "رمز التحقق 482910 لا تشاركه مع أحد" -> safety 92 (real OTP notice that warns you).
3) "تم إيقاف بطاقتك، حدّث بياناتك عبر alrajhi-update.com وأرسل رمز التحقق" -> safety 3 (impersonation + fake link + OTP theft).
4) "شحنتك معلقة، ادفع 12 ريال عبر الرابط" -> safety 10 (fake delivery fee).
5) "هلا، أنا أخوك هذا رقمي الجديد، حوّل لي 2000 بسرعة" -> safety 12 (family impersonation + urgent money).
6) "موعدك في المستشفى الأحد 10 صباحاً" -> safety 97 (normal reminder).
"""


def ask_ai(text: str, found_titles: list[str]) -> dict:
    """Ask the AI for a full analysis: score, quoted red flags, steps and a report title."""
    hints = "، ".join(found_titles) if found_titles else "لا شيء"
    prompt = f"""
Analyze the message and rate its SAFETY from 0 to 100:
90-100 clearly legitimate, 75-89 probably safe, 40-74 suspicious (needs verification), 0-39 fraud.

Think about: who claims to send it, what it asks the user to DO (click, pay, share a code, call, move to WhatsApp),
urgency or fear, too-good offers, links whose domain is not the official one (official Saudi gov sites end with .gov.sa),
shortened links, and anything that does not fit the claimed sender.
{AI_EXAMPLES}
A rule-based scanner found these signs: {hints}. They are hints only: ignore them if the context makes the message safe.

Return exactly this JSON:
{{
 "safety_score": <integer 0-100>,
 "scam_type": "<short Arabic name, e.g. انتحال بنك وسرقة رمز التحقق، or رسالة عادية>",
 "report_title": "<short Arabic title to warn other people, e.g. رسالة باسم بنك تطلب رمز التحقق>",
 "red_flags": [{{"quote": "<EXACT words copied from the message>", "why": "<short Arabic reason>"}}],
 "reasons": ["<2-4 short Arabic sentences explaining the judgment>"],
 "advice_steps": ["<2-4 short Arabic steps: what to do now>"],
 "if_already_clicked": ["<2-3 short Arabic steps if the user already clicked, paid or shared data; empty list if safe>"]
}}

Message:
\"\"\"{text}\"\"\"
""".strip()
    answer = ai_client.ask_json(AI_SYSTEM, prompt, max_tokens=800)

    def text_list(key: str, limit: int) -> list[str]:
        items = answer.get(key) or []
        return [str(item).strip() for item in items if str(item).strip()][:limit]

    quotes = []
    for flag in answer.get("red_flags") or []:
        if isinstance(flag, dict) and str(flag.get("quote", "")).strip():
            quotes.append({"quote": str(flag["quote"]).strip(), "why": str(flag.get("why", "")).strip()})

    return {
        "safety": max(0, min(100, int(float(answer.get("safety_score", 50))))),
        "scam_type": str(answer.get("scam_type", "")).strip(),
        "report_title": str(answer.get("report_title", "")).strip(),
        "red_flags": quotes[:6],
        "reasons": text_list("reasons", 4),
        "steps": text_list("advice_steps", 4),
        "if_clicked": text_list("if_already_clicked", 3),
    }


DEFAULT_STEPS = {
    "fraud": ["لا تضغط على أي رابط ولا ترد على المرسل.", "لا تشارك رمز التحقق أو بيانات البطاقة مع أي أحد.", "احذف الرسالة واحظر الرقم."],
    "suspicious": ["لا تستخدم أي رابط أو رقم موجود في الرسالة.", "تواصل مع الجهة من تطبيقها أو رقمها الرسمي وتأكد.", "إذا طلبوا منك دفع أو رمز، اعتبرها احتيال."],
    "safe": ["الرسالة تبدو عادية، تعامل معها بشكل طبيعي.", "تذكّر: لا تشارك رمز التحقق أو كلمة المرور مع أي أحد مهما كان."],
}

DEFAULT_IF_CLICKED = [
    "اتصل ببنكك فوراً من رقمه الرسمي واطلب إيقاف البطاقة.",
    "غيّر كلمة مرور حساباتك وفعّل التحقق الثنائي.",
    "قدّم بلاغ احتيال مالي عبر تطبيق أبشر.",
]


# Titles for automatic reports when the AI is not available (first match wins)
REPORT_TITLES = [
    ("credentials", "رسالة تطلب رمز التحقق أو بيانات البطاقة"),
    ("personal_data", "رسالة تطلب تحديث بياناتك الشخصية"),
    ("relative", "انتحال قريب برقم جديد وطلب تحويل"),
    ("prize", "رسالة جائزة وهمية تطلب رسوم"),
    ("too_good", "عرض وظيفة أو استثمار وهمي"),
    ("fake_domain", "رسالة برابط يقلّد جهة رسمية"),
    ("money", "رسالة تطلب دفع رسوم أو تحويل مبلغ"),
    ("short_link", "رسالة برابط مختصر مشبوه"),
    ("threat", "رسالة تهدد بإيقاف الحساب أو بغرامة"),
    ("off_channel", "طلب تواصل خارج القنوات الرسمية"),
]


def rules_report_title(rules: list[dict]) -> str:
    keys = {rule["key"] for rule in rules}
    for key, title in REPORT_TITLES:
        if key in keys:
            return title
    return "رسالة مشبوهة"


def ai_spans(text: str, red_flags: list[dict]) -> list[tuple]:
    """Find the words the AI quoted inside the message, so we can highlight them too."""
    spans = []
    for flag in red_flags:
        start = text.find(flag["quote"])
        if start != -1 and len(flag["quote"]) >= 3:
            spans.append((start, start + len(flag["quote"]), "ai"))
    return spans


def analyze(text: str) -> dict:
    """Run the full detector and return everything the result page needs."""
    local = local_scan(text)
    found_titles = [rule["title"] for rule in local["rules"]]

    try:
        ai = ask_ai(text, found_titles)
    except (ai_client.AIError, ValueError, TypeError):
        ai = None

    if ai:
        score = round(ai["safety"] * 0.65 + local["safety"] * 0.35)
        source = "ai"
    else:
        score = local["safety"]
        source = "rules"

    # A classic scam signature (e.g. OTP request + link) can never be "safe"
    if local["has_signature"]:
        score = min(score, 30)

    verdict = verdict_for(score)
    spans = local["spans"] + (ai_spans(text, ai["red_flags"]) if ai else [])
    if verdict == "safe":
        spans += local["safe_spans"]  # green words, only when the message is safe
    scam_type = ai["scam_type"] if ai and ai["scam_type"] else (local["rules"][0]["title"] if local["rules"] else "رسالة عادية")

    return {
        "text": text,
        "score": score,
        "verdict": verdict,
        "scam_type": scam_type,
        "report_title": ai["report_title"] if ai and ai["report_title"] else rules_report_title(local["rules"]),
        # Without AI the flags already explain everything, so "reasons" stays empty (no repeating)
        "reasons": ai["reasons"] if ai else [],
        "ai_flags": ai["red_flags"] if ai else [],
        "steps": ai["steps"] if ai and ai["steps"] else DEFAULT_STEPS[verdict],
        "if_clicked": (ai["if_clicked"] if ai and ai["if_clicked"] else DEFAULT_IF_CLICKED) if verdict != "safe" else [],
        "advice": " ".join(ai["steps"]) if ai and ai["steps"] else DEFAULT_ADVICE[verdict],
        "flags": [{"key": rule["key"], "title": rule["title"], "explain": rule["explain"]} for rule in local["rules"]],
        "segments": build_segments(text, spans),
        "source": source,
    }
