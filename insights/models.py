from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class IndustryInsight(models.Model):
    """Expert insights about engineering industries"""
    title = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insights')
    discipline = models.CharField(max_length=100)
    topics = models.JSONField(default=list)
    views = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['industry']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('insights:detail', kwargs={'pk': self.pk})
