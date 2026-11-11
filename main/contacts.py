"""Find phone numbers, emails and links inside a text, in one clean format.

We clean them so the same scammer is found even if people write the number differently:
"+966 55 123 4567", "00966551234567" and "0551234567" all become "0551234567".
"""

import re

PHONE = re.compile(r"(?:\+|00)?(?:966)?[\s-]?0?5\d(?:[\s-]?\d){7}\b|\b9200(?:[\s-]?\d){5}\b|\b800(?:[\s-]?\d){7}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
LINK = re.compile(r"(?:https?://)?(?:www\.)?((?:[a-z0-9-]+\.)+[a-z]{2,})(/[^\s،,]*)?", re.IGNORECASE)
# For short links the path matters (bit.ly/abc and bit.ly/xyz are different scammers)
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "cutt.ly", "goo.gl", "is.gd", "rb.gy", "shorturl.at", "t.ly", "wa.me"}


def clean_link(domain: str, path: str) -> str:
    domain = domain.lower()
    if domain in SHORTENERS and path:
        return (domain + path.rstrip("/.")).lower()
    return domain


def clean_phone(text: str) -> str:
    digits = re.sub(r"\D", "", text)
    if digits.startswith("00966"):
        digits = digits[5:]
    elif digits.startswith("966"):
        digits = digits[3:]
    if digits.startswith("5") and len(digits) == 9:
        digits = "0" + digits
    return digits


def clean(value: str) -> str:
    """Clean any single contact (phone, email or link) the user typed."""
    value = value.strip().lower()
    if EMAIL.fullmatch(value):
        return value
    if PHONE.fullmatch(value) or re.fullmatch(r"[\d\s+()-]{7,}", value):
        return clean_phone(value)
    link = LINK.fullmatch(value)
    if link:
        return clean_link(link.group(1), link.group(2) or "")
    return value.lstrip("@")


def find_contacts(text: str) -> dict:
    """Return the phones, emails and link domains found in a text (no duplicates)."""
    emails = list(dict.fromkeys(match.lower() for match in EMAIL.findall(text)))
    text_without_emails = EMAIL.sub(" ", text)
    phones = list(dict.fromkeys(clean_phone(match) for match in PHONE.findall(text_without_emails)))
    links = list(dict.fromkeys(clean_link(domain, path) for domain, path in LINK.findall(text_without_emails)))
    return {"phones": phones, "emails": emails, "links": links}


def all_contacts(found: dict) -> list[str]:
    return found["phones"] + found["emails"] + found["links"]
