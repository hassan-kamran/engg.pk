from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import (
    ThoughtLeader, ProfessionalBody, FeedPost, Comment,
    UserSubscription, OrganizationSubscription, TopicSubscription
)


class FeedModelsTest(TestCase):
    """Test Feed models"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.thought_leader_user = User.objects.create_user(
            username='leader',
            password='pass',
            first_name='Leader',
            last_name='Expert'
        )
        self.thought_leader = ThoughtLeader.objects.create(
            user=self.thought_leader_user,
            title='Senior Engineer',
            organization='Tech Corp',
            bio='Expert in software engineering',
            expertise_areas=['Python', 'Django', 'Cloud'],
            verified=True
        )
        self.organization = ProfessionalBody.objects.create(
            name='Pakistan Engineering Council',
            slug='pec',
            category='association',
            description='Professional engineering body',
            verified=True
        )

    def test_thought_leader_creation(self):
        """Test ThoughtLeader model creation"""
        self.assertEqual(self.thought_leader.title, 'Senior Engineer')
        self.assertTrue(self.thought_leader.verified)
        self.assertEqual(self.thought_leader.follower_count, 0)

    def test_professional_body_creation(self):
        """Test ProfessionalBody model creation"""
        self.assertEqual(self.organization.name, 'Pakistan Engineering Council')
        self.assertEqual(self.organization.slug, 'pec')
        self.assertTrue(self.organization.verified)

    def test_feed_post_by_user(self):
        """Test creating a feed post by a user"""
        post = FeedPost.objects.create(
            author_user=self.thought_leader_user,
            post_type='discussion',
            title='Test Post',
            content='This is a test post',
            topics=['software', 'career']
        )
        self.assertEqual(post.author_name, 'Leader Expert')
        self.assertEqual(post.like_count, 0)

    def test_feed_post_by_organization(self):
        """Test creating a feed post by an organization"""
        post = FeedPost.objects.create(
            author_organization=self.organization,
            post_type='announcement',
            title='Organization Announcement',
            content='Important announcement',
            topics=['industry']
        )
        self.assertEqual(post.author_name, 'Pakistan Engineering Council')
        self.assertTrue(post.author_is_verified)

    def test_user_subscription(self):
        """Test user subscribing to thought leader"""
        subscription = UserSubscription.objects.create(
            subscriber=self.user,
            thought_leader=self.thought_leader
        )
        self.assertEqual(subscription.subscriber, self.user)
        self.assertEqual(subscription.thought_leader, self.thought_leader)

    def test_organization_subscription(self):
        """Test user subscribing to organization"""
        subscription = OrganizationSubscription.objects.create(
            subscriber=self.user,
            organization=self.organization
        )
        self.assertEqual(subscription.subscriber, self.user)
        self.assertEqual(subscription.organization, self.organization)

    def test_topic_subscription(self):
        """Test user subscribing to topic"""
        subscription = TopicSubscription.objects.create(
            subscriber=self.user,
            topic='software'
        )
        self.assertEqual(subscription.subscriber, self.user)
        self.assertEqual(subscription.topic, 'software')

    def test_comment_creation(self):
        """Test creating a comment on a feed post"""
        post = FeedPost.objects.create(
            author_user=self.thought_leader_user,
            title='Test Post',
            content='Test content'
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content='Great post!'
        )
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.like_count, 0)


class FeedViewsTest(TestCase):
    """Test Feed views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.thought_leader_user = User.objects.create_user(
            username='leader',
            password='pass'
        )
        self.thought_leader = ThoughtLeader.objects.create(
            user=self.thought_leader_user,
            title='Senior Engineer',
            bio='Expert',
            verified=True
        )
        self.post = FeedPost.objects.create(
            author_user=self.thought_leader_user,
            title='Test Feed Post',
            content='This is test content',
            topics=['software']
        )
        self.organization = ProfessionalBody.objects.create(
            name='Test Org',
            slug='test-org',
            category='company',
            description='Test organization',
            verified=True
        )

    def test_feed_list_requires_login(self):
        """Test that feed list requires authentication"""
        response = self.client.get(reverse('feed:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_feed_list_authenticated(self):
        """Test feed list view when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('feed:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Professional Feed')

    def test_feed_shows_subscribed_content(self):
        """Test that feed shows content from subscribed thought leaders"""
        self.client.login(username='testuser', password='testpass123')

        # Subscribe to thought leader
        UserSubscription.objects.create(
            subscriber=self.user,
            thought_leader=self.thought_leader
        )

        response = self.client.get(reverse('feed:list'))
        self.assertContains(response, 'Test Feed Post')

    def test_feed_post_detail(self):
        """Test feed post detail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('feed:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Feed Post')
        self.assertContains(response, 'This is test content')

    def test_thought_leaders_list(self):
        """Test thought leaders list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('feed:thought_leaders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thought Leaders')

    def test_organizations_list(self):
        """Test organizations list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('feed:organizations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Professional Organizations')
        self.assertContains(response, 'Test Org')

    def test_toggle_user_subscription(self):
        """Test subscribing/unsubscribing to thought leader"""
        self.client.login(username='testuser', password='testpass123')

        # Subscribe
        response = self.client.post(
            reverse('feed:toggle_user_subscription', args=[self.thought_leader.pk])
        )
        self.assertEqual(response.status_code, 200)

        # Verify subscription exists
        subscription = UserSubscription.objects.filter(
            subscriber=self.user,
            thought_leader=self.thought_leader
        ).exists()
        self.assertTrue(subscription)

        # Unsubscribe
        response = self.client.post(
            reverse('feed:toggle_user_subscription', args=[self.thought_leader.pk])
        )
        self.assertEqual(response.status_code, 200)

        # Verify subscription removed
        subscription = UserSubscription.objects.filter(
            subscriber=self.user,
            thought_leader=self.thought_leader
        ).exists()
        self.assertFalse(subscription)

    def test_toggle_organization_subscription(self):
        """Test subscribing/unsubscribing to organization"""
        self.client.login(username='testuser', password='testpass123')

        # Subscribe
        response = self.client.post(
            reverse('feed:toggle_organization_subscription', args=[self.organization.pk])
        )
        self.assertEqual(response.status_code, 200)

        # Verify subscription exists
        subscription = OrganizationSubscription.objects.filter(
            subscriber=self.user,
            organization=self.organization
        ).exists()
        self.assertTrue(subscription)

    def test_toggle_post_like(self):
        """Test liking/unliking a feed post"""
        self.client.login(username='testuser', password='testpass123')

        # Like
        response = self.client.post(
            reverse('feed:toggle_post_like', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.like_count, 1)

        # Unlike
        response = self.client.post(
            reverse('feed:toggle_post_like', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.like_count, 0)

    def test_create_comment(self):
        """Test creating a comment on a feed post"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            reverse('feed:create_comment', args=[self.post.pk]),
            {'content': 'Great post!'}
        )
        self.assertEqual(response.status_code, 200)

        # Verify comment was created
        comment = Comment.objects.filter(post=self.post, author=self.user).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, 'Great post!')
