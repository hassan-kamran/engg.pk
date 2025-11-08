from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Core pages
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('subjects/', views.SubjectConnectionsView.as_view(), name='subjects'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User profiles
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='profile_edit'),
]
