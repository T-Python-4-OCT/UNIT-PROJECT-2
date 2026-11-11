from django.http import Http404
from django.shortcuts import render
from django.utils.translation import get_language
from .data import INDUSTRIES, AWARDS, ACHIEVEMENTS, MILESTONES, AWARD_WINNERS, SECTOR_STORIES, MAP_CITIES, SAUDI_REGIONS
from . import data_en


def _content():
    if get_language() == "en":
        return data_en
    return None


def home(request):
    content = _content()
    industries = content.INDUSTRIES if content else INDUSTRIES
    return render(request, "industry/home.html", {"industries": industries[:4]})


def industry_list(request):
    content = _content()
    return render(request, "industry/industries.html", {"industries": content.INDUSTRIES if content else INDUSTRIES})


def map_view(request):
    content = _content()
    cities = content.MAP_CITIES if content else MAP_CITIES
    regions = content.SAUDI_REGIONS if content else SAUDI_REGIONS
    sectors = sorted({sector for city in cities for sector in city["sectors"]})
    return render(request, "industry/map.html", {
        "cities": cities,
        "regions": regions,
        "sector_options": sectors,
    })


def project_detail(request, project_id):
    content = _content()
    cities = content.MAP_CITIES if content else MAP_CITIES
    project = next((item for item in cities if item["id"] == project_id), None)
    if project is None:
        raise Http404("المشروع غير موجود")
    if project_id == "sakaka":
        if content:
            timeline = [
                {"year": "2019", "title": "Connected to the national grid", "description": "Saudi Vision 2030’s energy transition timeline records Sakaka’s grid connection in 2019.", "source": "Vision 2030 Annual Report 2024", "url": "https://www.vision2030.gov.sa/media/r3ij40wu/en-annual-report-vision2030-2024.pdf"},
                {"year": "2021", "title": "Commercial operation completed · 300 MW", "description": "The 2021 NIDLP annual report records completion of commercial operation at a total capacity of 300 MW.", "source": "Vision 2030 NIDLP Annual Report 2021", "url": "https://www.vision2030.gov.sa/media/icrj1poh/annual-report-2021-en.pdf"},
                {"year": "2021", "title": "Officially inaugurated", "description": "The project page identifies Sakaka as inaugurated in 2021 and the first of its kind under the renewable energy initiative.", "source": "Saudi Vision 2030 · Sakaka Solar Power Plant", "url": "https://www.vision2030.gov.sa/en/explore/projects/sakaka-solar-power-plant"},
            ]
        else:
            timeline = [
                {"year": "2019", "title": "الربط بالشبكة الوطنية", "description": "يسجل تقرير رؤية السعودية 2030 عن تحول الطاقة ربط مشروع سكاكا بالشبكة في عام 2019.", "source": "التقرير السنوي لرؤية 2030 لعام 2024", "url": "https://www.vision2030.gov.sa/media/r3ij40wu/en-annual-report-vision2030-2024.pdf"},
                {"year": "2021", "title": "اكتمال التشغيل التجاري · 300 ميجاواط", "description": "يسجل التقرير السنوي لبرنامج ندلب لعام 2021 اكتمال التشغيل التجاري للمشروع بقدرة إجمالية تبلغ 300 ميجاواط.", "source": "التقرير السنوي لبرنامج ندلب لعام 2021", "url": "https://www.vision2030.gov.sa/media/icrj1poh/annual-report-2021-en.pdf"},
                {"year": "2021", "title": "افتتاح المشروع", "description": "تذكر صفحة المشروع في رؤية السعودية 2030 افتتاح المحطة في عام 2021، بوصفها الأولى من نوعها ضمن مبادرة الطاقة المتجددة.", "source": "رؤية السعودية 2030 · محطة سكاكا للطاقة الشمسية", "url": "https://www.vision2030.gov.sa/ar/explore/projects/sakaka-solar-power-plant"},
            ]
    else:
        timeline = []
    return render(request, "industry/project_detail.html", {"project": project, "timeline": timeline})


def industry_detail(request, slug):
    content = _content()
    industries = content.INDUSTRIES if content else INDUSTRIES
    stories = content.SECTOR_STORIES if content else SECTOR_STORIES
    index = next((i for i, item in enumerate(industries) if item["slug"] == slug), None)
    if index is None:
        raise Http404("القطاع غير موجود")
    industry = industries[index]
    context = {
        "industry": industry,
        "previous_industry": industries[index - 1] if index > 0 else None,
        "next_industry": industries[index + 1] if index + 1 < len(industries) else None,
        **stories.get(slug, {}),
    }
    return render(request, "industry/detail.html", context)


def awards(request):
    content = _content()
    if content:
        return render(request, "industry/awards.html", {
            "awards": content.AWARDS,
            "achievements": content.ACHIEVEMENTS,
            "milestones": content.MILESTONES,
            "award_winners": content.AWARD_WINNERS,
        })
    return render(request, "industry/awards.html", {
        "awards": AWARDS,
        "achievements": ACHIEVEMENTS,
        "milestones": MILESTONES,
        "award_winners": AWARD_WINNERS,
    })


def about(request):
    return render(request, "industry/about.html")
