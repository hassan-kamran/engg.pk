from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='detail'),

    # HTMX endpoints
    path('<int:pk>/save/', views.toggle_save_job, name='toggle_save'),
    path('<int:pk>/apply/', views.track_application, name='track_application'),
]
