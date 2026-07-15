from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'body', 'user', 'created_at']
    search_fields = ['title', 'body']
    list_display_links = ['title', 'body']
    list_filter = ['created_at', 'user']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'user', 'post__title']
    search_fields = ['content', 'user__username']
    list_display_links = ['content']
    list_filter = ['content', 'user', 'post']