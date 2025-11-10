from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.ForumListView.as_view(), name='list'),
    path('create/', views.ForumPostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', views.ForumPostDetailView.as_view(), name='post_detail'),

    # HTMX endpoints
    path('post/<int:pk>/like/', views.toggle_post_like, name='toggle_post_like'),
    path('reply/<int:pk>/like/', views.toggle_reply_like, name='toggle_reply_like'),
    path('post/<int:pk>/reply/', views.create_reply, name='create_reply'),
]
