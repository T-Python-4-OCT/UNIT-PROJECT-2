import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def get_lang(request):
    lang = request.COOKIES.get("lang", "en")
    if lang not in ("en", "ar"):
        lang = "en"
    return lang


def localize(item, lang):
    if lang == "ar":
        return {**item, **item.get("ar", {})}
    return item


def site_text(request):
    lang = get_lang(request)
    text = load_json("text.json")
    return {"t": text[lang], "lang": lang}
