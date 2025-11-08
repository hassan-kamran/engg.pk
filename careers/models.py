from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class CareerPath(models.Model):
    """Different engineering career paths"""
    title = models.CharField(max_length=200)
    discipline = models.CharField(max_length=100)
    overview = models.TextField()
    skills = models.JSONField(default=list)
    industries = models.JSONField(default=list)
    salary_range = models.CharField(max_length=100)
    growth_outlook = models.TextField()
    education_required = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.discipline})"

    def get_absolute_url(self):
        return reverse('careers:detail', kwargs={'pk': self.pk})


class ExperienceStory(models.Model):
    """Real stories from professionals"""
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='stories')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experience_stories')
    title = models.CharField(max_length=200)
    content = models.TextField()
    current_position = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Experience Stories'

    def __str__(self):
        return f"{self.title} by {self.author.username}"
