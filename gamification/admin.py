from django.contrib import admin
from .models import Badge, UserBadge, ReputationScore, WeeklyChallenge, ChallengeSubmission, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'rarity', 'points_value', 'times_awarded']
    list_filter = ['badge_type', 'rarity']
    search_fields = ['name', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at', 'display_on_profile']
    list_filter = ['badge', 'display_on_profile']
    search_fields = ['user__username']


@admin.register(ReputationScore)
class ReputationScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'reputation_level', 'posts_created', 'helpful_votes_received']
    list_filter = ['reputation_level']
    search_fields = ['user__username']


@admin.register(WeeklyChallenge)
class WeeklyChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_type', 'difficulty', 'start_date', 'end_date', 'points_reward']
    list_filter = ['challenge_type', 'difficulty', 'start_date']
    search_fields = ['title', 'discipline']


@admin.register(ChallengeSubmission)
class ChallengeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'user', 'score', 'is_winner', 'submitted_at']
    list_filter = ['is_winner', 'challenge']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['period_type', 'period_start', 'period_end', 'created_at']
    list_filter = ['period_type']
