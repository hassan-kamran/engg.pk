from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    """Achievement badges"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    badge_type = models.CharField(
        max_length=30,
        choices=[
            ('contribution', 'Contribution'),
            ('expertise', 'Expertise'),
            ('milestone', 'Milestone'),
            ('special', 'Special'),
        ]
    )

    # Criteria
    criteria = models.TextField(help_text="How to earn this badge")
    points_value = models.PositiveIntegerField(default=10)

    # Appearance
    icon = models.ImageField(upload_to='badges/', blank=True)
    color = models.CharField(max_length=20, default='blue')
    rarity = models.CharField(
        max_length=20,
        choices=[
            ('common', 'Common'),
            ('uncommon', 'Uncommon'),
            ('rare', 'Rare'),
            ('epic', 'Epic'),
            ('legendary', 'Legendary'),
        ],
        default='common'
    )

    times_awarded = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gamification_badges'
        ordering = ['rarity', 'name']

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """User-earned badges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges_earned')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    display_on_profile = models.BooleanField(default=True)

    class Meta:
        db_table = 'gamification_user_badges'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class ReputationScore(models.Model):
    """User reputation system"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reputation')

    # Overall scores
    total_points = models.IntegerField(default=0)
    reputation_level = models.CharField(
        max_length=20,
        choices=[
            ('newcomer', 'Newcomer'),
            ('member', 'Member'),
            ('contributor', 'Contributor'),
            ('expert', 'Expert'),
            ('guru', 'Guru'),
            ('legend', 'Legend'),
        ],
        default='newcomer'
    )

    # Activity breakdown
    posts_created = models.PositiveIntegerField(default=0)
    replies_posted = models.PositiveIntegerField(default=0)
    helpful_votes_received = models.PositiveIntegerField(default=0)
    best_answers = models.PositiveIntegerField(default=0)

    # Contributions
    resources_shared = models.PositiveIntegerField(default=0)
    projects_showcased = models.PositiveIntegerField(default=0)
    reviews_written = models.PositiveIntegerField(default=0)

    # Engagement
    consecutive_days_active = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(auto_now=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gamification_reputation_scores'

    def __str__(self):
        return f"{self.user.username} - {self.total_points} points ({self.reputation_level})"

    def calculate_level(self):
        """Calculate reputation level based on points"""
        if self.total_points < 100:
            return 'newcomer'
        elif self.total_points < 500:
            return 'member'
        elif self.total_points < 1500:
            return 'contributor'
        elif self.total_points < 5000:
            return 'expert'
        elif self.total_points < 15000:
            return 'guru'
        else:
            return 'legend'


class WeeklyChallenge(models.Model):
    """Weekly challenges"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(
        max_length=30,
        choices=[
            ('technical', 'Technical Problem'),
            ('design', 'Design Challenge'),
            ('trivia', 'Engineering Trivia'),
            ('code_review', 'Code Review'),
        ]
    )

    # Challenge content
    problem_statement = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ]
    )
    discipline = models.CharField(max_length=100)

    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Rewards
    points_reward = models.PositiveIntegerField(default=50)
    badge_reward = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)

    # Engagement
    participants = models.ManyToManyField(User, through='ChallengeSubmission', related_name='challenges_joined')
    views = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gamification_weekly_challenges'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['-start_date']),
            models.Index(fields=['challenge_type']),
        ]

    def __str__(self):
        return self.title

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date


class ChallengeSubmission(models.Model):
    """User submissions for challenges"""
    challenge = models.ForeignKey(WeeklyChallenge, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_submissions')

    submission_text = models.TextField()
    submission_file = models.FileField(upload_to='challenge_submissions/', blank=True)
    submission_url = models.URLField(blank=True)

    # Scoring
    score = models.PositiveIntegerField(null=True, blank=True)
    is_winner = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    upvotes = models.ManyToManyField(User, related_name='challenge_upvotes', blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gamification_challenge_submissions'
        unique_together = ['challenge', 'user']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

    def upvote_count(self):
        return self.upvotes.count()


class Leaderboard(models.Model):
    """Periodic leaderboards"""
    period_type = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('all_time', 'All Time'),
        ]
    )
    period_start = models.DateField()
    period_end = models.DateField()

    # Top users (JSON or separate relation)
    top_users_data = models.JSONField(help_text="Cached leaderboard data")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gamification_leaderboards'
        ordering = ['-period_start']
        indexes = [
            models.Index(fields=['period_type', '-period_start']),
        ]

    def __str__(self):
        return f"{self.period_type} - {self.period_start} to {self.period_end}"
