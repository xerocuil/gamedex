from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse

from .models import Collection, Game, Genre, Platform, Tag


def loading(request):
    return render(request, 'library/loading.html')


def home(request):
    games = Game.objects.order_by('-date_added')
    paginator = Paginator(games, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'library/game/index.html', {
        'page_obj': page_obj
    })
