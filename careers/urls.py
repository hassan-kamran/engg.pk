from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.CareerPathListView.as_view(), name='list'),
    path('<int:pk>/', views.CareerPathDetailView.as_view(), name='detail'),
]
