from django.db import models
from django.contrib.auth.models import User


class EngineeringCalculator(models.Model):
    """Engineering calculators suite"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    discipline = models.CharField(max_length=100)
    calculator_type = models.CharField(max_length=100, help_text="e.g., 'Beam Calculator', 'Power Factor Calculator'")
    formula_info = models.TextField(help_text="Mathematical formula and explanation")
    usage_instructions = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tools_calculators'
        ordering = ['-usage_count']

    def __str__(self):
        return self.name


class ReferenceLibrary(models.Model):
    """Engineering reference library"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(
        max_length=20,
        choices=[
            ('handbook', 'Handbook'),
            ('standard', 'Standard/Code'),
            ('paper', 'Research Paper'),
            ('tutorial', 'Tutorial'),
            ('video', 'Video'),
            ('book', 'Book'),
        ]
    )
    discipline = models.CharField(max_length=100)
    topics = models.TextField(help_text="Comma-separated topics")

    # Access
    url = models.URLField(blank=True)
    file = models.FileField(upload_to='references/', blank=True)
    is_free = models.BooleanField(default=True)

    # Details
    author = models.CharField(max_length=200, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='English')

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_references')
    downloads = models.PositiveIntegerField(default=0)
    rating_sum = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tools_reference_library'
        verbose_name_plural = 'Reference Libraries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['resource_type']),
        ]

    def __str__(self):
        return self.title

    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.rating_sum / self.rating_count


class SoftwareDirectory(models.Model):
    """Engineering software and tools directory"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, help_text="e.g., 'CAD', 'Simulation', 'Project Management'")
    discipline = models.CharField(max_length=100)

    # Pricing
    pricing_model = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('freemium', 'Freemium'),
            ('paid', 'Paid'),
            ('subscription', 'Subscription'),
            ('student_free', 'Free for Students'),
        ]
    )
    price_info = models.TextField(blank=True, help_text="Pricing details")

    # Platform
    platforms = models.CharField(max_length=100, help_text="Windows, Mac, Linux, Web (comma-separated)")
    system_requirements = models.TextField(blank=True)

    # Links
    website = models.URLField()
    download_link = models.URLField(blank=True)

    # Reviews
    reviews_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # Pakistani availability
    available_in_pakistan = models.BooleanField(default=True)
    local_vendor = models.CharField(max_length=200, blank=True, help_text="Local vendor in Pakistan")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tools_software_directory'
        verbose_name_plural = 'Software Directories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['discipline']),
        ]

    def __str__(self):
        return self.name


class SoftwareReview(models.Model):
    """Reviews for software"""
    software = models.ForeignKey(SoftwareDirectory, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='software_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200)
    review = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    use_case = models.TextField(help_text="What did you use it for?")
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tools_software_reviews'
        unique_together = ['software', 'reviewer']
        ordering = ['-created_at']


class EquipmentListing(models.Model):
    """Equipment marketplace"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment_listings')

    listing_type = models.CharField(
        max_length=20,
        choices=[
            ('sell', 'For Sale'),
            ('rent', 'For Rent'),
            ('wanted', 'Wanted to Buy/Rent'),
        ]
    )

    category = models.CharField(
        max_length=100,
        help_text="e.g., 'Lab Equipment', 'Tools', 'Instruments', 'Books'"
    )
    condition = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('like_new', 'Like New'),
            ('good', 'Good'),
            ('fair', 'Fair'),
        ]
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in PKR")
    negotiable = models.BooleanField(default=True)

    location = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    images = models.ImageField(upload_to='equipment/', blank=True)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tools_equipment_listings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing_type', 'is_active']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.title
