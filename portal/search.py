"""
Site search over the JSON content.

Arabic text is normalized before matching, so a search for "اداره" also
finds "إدارة" (different alef and ta marbuta forms, and diacritics).
"""

import re

from django.utils.html import escape
from django.utils.safestring import mark_safe

# Diacritics (tashkeel) and tatweel are dropped when matching.
ARABIC_MARKS = re.compile(r"[ؐ-ًؚ-ٰٟـ]")

# One-to-one letter swaps, so each normalized character still lines up
# with one original character (needed to highlight the right text).
LETTER_SWAPS = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ة": "ه", "ى": "ي"})

SNIPPET_RADIUS = 70
MAX_RESULTS = 20


def normalize(text):
    "Lowercase, remove Arabic diacritics, and unify letter forms."
    return ARABIC_MARKS.sub("", text).translate(LETTER_SWAPS).lower()


def normalize_with_positions(text):
    "Normalize text and remember which original character each result char came from."
    characters, positions = [], []

    for index, char in enumerate(text):
        if ARABIC_MARKS.match(char):
            continue
        characters.append(char.translate(LETTER_SWAPS).lower())
        positions.append(index)

    return "".join(characters), positions


def make_snippet(text, query):
    """
    Return a short, HTML-escaped piece of text around the first match,
    with the match wrapped in <mark>. Returns None when there is no match.
    """
    normalized, positions = normalize_with_positions(text)
    found = normalized.find(query)

    if found == -1:
        return None

    start = positions[found]
    end = positions[found + len(query) - 1] + 1

    snippet_start = max(0, start - SNIPPET_RADIUS)
    snippet_end = min(len(text), end + SNIPPET_RADIUS)

    before = ("…" if snippet_start > 0 else "") + text[snippet_start:start]
    after = text[end:snippet_end] + ("…" if snippet_end < len(text) else "")

    # Escape every piece of content first; only our own <mark> tag is trusted.
    return mark_safe(f"{escape(before)}<mark>{escape(text[start:end])}</mark>{escape(after)}")


def page_texts(page):
    "Yield (weight, text) pairs for one page. Titles count more than body text."
    yield 5, page.get("title", "")
    yield 3, page.get("subtitle", "")
    yield 2, page.get("intro", "")

    for section in page.get("sections", []):
        yield 3, section.get("heading", "")
        yield 1, section.get("note", "")

        for item in section.get("items", []):
            yield 3, item.get("title", "")
            yield 2, item.get("label", "")
            yield 1, item.get("text", "")
            yield 1, item.get("value", "")
            yield 1, item.get("date", "")


def search_pages(pages, query):
    """
    pages: list of (slug, page_content) pairs.
    Returns results sorted by score, best first.
    """
    query = normalize(query)
    results = []

    for slug, page in pages:
        score = 0
        snippet = None

        for weight, text in page_texts(page):
            if not text:
                continue

            matches = normalize(text).count(query)
            if matches:
                score += weight * matches
                # Show a snippet from the body when possible, not just the title.
                if snippet is None and text != page.get("title"):
                    snippet = make_snippet(text, query)

        if score:
            results.append({
                "slug": slug,
                "title": page["title"],
                "snippet": snippet or make_snippet(page["title"], query),
                "score": score,
            })

    results.sort(key=lambda result: result["score"], reverse=True)
    return results[:MAX_RESULTS]
