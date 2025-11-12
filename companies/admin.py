"""
Admin interface for companies app models.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Company,
    CompanyReview,
    SalaryReport,
    CompanyPhoto,
    CompanyBenefit
)


class CompanyReviewInline(admin.TabularInline):
    """Inline admin for company reviews"""
    model = CompanyReview
    extra = 0
    fields = ['author', 'employment_status', 'overall_rating', 'is_approved', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False


class SalaryReportInline(admin.TabularInline):
    """Inline admin for salary reports"""
    model = SalaryReport
    extra = 0
    fields = ['job_title', 'experience_years', 'total_compensation', 'currency', 'is_verified']
    readonly_fields = []
    can_delete = False


class CompanyPhotoInline(admin.TabularInline):
    """Inline admin for company photos"""
    model = CompanyPhoto
    extra = 0
    fields = ['photo', 'photo_type', 'is_approved', 'uploader', 'created_at']
    readonly_fields = ['created_at']


class CompanyBenefitInline(admin.TabularInline):
    """Inline admin for company benefits"""
    model = CompanyBenefit
    extra = 1
    fields = ['benefit_category', 'benefit_name', 'description']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model"""
    list_display = [
        'name',
        'industry',
        'size',
        'headquarters_location',
        'overall_rating_display',
        'total_reviews_count',
        'total_salaries_count',
        'verified',
        'created_at'
    ]
    list_filter = ['industry', 'size', 'verified', 'created_at']
    search_fields = ['name', 'description', 'headquarters_location']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = [
        'overall_rating',
        'recommend_to_friend_percentage',
        'ceo_approval_rating',
        'total_reviews_count',
        'total_salaries_count',
        'total_interviews_count',
        'created_at',
        'updated_at',
        'logo_preview'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'logo', 'logo_preview', 'industry', 'size')
        }),
        ('Location & Details', {
            'fields': ('headquarters_location', 'founded_year', 'website', 'description')
        }),
        ('CEO Information', {
            'fields': ('ceo_name', 'ceo_approval_rating'),
        }),
        ('Aggregated Data (Auto-calculated)', {
            'fields': (
                'overall_rating',
                'recommend_to_friend_percentage',
                'total_reviews_count',
                'total_salaries_count',
                'total_interviews_count',
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('verified', 'created_at', 'updated_at'),
        }),
    )
    inlines = [CompanyReviewInline, SalaryReportInline, CompanyPhotoInline, CompanyBenefitInline]
    actions = ['mark_verified', 'mark_unverified', 'update_aggregated_data']

    def overall_rating_display(self, obj):
        """Display overall rating with stars"""
        if obj.overall_rating > 0:
            stars = '⭐' * int(obj.overall_rating)
            return f"{obj.overall_rating} {stars}"
        return "No ratings"
    overall_rating_display.short_description = "Rating"

    def logo_preview(self, obj):
        """Display logo preview"""
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: contain;" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = "Logo Preview"

    def mark_verified(self, request, queryset):
        """Mark selected companies as verified"""
        updated = queryset.update(verified=True)
        self.message_user(request, f"{updated} companies marked as verified.")
    mark_verified.short_description = "Mark selected companies as verified"

    def mark_unverified(self, request, queryset):
        """Mark selected companies as unverified"""
        updated = queryset.update(verified=False)
        self.message_user(request, f"{updated} companies marked as unverified.")
    mark_unverified.short_description = "Mark selected companies as unverified"

    def update_aggregated_data(self, request, queryset):
        """Update aggregated data for selected companies"""
        for company in queryset:
            company.update_aggregated_data()
        self.message_user(request, f"Updated aggregated data for {queryset.count()} companies.")
    update_aggregated_data.short_description = "Update aggregated data"


