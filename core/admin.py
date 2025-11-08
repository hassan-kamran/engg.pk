from django.contrib import admin
from .models import UserProfile, SubjectConnection


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'affiliation', 'verified', 'created_at']
    list_filter = ['role', 'verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'affiliation']
    readonly_fields = ['created_at']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'verified')
        }),
        ('Professional Details', {
            'fields': ('expertise', 'affiliation', 'bio', 'avatar')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(SubjectConnection)
class SubjectConnectionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at', 'updated_at']
    search_fields = ['subject', 'description']
    readonly_fields = ['created_at', 'updated_at']
