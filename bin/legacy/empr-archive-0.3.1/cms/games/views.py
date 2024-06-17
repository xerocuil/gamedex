import csv
import os
import sys
import subprocess
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from .forms import CollectionForm, GameForm, GenreForm, PlatformForm, TagForm
from .models import Collection, Game, Genre, Platform, Tag
import lib.system

collections = Collection.objects.order_by('name')
games = Game.objects.order_by('sort_title')
genres = Genre.objects.order_by('name')
latest_games = Game.objects.order_by('-date_added')[:10]
platforms = Platform.objects.order_by('name')
tags = Tag.objects.order_by('name')


########
# Game #
########

## Index
def games_index(request):
	page_title = "Games"
	order_by = request.GET.get('order_by', '-date_added')
	object_list = Game.objects.order_by(order_by)
	paginator = Paginator(object_list, 50)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'games/games_index.html', {
		'page_title': page_title,
		'games': games,
		'object_list': object_list,
		'order_by': order_by,
		'page_obj': page_obj,
		'collections': collections,
		'genres': genres,
		'platforms': platforms,
		'tags': tags
	})

## Detail
def detail(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	installed = lib.system.check_installed(game.platform.slug, game.path)
	return render(request, 'games/detail.html', {
		'game': game,
		'installed': installed,
		'collections': collections,
		'genres': genres,
		'platforms': platforms,
		'tags': tags
	})

## Add
def add_game(request):
	if request.method == "POST":
		game_form = GameForm(request.POST, request.FILES)
		if game_form.is_valid():
			game_form.save()
			messages.success(request, 'Game was successfully added!', extra_tags='safe')
		else:
			messages.error(request, 'Error adding product.')
		return redirect("games:games_index")
	else:
		game_form = GameForm()

	return render(
		request=request,
		template_name="games/add.html",
		context={
			'game_form': game_form
		}
	)

## Delete
def delete_game(request, game_id):
	game = get_object_or_404(Game, pk=game_id)

	if request.method == 'POST':
		game.delete()
		messages.success(request, '<p class="tag">Game Deleted</p>', extra_tags='safe')
		return redirect("games:games_index")

	return render(
		request=request,
		template_name="games/delete.html",
		context={
			'game': game
		}
	)

## Edit
def edit_game(request, game_id):
	game = get_object_or_404(Game, pk=game_id)

	if request.method == 'POST':
		game_form = GameForm(request.POST, request.FILES, instance=game)
		if game_form.is_valid():
			game_form.save()
			messages.success(request, str(game.title) + ' was successfully edited.', extra_tags='safe')
		else:
			messages.error(request, game_form.errors)
		return redirect("games:games_index")
	else:
		game_form = GameForm(instance=game)

	return render(
		request=request,
		template_name="games/edit.html",
		context = {
			'game': game,
			'game_form': game_form
		}
	)

## Play
def play_game(request, platform_slug, filename):
	filename = filename
	platform_slug = platform_slug
	if platform_slug == 'pc':
		# game_path = lib.system.PC_DIR
		game_slug = os.path.splitext(filename)[0]
		game_path = os.path.join(lib.system.PC_DIR, game_slug + '/start.sh')
	else:
		game_path = os.path.join(lib.system.ROMS_DIR, platform_slug + '/' + filename)

	subprocess.run(["game-launcher.sh", platform_slug, game_path])

	return render(
		request=request,
		template_name="games/play.html",
		context={
			'game_path': game_path,
			'platform_slug': platform_slug,
			'filename': filename,
		}
	)

	

## Scrape Game
def scrape_game(request):
	if request.method == "POST":
		game_form = GameForm(request.POST, request.FILES)
		if game_form.is_valid():
			game_form.save()
			messages.success(request, 'Game was successfully added!', extra_tags='safe')
		else:
			messages.error(request, 'Error adding product.')
		return redirect("games:games_index")
	elif request.method == "GET":
		description = request.GET['description']
		developer = request.GET['developer']
		path = request.GET['path']
		publisher = request.GET['publisher']
		release_date = request.GET['release_date']
		title = request.GET['title']
		game_form = GameForm()

	return render(
		request=request,
		template_name="games/scrape.html",
		context={
			'description': description,
			'developer': developer,
			'path': path,
			'publisher': publisher,
			'release_date': release_date,
			'title': title,
			'game_form': game_form
		}
	)

## Search
class SearchResultsView(ListView):
	model = Game
	template_name = 'games/search_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q', '')
		object_list = Game.objects.filter(
			Q(sort_title__icontains=query) |
			Q(alt_title__icontains=query) |
			Q(developer__icontains=query) |
			Q(genre__name__icontains=query) |
			#Q(tags__name__icontains=query) |
			Q(platform__name__icontains=query) |
			Q(publisher__icontains=query)
			
		).order_by('sort_title')
		return object_list

