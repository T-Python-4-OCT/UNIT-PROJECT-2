
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("tournaments/", views.tournaments, name="tournaments"),
    path("teams/", views.teams, name="teams"),
    path("players/", views.players, name="players"),
    path("games/", views.games, name="games"),
    path("achievements/", views.achievements, name="achievements"),
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),
    path("players/<slug:slug>/", views.player_detail, name="player_detail"),
]
