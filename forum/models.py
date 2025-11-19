from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class ForumPost(models.Model):
    """Community forum posts"""
    CATEGORY_CHOICES = [
        ('general', 'General Discussion'),
        ('career', 'Career Guidance'),
        ('technical', 'Technical Questions'),
        ('industry', 'Industry Insights'),
        ('academia', 'Academia'),
        ('startups', 'Startups'),
        ('jobs', 'Job Opportunities'),
        ('scholarships', 'Scholarships'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, blank=True)

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        """
        Get the absolute URL for this forum post.

        Returns:
            str: The URL to view this post
        """
        return reverse('forum:post_detail', kwargs={'pk': self.pk})

    def get_reply_count(self) -> int:
        """
        Get the number of replies for this post.

        Note: This method is deprecated. Use annotate(reply_count=Count('replies'))
        in your queryset instead to avoid N+1 queries.

        Returns:
            int: Number of replies
        """
        return self.replies.count()

    def get_like_count(self) -> int:
        """
        Get the number of likes for this post.

        Note: This method is deprecated. Use annotate(like_count=Count('likes'))
        in your queryset instead to avoid N+1 queries.

        Returns:
            int: Number of likes
        """
        return self.likes.count()


class Reply(models.Model):
    """Replies to forum posts"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f"Reply by {self.author.username} on {self.post.title}"

    def get_like_count(self) -> int:
        """
        Get the number of likes for this reply.

        Note: This method is deprecated. Use annotate(like_count=Count('likes'))
        in your queryset instead to avoid N+1 queries.

        Returns:
            int: Number of likes
        """
        return self.likes.count()
