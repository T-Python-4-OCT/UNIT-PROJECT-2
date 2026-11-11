from . import data_loader


def site_data(request):
    """متغيرات متاحة في كل القوالب (القائمة العلوية والتذييل)."""
    content = data_loader.load_content()
    language = request.COOKIES.get("watan-language", "ar")
    if language not in ("ar", "en"):
        language = "ar"
    return {
        "site": content["site"],
        "nav_eras": content["eras"],
        "nav_cities": content["cities"],
        "current_language": language,
        "current_direction": "ltr" if language == "en" else "rtl",
    }
