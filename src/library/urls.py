from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.loading, name='loading'),
    path('games/', views.game_index, name='game_index'),
    path('game/<int:game_id>/', views.game_review, name='game_review'),
    path('search/', views.search_results, name='search_results'),
    path('platforms/', views.platform_index, name='platform_index'),
    path('platform/<int:platform_id>/', views.platform_review, name='platform_review'),
    path('settings/', views.settings, name='settings')
]