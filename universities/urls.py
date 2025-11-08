from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('', views.UniversityListView.as_view(), name='list'),
    path('<int:pk>/', views.UniversityProgramDetailView.as_view(), name='program_detail'),
]
