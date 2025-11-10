from django.contrib import admin
from .models import (
    MentorProfile, MentorshipRequest, MentorshipSession,
    SkillAssessment, InterviewExperience, StudyGroup, StudyGroupMembership
)


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'years_of_experience', 'current_position', 'available_for_mentorship', 'created_at']
    list_filter = ['available_for_mentorship', 'mentorship_type']
    search_fields = ['user__username', 'company', 'expertise_areas']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['mentee', 'mentor', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['mentee__username', 'mentor__user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ['mentorship', 'session_date', 'duration_minutes', 'mentee_rating', 'mentor_rating']
    list_filter = ['session_date']
    search_fields = ['mentorship__mentee__username', 'topics_discussed']
    readonly_fields = ['created_at']


@admin.register(SkillAssessment)
class SkillAssessmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_name', 'category', 'current_level', 'target_level']
    list_filter = ['category', 'current_level']
    search_fields = ['user__username', 'skill_name']


@admin.register(InterviewExperience)
class InterviewExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'author', 'outcome', 'difficulty_rating', 'created_at']
    list_filter = ['outcome', 'discipline', 'experience_level']
    search_fields = ['company', 'position', 'author__username']


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'discipline', 'creator', 'meeting_format', 'is_active']
    list_filter = ['discipline', 'meeting_format', 'is_active']
    search_fields = ['name', 'subject']


@admin.register(StudyGroupMembership)
class StudyGroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'study_group', 'is_moderator', 'joined_at']
    list_filter = ['is_moderator']
