from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

from .views import SearchResultsView

app_name = 'games'
urlpatterns = [
	path('', views.games_index, name='games_index'),
	path('admin/', admin.site.urls),

	# Collections
	path('collections/', views.collection_index, name='collection_index'),
	path('collection/<int:collection_id>/', views.collection, name='collection'),
	path('collection/add/', views.add_collection, name='add_collection'),
	path('collection/edit/<int:collection_id>/', views.edit_collection, name='edit_collection'),
	path('collection/delete/<int:collection_id>/', views.delete_collection, name='delete_collection'),

	# Games
	path('games/', views.games_index, name='games_index'),
	path('game/<int:game_id>/', views.detail, name='detail'),
	path('game/add/', views.add_game, name='add_game'),
	path('game/delete/<int:game_id>/', views.delete_game, name='delete_game'),
	path('game/edit/<int:game_id>/', views.edit_game, name='edit_game'),
	path('game/scrape/', views.scrape_game, name='scrape_game'),
	path('game/genre/<int:genre_id>/', views.genre, name='genre'),
	path('game/platform/<int:platform_id>/', views.platform, name='platform'),
	path('game/play/<str:platform_slug>/<str:filename>/', views.play_game, name='play_game'),
	
	# Genres
	path('genres/', views.genre_index, name='genre_index'),
	path('genre/add/', views.add_genre, name='add_genre'),
	path('genre/delete/<int:genre_id>/', views.delete_genre, name='delete_genre'),
	path('genre/edit/<int:genre_id>/', views.edit_genre, name='edit_genre'),

	# Platforms
	path('platforms/', views.platform_index, name='platform_index'),
	path('platform/add/', views.add_platform, name='add_platform'),
	path('platform/delete/<int:platform_id>/', views.delete_platform, name='delete_platform'),
	path('platform/edit/<int:platform_id>/', views.edit_platform, name='edit_platform'),

	# Tags
	path('tags/', views.tag_index, name='tag_index'),
	path('tag/add/', views.add_tag, name='add_tag'),
	path('tag/delete/<int:tag_id>/', views.delete_tag, name='delete_tag'),
	path('tag/edit/<int:tag_id>/', views.edit_tag, name='edit_tag'),

	# Launchers
	path('launcher/<int:game_id>/', views.launcher, name='launcher'),
	path('launcher_remote/<int:game_id>/', views.launcher_remote, name='launcher_remote'),

	# Reports
	path('export/', views.export_csv, name='export_csv'),
	path('gamelist/<int:platform_id>/', views.gamelist, name='gamelist'),
	
	# Misc
	path('loading/', views.loading, name='loading'),
	path('readme/<int:game_id>/', views.readme, name='readme'),
	# path('scrape_game/', views.scrape_game, name='scrape_game'),
	path('scrape_search/<str:file_name>', views.scrape_search, name='scrape_search'),
	path('search/', SearchResultsView.as_view(), name='search_results'),
	path('tag/<int:tag_id>/', views.tag, name='tag'),
	#path('test/', views.test, name='test'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
