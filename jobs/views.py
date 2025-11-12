from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Job, SavedJob, JobApplication


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

        # Check if user has saved or applied to this job
        if self.request.user.is_authenticated:
            context['is_saved'] = SavedJob.objects.filter(user=self.request.user, job=self.object).exists()
            context['has_applied'] = JobApplication.objects.filter(user=self.request.user, job=self.object).exists()

        return context


# HTMX Engagement Views
@login_required
def toggle_save_job(request, pk):
    """Toggle save on a job (HTMX)"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    job = get_object_or_404(Job, pk=pk)

    saved_job = SavedJob.objects.filter(user=request.user, job=job).first()
    if saved_job:
        saved_job.delete()
        is_saved = False
    else:
        SavedJob.objects.create(user=request.user, job=job)
        is_saved = True

    # Return updated save button HTML
    return render(request, 'jobs/partials/save_button.html', {
        'job': job,
        'is_saved': is_saved
    })


@login_required
def track_application(request, pk):
    """Track job application (HTMX)"""
    job = get_object_or_404(Job, pk=pk)

    application, created = JobApplication.objects.get_or_create(
        user=request.user,
        job=job
    )

    if request.method == 'POST':
        status = request.POST.get('status', 'applied')
        notes = request.POST.get('notes', '')
        application.status = status
        application.notes = notes
        application.save()

    # Return updated application button HTML
    return render(request, 'jobs/partials/application_button.html', {
        'job': job,
        'has_applied': True,
        'application': application
    })
