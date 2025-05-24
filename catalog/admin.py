from django.contrib import admin
from .models import Genre,Album,Song,Artist

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__name')
    list_filter = ('release_date', 'genres')
    date_hierarchy = 'release_date'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('track_number', 'title', 'album', 'artist', 'duration')
    search_fields = ('title', 'artist__name', 'album__title')
    list_filter = ('genres', 'album')
    ordering = ('album', 'track_number')