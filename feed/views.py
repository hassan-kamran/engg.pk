from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Exists, OuterRef, QuerySet
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from core.utils import toggle_like, validate_text_length
from .models import (
    FeedPost, Comment, ThoughtLeader, ProfessionalBody,
    UserSubscription, OrganizationSubscription, TopicSubscription
)
from .forms import FeedPostForm, CommentForm

# Constants
MAX_COMMENT_LENGTH = 5000


class FeedListView(LoginRequiredMixin, ListView):
    """Main feed with infinite scroll - shows posts from followed users/organizations"""
    model = FeedPost
    template_name = 'feed/list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Load 10 posts at a time for infinite scroll

    def get_queryset(self) -> QuerySet[FeedPost]:
        """
        Get the feed posts queryset with subscription filtering.

        Returns posts from followed users, organizations, or topics.
        If user follows nothing, shows all posts (discovery mode).

        Returns:
            QuerySet[FeedPost]: Optimized queryset with annotations
        """
        user = self.request.user

        # Get subscriptions (optimized to reduce queries)
        subscribed_thought_leaders = list(
            UserSubscription.objects.filter(subscriber=user)
            .values_list('thought_leader__user', flat=True)
        )
        subscribed_organizations = list(
            OrganizationSubscription.objects.filter(subscriber=user)
            .values_list('organization', flat=True)
        )
        subscribed_topics = list(
            TopicSubscription.objects.filter(subscriber=user)
            .values_list('topic', flat=True)
        )

        # Build query - show posts from followed users, organizations, or topics
        q_objects = self._build_subscription_query(
            subscribed_thought_leaders,
            subscribed_organizations,
            subscribed_topics
        )

        # Base queryset with optimization - annotate like_count to avoid N+1
        queryset = FeedPost.objects.select_related(
            'author_user', 'author_organization'
        ).annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )

        # Apply subscription filter if user follows anything
        if subscribed_thought_leaders or subscribed_organizations or subscribed_topics:
            queryset = queryset.filter(q_objects)

        # If user doesn't follow anyone yet, show all posts (discovery mode)
        # This ensures new users see content immediately

        # Apply search filter
        queryset = self._apply_search_filter(queryset)

        # Apply post type filter
        queryset = self._apply_type_filter(queryset)

        return queryset.distinct().order_by('-created_at')

    def _build_subscription_query(
        self,
        thought_leaders: list,
        organizations: list,
        topics: list
    ) -> Q:
        """
        Build Q objects for subscription filtering.

        Args:
            thought_leaders: List of thought leader user IDs
            organizations: List of organization IDs
            topics: List of topic choices

        Returns:
            Q: Combined Q object for filtering
        """
        q_objects = Q()

        if thought_leaders:
            q_objects |= Q(author_user__in=thought_leaders)

        if organizations:
            q_objects |= Q(author_organization__in=organizations)

        if topics:
            # Posts that contain any of the subscribed topics
            for topic in topics:
                q_objects |= Q(topics__contains=topic)

        return q_objects

    def _apply_search_filter(self, queryset: QuerySet[FeedPost]) -> QuerySet[FeedPost]:
        """
        Apply search filter to queryset.

        Args:
            queryset: The base queryset

        Returns:
            QuerySet[FeedPost]: Filtered queryset
        """
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return queryset

    def _apply_type_filter(self, queryset: QuerySet[FeedPost]) -> QuerySet[FeedPost]:
        """
        Apply post type filter to queryset.

        Args:
            queryset: The base queryset

        Returns:
            QuerySet[FeedPost]: Filtered queryset
        """
        post_type = self.request.GET.get('type', '').strip()
        if post_type:
            # Validate post_type against allowed choices
            valid_types = [choice[0] for choice in FeedPost.POST_TYPE_CHOICES]
            if post_type in valid_types:
                queryset = queryset.filter(post_type=post_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Feed - engg.pk'
        context['meta_description'] = 'Browse posts from the engineering community'
        context['post_types'] = FeedPost.POST_TYPE_CHOICES
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')

        # Add subscription stats for sidebar
        user = self.request.user
        context['following_count'] = UserSubscription.objects.filter(subscriber=user).count()
        context['organizations_count'] = OrganizationSubscription.objects.filter(subscriber=user).count()

        return context


class FeedPostDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a feed post"""
    model = FeedPost
    template_name = 'feed/detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        # Increment views
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Feed - engg.pk'
        context['meta_description'] = self.object.content[:155]
        context['comments'] = self.object.comments.select_related('author').prefetch_related('likes')
        context['comment_form'] = CommentForm()

        # Check if user has liked the post
        if self.request.user.is_authenticated:
            context['is_liked'] = self.object.likes.filter(id=self.request.user.id).exists()

        return context


class FeedPostCreateView(LoginRequiredMixin, CreateView):
    """Create a new feed post (for thought leaders)"""
    model = FeedPost
    form_class = FeedPostForm
    template_name = 'feed/create.html'

    def form_valid(self, form):
        """
        Validate form and set author with authorization checks.

        Returns:
            HttpResponse: Redirect to success URL or error page
        """
        user = self.request.user

        # Check if user is a thought leader
        if hasattr(user, 'thought_leader_profile'):
            form.instance.author_user = user
        # Check if user manages any organizations
        elif user.managed_organizations.exists():
            # If form has organization field, use it; otherwise use first managed org
            org_id = self.request.POST.get('organization')
            if org_id:
                # Verify user actually manages this organization
                try:
                    org = ProfessionalBody.objects.get(pk=org_id)
                    if not org.admins.filter(id=user.id).exists():
                        raise PermissionDenied("You don't have permission to post for this organization")
                    form.instance.author_organization = org
                except ProfessionalBody.DoesNotExist:
                    messages.error(self.request, 'Invalid organization selected.')
                    return redirect('feed:create')
            else:
                form.instance.author_organization = user.managed_organizations.first()
        else:
            messages.error(self.request, 'You must be a verified thought leader or organization admin to post.')
            return redirect('feed:list')

        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Get the URL to redirect to after successful form submission.

        Returns:
            str: URL to the created post detail page
        """
        return reverse_lazy('feed:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Post - Feed - engg.pk'

        # Pass managed organizations if user has any
        if self.request.user.managed_organizations.exists():
            context['managed_organizations'] = self.request.user.managed_organizations.all()

        return context


# Discover views for finding thought leaders and organizations
class ThoughtLeaderListView(LoginRequiredMixin, ListView):
    """List of thought leaders to follow"""
    model = ThoughtLeader
    template_name = 'feed/thought_leaders.html'
    context_object_name = 'thought_leaders'
    paginate_by = 20

    def get_queryset(self):
        queryset = ThoughtLeader.objects.filter(verified=True).select_related('user')

        # Annotate with subscription status for current user
        user_subscriptions = UserSubscription.objects.filter(
            subscriber=self.request.user,
            thought_leader=OuterRef('pk')
        )
        queryset = queryset.annotate(
            is_subscribed=Exists(user_subscriptions)
        )

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(title__icontains=search) |
                Q(organization__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Thought Leaders - engg.pk'
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProfessionalBodyListView(LoginRequiredMixin, ListView):
    """List of professional bodies to follow"""
    model = ProfessionalBody
    template_name = 'feed/organizations.html'
    context_object_name = 'organizations'
    paginate_by = 20

    def get_queryset(self):
        queryset = ProfessionalBody.objects.filter(verified=True)

        # Annotate with subscription status for current user
        org_subscriptions = OrganizationSubscription.objects.filter(
            subscriber=self.request.user,
            organization=OuterRef('pk')
        )
        queryset = queryset.annotate(
            is_subscribed=Exists(org_subscriptions)
        )

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Filter by category
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Professional Organizations - engg.pk'
        context['categories'] = ProfessionalBody.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


# HTMX Engagement Views
@login_required
def toggle_post_like(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Toggle like on a feed post (HTMX endpoint).

    Uses shared toggle_like utility to eliminate code duplication.

    Args:
        request: The HTTP request from an authenticated user
        pk: The primary key of the FeedPost to toggle like on

    Returns:
        HttpResponse: Rendered partial with updated like button HTML

    Raises:
        Http404: If post with given pk doesn't exist
    """
    post = get_object_or_404(FeedPost, pk=pk)

    # Use shared utility function
    liked, like_count = toggle_like(post, request.user)
    post.like_count = like_count

    return render(request, 'feed/partials/like_button.html', {
        'post': post,
        'liked': liked
    })


@login_required
def toggle_comment_like(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Toggle like on a comment (HTMX endpoint).

    Uses shared toggle_like utility to eliminate code duplication.

    Args:
        request: The HTTP request from an authenticated user
        pk: The primary key of the Comment to toggle like on

    Returns:
        HttpResponse: Rendered partial with updated like button HTML

    Raises:
        Http404: If comment with given pk doesn't exist
    """
    comment = get_object_or_404(Comment, pk=pk)

    # Use shared utility function
    liked, like_count = toggle_like(comment, request.user)
    comment.like_count = like_count

    return render(request, 'feed/partials/comment_like_button.html', {
        'comment': comment,
        'liked': liked
    })


@login_required
def create_comment(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Create a comment on a feed post (HTMX endpoint).

    Validates comment content for length and non-empty value before creating.

    Args:
        request: The HTTP POST request from an authenticated user
        pk: The primary key of the FeedPost to comment on

    Returns:
        HttpResponse: Rendered comment HTML on success, error message on failure

    Raises:
        Http404: If post with given pk doesn't exist
    """
    post = get_object_or_404(FeedPost, pk=pk)

    if request.method != 'POST':
        return HttpResponse('<p class="text-red-500">Invalid request method</p>', status=400)

    content = request.POST.get('content', '').strip()

    # Validate content using shared utility
    is_valid, error_msg = validate_text_length(content, "Comment", MAX_COMMENT_LENGTH)
    if not is_valid:
        return HttpResponse(error_msg, status=400)

    try:
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        return render(request, 'feed/partials/comment_item.html', {
            'comment': comment
        })
    except Exception as e:
        return HttpResponse(
            f'<p class="text-red-500">Error creating comment: {str(e)}</p>',
            status=500
        )


@login_required
def toggle_user_subscription(request, pk):
    """Follow/unfollow a thought leader (HTMX)"""
    thought_leader = get_object_or_404(ThoughtLeader, pk=pk)

    subscription = UserSubscription.objects.filter(
        subscriber=request.user,
        thought_leader=thought_leader
    ).first()

    if subscription:
        subscription.delete()
        thought_leader.follower_count = max(0, thought_leader.follower_count - 1)
        is_subscribed = False
    else:
        UserSubscription.objects.create(
            subscriber=request.user,
            thought_leader=thought_leader
        )
        thought_leader.follower_count += 1
        is_subscribed = True

    thought_leader.save(update_fields=['follower_count'])

    return render(request, 'feed/partials/subscribe_button.html', {
        'thought_leader': thought_leader,
        'is_subscribed': is_subscribed
    })


@login_required
def toggle_organization_subscription(request, pk):
    """Follow/unfollow a professional body (HTMX)"""
    organization = get_object_or_404(ProfessionalBody, pk=pk)

    subscription = OrganizationSubscription.objects.filter(
        subscriber=request.user,
        organization=organization
    ).first()

    if subscription:
        subscription.delete()
        organization.follower_count = max(0, organization.follower_count - 1)
        is_subscribed = False
    else:
        OrganizationSubscription.objects.create(
            subscriber=request.user,
            organization=organization
        )
        organization.follower_count += 1
        is_subscribed = True

    organization.save(update_fields=['follower_count'])

    return render(request, 'feed/partials/organization_subscribe_button.html', {
        'organization': organization,
        'is_subscribed': is_subscribed
    })


@login_required
def load_more_posts(request: HttpRequest) -> HttpResponse:
    """
    Load more posts for infinite scroll (HTMX endpoint).

    Args:
        request: The HTTP request with 'page' GET parameter

    Returns:
        HttpResponse: Rendered post list HTML for the requested page
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    # Get page number with error handling
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    # Reuse the logic from FeedListView
    view = FeedListView()
    view.request = request
    view.paginate_by = 10

    try:
        queryset = view.get_queryset()

        # Paginate
        paginator = Paginator(queryset, view.paginate_by)
        posts = paginator.get_page(page)

        return render(request, 'feed/partials/post_list.html', {
            'posts': posts,
            'page_obj': posts
        })
    except Exception as e:
        return HttpResponse(
            f'<p class="text-red-500">Error loading posts: {str(e)}</p>',
            status=500
        )