@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    """Admin interface for CompanyReview model"""
    list_display = [
        'company',
        'author',
        'employment_status',
        'job_title',
        'overall_rating',
        'recommend_to_friend',
        'is_approved',
        'created_at'
    ]
    list_filter = [
        'employment_status',
        'overall_rating',
        'recommend_to_friend',
        'is_approved',
        'created_at',
        'company__industry'
    ]
    search_fields = ['company__name', 'author__username', 'job_title', 'review_title', 'pros', 'cons']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count', 'get_average_rating_display']
    fieldsets = (
        ('Company & Author', {
            'fields': ('company', 'author', 'is_approved')
        }),
        ('Employment Details', {
            'fields': ('employment_status', 'job_title', 'location', 'employment_length')
        }),
        ('Ratings', {
            'fields': (
                'overall_rating',
                'work_life_balance_rating',
                'culture_values_rating',
                'career_opportunities_rating',
                'compensation_benefits_rating',
                'senior_management_rating',
                'get_average_rating_display'
            )
        }),
        ('Review Content', {
            'fields': ('review_title', 'pros', 'cons', 'advice_to_management')
        }),
        ('Additional Information', {
            'fields': ('recommend_to_friend', 'ceo_approval')
        }),
        ('Engagement', {
            'fields': ('helpful_count',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    actions = ['approve_reviews', 'unapprove_reviews']

    def get_average_rating_display(self, obj):
        """Display average of all dimension ratings"""
        return f"{obj.get_average_rating()} / 5.0"
    get_average_rating_display.short_description = "Average Rating"

    def approve_reviews(self, request, queryset):
        """Approve selected reviews"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"

    def unapprove_reviews(self, request, queryset):
        """Unapprove selected reviews"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} reviews unapproved.")
    unapprove_reviews.short_description = "Unapprove selected reviews"


@admin.register(SalaryReport)
class SalaryReportAdmin(admin.ModelAdmin):
    """Admin interface for SalaryReport model"""
    list_display = [
        'company',
        'job_title',
        'experience_years',
        'education_level',
        'base_salary_display',
        'total_compensation_display',
        'is_verified',
        'created_at'
    ]
    list_filter = [
        'company__industry',
        'employment_type',
        'education_level',
        'currency',
        'is_verified',
        'created_at'
    ]
    search_fields = ['company__name', 'job_title', 'location']
    readonly_fields = ['total_compensation', 'created_at']
    fieldsets = (
        ('Company & Submitter', {
            'fields': ('company', 'submitter', 'is_verified')
        }),
        ('Job Details', {
            'fields': ('job_title', 'location', 'experience_years', 'education_level', 'employment_type')
        }),
        ('Compensation', {
            'fields': ('currency', 'base_salary', 'bonus', 'additional_compensation', 'total_compensation')
        }),
        ('Metadata', {
            'fields': ('created_at',),
        }),
    )
    actions = ['mark_verified', 'mark_unverified']

    def base_salary_display(self, obj):
        """Display base salary with currency"""
        return f"{obj.currency} {obj.base_salary:,.2f}"
    base_salary_display.short_description = "Base Salary"

    def total_compensation_display(self, obj):
        """Display total compensation with currency"""
        return f"{obj.currency} {obj.total_compensation:,.2f}"
    total_compensation_display.short_description = "Total Compensation"

    def mark_verified(self, request, queryset):
        """Mark selected salary reports as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} salary reports marked as verified.")
    mark_verified.short_description = "Mark selected reports as verified"

    def mark_unverified(self, request, queryset):
        """Mark selected salary reports as unverified"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} salary reports marked as unverified.")
    mark_unverified.short_description = "Mark selected reports as unverified"


@admin.register(CompanyPhoto)
class CompanyPhotoAdmin(admin.ModelAdmin):
    """Admin interface for CompanyPhoto model"""
    list_display = [
        'company',
        'photo_type',
        'uploader',
        'is_approved',
        'created_at',
        'photo_preview'
    ]
    list_filter = ['photo_type', 'is_approved', 'created_at']
    search_fields = ['company__name', 'caption', 'uploader__username']
    readonly_fields = ['created_at', 'photo_preview']
    fieldsets = (
        ('Photo Information', {
            'fields': ('company', 'uploader', 'photo', 'photo_preview', 'caption', 'photo_type')
        }),
        ('Approval', {
            'fields': ('is_approved',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
        }),
    )
    actions = ['approve_photos', 'unapprove_photos']

    def photo_preview(self, obj):
        """Display photo preview"""
        if obj.photo:
            return format_html('<img src="{}" width="200" style="max-height: 200px; object-fit: contain;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo Preview"

    def approve_photos(self, request, queryset):
        """Approve selected photos"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} photos approved.")
    approve_photos.short_description = "Approve selected photos"

    def unapprove_photos(self, request, queryset):
        """Unapprove selected photos"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} photos unapproved.")
    unapprove_photos.short_description = "Unapprove selected photos"


@admin.register(CompanyBenefit)
class CompanyBenefitAdmin(admin.ModelAdmin):
    """Admin interface for CompanyBenefit model"""
    list_display = ['company', 'benefit_category', 'benefit_name', 'created_at']
    list_filter = ['benefit_category', 'created_at']
    search_fields = ['company__name', 'benefit_name', 'description']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Benefit Information', {
            'fields': ('company', 'benefit_category', 'benefit_name', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
        }),
    )
