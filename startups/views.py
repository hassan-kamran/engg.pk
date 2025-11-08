from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import StartupResource


class StartupResourceListView(ListView):
    model = StartupResource
    template_name = 'startups/list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        queryset = StartupResource.objects.all()

        # Category filter
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Startup Resources - engg.pk'
        context['meta_description'] = 'Access resources, funding opportunities, and guidance for building tech startups in Pakistan.'
        context['categories'] = StartupResource.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class StartupResourceDetailView(DetailView):
    model = StartupResource
    template_name = 'startups/detail.html'
    context_object_name = 'resource'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Startup Resources - engg.pk'
        context['meta_description'] = self.object.description[:155]
        return context
