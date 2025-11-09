from django.db import models
from django.contrib.auth.models import User


class ThesisTopic(models.Model):
    """Thesis and project topic database"""
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    discipline = models.CharField(max_length=100)
    degree_level = models.CharField(
        max_length=20,
        choices=[
            ('undergraduate', 'Undergraduate'),
            ('masters', 'Masters'),
            ('phd', 'PhD'),
        ]
    )

    # Details
    university = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    supervisor = models.CharField(max_length=200)
    completion_year = models.PositiveIntegerField()

    # Content
    keywords = models.TextField(help_text="Comma-separated keywords")
    methodology = models.TextField()
    key_findings = models.TextField(blank=True)
    future_work = models.TextField(blank=True)

    # Access
    full_text_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to='theses/', blank=True)
    is_public = models.BooleanField(default=True)

    # Engagement
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    citations = models.PositiveIntegerField(default=0)

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thesis_topics_submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academic_thesis_topics'
        ordering = ['-completion_year']
        indexes = [
            models.Index(fields=['discipline', 'degree_level']),
            models.Index(fields=['university']),
            models.Index(fields=['-completion_year']),
        ]

    def __str__(self):
        return self.title


class ResearchSupervisor(models.Model):
    """Research supervisor finder"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_profile')

    # Academic info
    title = models.CharField(max_length=50, help_text="Prof., Dr., etc.")
    full_name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text="Professor, Associate Professor, etc.")

    # Research
    research_interests = models.TextField(help_text="Research areas (comma-separated)")
    discipline = models.CharField(max_length=100)
    expertise_keywords = models.TextField()

    # Supervision
    accepting_students = models.BooleanField(default=True)
    accepting_levels = models.CharField(
        max_length=100,
        help_text="MS, PhD (comma-separated)"
    )
    current_students_count = models.PositiveIntegerField(default=0)
    max_students = models.PositiveIntegerField(default=5)

    # Profile
    bio = models.TextField()
    education = models.TextField()
    publications_count = models.PositiveIntegerField(default=0)
    h_index = models.PositiveIntegerField(null=True, blank=True)

    # Contact preferences
    preferred_contact_method = models.CharField(max_length=50)
    email = models.EmailField()
    office_hours = models.TextField(blank=True)

    # Links
    google_scholar_url = models.URLField(blank=True)
    researchgate_url = models.URLField(blank=True)
    university_profile_url = models.URLField(blank=True)

    # Reviews
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentage")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    reviews_count = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_research_supervisors'
        ordering = ['university', 'full_name']
        indexes = [
            models.Index(fields=['university', 'discipline']),
            models.Index(fields=['accepting_students']),
        ]

    def __str__(self):
        return f"{self.title} {self.full_name}"


class SupervisorReview(models.Model):
    """Anonymous reviews of supervisors"""
    supervisor = models.ForeignKey(ResearchSupervisor, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor_reviews')

    # Relationship
    relationship = models.CharField(
        max_length=20,
        choices=[
            ('current', 'Current Student'),
            ('former', 'Former Student'),
            ('applicant', 'Prospective Student'),
        ]
    )
    degree_level = models.CharField(max_length=20)
    years_supervised = models.PositiveIntegerField(help_text="Duration in years")

    # Ratings
    overall_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    availability = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    guidance_quality = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    research_environment = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    # Review
    pros = models.TextField()
    cons = models.TextField()
    advice = models.TextField(help_text="Advice for future students")

    would_recommend = models.BooleanField()
    helpful_count = models.PositiveIntegerField(default=0)
    verified_student = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academic_supervisor_reviews'
        ordering = ['-created_at']


class Publication(models.Model):
    """Track Pakistani engineering research output"""
    title = models.CharField(max_length=300)
    authors = models.TextField()
    pakistani_authors = models.ManyToManyField(User, related_name='publications', blank=True)

    # Publication details
    publication_type = models.CharField(
        max_length=20,
        choices=[
            ('journal', 'Journal Article'),
            ('conference', 'Conference Paper'),
            ('thesis', 'Thesis'),
            ('book', 'Book/Chapter'),
            ('preprint', 'Preprint'),
        ]
    )
    venue = models.CharField(max_length=300, help_text="Journal/Conference name")
    year = models.PositiveIntegerField()
    volume = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)

    # Content
    abstract = models.TextField()
    keywords = models.TextField()
    discipline = models.CharField(max_length=100)

    # Metrics
    doi = models.CharField(max_length=100, blank=True)
    citations = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    # Links
    pdf_url = models.URLField(blank=True)
    external_url = models.URLField()

    # Pakistani context
    pakistani_institutions = models.TextField(help_text="Institutions of Pakistani authors")
    pakistan_focused = models.BooleanField(default=False, help_text="Research focused on Pakistan")

    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publications_added')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academic_publications'
        ordering = ['-year']
        indexes = [
            models.Index(fields=['discipline', '-year']),
            models.Index(fields=['-citations']),
        ]

    def __str__(self):
        return self.title
