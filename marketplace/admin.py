from django.contrib import admin
from .models import FreelanceProject, FreelanceProposal, ResearchCollaboration, Conference


@admin.register(FreelanceProject)
class FreelanceProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted_by', 'category', 'status', 'budget_min', 'budget_max', 'deadline']
    list_filter = ['status', 'category', 'remote_ok']
    search_fields = ['title', 'description', 'posted_by__username']


@admin.register(FreelanceProposal)
class FreelanceProposalAdmin(admin.ModelAdmin):
    list_display = ['project', 'freelancer', 'proposed_budget', 'status', 'created_at']
    list_filter = ['status']


@admin.register(ResearchCollaboration)
class ResearchCollaborationAdmin(admin.ModelAdmin):
    list_display = ['title', 'discipline', 'collaboration_type', 'initiator', 'is_active']
    list_filter = ['collaboration_type', 'discipline', 'is_active']
    search_fields = ['title', 'research_area']


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'conference_type', 'location', 'start_date', 'paper_submission_deadline']
    list_filter = ['conference_type', 'pakistan_friendly']
    search_fields = ['name', 'venue', 'topics']
