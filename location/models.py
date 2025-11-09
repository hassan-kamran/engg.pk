from django.db import models
from django.contrib.auth.models import User


class IndustryZone(models.Model):
    """Engineering industry map"""
    name = models.CharField(max_length=200)
    zone_type = models.CharField(
        max_length=30,
        choices=[
            ('manufacturing', 'Manufacturing Hub'),
            ('tech_park', 'Technology Park'),
            ('industrial_estate', 'Industrial Estate'),
            ('special_economic', 'Special Economic Zone'),
            ('cluster', 'Industry Cluster'),
        ]
    )

    # Location
    city = models.CharField(max_length=100)
    province = models.CharField(
        max_length=20,
        choices=[
            ('punjab', 'Punjab'),
            ('sindh', 'Sindh'),
            ('kpk', 'Khyber Pakhtunkhwa'),
            ('balochistan', 'Balochistan'),
            ('ajk', 'Azad Jammu & Kashmir'),
            ('gilgit', 'Gilgit-Baltistan'),
            ('islamabad', 'Islamabad Capital Territory'),
        ]
    )
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Details
    description = models.TextField()
    primary_industries = models.TextField(help_text="Primary engineering industries (comma-separated)")
    number_of_companies = models.PositiveIntegerField(default=0)
    approximate_employment = models.PositiveIntegerField(default=0)

    # Facilities
    infrastructure = models.TextField(help_text="Available infrastructure and facilities")
    utilities = models.TextField(help_text="Power, water, gas availability")

    # Information
    established_year = models.PositiveIntegerField(null=True, blank=True)
    managing_authority = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    contact_info = models.TextField(blank=True)

    # Engineering specific
    engineering_density = models.CharField(
        max_length=20,
        choices=[
            ('high', 'High (50+ companies)'),
            ('medium', 'Medium (20-50 companies)'),
            ('low', 'Low (<20 companies)'),
        ],
        default='medium'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'location_industry_zones'
        ordering = ['province', 'city']
        indexes = [
            models.Index(fields=['province', 'city']),
            models.Index(fields=['zone_type']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}"


class ProfessionalService(models.Model):
    """Professional services directory"""
    name = models.CharField(max_length=200)
    service_type = models.CharField(
        max_length=30,
        choices=[
            ('consultancy', 'Engineering Consultancy'),
            ('testing_lab', 'Testing Laboratory'),
            ('design_firm', 'Design Firm'),
            ('inspection', 'Inspection Services'),
            ('certification', 'Certification Body'),
            ('surveying', 'Surveying Services'),
            ('association', 'Professional Association'),
        ]
    )

    # Details
    description = models.TextField()
    disciplines_served = models.TextField(help_text="Engineering disciplines (comma-separated)")
    services_offered = models.TextField()

    # Location
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    address = models.TextField()
    serves_nationwide = models.BooleanField(default=False)

    # Contact
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)

    # Credentials
    accreditations = models.TextField(blank=True, help_text="Relevant accreditations (PSQCA, ISO, etc.)")
    established_year = models.PositiveIntegerField(null=True, blank=True)
    pec_registered = models.BooleanField(default=False, help_text="Registered with Pakistan Engineering Council")
    pec_registration_number = models.CharField(max_length=100, blank=True)

    # Engagement
    verified = models.BooleanField(default=False)
    rating_sum = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)

    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'location_professional_services'
        ordering = ['city', 'name']
        indexes = [
            models.Index(fields=['service_type', 'city']),
            models.Index(fields=['pec_registered']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}"

    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.rating_sum / self.rating_count


class ServiceReview(models.Model):
    """Reviews for professional services"""
    service = models.ForeignKey(ProfessionalService, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_reviews')

    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField()
    service_used = models.CharField(max_length=200, help_text="Which service did you use?")
    project_type = models.CharField(max_length=200, blank=True)

    pros = models.TextField()
    cons = models.TextField()

    would_recommend = models.BooleanField()
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'location_service_reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service.name} review by {self.reviewer.username}"
