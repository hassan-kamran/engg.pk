from django.db import models
from django.urls import reverse


class StartupResource(models.Model):
    """Resources for tech startups in Pakistan"""
    CATEGORY_CHOICES = [
        ('funding', 'Funding'),
        ('incubator', 'Incubator'),
        ('accelerator', 'Accelerator'),
        ('mentorship', 'Mentorship'),
        ('legal', 'Legal'),
        ('technical', 'Technical'),
        ('guide', 'Guide'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    provider = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    eligibility = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def get_absolute_url(self):
        return reverse('startups:detail', kwargs={'pk': self.pk})
