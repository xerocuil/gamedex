from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.loading, name='loading'),
    path('home/', views.home, name='home'),
    path('game/<int:game_id>/', views.game_review, name='game_review'),
    path('search/', views.search_results, name='search_results'),
    path('platforms/', views.platforms, name='platforms'),
    path('platform/<int:platform_id>/', views.platform_review, name='platform_review'),
]