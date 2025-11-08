from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import CareerPath


class CareerPathListView(ListView):
    model = CareerPath
    template_name = 'careers/list.html'
    context_object_name = 'careers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Career Paths - engg.pk'
        context['meta_description'] = 'Explore different engineering careers and learn from experienced professionals in Pakistan.'
        return context


class CareerPathDetailView(DetailView):
    model = CareerPath
    template_name = 'careers/detail.html'
    context_object_name = 'career'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - Career Paths - engg.pk'
        context['meta_description'] = self.object.overview[:155]
        context['stories'] = self.object.stories.select_related('author', 'author__profile')
        return context
