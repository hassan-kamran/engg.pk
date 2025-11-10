from django.contrib import admin
from .models import ThesisTopic, ResearchSupervisor, SupervisorReview, Publication


@admin.register(ThesisTopic)
class ThesisTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'university', 'degree_level', 'completion_year', 'views']
    list_filter = ['degree_level', 'discipline', 'completion_year', 'is_public']
    search_fields = ['title', 'author', 'university', 'keywords']


@admin.register(ResearchSupervisor)
class ResearchSupervisorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'university', 'discipline', 'accepting_students', 'verified', 'average_rating']
    list_filter = ['accepting_students', 'verified', 'university']
    search_fields = ['full_name', 'university', 'research_interests']


@admin.register(SupervisorReview)
class SupervisorReviewAdmin(admin.ModelAdmin):
    list_display = ['supervisor', 'reviewer', 'relationship', 'overall_rating', 'would_recommend']
    list_filter = ['relationship', 'overall_rating', 'would_recommend']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_type', 'venue', 'year', 'citations', 'pakistan_focused']
    list_filter = ['publication_type', 'year', 'discipline', 'pakistan_focused']
    search_fields = ['title', 'authors', 'keywords']
