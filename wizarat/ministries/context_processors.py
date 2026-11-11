from django.urls import reverse

from .data_loader import get_all_ministries, get_home_features, get_site_content


def nav_ministries(request):
    ministries = get_all_ministries()
    nav_ministries = [ministry for ministry in ministries if ministry.get("detail_slug")]
    chatbot_ministries = []
    for ministry in ministries:
        has_detail = bool(ministry.get("detail_slug"))
        chatbot_ministries.append(
            {
                "name": ministry["name"],
                "category": ministry["category"],
                "summary": ministry.get("about") or ministry["summary"],
                "founded": ministry.get("founded", ""),
                "tasks": ministry.get("tasks", []),
                "website": ministry.get("website", ""),
                "url": reverse(
                    "ministries:detail",
                    args=[ministry["detail_slug"]],
                )
                if has_detail
                else reverse("ministries:directory"),
            }
        )
    return {
        "nav_ministries": nav_ministries,
        "site_content": get_site_content(),
        "home_features": get_home_features(),
        "chatbot_ministries": chatbot_ministries,
    }