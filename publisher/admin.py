from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'user', 'created_at')
    search_fields = ('title', 'body')
    list_display_links = ('title', 'body')
    list_filter = ('created_at', 'user')