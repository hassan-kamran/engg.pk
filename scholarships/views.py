from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from .models import Scholarship


class ScholarshipListView(ListView):
    model = Scholarship
    template_name = 'scholarships/list.html'
    context_object_name = 'scholarships'
    paginate_by = 20

    def get_queryset(self):
        queryset = Scholarship.objects.filter(
            is_active=True,
            deadline__gte=timezone.now().date()
        )

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(provider__icontains=search) |
                Q(country__icontains=search)
            )

        # Level filter
        level = self.request.GET.get('level', '')
        if level:
            queryset = queryset.filter(level=level)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Scholarships - engg.pk'
        context['meta_description'] = 'Discover scholarship opportunities for engineering students in Pakistan and abroad.'
        context['levels'] = Scholarship.LEVEL_CHOICES
        context['selected_level'] = self.request.GET.get('level', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ScholarshipDetailView(DetailView):
    model = Scholarship
    template_name = 'scholarships/detail.html'
    context_object_name = 'scholarship'

    def get_queryset(self):
        return Scholarship.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.name} - Scholarships - engg.pk'
        context['meta_description'] = self.object.description[:155]
        return context
