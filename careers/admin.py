from django.contrib import admin
from .models import CareerPath, ExperienceStory


class ExperienceStoryInline(admin.TabularInline):
    model = ExperienceStory
    extra = 0
    fields = ['author', 'title', 'current_position', 'years_of_experience']


@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ['title', 'discipline', 'salary_range', 'created_at']
    list_filter = ['discipline']
    search_fields = ['title', 'discipline', 'overview']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ExperienceStoryInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'discipline', 'overview')
        }),
        ('Career Details', {
            'fields': ('skills', 'industries', 'salary_range', 'growth_outlook', 'education_required')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ExperienceStory)
class ExperienceStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'career_path', 'current_position', 'years_of_experience', 'created_at']
    list_filter = ['career_path', 'years_of_experience']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at']
