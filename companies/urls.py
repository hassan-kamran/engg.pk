"""
URL patterns for the companies app - Glassdoor-like company reviews and insights.
"""
from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    # Company listing and detail pages
    path('', views.CompanyListView.as_view(), name='list'),
    path('<slug:slug>/', views.CompanyDetailView.as_view(), name='company_detail'),

    # Review creation
    path('<slug:slug>/review/create/', views.CompanyReviewCreateView.as_view(), name='review_create'),

    # Salary reporting
    path('<slug:slug>/salary/create/', views.SalaryReportCreateView.as_view(), name='salary_create'),

    # Photo uploading
    path('<slug:slug>/photo/upload/', views.CompanyPhotoUploadView.as_view(), name='photo_upload'),

    # HTMX endpoints for interactive features
    path('review/<int:pk>/helpful/', views.toggle_review_helpful, name='toggle_review_helpful'),
]
