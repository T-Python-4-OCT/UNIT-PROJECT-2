from django.http import Http404
from .data import PLACES, PROJECTS
from .place_extras import PLACE_EXTRAS


def place_context(slug):
    place = next(
        (item for item in PLACES if item['slug'] == slug),
        None
    )

    if place is None:
        raise Http404('المكان غير موجود')

    place = {
        **place,
        **PLACE_EXTRAS.get(slug, {})
    }

    return {'place': place}


def project_context(slug):
    project = next(
        (item for item in PROJECTS if item['slug'] == slug),
        None
    )

    if project is None:
        raise Http404('المشروع غير موجود')

    related = [
        item for item in PROJECTS
        if item['slug'] != slug
    ][:3]

    return {
        'project': project,
        'related_projects': related
    }
