from django.contrib import admin
from .models import CofounderProfile, RegulatoryGuide, FundingOpportunity


@admin.register(CofounderProfile)
class CofounderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'background_type', 'startup_stage', 'looking_for_cofounder', 'is_active']
    list_filter = ['background_type', 'startup_stage', 'looking_for_cofounder', 'is_active']
    search_fields = ['user__username', 'expertise', 'industry_interests']


@admin.register(RegulatoryGuide)
class RegulatoryGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'last_verified_date', 'helpful_count']
    list_filter = ['category']
    search_fields = ['title', 'slug']


@admin.register(FundingOpportunity)
class FundingOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'funding_type', 'provider', 'amount', 'application_deadline', 'pakistan_friendly']
    list_filter = ['funding_type', 'pakistan_friendly']
    search_fields = ['title', 'provider']
