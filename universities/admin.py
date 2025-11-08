from django.contrib import admin
from .models import UniversityProgram, ProgramReview


class ProgramReviewInline(admin.TabularInline):
    model = ProgramReview
    extra = 0
    fields = ['author', 'rating', 'graduation_year', 'created_at']
    readonly_fields = ['created_at']


@admin.register(UniversityProgram)
class UniversityProgramAdmin(admin.ModelAdmin):
    list_display = ['university_name', 'program_name', 'degree', 'discipline', 'location', 'average_rating']
    list_filter = ['degree', 'discipline', 'location']
    search_fields = ['university_name', 'program_name', 'discipline']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProgramReviewInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('university_name', 'program_name', 'degree', 'discipline', 'location')
        }),
        ('Program Details', {
            'fields': ('duration', 'overview', 'accreditation', 'pros', 'cons')
        }),
        ('Metrics', {
            'fields': ('employability_score', 'research_opportunities')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProgramReview)
class ProgramReviewAdmin(admin.ModelAdmin):
    list_display = ['program', 'author', 'rating', 'graduation_year', 'helpful_count', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['content', 'author__username', 'program__program_name']
    readonly_fields = ['created_at']
