"""
العروض (Views) — رفيعة عمداً: كل منطق تجهيز المحتوى في main/content.py
(بايثون خالص بلا قاعدة بيانات)، والعرض يمرّر السياق إلى القالب فقط.
"""
from django.http import Http404
from django.shortcuts import render

from . import content


def home(request):
    return render(request, "main/home.html", content.home_context())


def old_riyadh(request):
    return render(request, "main/old_riyadh.html", content.old_riyadh_context())


def king(request):
    return render(request, "main/king.html", content.king_context())


def participants(request):
    return render(request, "main/participants.html", content.participants_context())


def person_detail(request, slug):
    try:
        ctx = content.person_context(slug)
    except KeyError:
        raise Http404("لا يوجد مشارك بهذا المعرّف")
    return render(request, "main/person_detail.html", ctx)


def story(request):
    return render(request, "main/story.html", content.story_context())


def chapter_detail(request, slug):
    try:
        ctx = content.chapter_context(slug)
    except KeyError:
        raise Http404("لا يوجد فصل بهذا المعرّف")
    return render(request, "main/chapter_detail.html", ctx)


def tour(request):
    return render(request, "main/tour.html", content.tour_context())


def timeline(request):
    return render(request, "main/timeline.html", content.timeline_context())


def museum(request):
    return render(request, "main/museum.html", content.museum_context())


def quiz(request):
    return render(request, "main/quiz.html", content.quiz_context())
