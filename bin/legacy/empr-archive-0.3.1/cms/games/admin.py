from django.contrib import admin

from .models import Collection, Game, Genre, Platform, Tag

def mark_as_archived(modeladmin, request, queryset):
	queryset.update(archived=True)
mark_as_archived.short_description = "Archived"

class GameAdmin(admin.ModelAdmin):
	list_display = ('sort_title', 'genre', 'developer', 'publisher', 'platform', 'archived')
	search_fields = (
		'sort_title',
		'path',
		'genre__name',
		'developer',
		'publisher',
		'platform__name',
	)
	actions = [ mark_as_archived ]

admin.site.register(Collection)
admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Tag)
