
from django.shortcuts import render
from django.http import Http404
from pathlib import Path
import json


def home(request):
    return render(request, 'main/home.html')


def history(request):
    return render(request, 'main/history.html')


def companies(request):
    return render(request, 'main/companies.html')


def vision(request):
    return render(request, 'main/vision.html')


def about(request):
    return render(request, 'main/about.html')


def sectors(request):
    return render(request, 'main/sectors.html')


def sector_detail(request, sector_slug):
    json_path = Path(__file__).resolve().parent / 'data' / 'sectors.json'

    with open(json_path, 'r', encoding='utf-8') as file:
        sectors_data = json.load(file)

    sector = sectors_data.get(sector_slug)

    if sector is None:
        raise Http404('القطاع غير موجود')

    return render(request, 'main/sector_detail.html', {
        'sector': sector
    })
