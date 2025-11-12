from django.db import models
from django.contrib.auth.models import User
from core.models import UserProfile


class MentorProfile(models.Model):
    """Extended profile for mentors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(help_text="Tell potential mentees about your background and what you can help with")
    years_of_experience = models.PositiveIntegerField()
    current_position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    expertise_areas = models.TextField(help_text="Comma-separated list of expertise areas")
    max_mentees = models.PositiveIntegerField(default=3, help_text="Maximum number of mentees at once")
    available_for_mentorship = models.BooleanField(default=True)
    mentorship_type = models.CharField(
        max_length=20,
        choices=[
            ('one_on_one', 'One-on-One'),
            ('group', 'Group'),
            ('both', 'Both')
        ],
        default='one_on_one'
    )
    linkedin_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentorship_mentor_profiles'
        indexes = [
            models.Index(fields=['available_for_mentorship']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Mentor: {self.user.get_full_name() or self.user.username}"

    def current_mentees_count(self):
        return self.mentorship_requests.filter(status='accepted').count()


class MentorshipRequest(models.Model):
    """Mentorship connection requests"""
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_requests_sent')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='mentorship_requests')
    message = models.TextField(help_text="Tell the mentor why you want their guidance")
    goals = models.TextField(help_text="What are your mentorship goals?")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('declined', 'Declined'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'mentorship_requests'
        unique_together = ['mentee', 'mentor']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.mentee.username} -> {self.mentor.user.username} ({self.status})"


class MentorshipSession(models.Model):
    """Track individual mentorship sessions"""
    mentorship = models.ForeignKey(MentorshipRequest, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    topics_discussed = models.TextField()
    notes = models.TextField(blank=True, help_text="Session notes (visible to both parties)")
    action_items = models.TextField(blank=True, help_text="Action items for mentee")
    mentee_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Mentee's rating of the session"
    )
    mentor_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Mentor's rating of the session"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentorship_sessions'
        ordering = ['-session_date']
        indexes = [
            models.Index(fields=['-session_date']),
        ]

    def __str__(self):
        return f"Session: {self.mentorship} on {self.session_date.date()}"


class SkillAssessment(models.Model):
    """Skill self-assessment tool"""
    SKILL_CATEGORIES = [
        ('technical', 'Technical Skills'),
        ('soft', 'Soft Skills'),
        ('tools', 'Tools & Software'),
        ('domain', 'Domain Knowledge'),
    ]

    SKILL_LEVELS = [
        (1, 'Beginner'),
        (2, 'Elementary'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_assessments')
    skill_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    current_level = models.PositiveSmallIntegerField(choices=SKILL_LEVELS)
    target_level = models.PositiveSmallIntegerField(choices=SKILL_LEVELS)
    notes = models.TextField(blank=True, help_text="How did you acquire this skill? What projects have you used it in?")
    last_used = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentorship_skill_assessments'
        unique_together = ['user', 'skill_name']
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['-updated_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.skill_name} (Level {self.current_level})"


class InterviewExperience(models.Model):
    """Share interview experiences"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_experiences')
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='interview_experiences',
        null=True,
        blank=True,
        verbose_name="Company"
    )
    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Company Name (if not in system)",
        help_text="Enter company name if not found in the company list"
    )
    position = models.CharField(max_length=200)
    discipline = models.CharField(
        max_length=50,
        choices=[
            ('computer_science', 'Computer Science'),
            ('electrical', 'Electrical Engineering'),
            ('mechanical', 'Mechanical Engineering'),
            ('civil', 'Civil Engineering'),
            ('chemical', 'Chemical Engineering'),
            ('software', 'Software Engineering'),
            ('biomedical', 'Biomedical Engineering'),
            ('aerospace', 'Aerospace Engineering'),
            ('industrial', 'Industrial Engineering'),
            ('other', 'Other'),
        ]
    )
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
            ('lead', 'Lead/Principal'),
        ]
    )
    interview_date = models.DateField()
    location = models.CharField(max_length=100, help_text="City, Pakistan")
    interview_process = models.TextField(help_text="Describe the stages of the interview process")
    technical_questions = models.TextField(blank=True, help_text="Technical questions asked")
    behavioral_questions = models.TextField(blank=True, help_text="Behavioral questions asked")
    tips = models.TextField(blank=True, help_text="Your tips for others")
    outcome = models.CharField(
        max_length=20,
        choices=[
            ('offered', 'Offer Received'),
            ('rejected', 'Rejected'),
            ('ongoing', 'Still In Process'),
            ('declined', 'Declined Offer'),
        ]
    )
    difficulty_rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How difficult was the interview? (1=Easy, 5=Very Hard)"
    )
    helpful_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentorship_interview_experiences'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['discipline']),
            models.Index(fields=['-helpful_count']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        company_display = self.company.name if self.company else self.company_name
        return f"{company_display} - {self.position} ({self.author.username})"

    def get_company_display(self):
        """Return the company name from either the ForeignKey or the text field."""
        return self.company.name if self.company else self.company_name


class StudyGroup(models.Model):
    """Peer learning study groups"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    discipline = models.CharField(
        max_length=50,
        choices=[
            ('computer_science', 'Computer Science'),
            ('electrical', 'Electrical Engineering'),
            ('mechanical', 'Mechanical Engineering'),
            ('civil', 'Civil Engineering'),
            ('chemical', 'Chemical Engineering'),
            ('software', 'Software Engineering'),
            ('biomedical', 'Biomedical Engineering'),
            ('aerospace', 'Aerospace Engineering'),
            ('industrial', 'Industrial Engineering'),
            ('other', 'Other'),
        ]
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_groups_created')
    members = models.ManyToManyField(User, related_name='study_groups', through='StudyGroupMembership')
    max_members = models.PositiveIntegerField(default=10)
    meeting_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-Weekly'),
            ('monthly', 'Monthly'),
            ('flexible', 'Flexible'),
        ]
    )
    meeting_format = models.CharField(
        max_length=20,
        choices=[
            ('online', 'Online'),
            ('in_person', 'In-Person'),
            ('hybrid', 'Hybrid'),
        ]
    )
    location = models.CharField(max_length=200, blank=True, help_text="For in-person/hybrid groups")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentorship_study_groups'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discipline', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def current_members_count(self):
        return self.members.count()

    def is_full(self):
        return self.current_members_count() >= self.max_members


class StudyGroupMembership(models.Model):
    """Track study group memberships"""
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        db_table = 'mentorship_study_group_memberships'
        unique_together = ['study_group', 'user']
        indexes = [
            models.Index(fields=['study_group', '-joined_at']),
        ]

    def __str__(self):
        return f"{self.user.username} in {self.study_group.name}"
