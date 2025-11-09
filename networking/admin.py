from django.contrib import admin
from .models import AlumniProfile, CompanyProfile, CompanyReview, Event, EventAttendance


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'degree', 'graduation_year', 'current_company', 'willing_to_help']
    list_filter = ['degree', 'graduation_year', 'willing_to_help']
    search_fields = ['user__username', 'university', 'current_company']


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'size', 'headquarters', 'verified']
    list_filter = ['size', 'industry', 'verified']
    search_fields = ['name', 'industry']
    readonly_fields = ['created_at']


@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ['company', 'author', 'position', 'overall_rating', 'employment_status', 'would_recommend']
    list_filter = ['employment_status', 'overall_rating', 'would_recommend']
    search_fields = ['company__name', 'author__username', 'position']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'format', 'start_date', 'location', 'featured']
    list_filter = ['event_type', 'format', 'featured', 'start_date']
    search_fields = ['title', 'organizer', 'location']


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registered_at', 'attended', 'rating']
    list_filter = ['attended']
