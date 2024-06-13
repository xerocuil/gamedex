from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Game, Platform


def loading(request):
    return render(request, 'library/shared/loading.html')


def home(request):
    page_title = 'Home Page'
    games = Game.objects.order_by('-date_added')
    paginator = Paginator(games, 50)
    page_total = paginator.num_pages
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'library/game/index.html', {
        'page_title': page_title,
        'page_obj': page_obj,
        'page_total': page_total
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

def platforms(request):
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
