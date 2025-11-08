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

    def get_absolute_url(self):
        return reverse('forum:post_detail', kwargs={'pk': self.pk})

    @property
    def reply_count(self):
        return self.replies.count()

    @property
    def like_count(self):
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

    @property
    def like_count(self):
        return self.likes.count()
