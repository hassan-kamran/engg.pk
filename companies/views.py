"""
Views for the companies app - Glassdoor-like company reviews and insights.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from .models import Company, CompanyReview, SalaryReport, CompanyPhoto
from .forms import CompanyReviewForm, SalaryReportForm, CompanyPhotoForm


class CompanyListView(ListView):
    """
    List all companies with filtering capabilities.
    Supports filtering by industry and search functionality.
    """
    model = Company
    template_name = 'companies/list.html'
    context_object_name = 'companies'
    paginate_by = 20

    def get_queryset(self):
        """
        Get filtered queryset based on search and industry filters.
        """
        queryset = Company.objects.all()

        # Search by company name or description
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(headquarters_location__icontains=search)
            )

        # Filter by industry
        industry = self.request.GET.get('industry', '')
        if industry:
            queryset = queryset.filter(industry=industry)

        # Filter by verified companies only (optional)
        verified_only = self.request.GET.get('verified', '')
        if verified_only == 'true':
            queryset = queryset.filter(verified=True)

        return queryset.order_by('-overall_rating', 'name')

    def get_context_data(self, **kwargs):
        """Add additional context for filtering and display."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Companies - engg.pk'
        context['meta_description'] = 'Browse company reviews, salaries, and insights for Pakistani companies.'
        context['industries'] = Company.INDUSTRY_CHOICES
        context['selected_industry'] = self.request.GET.get('industry', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['verified_only'] = self.request.GET.get('verified', '')
        return context


class CompanyDetailView(DetailView):
    """
    Display detailed company information with tabs for:
    - Overview (company info)
    - Reviews (employee reviews)
    - Salaries (salary reports)
    - Interviews (from mentorship app)
    - Photos (company photos)
    """
    model = Company
    template_name = 'companies/detail.html'
    context_object_name = 'company'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Add reviews, salaries, and other related data."""
        context = super().get_context_data(**kwargs)
        company = self.object

        # Get active tab from query params (default to 'overview')
        active_tab = self.request.GET.get('tab', 'overview')
        context['active_tab'] = active_tab

        # Overview tab data
        context['page_title'] = f'{company.name} - Companies - engg.pk'
        context['meta_description'] = company.description[:155]

        # Reviews tab data
        reviews = company.reviews.filter(is_approved=True).select_related('author')
        context['reviews'] = reviews[:10]  # Limit to 10 most recent
        context['reviews_count'] = reviews.count()

        # Calculate rating breakdowns
        context['rating_breakdown'] = {
            'work_life_balance': reviews.aggregate(Avg('work_life_balance_rating'))['work_life_balance_rating__avg'] or 0,
            'culture_values': reviews.aggregate(Avg('culture_values_rating'))['culture_values_rating__avg'] or 0,
            'career_opportunities': reviews.aggregate(Avg('career_opportunities_rating'))['career_opportunities_rating__avg'] or 0,
            'compensation_benefits': reviews.aggregate(Avg('compensation_benefits_rating'))['compensation_benefits_rating__avg'] or 0,
            'senior_management': reviews.aggregate(Avg('senior_management_rating'))['senior_management_rating__avg'] or 0,
        }

        # Check if current user has already reviewed this company
        context['user_has_reviewed'] = False
        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = reviews.filter(author=self.request.user).exists()

        # Salaries tab data
        salaries = company.salaries.all()
        context['salaries'] = salaries[:10]  # Limit to 10 most recent
        context['salaries_count'] = salaries.count()

        # Calculate average salary by job title (top 5 roles)
        salary_by_role = salaries.values('job_title').annotate(
            avg_salary=Avg('total_compensation'),
            count=Count('id')
        ).order_by('-count')[:5]
        context['salary_by_role'] = salary_by_role

        # Interviews tab data (from mentorship app)
        # Note: This assumes interview_experiences is the related_name from mentorship app
        if hasattr(company, 'interview_experiences'):
            interviews = company.interview_experiences.all()
            context['interviews'] = interviews[:10]
            context['interviews_count'] = interviews.count()
        else:
            context['interviews'] = []
            context['interviews_count'] = 0

        # Photos tab data
        photos = company.photos.filter(is_approved=True)
        context['photos'] = photos[:20]  # Limit to 20 most recent
        context['photos_count'] = photos.count()

        # Benefits data
        context['benefits'] = company.benefits.all()

        return context


class CompanyReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new company review.
    Requires user to be authenticated.
    One review per user per company.
    """
    model = CompanyReview
    form_class = CompanyReviewForm
    template_name = 'companies/review_create.html'

    def dispatch(self, request, *args, **kwargs):
        """Check if user has already reviewed this company."""
        self.company = get_object_or_404(Company, slug=kwargs.get('slug'))

        # Check if user has already reviewed this company
        if CompanyReview.objects.filter(company=self.company, author=request.user).exists():
            messages.warning(request, 'You have already submitted a review for this company.')
            return redirect('companies:company_detail', slug=self.company.slug)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set the company and author before saving."""
        form.instance.company = self.company
        form.instance.author = self.request.user
        messages.success(self.request, 'Your review has been submitted successfully!')

        # Update company aggregated data
        response = super().form_valid(form)
        self.company.update_aggregated_data()

        return response

    def get_success_url(self):
        """Redirect to company detail page after successful review."""
        return reverse('companies:company_detail', kwargs={'slug': self.company.slug}) + '?tab=reviews'

    def get_context_data(self, **kwargs):
        """Add company to context."""
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['page_title'] = f'Write Review - {self.company.name} - engg.pk'
        return context


class SalaryReportCreateView(LoginRequiredMixin, CreateView):
    """
    Submit salary information for a company.
    Can be submitted anonymously (optional).
    """
    model = SalaryReport
    form_class = SalaryReportForm
    template_name = 'companies/salary_create.html'

    def dispatch(self, request, *args, **kwargs):
        """Get the company from URL."""
        self.company = get_object_or_404(Company, slug=kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set the company and optionally the submitter."""
        form.instance.company = self.company

        # Check if user wants to submit anonymously
        is_anonymous = form.cleaned_data.get('is_anonymous', False)
        if not is_anonymous:
            form.instance.submitter = self.request.user
        else:
            form.instance.submitter = None

        messages.success(self.request, 'Your salary information has been submitted successfully!')

        # Update company aggregated data
        response = super().form_valid(form)
        self.company.update_aggregated_data()

        return response

    def get_success_url(self):
        """Redirect to company detail page after successful submission."""
        return reverse('companies:company_detail', kwargs={'slug': self.company.slug}) + '?tab=salaries'

    def get_context_data(self, **kwargs):
        """Add company to context."""
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['page_title'] = f'Submit Salary - {self.company.name} - engg.pk'
        return context


class CompanyPhotoUploadView(LoginRequiredMixin, CreateView):
    """
    Upload photos of company offices, teams, and events.
    Photos require admin approval before being displayed.
    """
    model = CompanyPhoto
    form_class = CompanyPhotoForm
    template_name = 'companies/photo_upload.html'

    def dispatch(self, request, *args, **kwargs):
        """Get the company from URL."""
        self.company = get_object_or_404(Company, slug=kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set the company and uploader before saving."""
        form.instance.company = self.company
        form.instance.uploader = self.request.user
        messages.success(
            self.request,
            'Your photo has been uploaded successfully! It will be visible after admin approval.'
        )
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to company detail page after successful upload."""
        return reverse('companies:company_detail', kwargs={'slug': self.company.slug}) + '?tab=photos'

    def get_context_data(self, **kwargs):
        """Add company to context."""
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['page_title'] = f'Upload Photo - {self.company.name} - engg.pk'
        return context


# HTMX Interactive Views

@login_required
def toggle_review_helpful(request, pk):
    """
    Toggle 'helpful' marking on a company review (HTMX endpoint).
    Users can mark reviews as helpful to surface the most useful content.
    """
    review = get_object_or_404(CompanyReview, pk=pk)

    # Toggle helpful status
    if request.user in review.helpful_users.all():
        review.helpful_users.remove(request.user)
        review.helpful_count = review.helpful_users.count()
        review.save(update_fields=['helpful_count'])
        is_helpful = False
    else:
        review.helpful_users.add(request.user)
        review.helpful_count = review.helpful_users.count()
        review.save(update_fields=['helpful_count'])
        is_helpful = True

    # Return updated button HTML for HTMX
    return render(request, 'companies/partials/helpful_button.html', {
        'review': review,
        'is_helpful': is_helpful
    })
