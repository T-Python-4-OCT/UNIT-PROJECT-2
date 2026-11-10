from .data_loader import get_ministries, get_site_content


def nav_ministries(request):
    return {
        "nav_ministries": get_ministries(),
        "site_content": get_site_content(),
    }