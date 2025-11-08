from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import ForumPost, Reply


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
        # Increment views
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Forum - engg.pk'
        context['meta_description'] = self.object.content[:155]
        context['replies'] = self.object.replies.select_related('author', 'author__profile')
        return context
