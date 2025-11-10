from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ForumPost, Reply


class ForumPostModelTest(TestCase):
    """Test ForumPost model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = ForumPost.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
            category='technical',
            tags=['python', 'django']
        )

    def test_post_creation(self):
        """Test that a forum post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, 'technical')
        self.assertEqual(self.post.like_count, 0)
        self.assertEqual(self.post.reply_count, 0)

    def test_post_str_representation(self):
        """Test the string representation of a forum post"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_like_count_property(self):
        """Test the like_count property"""
        user2 = User.objects.create_user(username='user2', password='pass')
        self.post.likes.add(self.user, user2)
        self.assertEqual(self.post.like_count, 2)

    def test_reply_count_property(self):
        """Test the reply_count property"""
        Reply.objects.create(post=self.post, author=self.user, content='Reply 1')
        Reply.objects.create(post=self.post, author=self.user, content='Reply 2')
        self.assertEqual(self.post.reply_count, 2)


class ForumViewsTest(TestCase):
    """Test Forum views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = ForumPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category='general'
        )

    def test_forum_list_view(self):
        """Test forum list view is accessible"""
        response = self.client.get(reverse('forum:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Community Forum')
        self.assertContains(response, 'Test Post')

    def test_forum_detail_view(self):
        """Test forum detail view is accessible"""
        response = self.client.get(reverse('forum:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')

    def test_forum_detail_increments_views(self):
        """Test that viewing a post increments the view count"""
        initial_views = self.post.views
        self.client.get(reverse('forum:post_detail', args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)

    def test_create_post_requires_login(self):
        """Test that creating a post requires authentication"""
        response = self.client.get(reverse('forum:create_post'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_post_authenticated(self):
        """Test creating a post when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('forum:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create New Post')

    def test_toggle_post_like_requires_login(self):
        """Test that liking a post requires authentication"""
        response = self.client.post(reverse('forum:toggle_post_like', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_toggle_post_like_authenticated(self):
        """Test liking a post when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('forum:toggle_post_like', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.like_count, 1)

    def test_search_functionality(self):
        """Test forum search functionality"""
        response = self.client.get(reverse('forum:list'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_category_filter(self):
        """Test category filtering"""
        response = self.client.get(reverse('forum:list'), {'category': 'general'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
