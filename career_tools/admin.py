from django.contrib import admin
from .models import (
    Resume, ResumeEducation, ResumeExperience, ResumeSkill, ResumeProject,
    SalaryData, CareerTransitionStory
)


class ResumeEducationInline(admin.TabularInline):
    model = ResumeEducation
    extra = 1


class ResumeExperienceInline(admin.TabularInline):
    model = ResumeExperience
    extra = 1


class ResumeSkillInline(admin.TabularInline):
    model = ResumeSkill
    extra = 1


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'template', 'is_default', 'updated_at']
    list_filter = ['template', 'is_default']
    search_fields = ['user__username', 'title', 'full_name']
    inlines = [ResumeEducationInline, ResumeExperienceInline, ResumeSkillInline]


@admin.register(SalaryData)
class SalaryDataAdmin(admin.ModelAdmin):
    list_display = ['position', 'city', 'years_of_experience', 'base_salary_monthly', 'company_type', 'data_year']
    list_filter = ['company_type', 'company_size', 'city', 'data_year']
    search_fields = ['position', 'discipline']


@admin.register(CareerTransitionStory)
class CareerTransitionStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'transition_type', 'from_discipline', 'to_discipline', 'helpful_count']
    list_filter = ['transition_type']
    search_fields = ['title', 'author__username']
