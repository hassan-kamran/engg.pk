from django.db import models
from django.contrib.auth.models import User


class FreelanceProject(models.Model):
    """Freelance and consulting marketplace"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelance_projects_posted')

    # Project details
    category = models.CharField(
        max_length=30,
        choices=[
            ('design', 'Design & CAD'),
            ('analysis', 'Analysis & Simulation'),
            ('development', 'Software Development'),
            ('consulting', 'Technical Consulting'),
            ('documentation', 'Technical Documentation'),
            ('other', 'Other'),
        ]
    )
    discipline = models.CharField(max_length=100)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, help_text="In PKR")
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, help_text="In PKR")

    duration = models.CharField(max_length=100, help_text="e.g., '2 weeks', '1 month'")
    required_skills = models.TextField(help_text="Comma-separated skills")
    experience_required = models.CharField(
        max_length=20,
        choices=[
            ('entry', 'Entry Level'),
            ('intermediate', 'Intermediate'),
            ('expert', 'Expert'),
        ]
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open for Proposals'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='open'
    )

    location_required = models.CharField(max_length=100, blank=True, help_text="If on-site work needed")
    remote_ok = models.BooleanField(default=True)

    proposals_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    class Meta:
        db_table = 'marketplace_freelance_projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['discipline']),
        ]

    def __str__(self):
        return self.title


class FreelanceProposal(models.Model):
    """Proposals for freelance projects"""
    project = models.ForeignKey(FreelanceProject, on_delete=models.CASCADE, related_name='proposals')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelance_proposals')
    cover_letter = models.TextField()
    proposed_budget = models.DecimalField(max_digits=10, decimal_places=2)
    proposed_timeline = models.CharField(max_length=100)
    portfolio_links = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'marketplace_freelance_proposals'
        unique_together = ['project', 'freelancer']
        ordering = ['-created_at']


class ResearchCollaboration(models.Model):
    """Research collaboration network"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='research_collaborations_initiated')

    # Research details
    discipline = models.CharField(max_length=100)
    research_area = models.CharField(max_length=200)
    keywords = models.TextField(help_text="Comma-separated keywords")

    collaboration_type = models.CharField(
        max_length=30,
        choices=[
            ('co_author', 'Looking for Co-Authors'),
            ('data_sharing', 'Data Sharing'),
            ('equipment_sharing', 'Equipment/Lab Sharing'),
            ('expertise', 'Need Specific Expertise'),
            ('funding_partner', 'Looking for Funding Partner'),
        ]
    )

    # Requirements
    looking_for = models.TextField(help_text="What kind of collaborators are you looking for?")
    expected_commitment = models.TextField()
    timeline = models.CharField(max_length=100)

    # Institution
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)

    remote_collaboration_ok = models.BooleanField(default=True)
    funding_available = models.BooleanField(default=False)
    funding_details = models.TextField(blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    interested_users = models.ManyToManyField(User, related_name='research_interests', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'marketplace_research_collaborations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.title


class Conference(models.Model):
    """Conference and workshop directory"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    conference_type = models.CharField(
        max_length=20,
        choices=[
            ('conference', 'Conference'),
            ('workshop', 'Workshop'),
            ('symposium', 'Symposium'),
            ('seminar', 'Seminar'),
        ]
    )

    # Disciplines and topics
    discipline = models.CharField(max_length=100)
    topics = models.TextField(help_text="Comma-separated topics")

    # Dates and location
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    virtual_option = models.BooleanField(default=False)

    # Paper submission
    accepts_papers = models.BooleanField(default=True)
    paper_submission_deadline = models.DateField(null=True, blank=True)
    notification_date = models.DateField(null=True, blank=True)
    camera_ready_deadline = models.DateField(null=True, blank=True)

    # Registration
    early_registration_deadline = models.DateField(null=True, blank=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="In USD")
    student_discount = models.BooleanField(default=False)

    # Links
    website = models.URLField()
    submission_portal = models.URLField(blank=True)

    # Pakistani participation
    pakistan_friendly = models.BooleanField(default=False, help_text="Easy visa/affordable for Pakistanis")
    travel_grants_available = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'marketplace_conferences'
        ordering = ['paper_submission_deadline']
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['paper_submission_deadline']),
        ]

    def __str__(self):
        return f"{self.name} ({self.start_date.year})"
