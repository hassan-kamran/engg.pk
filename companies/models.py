"""
Models for the companies app - Glassdoor-like company reviews and insights.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse


class Company(models.Model):
    """
    Company profile with comprehensive information and aggregated ratings.
    """
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1001-5000', '1001-5000 employees'),
        ('5001+', '5000+ employees'),
    ]

    INDUSTRY_CHOICES = [
        ('software', 'Software Development'),
        ('telecom', 'Telecommunications'),
        ('finance', 'Finance & Banking'),
        ('manufacturing', 'Manufacturing'),
        ('consulting', 'Consulting'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('energy', 'Energy & Utilities'),
        ('construction', 'Construction & Engineering'),
        ('retail', 'Retail & E-commerce'),
        ('transportation', 'Transportation & Logistics'),
        ('government', 'Government & Public Sector'),
        ('other', 'Other'),
    ]

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Company Name",
        help_text="Official company name"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL Slug"
    )
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True,
        verbose_name="Company Logo"
    )
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
        verbose_name="Industry",
        db_index=True
    )
    size = models.CharField(
        max_length=20,
        choices=COMPANY_SIZE_CHOICES,
        verbose_name="Company Size"
    )
    headquarters_location = models.CharField(
        max_length=200,
        verbose_name="Headquarters Location",
        help_text="City and country of headquarters"
    )
    founded_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2100)],
        blank=True,
        null=True,
        verbose_name="Founded Year"
    )
    website = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Company Website"
    )
    description = models.TextField(
        verbose_name="Company Description",
        help_text="Overview of the company and what they do"
    )

    # Aggregated ratings and counts (updated via signals or periodic tasks)
    overall_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Overall Rating",
        help_text="Average rating from all reviews"
    )
    recommend_to_friend_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        verbose_name="Recommend to Friend %",
        help_text="Percentage of employees who recommend this company"
    )

    # CEO information
    ceo_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="CEO Name"
    )
    ceo_approval_rating = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        verbose_name="CEO Approval Rating",
        help_text="Percentage of employees who approve of the CEO"
    )

    # Counts
    total_reviews_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Reviews"
    )
    total_salaries_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Salaries"
    )
    total_interviews_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Interviews"
    )

    # Metadata
    verified = models.BooleanField(
        default=False,
        verbose_name="Verified Company",
        help_text="Company profile verified by admin",
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        ordering = ['-overall_rating', 'name']
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        indexes = [
            models.Index(fields=['industry', '-overall_rating']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('companies:company_detail', kwargs={'slug': self.slug})

    def update_aggregated_data(self):
        """Update aggregated ratings and counts from related reviews."""
        from django.db.models import Avg, Count, Q

        reviews = self.reviews.all()
        self.total_reviews_count = reviews.count()

        if self.total_reviews_count > 0:
            # Calculate average overall rating
            avg_rating = reviews.aggregate(Avg('overall_rating'))['overall_rating__avg']
            self.overall_rating = round(avg_rating, 2) if avg_rating else 0.00

            # Calculate recommend percentage
            recommend_count = reviews.filter(recommend_to_friend=True).count()
            self.recommend_to_friend_percentage = int((recommend_count / self.total_reviews_count) * 100)

            # Calculate CEO approval (from reviews that have this field)
            # We'll add this to reviews later

        # Update salary count
        self.total_salaries_count = self.salaries.count()

        # Update interview count (from mentorship app)
        self.total_interviews_count = self.interview_experiences.count()

        self.save(update_fields=[
            'overall_rating',
            'recommend_to_friend_percentage',
            'total_reviews_count',
            'total_salaries_count',
            'total_interviews_count',
        ])


class CompanyReview(models.Model):
    """
    Detailed company review with multi-dimensional ratings.
    """
    EMPLOYMENT_STATUS_CHOICES = [
        ('current', 'Current Employee'),
        ('former', 'Former Employee'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Company"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='glassdoor_reviews',
        verbose_name="Author"
    )

    # Employment details
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        verbose_name="Employment Status"
    )
    job_title = models.CharField(
        max_length=200,
        verbose_name="Job Title",
        help_text="Your role at the company"
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Location",
        help_text="City where you worked"
    )
    employment_length = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        verbose_name="Employment Length (Years)",
        help_text="How long you worked at the company"
    )

    # Ratings (1-5 scale)
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Overall Rating",
        db_index=True
    )
    work_life_balance_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Work-Life Balance"
    )
    culture_values_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Culture & Values"
    )
    career_opportunities_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Career Opportunities"
    )
    compensation_benefits_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Compensation & Benefits"
    )
    senior_management_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Senior Management"
    )

    # Review content
    review_title = models.CharField(
        max_length=200,
        verbose_name="Review Title",
        help_text="Brief summary of your experience"
    )
    pros = models.TextField(
        verbose_name="Pros",
        help_text="What are the positives about working at this company?"
    )
    cons = models.TextField(
        verbose_name="Cons",
        help_text="What are the negatives or areas for improvement?"
    )
    advice_to_management = models.TextField(
        blank=True,
        verbose_name="Advice to Management",
        help_text="What would you suggest management do to improve?"
    )

    # Additional fields
    recommend_to_friend = models.BooleanField(
        default=True,
        verbose_name="Would Recommend to Friend"
    )
    ceo_approval = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Approve of CEO",
        help_text="Do you approve of the CEO's leadership?"
    )

    # Engagement
    helpful_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Helpful Count"
    )
    helpful_users = models.ManyToManyField(
        User,
        related_name='helpful_company_reviews',
        blank=True,
        verbose_name="Users who found this helpful"
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name="Approved",
        help_text="Review approved for display",
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Company Review"
        verbose_name_plural = "Company Reviews"
        indexes = [
            models.Index(fields=['company', '-created_at']),
            models.Index(fields=['company', '-overall_rating']),
        ]
        # One review per user per company
        unique_together = [['company', 'author']]

    def __str__(self):
        return f"{self.author.username}'s review of {self.company.name}"

    def get_average_rating(self):
        """Calculate average of all dimension ratings."""
        ratings = [
            self.work_life_balance_rating,
            self.culture_values_rating,
            self.career_opportunities_rating,
            self.compensation_benefits_rating,
            self.senior_management_rating,
        ]
        return round(sum(ratings) / len(ratings), 2)


class SalaryReport(models.Model):
    """
    Anonymous salary information by role and experience level.
    """
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('bachelors', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('no_degree', 'No Degree'),
    ]

    CURRENCY_CHOICES = [
        ('PKR', 'Pakistani Rupee'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='salaries',
        verbose_name="Company"
    )
    submitter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='salary_reports',
        verbose_name="Submitter",
        help_text="Optional - can be anonymous"
    )

    # Job details
    job_title = models.CharField(
        max_length=200,
        verbose_name="Job Title",
        db_index=True
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Location",
        help_text="City where the job is based"
    )
    experience_years = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        verbose_name="Years of Experience",
        db_index=True
    )
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        verbose_name="Education Level"
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time',
        verbose_name="Employment Type"
    )

    # Compensation details
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='PKR',
        verbose_name="Currency"
    )
    base_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Base Salary (Annual)",
        help_text="Annual base salary"
    )
    bonus = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Annual Bonus"
    )
    additional_compensation = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Additional Compensation",
        help_text="Stock, commissions, etc."
    )
    total_compensation = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total Annual Compensation"
    )

    # Metadata
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified",
        help_text="Salary verified by admin"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Salary Report"
        verbose_name_plural = "Salary Reports"
        indexes = [
            models.Index(fields=['company', 'job_title']),
            models.Index(fields=['company', '-created_at']),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company.name} - {self.currency} {self.total_compensation}"

    def save(self, *args, **kwargs):
        # Calculate total compensation
        self.total_compensation = self.base_salary + self.bonus + self.additional_compensation
        super().save(*args, **kwargs)


class CompanyPhoto(models.Model):
    """
    Photos showcasing company offices, teams, events, and culture.
    """
    PHOTO_TYPE_CHOICES = [
        ('office', 'Office'),
        ('team', 'Team'),
        ('event', 'Event'),
        ('culture', 'Culture'),
        ('other', 'Other'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Company"
    )
    uploader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_company_photos',
        verbose_name="Uploader"
    )
    photo = models.ImageField(
        upload_to='company_photos/',
        verbose_name="Photo"
    )
    caption = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Caption"
    )
    photo_type = models.CharField(
        max_length=20,
        choices=PHOTO_TYPE_CHOICES,
        default='other',
        verbose_name="Photo Type",
        db_index=True
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approved",
        help_text="Photo approved for display by admin",
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Company Photo"
        verbose_name_plural = "Company Photos"
        indexes = [
            models.Index(fields=['company', '-created_at']),
        ]

    def __str__(self):
        return f"Photo of {self.company.name} - {self.photo_type}"


class CompanyBenefit(models.Model):
    """
    Company benefits and perks information.
    """
    BENEFIT_CATEGORY_CHOICES = [
        ('health', 'Health & Wellness'),
        ('insurance', 'Insurance'),
        ('retirement', 'Retirement & Savings'),
        ('pto', 'Paid Time Off'),
        ('perks', 'Office Perks'),
        ('professional_development', 'Professional Development'),
        ('family', 'Family & Parenting'),
        ('other', 'Other'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='benefits',
        verbose_name="Company"
    )
    benefit_category = models.CharField(
        max_length=50,
        choices=BENEFIT_CATEGORY_CHOICES,
        verbose_name="Benefit Category",
        db_index=True
    )
    benefit_name = models.CharField(
        max_length=200,
        verbose_name="Benefit Name",
        help_text="e.g., 'Health Insurance', 'Remote Work', '401k Matching'"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Details about this benefit"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        ordering = ['benefit_category', 'benefit_name']
        verbose_name = "Company Benefit"
        verbose_name_plural = "Company Benefits"

    def __str__(self):
        return f"{self.company.name} - {self.benefit_name}"
