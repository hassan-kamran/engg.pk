from django.db import models
from django.urls import reverse


class Scholarship(models.Model):
    """Scholarship opportunities for engineers"""
    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctoral', 'Doctoral'),
        ('postdoctoral', 'Postdoctoral'),
    ]

    FUNDING_CHOICES = [
        ('fully', 'Fully Funded'),
        ('partial', 'Partially Funded'),
    ]

    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    disciplines = models.JSONField(default=list)
    amount = models.CharField(max_length=200)
    deadline = models.DateField()
    description = models.TextField()
    eligibility = models.JSONField(default=list)
    application_url = models.URLField()
    funded = models.CharField(max_length=20, choices=FUNDING_CHOICES)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deadline']
        indexes = [
            models.Index(fields=['deadline']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return f"{self.name} - {self.provider}"

    def get_absolute_url(self):
        return reverse('scholarships:detail', kwargs={'pk': self.pk})
