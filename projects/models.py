from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """Project showcase platform"""
    PROJECT_TYPES = [
        ('final_year', 'Final Year Project'),
        ('personal', 'Personal Project'),
        ('hackathon', 'Hackathon Project'),
        ('research', 'Research Project'),
        ('open_source', 'Open Source'),
        ('commercial', 'Commercial Project'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    discipline = models.CharField(max_length=100)

    # Details
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_owned')
    team_members = models.ManyToManyField(User, related_name='projects_member', blank=True)
    university = models.CharField(max_length=200, blank=True)
    completion_date = models.DateField()

    # Technical details
    technologies_used = models.TextField(help_text="Comma-separated list")
    problem_statement = models.TextField()
    solution_approach = models.TextField()
    key_features = models.TextField()
    challenges_faced = models.TextField(blank=True)

    # Links and media
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True)

    # Engagement
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='projects_liked', blank=True)
    featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects_projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['project_type']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-views']),
        ]

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()


class OpenSourceProject(models.Model):
    """Open source collaboration board"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    repository_url = models.URLField()
    primary_language = models.CharField(max_length=50)
    maintainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='os_projects_maintained')

    # Project details
    license = models.CharField(max_length=50)
    topics = models.TextField(help_text="Comma-separated topics/tags")
    looking_for_contributors = models.BooleanField(default=True)
    skill_level_required = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner Friendly'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )

    # Contribution info
    contribution_guidelines = models.TextField()
    good_first_issues = models.PositiveIntegerField(default=0, help_text="Number of good first issues")
    contributors_count = models.PositiveIntegerField(default=0)
    stars = models.PositiveIntegerField(default=0)
    forks = models.PositiveIntegerField(default=0)

    # Pakistani contributor focus
    pakistani_contributors = models.ManyToManyField(User, related_name='os_projects_contributed', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects_open_source'
        ordering = ['-stars']
        indexes = [
            models.Index(fields=['primary_language']),
            models.Index(fields=['looking_for_contributors']),
        ]

    def __str__(self):
        return self.name


class Competition(models.Model):
    """Engineering competitions hub"""
    COMPETITION_TYPES = [
        ('robotics', 'Robotics'),
        ('hackathon', 'Hackathon'),
        ('design', 'Design Challenge'),
        ('coding', 'Coding Competition'),
        ('innovation', 'Innovation Contest'),
        ('case_study', 'Case Study'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    competition_type = models.CharField(max_length=20, choices=COMPETITION_TYPES)
    organizer = models.CharField(max_length=200)

    # Eligibility
    discipline = models.CharField(max_length=100, blank=True)
    eligible_levels = models.CharField(
        max_length=100,
        help_text="Undergraduate, Graduate, etc. (comma-separated)"
    )
    team_size_min = models.PositiveIntegerField(default=1)
    team_size_max = models.PositiveIntegerField()

    # Dates
    registration_start = models.DateField()
    registration_deadline = models.DateField()
    event_start_date = models.DateField()
    event_end_date = models.DateField()

    # Details
    location = models.CharField(max_length=200)
    format = models.CharField(
        max_length=20,
        choices=[
            ('online', 'Online'),
            ('in_person', 'In-Person'),
            ('hybrid', 'Hybrid'),
        ]
    )
    prizes = models.TextField(help_text="Prize details")
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    registration_url = models.URLField()
    website = models.URLField(blank=True)

    # Engagement
    participants = models.ManyToManyField(User, related_name='competitions_joined', through='CompetitionParticipation')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects_competitions'
        ordering = ['registration_deadline']
        indexes = [
            models.Index(fields=['competition_type']),
            models.Index(fields=['registration_deadline']),
        ]

    def __str__(self):
        return self.title

    def is_registration_open(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.registration_start <= today <= self.registration_deadline


class CompetitionParticipation(models.Model):
    """Track competition participation"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=200, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects_competition_participation'
        unique_together = ['competition', 'user']


class WinningProject(models.Model):
    """Archive of past winning projects"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='winners')
    project_title = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200)
    team_members = models.TextField()
    university = models.CharField(max_length=200, blank=True)
    prize = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(blank=True)
    year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects_winning_projects'
        ordering = ['-year']
        indexes = [
            models.Index(fields=['-year']),
        ]

    def __str__(self):
        return f"{self.project_title} - {self.competition.title} {self.year}"
