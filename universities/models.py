from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class UniversityProgram(models.Model):
    """Engineering programs at Pakistani universities"""
    DEGREE_CHOICES = [
        ('BS', 'BS'),
        ('MS', 'MS'),
        ('PhD', 'PhD'),
        ('Diploma', 'Diploma'),
    ]

    university_name = models.CharField(max_length=200)
    program_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    discipline = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    accreditation = models.JSONField(default=list)  # e.g., ['PEC', 'HEC']
    duration = models.CharField(max_length=50)
    overview = models.TextField()
    pros = models.JSONField(default=list)
    cons = models.JSONField(default=list)
    employability_score = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    research_opportunities = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['university_name', 'program_name']
        unique_together = ['university_name', 'program_name', 'degree']

    def __str__(self):
        return f"{self.degree} in {self.program_name} - {self.university_name}"

    def get_absolute_url(self):
        return reverse('universities:program_detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(r.rating for r in reviews) / len(reviews)


class ProgramReview(models.Model):
    """Reviews of university programs"""
    program = models.ForeignKey(UniversityProgram, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    graduation_year = models.CharField(max_length=4, blank=True)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['program', 'author']

    def __str__(self):
        return f"{self.author.username}'s review of {self.program}"
