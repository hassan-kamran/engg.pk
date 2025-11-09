from django.contrib import admin
from .models import (
    EngineeringCalculator, ReferenceLibrary, SoftwareDirectory,
    SoftwareReview, EquipmentListing
)


@admin.register(EngineeringCalculator)
class EngineeringCalculatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'discipline', 'calculator_type', 'usage_count']
    list_filter = ['discipline']
    search_fields = ['name', 'description']


@admin.register(ReferenceLibrary)
class ReferenceLibraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'discipline', 'author', 'is_free', 'downloads']
    list_filter = ['resource_type', 'discipline', 'is_free']
    search_fields = ['title', 'author', 'topics']


@admin.register(SoftwareDirectory)
class SoftwareDirectoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'pricing_model', 'available_in_pakistan', 'average_rating']
    list_filter = ['pricing_model', 'category', 'available_in_pakistan']
    search_fields = ['name', 'description']


@admin.register(SoftwareReview)
class SoftwareReviewAdmin(admin.ModelAdmin):
    list_display = ['software', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating']


@admin.register(EquipmentListing)
class EquipmentListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'listing_type', 'category', 'condition', 'price', 'location', 'is_active']
    list_filter = ['listing_type', 'condition', 'is_active', 'location']
    search_fields = ['title', 'description']
