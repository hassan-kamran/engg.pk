from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Job, SavedJob, JobApplication


class JobModelTest(TestCase):
    """Test Job model functionality"""

    def setUp(self):
        self.job = Job.objects.create(
            title='Software Engineer',
            company='Tech Corp',
            location='Karachi',
            description='Great opportunity',
            requirements=['Python', 'Django', '3+ years experience'],
            job_type='full_time',
            experience_level='mid',
            discipline='Software',
            salary='PKR 150,000 - 200,000',
            application_url='https://example.com/apply',
            is_active=True
        )

    def test_job_creation(self):
        """Test that a job is created correctly"""
        self.assertEqual(self.job.title, 'Software Engineer')
        self.assertEqual(self.job.company, 'Tech Corp')
        self.assertEqual(self.job.location, 'Karachi')
        self.assertTrue(self.job.is_active)

    def test_job_str_representation(self):
        """Test the string representation of a job"""
        expected = 'Software Engineer at Tech Corp'
        self.assertEqual(str(self.job), expected)

    def test_job_type_choices(self):
        """Test job type is one of the valid choices"""
        self.assertIn(self.job.job_type, ['full_time', 'part_time', 'contract', 'internship'])


class JobViewsTest(TestCase):
    """Test Jobs views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.job = Job.objects.create(
            title='Software Engineer',
            company='Tech Corp',
            location='Karachi',
            description='Great opportunity',
            requirements=['Python', 'Django'],
            job_type='full_time',
            experience_level='mid',
            discipline='Software',
            is_active=True
        )

    def test_jobs_list_view(self):
        """Test jobs list view is accessible"""
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Opportunities')
        self.assertContains(response, 'Software Engineer')

    def test_job_detail_view(self):
        """Test job detail view is accessible"""
        response = self.client.get(reverse('jobs:detail', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Engineer')
        self.assertContains(response, 'Tech Corp')

    def test_inactive_job_not_in_list(self):
        """Test that inactive jobs don't appear in the list"""
        self.job.is_active = False
        self.job.save()
        response = self.client.get(reverse('jobs:list'))
        self.assertNotContains(response, 'Software Engineer')

    def test_toggle_save_job_requires_login(self):
        """Test that saving a job requires authentication"""
        response = self.client.post(reverse('jobs:toggle_save', args=[self.job.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_toggle_save_job_authenticated(self):
        """Test saving a job when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('jobs:toggle_save', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)

        # Verify job was saved
        saved = SavedJob.objects.filter(user=self.user, job=self.job).exists()
        self.assertTrue(saved)

    def test_unsave_job(self):
        """Test unsaving a job"""
        self.client.login(username='testuser', password='testpass123')

        # Save the job first
        SavedJob.objects.create(user=self.user, job=self.job)

        # Now unsave it
        response = self.client.post(reverse('jobs:toggle_save', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)

        # Verify job was unsaved
        saved = SavedJob.objects.filter(user=self.user, job=self.job).exists()
        self.assertFalse(saved)

    def test_job_search(self):
        """Test job search functionality"""
        response = self.client.get(reverse('jobs:list'), {'search': 'Software'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Engineer')

    def test_job_type_filter(self):
        """Test filtering jobs by type"""
        response = self.client.get(reverse('jobs:list'), {'type': 'full_time'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Engineer')

    def test_track_job_application(self):
        """Test tracking job application"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('jobs:track_application', args=[self.job.pk]),
            {'status': 'applied', 'notes': 'Applied via website'}
        )
        self.assertEqual(response.status_code, 200)

        # Verify application was tracked
        application = JobApplication.objects.filter(user=self.user, job=self.job).first()
        self.assertIsNotNone(application)
        self.assertEqual(application.status, 'applied')
