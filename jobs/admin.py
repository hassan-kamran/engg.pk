from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'experience_level', 'is_active', 'posted_date']
    list_filter = ['job_type', 'experience_level', 'is_active', 'discipline', 'posted_date']
    search_fields = ['title', 'company', 'location', 'description']
    readonly_fields = ['posted_date']
    list_editable = ['is_active']

    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'company', 'location', 'job_type', 'discipline', 'experience_level')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'salary', 'application_url')
        }),
        ('Status', {
            'fields': ('is_active', 'posted_date')
        }),
    )
