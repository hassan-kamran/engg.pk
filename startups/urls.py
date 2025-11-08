from django.urls import path
from . import views

app_name = 'startups'

urlpatterns = [
    path('', views.StartupResourceListView.as_view(), name='list'),
    path('<int:pk>/', views.StartupResourceDetailView.as_view(), name='detail'),
]
