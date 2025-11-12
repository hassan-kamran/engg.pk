from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Exists, OuterRef
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import (
    FeedPost, Comment, ThoughtLeader, ProfessionalBody,
    UserSubscription, OrganizationSubscription, TopicSubscription
)
from .forms import FeedPostForm, CommentForm


class FeedListView(LoginRequiredMixin, ListView):
    """Main feed with infinite scroll - shows posts from followed users/organizations"""
    model = FeedPost
    template_name = 'feed/list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Load 10 posts at a time for infinite scroll

    def get_queryset(self):
        user = self.request.user

        # Get users that the current user follows (thought leaders)
        subscribed_thought_leaders = UserSubscription.objects.filter(
            subscriber=user
        ).values_list('thought_leader__user', flat=True)

        # Get organizations that the current user follows
        subscribed_organizations = OrganizationSubscription.objects.filter(
            subscriber=user
        ).values_list('organization', flat=True)

        # Get topics the user subscribed to
        subscribed_topics = TopicSubscription.objects.filter(
            subscriber=user
        ).values_list('topic', flat=True)

        # Build query - show posts from followed users, organizations, or topics
        q_objects = Q()

        if subscribed_thought_leaders:
            q_objects |= Q(author_user__in=subscribed_thought_leaders)

        if subscribed_organizations:
            q_objects |= Q(author_organization__in=subscribed_organizations)

        if subscribed_topics:
            # Posts that contain any of the subscribed topics
            for topic in subscribed_topics:
                q_objects |= Q(topics__contains=topic)

        # Base queryset with optimization
        queryset = FeedPost.objects.select_related(
            'author_user', 'author_organization'
        ).prefetch_related('likes', 'comments').annotate(
            comment_count=Count('comments')
        )

        # Apply subscription filter if user follows anything
        if subscribed_thought_leaders or subscribed_organizations or subscribed_topics:
            queryset = queryset.filter(q_objects)

        # If user doesn't follow anyone yet, show all posts (discovery mode)
        # This ensures new users see content immediately

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # Filter by post type
        post_type = self.request.GET.get('type', '')
        if post_type:
            queryset = queryset.filter(post_type=post_type)

        return queryset.distinct().order_by('-created_at')

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
        user = self.request.user

        # Check if user is a thought leader
        if hasattr(user, 'thought_leader_profile'):
            form.instance.author_user = user
        # Check if user manages any organizations
        elif user.managed_organizations.exists():
            # If form has organization field, use it; otherwise use first managed org
            org_id = self.request.POST.get('organization')
            if org_id:
                form.instance.author_organization_id = org_id
            else:
                form.instance.author_organization = user.managed_organizations.first()
        else:
            messages.error(self.request, 'You must be a verified thought leader or organization admin to post.')
            return redirect('feed:list')

        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

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
def toggle_post_like(request, pk):
    """Toggle like on a feed post (HTMX)"""
    post = get_object_or_404(FeedPost, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return render(request, 'feed/partials/like_button.html', {
        'post': post,
        'liked': liked
    })


@login_required
def toggle_comment_like(request, pk):
    """Toggle like on a comment (HTMX)"""
    comment = get_object_or_404(Comment, pk=pk)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return render(request, 'feed/partials/comment_like_button.html', {
        'comment': comment,
        'liked': liked
    })


@login_required
def create_comment(request, pk):
    """Create a comment on a feed post (HTMX)"""
    post = get_object_or_404(FeedPost, pk=pk)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            return render(request, 'feed/partials/comment_item.html', {
                'comment': comment
            })
        else:
            return HttpResponse('<p class="text-red-500">Comment cannot be empty</p>', status=400)

    return HttpResponse(status=400)


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
def load_more_posts(request):
    """Load more posts for infinite scroll (HTMX)"""
    page = int(request.GET.get('page', 1))

    # Reuse the logic from FeedListView
    view = FeedListView()
    view.request = request
    view.paginate_by = 10

    queryset = view.get_queryset()

    # Paginate
    from django.core.paginator import Paginator
    paginator = Paginator(queryset, view.paginate_by)
    posts = paginator.get_page(page)

    return render(request, 'feed/partials/post_list.html', {
        'posts': posts,
        'page_obj': posts
    })
