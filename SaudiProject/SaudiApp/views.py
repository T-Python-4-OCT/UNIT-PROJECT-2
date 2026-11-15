
from django.shortcuts import render


def home(request):
    return render(request, 'SaudiApp/home.html')


def kingdom(request):
    return render(request, 'SaudiApp/kingdom.html', {
        'section': 'المملكة وتاريخها',
        'section_class': 'kingdom-page',
        'eyebrow': 'جذور راسخة ومجد متجدد',
        'description': 'من جذور الدولة السعودية الأولى إلى المملكة العربية السعودية الحديثة، رحلة وطن امتدت عبر ثلاثة قرون من التاريخ والعزيمة.',
    })


def tourism_entertainment(request):
    return render(request, 'SaudiApp/section.html', {
        'section': 'السياحة والترفيه',
        'section_class': 'tourism-entertainment-page',
        'eyebrow': 'وجهات تلهم وتجارب لا تُنسى',
        'description': 'اكتشف تنوع المملكة بين الوجهات السياحية الساحرة والتجارب الترفيهية والفعاليات التي تصنع لحظات استثنائية.',
    })


def sports(request):
    return render(request, 'SaudiApp/section.html', {
        'section': 'الرياضة',
        'section_class': 'sports-page'
    })


def culture(request):
    return render(request, 'SaudiApp/culture.html', {
        'section': 'الثقافة والمعرفة',
        'section_class': 'culture-page'
    })


def red_sea(request):
    return render(request, 'SaudiApp/red_sea.html')

def alula(request):
    return render(request, 'SaudiApp/alula.html')

def diriyah(request):
    return render(request, 'SaudiApp/diriyah.html')

def al_ahsa(request):
    return render(request, 'SaudiApp/al_ahsa.html')

def sports(request):
    return render(request, 'SaudiApp/sports.html')
