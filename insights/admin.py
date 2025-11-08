from django.contrib import admin
from .models import IndustryInsight


@admin.register(IndustryInsight)
class IndustryInsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'industry', 'discipline', 'views', 'helpful_count', 'created_at']
    list_filter = ['industry', 'discipline', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['views', 'helpful_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'industry', 'discipline')
        }),
        ('Content', {
            'fields': ('content', 'topics')
        }),
        ('Engagement', {
            'fields': ('views', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