def scrape_search(request,file_name):
	notification = 'You submitted: ' + file_name
	cmd = '/home/xerocuil/Projects/empr/utils/scrapers/tgdb/tgdb_scraper.sh ' + file_name
	subprocess.Popen(cmd, shell=True)
	return render(request, 'games/scrape_search.html', {
		'notification': notification
	})

## Game filters

### Collection
def collection(request, collection_id):
	collection = get_object_or_404(Collection, pk=collection_id)
	games = Collection.objects.get(id=collection_id).game_set.order_by('release_date')
	return render(request, 'games/collection.html', {
		'games': games,
		'collection': collection,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'platforms': platforms,
		'tags': tags
	})

### Genre
def genre(request, genre_id):
	genre = get_object_or_404(Genre, pk=genre_id)
	order_by = request.GET.get('order_by', 'sort_title')
	games = Genre.objects.get(id=genre_id).game_set.order_by(order_by)
	return render(request, 'games/genre.html', {
		'games': games,
		'genre': genre,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'order_by': order_by,
		'platforms': platforms,
		'tags': tags
	})

### Platform
def platform(request, platform_id):
	platform = get_object_or_404(Platform, pk=platform_id)
	order_by = request.GET.get('order_by', 'sort_title')
	games = Platform.objects.get(id=platform_id).game_set.order_by(order_by)
	return render(request, 'games/platform.html', {
		'games': games,
		'platform': platform,
		'collections': collections,
		'genres': genres,
		'order_by': order_by,
		'platforms': platforms,
		'tags': tags
	})

### Tag
def tag(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)
	games = Tag.objects.get(id=tag_id).game_set.order_by('sort_title')
	return render(request, 'games/tag.html', {
		'games': games,
		'tag': tag,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'platforms': platforms,
		'tags': tags
	})


##############
# Collection #
##############

## Index
def collection_index(request):
	page_title = "Collections"
	collections = Collection.objects.order_by('name')
	return render(request, 'collection/index.html', {
		'page_title': page_title,
		'collections': collections,
		'genres': genres,
		'platforms': platforms,
		'tags': tags
		})

## Add
def add_collection(request):
	page_title = "Add Collection"
	if request.method == "POST":
		form = CollectionForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Collection was successfully added!', extra_tags='safe')
		else:
			messages.error(request, 'Error adding product.')
		return redirect("games:collection_index")
	else:
		form = CollectionForm()

	return render(
		request=request,
		template_name="collection/edit.html",
		context={
			'page_title': page_title,
			'form': form
		}
	)

## Edit
def edit_collection(request, collection_id):
	page_title = "Edit Collection"
	collection = get_object_or_404(Collection, pk=collection_id)

	if request.method == 'POST':
		form = CollectionForm(request.POST, request.FILES, instance=collection)
		if form.is_valid():
			form.save()
			messages.success(request, str(collection.name) + ' was successfully edited.', extra_tags='safe')
		else:
			messages.error(request, form.errors)
		return redirect("games:collection_index")
	else:
		form = CollectionForm(instance=collection)

	return render(
		request=request,
		template_name="collection/edit.html",
		context = {
			'page_title': page_title,
			'collection': collection,
			'form': form
		}
	)

