from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    """Resume/CV builder"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, help_text="e.g., 'Software Engineer Resume'")

    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    # Professional Summary
    summary = models.TextField()

    # Template and styling
    template = models.CharField(
        max_length=20,
        choices=[
            ('modern', 'Modern'),
            ('classic', 'Classic'),
            ('technical', 'Technical'),
            ('minimalist', 'Minimalist'),
        ],
        default='modern'
    )

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'career_tools_resumes'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ResumeEducation(models.Model):
    """Education section of resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_studying = models.BooleanField(default=False)
    gpa = models.CharField(max_length=20, blank=True)
    achievements = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_tools_resume_education'
        ordering = ['order', '-start_date']


class ResumeExperience(models.Model):
    """Work experience section"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    responsibilities = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_tools_resume_experience'
        ordering = ['order', '-start_date']


class ResumeSkill(models.Model):
    """Skills section"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    category = models.CharField(max_length=100, help_text="e.g., Programming Languages, Tools, etc.")
    skills = models.TextField(help_text="Comma-separated skills")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_tools_resume_skills'
        ordering = ['order']


class ResumeProject(models.Model):
    """Projects section"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_tools_resume_projects'
        ordering = ['order']


class SalaryData(models.Model):
    """Anonymous salary comparison data"""
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Job details
    position = models.CharField(max_length=200)
    discipline = models.CharField(max_length=100)
    company_size = models.CharField(
        max_length=20,
        choices=[
            ('startup', 'Startup (1-50)'),
            ('small', 'Small (51-200)'),
            ('medium', 'Medium (201-1000)'),
            ('large', 'Large (1000+)'),
        ]
    )
    company_type = models.CharField(
        max_length=20,
        choices=[
            ('local', 'Local Pakistani Company'),
            ('multinational', 'Multinational'),
            ('remote_foreign', 'Remote for Foreign Company'),
        ]
    )

    # Experience and location
    years_of_experience = models.PositiveIntegerField()
    city = models.CharField(max_length=100)

    # Compensation (in PKR)
    base_salary_monthly = models.DecimalField(max_digits=12, decimal_places=2)
    bonus_annual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_options = models.BooleanField(default=False)

    # Benefits
    health_insurance = models.BooleanField(default=False)
    provident_fund = models.BooleanField(default=False)
    paid_leave_days = models.PositiveIntegerField(default=0)

    # Additional info
    work_from_home = models.BooleanField(default=False)
    satisfaction_rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Overall job satisfaction"
    )

    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    data_year = models.PositiveIntegerField()

    class Meta:
        db_table = 'career_tools_salary_data'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['position', 'city']),
            models.Index(fields=['discipline']),
            models.Index(fields=['years_of_experience']),
        ]

    def __str__(self):
        return f"{self.position} - {self.city} ({self.years_of_experience} years)"

    def total_annual_compensation(self):
        return (self.base_salary_monthly * 12) + self.bonus_annual


class CareerTransitionStory(models.Model):
    """Stories of career transitions"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transition_stories')
    title = models.CharField(max_length=200)

    # Transition details
    from_discipline = models.CharField(max_length=100)
    to_discipline = models.CharField(max_length=100)
    from_role = models.CharField(max_length=200)
    to_role = models.CharField(max_length=200)

    transition_type = models.CharField(
        max_length=30,
        choices=[
            ('discipline_switch', 'Switched Engineering Discipline'),
            ('academia_to_industry', 'Academia to Industry'),
            ('industry_to_academia', 'Industry to Academia'),
            ('pakistan_to_abroad', 'Pakistan to Abroad'),
            ('abroad_to_pakistan', 'Abroad to Pakistan'),
            ('startup_journey', 'Started Own Company'),
        ]
    )

    # Timeline
    years_in_previous_field = models.PositiveIntegerField()
    transition_duration_months = models.PositiveIntegerField(help_text="How long did the transition take?")

    # Story
    motivation = models.TextField(help_text="Why did you make this transition?")
    challenges_faced = models.TextField()
    how_you_did_it = models.TextField(help_text="Steps you took to make the transition")
    advice = models.TextField(help_text="Advice for others considering similar transition")

    # Engagement
    helpful_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'career_tools_transition_stories'
        verbose_name_plural = 'Career Transition Stories'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transition_type']),
            models.Index(fields=['-helpful_count']),
        ]

    def __str__(self):
        return self.title
