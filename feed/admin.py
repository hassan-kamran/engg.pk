from django.contrib import admin
from .models import (
    ThoughtLeader, ProfessionalBody, UserSubscription,
    OrganizationSubscription, TopicSubscription, FeedPost, Comment
)


@admin.register(ThoughtLeader)
class ThoughtLeaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'organization', 'verified', 'follower_count', 'created_at')
    list_filter = ('verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'organization')
    readonly_fields = ('follower_count', 'created_at', 'updated_at')


@admin.register(ProfessionalBody)
class ProfessionalBodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'verified', 'follower_count', 'created_at')
    list_filter = ('category', 'verified', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('follower_count', 'created_at', 'updated_at')
    filter_horizontal = ('admins',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'thought_leader', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subscriber__username', 'thought_leader__user__username')
    raw_id_fields = ('subscriber', 'thought_leader')


@admin.register(OrganizationSubscription)
class OrganizationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'organization', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subscriber__username', 'organization__name')
    raw_id_fields = ('subscriber', 'organization')


@admin.register(TopicSubscription)
class TopicSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'topic', 'created_at')
    list_filter = ('topic', 'created_at')
    search_fields = ('subscriber__username',)


@admin.register(FeedPost)
class FeedPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'post_type', 'like_count', 'views', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('title', 'content', 'author_user__username', 'author_organization__name')
    readonly_fields = ('views', 'created_at', 'updated_at')
    raw_id_fields = ('author_user', 'author_organization')
    filter_horizontal = ('likes',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'like_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')
    raw_id_fields = ('author', 'post')
    filter_horizontal = ('likes',)
