from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    # Main feed
    path('', views.FeedListView.as_view(), name='list'),
    path('create/', views.FeedPostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.FeedPostDetailView.as_view(), name='post_detail'),

    # Discover
    path('thought-leaders/', views.ThoughtLeaderListView.as_view(), name='thought_leaders'),
    path('organizations/', views.ProfessionalBodyListView.as_view(), name='organizations'),

    # HTMX endpoints
    path('post/<int:pk>/like/', views.toggle_post_like, name='toggle_post_like'),
    path('comment/<int:pk>/like/', views.toggle_comment_like, name='toggle_comment_like'),
    path('post/<int:pk>/comment/', views.create_comment, name='create_comment'),
    path('thought-leader/<int:pk>/subscribe/', views.toggle_user_subscription, name='toggle_user_subscription'),
    path('organization/<int:pk>/subscribe/', views.toggle_organization_subscription, name='toggle_organization_subscription'),
    path('load-more/', views.load_more_posts, name='load_more_posts'),
]
