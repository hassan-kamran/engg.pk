from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile for engineers"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('expert', 'Expert'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', db_index=True)
    expertise = models.JSONField(default=list, blank=True)  # List of expertise areas
    affiliation = models.CharField(max_length=200, blank=True)
    verified = models.BooleanField(default=False, db_index=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"


class SubjectConnection(models.Model):
    """Mapping of how subjects connect to real-world applications"""
    subject = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    related_subjects = models.JSONField(default=list)  # List of related subject names
    applications = models.JSONField(default=list)  # Real-world applications
    career_paths = models.JSONField(default=list)  # Related career paths
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return self.subject
