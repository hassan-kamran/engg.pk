from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Job


class JobListView(ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    paginate_by = 20

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(company__icontains=search) |
                Q(location__icontains=search)
            )

        # Type filter
        job_type = self.request.GET.get('type', '')
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Job Opportunities - engg.pk'
        context['meta_description'] = 'Find engineering job opportunities across Pakistan in various industries.'
        context['job_types'] = Job.TYPE_CHOICES
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        return Job.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} at {self.object.company} - Jobs - engg.pk'
        context['meta_description'] = self.object.description[:155]
        return context
