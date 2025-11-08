from django.contrib import admin
from .models import StartupResource


@admin.register(StartupResource)
class StartupResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'provider', 'location', 'created_at']
    list_filter = ['category', 'location']
    search_fields = ['title', 'description', 'provider']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'provider', 'location')
        }),
        ('Details', {
            'fields': ('description', 'eligibility', 'link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
