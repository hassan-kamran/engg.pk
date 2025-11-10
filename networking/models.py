from django.db import models
from django.contrib.auth.models import User


class AlumniProfile(models.Model):
    """Alumni network profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    university = models.CharField(max_length=200)
    degree = models.CharField(
        max_length=20,
        choices=[
            ('bs', 'Bachelor of Science'),
            ('ms', 'Master of Science'),
            ('phd', 'Doctor of Philosophy'),
            ('diploma', 'Diploma'),
        ]
    )
    discipline = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    current_position = models.CharField(max_length=200, blank=True)
    current_company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, help_text="Current city/country")
    willing_to_help = models.BooleanField(default=True, help_text="Willing to help current students?")
    help_areas = models.TextField(blank=True, help_text="What can you help with? (Career advice, referrals, etc.)")
    linkedin_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'networking_alumni_profiles'
        indexes = [
            models.Index(fields=['university', 'graduation_year']),
            models.Index(fields=['discipline']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.university} '{self.graduation_year})"


class CompanyProfile(models.Model):
    """Company profiles for reviews"""
    name = models.CharField(max_length=200, unique=True)
    industry = models.CharField(max_length=100)
    headquarters = models.CharField(max_length=100)
    pakistan_locations = models.TextField(help_text="Cities where company has offices in Pakistan")
    size = models.CharField(
        max_length=20,
        choices=[
            ('startup', '1-50 employees'),
            ('small', '51-200 employees'),
            ('medium', '201-1000 employees'),
            ('large', '1000+ employees'),
        ]
    )
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    website = models.URLField()
    description = models.TextField()
    tech_stack = models.TextField(blank=True, help_text="Technologies used (comma-separated)")
    logo = models.ImageField(upload_to='companies/logos/', blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'networking_company_profiles'
        verbose_name_plural = 'Company Profiles'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['industry']),
        ]

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(r.overall_rating for r in reviews) / len(reviews)


class CompanyReview(models.Model):
    """Employee reviews of companies"""
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_reviews')
    position = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('current', 'Current Employee'),
            ('former', 'Former Employee'),
        ]
    )
    duration_months = models.PositiveIntegerField(help_text="How long did you work there?")
    location = models.CharField(max_length=100)

    # Ratings (1-5)
    overall_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    work_life_balance = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    compensation = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    culture = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    career_growth = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    management = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    # Review content
    pros = models.TextField()
    cons = models.TextField()
    advice_to_management = models.TextField(blank=True)
    engineering_specific_feedback = models.TextField(blank=True, help_text="Technical environment, tools, processes")

    would_recommend = models.BooleanField()
    helpful_count = models.PositiveIntegerField(default=0)
    verified_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'networking_company_reviews'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', '-overall_rating']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.company.name} review by {self.author.username}"


class Event(models.Model):
    """Engineering events calendar"""
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
        ('workshop', 'Workshop'),
        ('meetup', 'Meetup'),
        ('career_fair', 'Career Fair'),
        ('hackathon', 'Hackathon'),
        ('seminar', 'Seminar'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    organizer = models.CharField(max_length=200)
    discipline = models.CharField(max_length=100, blank=True, help_text="Relevant engineering discipline")

    # Date and time
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timezone = models.CharField(max_length=50, default='Asia/Karachi')

    # Location
    format = models.CharField(
        max_length=20,
        choices=[
            ('online', 'Online'),
            ('in_person', 'In-Person'),
            ('hybrid', 'Hybrid'),
        ]
    )
    location = models.CharField(max_length=200, blank=True, help_text="For in-person events")
    online_link = models.URLField(blank=True, help_text="For online events")

    # Details
    registration_required = models.BooleanField(default=True)
    registration_url = models.URLField(blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Fee in PKR (0 for free)")
    max_attendees = models.PositiveIntegerField(null=True, blank=True)

    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    attendees = models.ManyToManyField(User, related_name='events_attending', through='EventAttendance')
    featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'networking_events'
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['event_type']),
            models.Index(fields=['format']),
        ]

    def __str__(self):
        return f"{self.title} ({self.start_date.date()})"

    def is_upcoming(self):
        from django.utils import timezone
        return self.start_date > timezone.now()

    def is_free(self):
        return self.fee == 0

    def attendee_count(self):
        return self.attendees.count()


class EventAttendance(models.Model):
    """Track event attendance"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)]
    )

    class Meta:
        db_table = 'networking_event_attendance'
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
