from django.urls import reverse

from .data_loader import get_home_features, get_ministries, get_site_content


def nav_ministries(request):
    ministries = get_ministries()
    chatbot_ministries = [
        {
            "name": ministry["name"],
            "icon": ministry["icon"],
            "tagline": ministry["tagline"],
            "minister": ministry.get("minister", ""),
            "category": ministry["category"],
            "summary": ministry["about"],
            "founded": ministry.get("founded", ""),
            "tasks": ministry.get("tasks", []),
            "website": ministry.get("website", ""),
            "url": reverse("ministries:detail", args=[ministry["slug"]]),
        }
        for ministry in ministries
    ]
    return {
        "nav_ministries": ministries,
        "site_content": get_site_content(),
        "home_features": get_home_features(),
        "chatbot_ministries": chatbot_ministries,
    }
