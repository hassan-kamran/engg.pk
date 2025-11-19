from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ThoughtLeader(models.Model):
    """Verified professionals and thought leaders users can follow"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='thought_leader_profile')
    title = models.CharField(max_length=200, help_text="e.g., Senior Software Engineer, CEO")
    organization = models.CharField(max_length=200, blank=True)
    bio = models.TextField()
    expertise_areas = models.JSONField(default=list, help_text="List of expertise areas")
    verified = models.BooleanField(default=False)
    follower_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-follower_count']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.title}"


class ProfessionalBody(models.Model):
    """Professional organizations and bodies that users can follow"""
    CATEGORY_CHOICES = [
        ('association', 'Professional Association'),
        ('company', 'Company'),
        ('university', 'University'),
        ('government', 'Government Body'),
        ('startup', 'Startup'),
        ('ngo', 'NGO/Non-Profit'),
    ]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organizations/', blank=True, null=True)

    verified = models.BooleanField(default=False)
    follower_count = models.PositiveIntegerField(default=0)

    # Admins who can post on behalf of the organization
    admins = models.ManyToManyField(User, related_name='managed_organizations', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Professional Bodies'

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    """Users following thought leaders"""
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    thought_leader = models.ForeignKey(ThoughtLeader, on_delete=models.CASCADE, related_name='followers')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'thought_leader')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subscriber.username} follows {self.thought_leader.user.username}"


class OrganizationSubscription(models.Model):
    """Users following professional bodies"""
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_subscriptions')
    organization = models.ForeignKey(ProfessionalBody, on_delete=models.CASCADE, related_name='followers')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'organization')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subscriber.username} follows {self.organization.name}"


class TopicSubscription(models.Model):
    """Users subscribing to specific topics/categories"""
    TOPIC_CHOICES = [
        ('general', 'General Engineering'),
        ('career', 'Career Development'),
        ('technical', 'Technical Discussions'),
        ('industry', 'Industry News'),
        ('academia', 'Academia & Research'),
        ('startups', 'Startups & Entrepreneurship'),
        ('jobs', 'Job Opportunities'),
        ('scholarships', 'Scholarships'),
        ('software', 'Software Engineering'),
        ('civil', 'Civil Engineering'),
        ('electrical', 'Electrical Engineering'),
        ('mechanical', 'Mechanical Engineering'),
        ('chemical', 'Chemical Engineering'),
    ]

    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_subscriptions')
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'topic')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subscriber.username} follows {self.get_topic_display()}"


class FeedPost(models.Model):
    """Posts that appear in user feeds - can be from thought leaders or organizations"""
    POST_TYPE_CHOICES = [
        ('article', 'Article'),
        ('announcement', 'Announcement'),
        ('insight', 'Industry Insight'),
        ('discussion', 'Discussion'),
        ('job', 'Job Posting'),
        ('event', 'Event'),
    ]

    # Author can be either a user or an organization
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feed_posts', null=True, blank=True)
    author_organization = models.ForeignKey(ProfessionalBody, on_delete=models.CASCADE, related_name='feed_posts', null=True, blank=True)

    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='discussion')
    title = models.CharField(max_length=300)
    content = models.TextField()

    # Optional link to external content
    external_link = models.URLField(blank=True)

    # Topics/tags for categorization
    topics = models.JSONField(default=list, help_text="List of relevant topics")

    # Engagement metrics
    likes = models.ManyToManyField(User, related_name='liked_feed_posts', blank=True)
    views = models.PositiveIntegerField(default=0)

    # Optional reference to related content (forum post, job, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['post_type']),
        ]

    def __str__(self):
        author = self.author_user.get_full_name() if self.author_user else self.author_organization.name
        return f"{author}: {self.title[:50]}"

    @property
    def author_name(self) -> str:
        """
        Get the author name regardless of type.

        Returns:
            str: Full name or username for user authors, name for organization authors
        """
        if self.author_user:
            return self.author_user.get_full_name() or self.author_user.username
        elif self.author_organization:
            return self.author_organization.name
        return "Unknown"

    @property
    def author_is_verified(self) -> bool:
        """
        Check if author is verified.

        Returns:
            bool: True if author is a verified thought leader or organization
        """
        if self.author_user and hasattr(self.author_user, 'thought_leader_profile'):
            return self.author_user.thought_leader_profile.verified
        elif self.author_organization:
            return self.author_organization.verified
        return False

    def get_like_count(self) -> int:
        """
        Get the number of likes for this post.

        Note: This method is deprecated. Use annotate(like_count=Count('likes'))
        in your queryset instead to avoid N+1 queries.

        Returns:
            int: Number of likes
        """
        return self.likes.count()


class Comment(models.Model):
    """Comments on feed posts"""
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feed_comments')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_feed_comments', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title[:30]}"

    def get_like_count(self) -> int:
        """
        Get the number of likes for this comment.

        Note: This method is deprecated. Use annotate(like_count=Count('likes'))
        in your queryset instead to avoid N+1 queries.

        Returns:
            int: Number of likes
        """
        return self.likes.count()
