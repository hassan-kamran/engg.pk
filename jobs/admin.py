from django.contrib import admin
from .models import Job, SavedJob, JobApplication


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


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'job__title']
    readonly_fields = ['saved_at']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'applied_at', 'updated_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__username', 'job__title']
    readonly_fields = ['applied_at', 'updated_at']
    list_editable = ['status']
