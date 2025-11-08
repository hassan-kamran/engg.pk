from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.ForumListView.as_view(), name='list'),
    path('<int:pk>/', views.ForumPostDetailView.as_view(), name='post_detail'),
]
