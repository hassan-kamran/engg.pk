from django.contrib import admin
from .models import LocalHub, SuccessStory, NewsArticle, WikiArticle, WikiRevision


@admin.register(LocalHub)
class LocalHubAdmin(admin.ModelAdmin):
    list_display = ['name', 'hub_type', 'city', 'open_to_public', 'created_at']
    list_filter = ['hub_type', 'city', 'for_students', 'for_professionals']
    search_fields = ['name', 'city', 'address']


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_person', 'story_type', 'featured', 'views', 'published_date']
    list_filter = ['story_type', 'featured']
    search_fields = ['title', 'featured_person']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'source', 'published_date', 'views']
    list_filter = ['category', 'published_date']
    search_fields = ['title', 'source']


@admin.register(WikiArticle)
class WikiArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'version', 'verified', 'views', 'updated_at']
    list_filter = ['category', 'verified']
    search_fields = ['title', 'slug', 'tags']


@admin.register(WikiRevision)
class WikiRevisionAdmin(admin.ModelAdmin):
    list_display = ['article', 'editor', 'version', 'created_at']
    list_filter = ['created_at']
