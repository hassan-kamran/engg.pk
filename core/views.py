from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import SubjectConnection


class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Engineering Community of Pakistan'
        context['meta_description'] = 'Empowering Pakistani engineers with knowledge, opportunities, and community. Join us to connect, learn, and grow.'
        return context


class AboutPageView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us - engg.pk'
        context['meta_description'] = 'Learn about our mission to empower Pakistani engineers and combat brain drain through community and knowledge sharing.'
        return context


class SubjectConnectionsView(ListView):
    model = SubjectConnection
    template_name = 'core/subjects.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Subject Connections - engg.pk'
        context['meta_description'] = 'Understand how different engineering subjects connect and apply to real-world problems and career paths.'
        return context
