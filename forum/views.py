from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, F
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from .models import ForumPost, Reply
from .forms import ForumPostForm, ReplyForm


class ForumListView(ListView):
    model = ForumPost
    template_name = 'forum/list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = ForumPost.objects.annotate(
            reply_count=Count('replies')
        ).select_related('author', 'author__profile')

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # Category filter
        category = self.request.GET.get('category', '')
        if category:
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

    def get_object(self):
        obj = super().get_object()
        # Increment views using F() to avoid race conditions
        obj.views = F('views') + 1
        obj.save(update_fields=['views'])
        obj.refresh_from_db()  # Refresh to get the actual value
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Forum - engg.pk'
        context['meta_description'] = self.object.content[:155]
        context['replies'] = self.object.replies.select_related('author', 'author__profile')
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
def toggle_post_like(request, pk):
    """Toggle like on a forum post (HTMX)"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    post = get_object_or_404(ForumPost, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    # Return updated like button HTML
    return render(request, 'forum/partials/like_button.html', {
        'post': post,
        'liked': liked
    })


@login_required
def toggle_reply_like(request, pk):
    """Toggle like on a reply (HTMX)"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    reply = get_object_or_404(Reply, pk=pk)

    if request.user in reply.likes.all():
        reply.likes.remove(request.user)
        liked = False
    else:
        reply.likes.add(request.user)
        liked = True

    # Return updated like button HTML
    return render(request, 'forum/partials/reply_like_button.html', {
        'reply': reply,
        'liked': liked
    })


@login_required
def create_reply(request, pk):
    """Create a reply to a forum post (HTMX)"""
    post = get_object_or_404(ForumPost, pk=pk)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            reply = Reply.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            # Return the new reply HTML
            return render(request, 'forum/partials/reply_item.html', {
                'reply': reply
            })
        else:
            return HttpResponse('<p class="text-red-500">Reply cannot be empty</p>', status=400)

    return HttpResponse(status=400)
