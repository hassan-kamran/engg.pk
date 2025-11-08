from django.contrib import admin
from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'country', 'level', 'funded', 'deadline', 'is_active']
    list_filter = ['level', 'funded', 'is_active', 'country', 'deadline']
    search_fields = ['name', 'provider', 'country', 'description']
    readonly_fields = ['created_at']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'provider', 'country', 'level')
        }),
        ('Details', {
            'fields': ('disciplines', 'amount', 'deadline', 'funded', 'description', 'eligibility')
        }),
        ('Application', {
            'fields': ('application_url', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
