from django.contrib import admin
from .models import Project, OpenSourceProject, Competition, CompetitionParticipation, WinningProject


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'discipline', 'owner', 'completion_date', 'views', 'featured']
    list_filter = ['project_type', 'discipline', 'featured']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['views', 'created_at']


@admin.register(OpenSourceProject)
class OpenSourceProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_language', 'maintainer', 'looking_for_contributors', 'stars']
    list_filter = ['primary_language', 'skill_level_required', 'looking_for_contributors']
    search_fields = ['name', 'description']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'competition_type', 'organizer', 'registration_deadline', 'featured']
    list_filter = ['competition_type', 'format', 'featured']
    search_fields = ['title', 'organizer']


@admin.register(CompetitionParticipation)
class CompetitionParticipationAdmin(admin.ModelAdmin):
    list_display = ['competition', 'user', 'team_name', 'registered_at']


@admin.register(WinningProject)
class WinningProjectAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'competition', 'team_name', 'prize', 'year']
    list_filter = ['year']
    search_fields = ['project_title', 'team_name']
