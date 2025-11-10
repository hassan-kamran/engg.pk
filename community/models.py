from django.db import models
from django.contrib.auth.models import User


class LocalHub(models.Model):
    """Local hubs directory (coworking, makerspaces, etc.)"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    hub_type = models.CharField(
        max_length=20,
        choices=[
            ('coworking', 'Coworking Space'),
            ('makerspace', 'Makerspace/Fab Lab'),
            ('library', 'University Library'),
            ('cafe', 'Study Cafe'),
            ('incubator', 'Incubator'),
        ]
    )

    # Location
    city = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Details
    facilities = models.TextField(help_text="Available facilities (comma-separated)")
    for_students = models.BooleanField(default=True)
    for_professionals = models.BooleanField(default=True)
    open_to_public = models.BooleanField(default=True)

    # Contact
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Hours and pricing
    operating_hours = models.TextField()
    pricing_info = models.TextField()

    rating_sum = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_local_hubs'
        ordering = ['city', 'name']
        indexes = [
            models.Index(fields=['city', 'hub_type']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}"

    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.rating_sum / self.rating_count


class SuccessStory(models.Model):
    """Success stories spotlight"""
    title = models.CharField(max_length=200)
    featured_person = models.CharField(max_length=200)
    current_position = models.CharField(max_length=200)
    current_company = models.CharField(max_length=200, blank=True)

    story_type = models.CharField(
        max_length=30,
        choices=[
            ('startup_success', 'Startup Success'),
            ('innovation', 'Innovation Story'),
            ('return_to_pakistan', 'Returned to Pakistan'),
            ('career_achievement', 'Career Achievement'),
            ('social_impact', 'Social Impact'),
        ]
    )

    # Background
    education = models.TextField()
    journey = models.TextField(help_text="Their journey and story")
    challenges_overcome = models.TextField()
    key_lessons = models.TextField()
    advice = models.TextField()

    # Media
    photo = models.ImageField(upload_to='success_stories/', blank=True)
    video_url = models.URLField(blank=True)

    # Contact
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    inspiring_count = models.PositiveIntegerField(default=0)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_success_stories'
        verbose_name_plural = 'Success Stories'
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['story_type']),
            models.Index(fields=['-published_date']),
        ]

    def __str__(self):
        return self.title


class NewsArticle(models.Model):
    """Engineering industry news aggregator"""
    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = models.TextField()
    source = models.CharField(max_length=200)
    source_url = models.URLField()

    category = models.CharField(
        max_length=30,
        choices=[
            ('policy', 'Policy & Regulations'),
            ('infrastructure', 'Infrastructure Projects'),
            ('technology', 'Technology Trends'),
            ('education', 'Engineering Education'),
            ('jobs', 'Job Market'),
            ('innovation', 'Innovations'),
        ]
    )

    discipline = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")

    thumbnail = models.ImageField(upload_to='news/', blank=True)
    views = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_articles_added')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_news_articles'
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['category', '-published_date']),
            models.Index(fields=['-published_date']),
        ]

    def __str__(self):
        return self.title


class WikiArticle(models.Model):
    """Knowledge base wiki"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    category = models.CharField(
        max_length=30,
        choices=[
            ('how_to', 'How-To Guides'),
            ('procedure', 'Government Procedures'),
            ('certification', 'Certifications'),
            ('city_guide', 'City Guides'),
            ('career', 'Career Guides'),
        ]
    )

    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wiki_articles_authored')
    contributors = models.ManyToManyField(User, related_name='wiki_articles_contributed', blank=True)

    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    related_articles = models.ManyToManyField('self', blank=True)

    # Version control
    version = models.PositiveIntegerField(default=1)
    last_edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

    # Engagement
    views = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'community_wiki_articles'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title


class WikiRevision(models.Model):
    """Track wiki article revisions"""
    article = models.ForeignKey(WikiArticle, on_delete=models.CASCADE, related_name='revisions')
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    edit_summary = models.CharField(max_length=200)
    version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_wiki_revisions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.article.title} v{self.version}"
