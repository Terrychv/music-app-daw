from django.contrib import admin
from .models import Comment, Rating



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'content_type')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'value', 'created_at')
    list_filter = ('value', 'created_at', 'content_type')
    search_fields = ('user__username',)