import json
from pathlib import Path

from django.shortcuts import render, redirect, resolve_url
from django.http import HttpRequest
from django.utils.http import url_has_allowed_host_and_scheme


DATA_FILE = Path(__file__).resolve().parent / 'data' / 'projects.json'


def load_projects():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def home(request: HttpRequest):
    projects = load_projects()
    return render(request, 'projects/home.html', {'projects': projects})


def all_projects(request: HttpRequest):
    projects = load_projects()
    categories = sorted({project['category'] for project in projects})

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')

    if q:
        text = q.lower()
        projects = [
            project for project in projects
            if text in project['name'].lower()
            or text in project['location'].lower()
            or text in project['category'].lower()
        ]

    if category:
        projects = [project for project in projects if project['category'] == category]

    context = {
        'projects': projects,
        'categories': categories,
        'q': q,
        'category': category,
    }
    return render(request, 'projects/all_projects.html', context)


def project_detail(request: HttpRequest, project_slug):
    return render(request, 'projects/project_detail.html', {'project_slug': project_slug})


def about(request: HttpRequest):
    return render(request, 'projects/about.html')


def set_theme(request: HttpRequest, theme):
    if theme not in ('light', 'dark'):
        theme = 'light'

    next_url = request.GET.get('next')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = resolve_url('projects:home')

    response = redirect(next_url)
    response.set_cookie('site_theme', theme, max_age=60 * 60 * 24 * 365)
    return response