## Delete
def delete_collection(request, collection_id):
	collection = get_object_or_404(Collection, pk=collection_id)

	if request.method == 'POST':
		collection.delete()
		messages.success(request, '<p class="tag">Collection Deleted</p>', extra_tags='safe')
		return redirect("games:collection_index")

	return render(
		request=request,
		template_name="collection/delete.html",
		context={
			'collection': collection
		}
	)


#########
# Genre #
#########

## Index
def genre_index(request):
	page_title = "Genres"
	genres = Genre.objects.order_by('name')
	return render(request, 'genre/index.html', {
		'page_title': page_title,
		'genres': genres,
		'collections': collections,
		'platforms': platforms,
		'tags': tags
		})

## Add
def add_genre(request):
	page_title = "Add Genre"
	if request.method == "POST":
		form = GenreForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Genre was successfully added!', extra_tags='safe')
		else:
			messages.error(request, 'Error adding product.')
		return redirect("games:genre_index")
	else:
		form = GenreForm()

	return render(
		request=request,
		template_name="genre/edit.html",
		context={
			'page_title': page_title,
			'form': form
		}
	)

## Edit
def edit_genre(request, genre_id):
	page_title = "Edit Genre"
	genre = get_object_or_404(Genre, pk=genre_id)

	if request.method == 'POST':
		form = GenreForm(request.POST, request.FILES, instance=genre)
		if form.is_valid():
			form.save()
			messages.success(request, str(genre.name) + ' was successfully edited.', extra_tags='safe')
		else:
			messages.error(request, form.errors)
		return redirect("games:genre_index")
	else:
		form = GenreForm(instance=genre)

	return render(
		request=request,
		template_name="genre/edit.html",
		context = {
			'page_title': page_title,
			'genre': genre,
			'form': form
		}
	)

## Delete
def delete_genre(request, genre_id):
	genre = get_object_or_404(Genre, pk=genre_id)

	if request.method == 'POST':
		genre.delete()
		messages.success(request, '<p class="tag">Genre Deleted</p>', extra_tags='safe')
		return redirect("games:genre_index")

	return render(
		request=request,
		template_name="genre/delete.html",
		context={
			'genre': genre
		}
	)


#############
# Launchers #
#############

