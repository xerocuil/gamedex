from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Game, Platform
from extensions.utils import count_platforms, count_tags, total_playtime


def loading(request):
    return render(request, 'library/shared/loading.html')


# GAMES
def game_index(request):
    page_title = 'Home Page'
    favorites_q = Game.objects.filter(favorite=True).order_by('-last_played')
    favorites_count = favorites_q.count()
    favorites = favorites_q[:4]
    game_obj = Game.objects
    games = game_obj.order_by('-date_added')
    game_count = game_obj.all().count()
    most_played = game_obj.order_by('-play_time')[:4]
    paginator = Paginator(games, 50)
    page_total = paginator.num_pages
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    platform_count = Platform.objects.all().count()
    recently_added = game_obj.order_by('-date_added')[:4]
    recently_played = game_obj.order_by('-last_played')[:4]
    top_tags = count_tags()[:4]
    top_platforms = count_platforms()[:4]
    playtime = total_playtime()

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
        'recently_played': recently_played,
        'top_platforms': top_platforms,
        'top_tags': top_tags
    })


def game_review(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'library/game/review.html', {
        'game': game
    })


def search_results(request):
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


############
# Platform #
############

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
