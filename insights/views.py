from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import IndustryInsight


class InsightListView(ListView):
    model = IndustryInsight
    template_name = 'insights/list.html'
    context_object_name = 'insights'
    paginate_by = 10

    def get_queryset(self):
        return IndustryInsight.objects.select_related('author', 'author__profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Industry Insights - engg.pk'
        context['meta_description'] = 'Learn about real-world applications and industry trends from verified Pakistani engineering experts.'
        return context


class InsightDetailView(DetailView):
    model = IndustryInsight
    template_name = 'insights/detail.html'
    context_object_name = 'insight'

    def get_object(self):
        obj = super().get_object()
        # Increment views
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Industry Insights - engg.pk'
        context['meta_description'] = self.object.content[:155]
        return context
