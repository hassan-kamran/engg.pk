from django.db import models
from django.urls import reverse


class Job(models.Model):
    """Engineering job listings"""
    TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    LEVEL_CHOICES = [
        ('entry', 'Entry'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    discipline = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField()
    requirements = models.JSONField(default=list)
    salary = models.CharField(max_length=100, blank=True)
    application_url = models.URLField()
    is_active = models.BooleanField(default=True)
    posted_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_date']
        indexes = [
            models.Index(fields=['-posted_date']),
            models.Index(fields=['job_type']),
            models.Index(fields=['discipline']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'pk': self.pk})
