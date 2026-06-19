from django.contrib import admin
from .models import Posts

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'published_at', 'views', 'is_published', 'created_at')
    list_filter = ('published_at', 'is_published')
    search_fields = ('title',)
    date_hierarchy = 'published_at'