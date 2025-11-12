from django.db import models
from django.contrib.auth.models import User
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
    is_active = models.BooleanField(default=True, db_index=True)
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

    @property
    def saved_count(self):
        return self.saved_by.count()


class SavedJob(models.Model):
    """Jobs saved by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class JobApplication(models.Model):
    """Track job applications"""
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Under Review'),
        ('interview', 'Interview Scheduled'),
        ('offer', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"
