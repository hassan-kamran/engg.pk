from django.db import models
from django.contrib.auth.models import User


class CofounderProfile(models.Model):
    """Co-founder matching profiles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cofounder_profile')

    # Background
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('technical', 'Technical/Engineering'),
            ('business', 'Business/Management'),
            ('designer', 'Design/UX'),
            ('domain_expert', 'Domain Expert'),
        ]
    )
    expertise = models.TextField(help_text="Your areas of expertise (comma-separated)")
    years_of_experience = models.PositiveIntegerField()
    current_status = models.CharField(max_length=200, help_text="Current role/status")

    # What they're looking for
    looking_for_cofounder = models.BooleanField(default=True)
    seeking_background = models.TextField(help_text="What type of co-founder are you looking for?")
    startup_stage = models.CharField(
        max_length=20,
        choices=[
            ('idea', 'Just an Idea'),
            ('mvp', 'Building MVP'),
            ('launched', 'Launched'),
            ('growing', 'Growing'),
        ]
    )

    # Startup interests
    industry_interests = models.TextField(help_text="Industries of interest (comma-separated)")
    startup_idea_summary = models.TextField(blank=True)
    looking_for_equity_split = models.CharField(max_length=100, blank=True, help_text="e.g., '50/50', '60/40'")

    # Commitment
    can_work_fulltime = models.BooleanField(default=False)
    location_preference = models.CharField(max_length=100)
    remote_ok = models.BooleanField(default=True)

    # Profile
    bio = models.TextField()
    past_ventures = models.TextField(blank=True, help_text="Previous startup/business experience")
    skills = models.TextField()
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'business_cofounder_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['background_type', 'is_active']),
            models.Index(fields=['startup_stage']),
        ]

    def __str__(self):
        return f"{self.user.username} - Looking for {self.seeking_background}"


class RegulatoryGuide(models.Model):
    """Regulatory and compliance guides"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(
        max_length=30,
        choices=[
            ('business_registration', 'Business Registration'),
            ('tax', 'Tax & Compliance'),
            ('import_export', 'Import/Export'),
            ('intellectual_property', 'IP & Patents'),
            ('labor_law', 'Labor Laws'),
            ('engineering_practice', 'Engineering Practice Act'),
        ]
    )

    # Content
    summary = models.TextField()
    detailed_guide = models.TextField()
    step_by_step_process = models.TextField()
    required_documents = models.TextField()
    estimated_cost = models.CharField(max_length=100, blank=True)
    estimated_timeline = models.CharField(max_length=100, blank=True)

    # Authorities
    relevant_authorities = models.TextField(help_text="Which government bodies are involved?")
    authority_contacts = models.TextField(blank=True)

    # Resources
    official_links = models.TextField(blank=True, help_text="Official government links")
    downloadable_forms = models.FileField(upload_to='regulatory/forms/', blank=True)

    # Updates
    last_verified_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='regulatory_guides_authored')

    helpful_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'business_regulatory_guides'
        ordering = ['category', 'title']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title


class FundingOpportunity(models.Model):
    """Funding calendar for startups"""
    title = models.CharField(max_length=200)
    funding_type = models.CharField(
        max_length=30,
        choices=[
            ('grant', 'Grant'),
            ('competition', 'Pitch Competition'),
            ('accelerator', 'Accelerator Program'),
            ('investor', 'Investor Funding Round'),
            ('government', 'Government Fund'),
        ]
    )

    # Details
    description = models.TextField()
    provider = models.CharField(max_length=200)
    amount = models.CharField(max_length=100, help_text="Funding amount available")
    equity_required = models.CharField(max_length=100, blank=True)

    # Eligibility
    eligibility_criteria = models.TextField()
    target_industries = models.TextField(help_text="Comma-separated industries")
    startup_stage_required = models.CharField(max_length=100)
    location_requirement = models.CharField(max_length=200, blank=True)

    # Dates
    application_open_date = models.DateField()
    application_deadline = models.DateField()
    decision_date = models.DateField(null=True, blank=True)

    # Application
    application_url = models.URLField()
    application_process = models.TextField()
    required_materials = models.TextField()

    # Additional info
    website = models.URLField()
    contact_email = models.EmailField(blank=True)
    pakistan_friendly = models.BooleanField(default=True, help_text="Open to Pakistani startups")

    views = models.PositiveIntegerField(default=0)
    applicants_interested = models.ManyToManyField(User, related_name='interested_funding', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'business_funding_opportunities'
        verbose_name_plural = 'Funding Opportunities'
        ordering = ['application_deadline']
        indexes = [
            models.Index(fields=['funding_type']),
            models.Index(fields=['application_deadline']),
        ]

    def __str__(self):
        return self.title

    def is_open(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.application_open_date <= today <= self.application_deadline
