import requests
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Game, Platform
from .forms import SettingsForm
import extensions.config as config
from extensions.utils import count_platforms, count_tags, total_playtime


# GUI

def loading(request):
    return render(request, 'library/shared/loading.html')


# GAME

def game_index(request):
    """List paginated view of all games in database."""

    print('request', request, type(request))
    page_title = 'Home Page'

    # Query game objects
    game_obj = Game.objects
    games = game_obj.order_by('-date_added')
    game_count = game_obj.all().count()

    favorites_q = game_obj.filter(favorite=True).order_by('-last_played')
    favorites_count = favorites_q.count()
    favorites = favorites_q[:4]

    most_played = game_obj.order_by('-play_time')[:4]
    recently_added = game_obj.order_by('-date_added')[:4]
    recently_modified = game_obj.order_by('-date_modified')[:4]
    recently_played = game_obj.order_by('-last_played')[:4]
    top_tags = count_tags()[:4]
    playtime = total_playtime()

    # Create platform objects
    platform_obj = Platform.objects
    platform_count = platform_obj.all().count()
    top_platforms = count_platforms()[:4]

    # Create page objects
    paginator = Paginator(games, 50)
    page_total = paginator.num_pages
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/game/index.html', {
        'page_title': page_title,
        'favorites': favorites,
        'favorites_count': favorites_count,
        'game_count': game_count,
        'most_played': most_played,
        'page_obj': page_obj,
        'page_total': page_total,
        'platform_count': platform_count,
        'playtime': playtime,
        'recently_added': recently_added,
        'recently_modified': recently_modified,
        'recently_played': recently_played,
        'top_platforms': top_platforms,
        'top_tags': top_tags
    })


def game_review(request, game_id):
    print(type(game_review))
    """Create report of single game instance.

    Args:
        game_id (int): Game ID number
    """  # noqa W291

    game = get_object_or_404(Game, pk=game_id)
    installed_games_url = request.build_absolute_uri('/') + 'assets/json/library/installed.json'
    registered_games = requests.get(installed_games_url).json()['registered']
    query = next((item['id'] for item in registered_games if item['id'] == game.id), None)
    if query:
        game.installed = True
    else:
        game.installed = False
    return render(request, 'library/game/review.html', {
        'game': game
    })


def search_results(request):
    """Display results of game query."""

    query = request.GET.get('q')
    results = Game.objects.filter(
        Q(title__icontains=query) |
        Q(alt_title__icontains=query) |
        Q(filename__icontains=query))
    page_title = str(len(results)) + ' results for "' + query + '"'
    paginator = Paginator(results, 50)
    page_total = paginator.num_pages
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/game/search_results.html', {
        'page_title': page_title,
        'page_obj': page_obj,
        'page_total': page_total,
        'query': query
    })


# PLATFORM

def platform_index(request):
    page_title = 'Platforms'
    platforms = Platform.objects.order_by('name')
    return render(request, 'library/platform/index.html', {
        'page_title': page_title,
        'platforms': platforms
    })


def platform_review(request, platform_id):
    platform = get_object_or_404(Platform, pk=platform_id)
    page_title = platform.name
    games = Game.objects.filter(platform=platform_id).order_by('title')
    paginator = Paginator(games, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/platform/review.html', {
        'page_title': page_title,
        'platform': platform,
        'page_obj': page_obj
    })


# SYSTEM

def user_settings(request):
    """Form to update `config.ini` settings."""

    page_title = 'Settings'
    message = ''

    if request.method == "POST":
        form = SettingsForm(request.POST)

        if form.is_valid():
            # config.cfg['APP']['debug'] = form.cleaned_data['app_debug']
            if form.cleaned_data['app_debug']:
                config.cfg['APP']['debug'] = 'True'
            else:
                config.cfg['APP']['debug'] = 'False'
            config.cfg['DIR']['games'] = form.cleaned_data['dir_games']

            with open(config.CONFIG_PATH, 'w') as f:
                config.cfg.write(f)

            message = 'Configuration saved.'
    else:
        form = SettingsForm()

    return render(request, 'library/system/settings.html', {
        'page_title': page_title,
        'form': form,
        'message': message
        })
