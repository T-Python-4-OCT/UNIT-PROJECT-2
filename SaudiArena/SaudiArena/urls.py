
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Arabic / English language switching
    path('i18n/', include('django.conf.urls.i18n')),

    # Saudi Arena pages
    path('', include('esports.urls')),
]
