from django.urls import path

from reports import views

app_name = "reports"

urlpatterns = [
    path("", views.report_list, name="list"),
    path("new/", views.new_report, name="new"),
    path("searches/clear/", views.clear_searches, name="clear_searches"),
    path("<int:report_id>/", views.report_detail, name="detail"),
]