def launcher(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	name = game.title
	filename = game.path
	platform = game.platform.slug
	cmd = 'game-launcher ' + platform + ' ' + filename + ' &'
	subprocess.Popen(cmd, shell=True)
	return render(request, 'games/launcher.html', {
		'game': game,
	})

def launcher_remote(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	name = game.title
	filename = game.path
	platform = game.platform.slug
	cmd = 'ssh arcade "export DISPLAY=:0;game-launcher ' + platform + ' ' + filename + '"'
	subprocess.Popen(cmd, shell=True)
	return render(request, 'games/launcher.html', {
		'game': game,
	})


############
# Platform #
############

## Index
def platform_index(request):
	page_title = "Platforms"
	platforms = Platform.objects.order_by('name')
	return render(request, 'platform/index.html', {
		'page_title': page_title,
		'platforms': platforms,
		'collections': collections,
		'genres': genres,
		'tags': tags
		})

## Add
def add_platform(request):
	page_title = "Add Platform"
	if request.method == "POST":
		form = PlatformForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Platform was successfully added!', extra_tags='safe')
		else:
			messages.error(request, 'Error adding product.')
		return redirect("games:platform_index")
	else:
		form = PlatformForm()

	return render(
		request=request,
		template_name="platform/edit.html",
		context={
			'page_title': page_title,
			'form': form
		}
	)

## Delete
def delete_platform(request, platform_id):
	platform = get_object_or_404(Platform, pk=platform_id)

	if request.method == 'POST':
		platform.delete()
		messages.success(request, '<p class="tag">Platform Deleted</p>', extra_tags='safe')
		return redirect("games:platform_index")

	return render(
		request=request,
		template_name="platform/delete.html",
		context={
			'platform': platform
		}
	)

## Edit
def edit_platform(request, platform_id):
	page_title = "Edit Platform"
	platform = get_object_or_404(Platform, pk=platform_id)

	if request.method == 'POST':
		form = PlatformForm(request.POST, request.FILES, instance=platform)
		if form.is_valid():
			form.save()
			messages.success(request, str(platform.name) + ' was successfully edited.', extra_tags='safe')
		else:
			messages.error(request, form.errors)
		return redirect("games:platform_index")
	else:
		form = PlatformForm(instance=platform)

	return render(
		request=request,
		template_name="platform/edit.html",
		context = {
			'page_title': page_title,
			'platform': platform,
			'form': form
		}
	)


#######
# Tag #
#######

## Index
def tag_index(request):
	page_title = "Tags"
	tags = Tag.objects.order_by('name')
	return render(request, 'tag/index.html', {
		'page_title': page_title,
		'tags': tags,
		'platforms': platforms,
		'collections': collections,
		'genres': genres
		})

## Add
def add_tag(request):
	page_title = "Add Tag"
	if request.method == "POST":
		form = TagForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Tag was successfully added!', extra_tags='safe')
		else:
			messages.error(request, 'Error adding product.')
		return redirect("games:tag_index")
	else:
		form = TagForm()

	return render(
		request=request,
		template_name="tag/edit.html",
		context={
			'page_title': page_title,
			'form': form
		}
	)

## Edit
def edit_tag(request, tag_id):
	page_title = "Edit Tag"
	tag = get_object_or_404(Tag, pk=tag_id)

	if request.method == 'POST':
		form = TagForm(request.POST, request.FILES, instance=tag)
		if form.is_valid():
			form.save()
			messages.success(request, str(tag.name) + ' was successfully edited.', extra_tags='safe')
		else:
			messages.error(request, form.errors)
		return redirect("games:tag_index")
	else:
		form = TagForm(instance=tag)

	return render(
		request=request,
		template_name="tag/edit.html",
		context = {
			'page_title': page_title,
			'tag': tag,
			'form': form
		}
	)

## Delete
def delete_tag(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)

	if request.method == 'POST':
		tag.delete()
		messages.success(request, '<p class="tag">Tag Deleted</p>', extra_tags='safe')
		return redirect("games:tag_index")

	return render(
		request=request,
		template_name="tag/delete.html",
		context={
			'tag': tag
		}
	)


########
# Misc #
########

## Loading
def loading(request):
	return render(request, 'gui/loading.html')

## Readme
def readme(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	return render(request, 'games/readme.html', {
		'game': game,
	})

## Gamelist
def gamelist(request, platform_id):
	platform = get_object_or_404(Platform, pk=platform_id)
	games = Platform.objects.get(id=platform_id).game_set.order_by('sort_title')
	return render(request, 'games/xml_list.html', {
		'games': games,
		'platform': platform
	})

## CSV Export
def export_csv(request):
	games = Game.objects.all()
	fieldnames = [
		'sort_title',
		'description',
		'developer',
		'publisher',
		'esrb',
		'genre',
		# 'tags',
		'region',
		'translation',
		'release_date',
		'store',
		'collection',
		'controller_support',
		'platform',
		'player',
		'co_op',
		'online_multiplayer',
		'display',
	]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="empr_games.csv"'
	writer = csv.DictWriter(response, fieldnames=fieldnames, restval='')
	writer.writeheader()

	for g in games:
		writer.writerow({
			'sort_title': g.sort_title,
			'description': g.description,
			'developer': g.developer,
			'publisher': g.publisher,
			'esrb': g.esrb,
			'genre': g.genre,
			# 'tags': g.tags,
			'region': g.region,
			'translation': g.translation,
			'release_date': g.release_date,
			'store': g.store,
			'collection': g.collection,
			'controller_support': g.controller_support,
			'platform': g.platform,
			'player': g.player,
			'co_op': g.co_op,
			'online_multiplayer': g.online_multiplayer,
			'display': g.display,
		})

	return response
