
import json

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


# ==========================================
# LOAD DATA FROM JSON
# ==========================================

def load_data():
    file_path = settings.BASE_DIR / "esports" / "data" / "content.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================
# HOME PAGE
# ==========================================

def home(request):
    data = load_data()

    context = {
        "featured_games": data["featured_games"],
        "featured_tournaments": data["featured_tournaments"],
        "featured_teams": data["featured_teams"],
        "featured_players": data["featured_players"],
        "featured_achievements": data["featured_achievements"],
    }

    return render(request, "esports/home.html", context)


# ==========================================
# TOURNAMENTS PAGE - DROPDOWN FILTERS
# ==========================================

def tournaments(request):
    data = load_data()

    all_tournaments = data.get("featured_tournaments", [])

    # Get available games from JSON
    available_games = sorted({
        tournament.get("game", {}).get("name", "")
        for tournament in all_tournaments
        if tournament.get("game", {}).get("name")
    })

    # Get selected filters
    selected_game = request.GET.get("game", "").strip()
    selected_status = request.GET.get("status", "").strip()

    filtered_tournaments = all_tournaments

    # Filter tournaments by game
    if selected_game:
        filtered_tournaments = [
            tournament
            for tournament in filtered_tournaments
            if tournament.get("game", {}).get("name") == selected_game
        ]

    # Filter tournaments by status
    if selected_status:
        filtered_tournaments = [
            tournament
            for tournament in filtered_tournaments
            if tournament.get("status") == selected_status
        ]

    context = {
        "tournaments": filtered_tournaments,
        "available_games": available_games,
        "selected_game": selected_game,
        "selected_status": selected_status,
    }

    return render(
        request,
        "esports/tournaments.html",
        context
    )


# ==========================================
# DARK / LIGHT MODE
# ==========================================

@require_POST
def toggle_theme(request):
    current_theme = request.COOKIES.get("saudiArenaTheme", "dark")

    new_theme = "light" if current_theme == "dark" else "dark"

    next_url = request.POST.get("next", "/")

    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        next_url = "/"

    response = redirect(next_url)

    response.set_cookie(
        key="saudiArenaTheme",
        value=new_theme,
        max_age=31536000,
        path="/",
        httponly=True,
        secure=request.is_secure(),
        samesite="Lax"
    )

    return response


# ==========================================
# TEAMS PAGE - DROPDOWN FILTER
# ==========================================

def teams(request):
    data = load_data()

    all_teams = data.get("featured_teams", [])

    search_query = request.GET.get("search", "").strip()

    if search_query:
        filtered_teams = [
            team
            for team in all_teams
            if team.get("name", "").casefold() == search_query.casefold()
        ]
    else:
        filtered_teams = all_teams

    context = {
        "teams": filtered_teams,
        "search_query": search_query,
        "total_teams": len(filtered_teams),
        "teams_page": data.get("teams_page", {}),
    }

    return render(
        request,
        "esports/teams.html",
        context
    )


# ==========================================
# ABOUT PAGE
# ==========================================

def about(request):
    data = load_data()

    context = {
        "about": data.get("about", {})
    }

    return render(
        request,
        "esports/about.html",
        context
    )


# ==========================================
# PLAYERS PAGE
# ==========================================

def players(request):
    data = load_data()

    context = {
        "players": data.get("featured_players", [])
    }

    return render(
        request,
        "esports/players.html",
        context
    )


# ==========================================
# GAMES PAGE
# ==========================================

def games(request):
    data = load_data()

    context = {
        "games": data.get("featured_games", [])
    }

    return render(
        request,
        "esports/games.html",
        context
    )


# ==========================================
# ACHIEVEMENTS PAGE
# ==========================================

def achievements(request):
    data = load_data()

    achievements_list = data.get("featured_achievements", [])

    achievements_list = sorted(
        achievements_list,
        key=lambda item: int(item.get("year", 0)),
        reverse=True
    )

    total_achievements = len(achievements_list)

    teams = {
        item["team"]
        for item in achievements_list
        if item.get("team")
    }

    games = {
        item["game"]
        for item in achievements_list
        if item.get("game")
    }

    years = {
        item["year"]
        for item in achievements_list
        if item.get("year")
    }

    context = {
        "achievements": achievements_list,
        "total_achievements": total_achievements,
        "total_teams": len(teams),
        "total_games": len(games),
        "total_years": len(years),
    }

    return render(
        request,
        "esports/achievements.html",
        context
    )


# ==========================================
# PLAYER DETAIL PAGE
# ==========================================

def player_detail(request, slug):
    data = load_data()

    players = data.get("featured_players", [])

    player = next(
        (
            item
            for item in players
            if item.get("slug") == slug
        ),
        None
    )

    if player is None:
        raise Http404("Player not found")

    context = {
        "player": player
    }

    return render(
        request,
        "esports/player_detail.html",
        context
    )
