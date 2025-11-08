from django.contrib import admin
from .models import ForumPost, Reply


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    fields = ['author', 'content', 'created_at']
    readonly_fields = ['created_at']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'reply_count', 'like_count', 'views', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines = [ReplyInline]

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content', 'author', 'category', 'tags')
        }),
        ('Engagement', {
            'fields': ('views', 'likes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'like_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at']
