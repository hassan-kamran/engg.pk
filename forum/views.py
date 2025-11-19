from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, QuerySet
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from core.utils import toggle_like, validate_text_length
from .models import ForumPost, Reply
from .forms import ForumPostForm, ReplyForm

# Constants
MAX_REPLY_LENGTH = 5000


class ForumListView(ListView):
    model = ForumPost
    template_name = 'forum/list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[ForumPost]:
        """
        Get the forum posts queryset with optimizations.

        Includes reply_count and like_count annotations to avoid N+1 queries.

        Returns:
            QuerySet[ForumPost]: Optimized queryset with annotations
        """
        queryset = ForumPost.objects.annotate(
            reply_count=Count('replies', distinct=True),
            like_count=Count('likes', distinct=True)
        ).select_related('author', 'author__profile')

        # Apply search filter
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # Apply category filter
        category = self.request.GET.get('category', '').strip()
        if category:
            # Validate category against allowed choices
            valid_categories = [choice[0] for choice in ForumPost.CATEGORY_CHOICES]
            if category in valid_categories:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Community Forum - engg.pk'
        context['meta_description'] = 'Discuss technical questions, share experiences, and learn from fellow Pakistani engineers.'
        context['categories'] = ForumPost.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'forum/detail.html'
    context_object_name = 'post'

    def get_object(self) -> ForumPost:
        """
        Get the forum post object and increment views.

        Returns:
            ForumPost: The requested forum post with incremented view count
        """
        obj = super().get_object()
        # Increment views
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get context data with optimized reply queryset.

        Returns:
            Dict[str, Any]: Context dictionary with replies and forms
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Forum - engg.pk'
        context['meta_description'] = self.object.content[:155]

        # Optimize reply queryset with like_count annotation
        context['replies'] = self.object.replies.select_related(
            'author', 'author__profile'
        ).annotate(
            like_count=Count('likes')
        )
        context['reply_form'] = ReplyForm()
        return context


class ForumPostCreateView(LoginRequiredMixin, CreateView):
    """Create a new forum post"""
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'forum/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Post - Forum - engg.pk'
        return context


# HTMX Engagement Views
@login_required
def toggle_post_like(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Toggle like on a forum post (HTMX endpoint).

    Uses shared toggle_like utility to eliminate code duplication.

    Args:
        request: The HTTP request from an authenticated user
        pk: The primary key of the ForumPost to toggle like on

    Returns:
        HttpResponse: Rendered partial with updated like button HTML

    Raises:
        Http404: If post with given pk doesn't exist
    """
    post = get_object_or_404(ForumPost, pk=pk)

    # Use shared utility function
    liked, like_count = toggle_like(post, request.user)
    post.like_count = like_count

    return render(request, 'forum/partials/like_button.html', {
        'post': post,
        'liked': liked
    })


@login_required
def toggle_reply_like(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Toggle like on a reply (HTMX endpoint).

    Uses shared toggle_like utility to eliminate code duplication.

    Args:
        request: The HTTP request from an authenticated user
        pk: The primary key of the Reply to toggle like on

    Returns:
        HttpResponse: Rendered partial with updated like button HTML

    Raises:
        Http404: If reply with given pk doesn't exist
    """
    reply = get_object_or_404(Reply, pk=pk)

    # Use shared utility function
    liked, like_count = toggle_like(reply, request.user)
    reply.like_count = like_count

    return render(request, 'forum/partials/reply_like_button.html', {
        'reply': reply,
        'liked': liked
    })


@login_required
def create_reply(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Create a reply to a forum post (HTMX endpoint).

    Validates reply content for length and non-empty value before creating.

    Args:
        request: The HTTP POST request from an authenticated user
        pk: The primary key of the ForumPost to reply to

    Returns:
        HttpResponse: Rendered reply HTML on success, error message on failure

    Raises:
        Http404: If post with given pk doesn't exist
    """
    post = get_object_or_404(ForumPost, pk=pk)

    if request.method != 'POST':
        return HttpResponse('<p class="text-red-500">Invalid request method</p>', status=400)

    content = request.POST.get('content', '').strip()

    # Validate content using shared utility
    is_valid, error_msg = validate_text_length(content, "Reply", MAX_REPLY_LENGTH)
    if not is_valid:
        return HttpResponse(error_msg, status=400)

    try:
        reply = Reply.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        # Return the new reply HTML
        return render(request, 'forum/partials/reply_item.html', {
            'reply': reply
        })
    except Exception as e:
        return HttpResponse(
            f'<p class="text-red-500">Error creating reply: {str(e)}</p>',
            status=500
        )
