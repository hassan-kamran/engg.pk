from django.contrib import admin
from .models import IndustryZone, ProfessionalService, ServiceReview


@admin.register(IndustryZone)
class IndustryZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'zone_type', 'city', 'province', 'engineering_density', 'number_of_companies']
    list_filter = ['zone_type', 'province', 'city', 'engineering_density']
    search_fields = ['name', 'city', 'primary_industries']


@admin.register(ProfessionalService)
class ProfessionalServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'city', 'pec_registered', 'verified']
    list_filter = ['service_type', 'city', 'pec_registered', 'verified']
    search_fields = ['name', 'disciplines_served']


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ['service', 'reviewer', 'rating', 'would_recommend', 'created_at']
    list_filter = ['rating', 'would_recommend']
