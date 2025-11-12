from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import SubjectConnection, UserProfile
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm


class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Engineering Community of Pakistan'
        context['meta_description'] = 'Empowering Pakistani engineers with knowledge, opportunities, and community. Join us to connect, learn, and grow.'
        return context


class AboutPageView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us - engg.pk'
        context['meta_description'] = 'Learn about our mission to empower Pakistani engineers and combat brain drain through community and knowledge sharing.'
        return context


class SubjectConnectionsView(ListView):
    model = SubjectConnection
    template_name = 'core/subjects.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Subject Connections - engg.pk'
        context['meta_description'] = 'Understand how different engineering subjects connect and apply to real-world problems and career paths.'
        return context


# Authentication Views
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to engg.pk, {user.get_full_name()}!')
            return redirect('core:home')
    else:
        form = UserRegisterForm()

    return render(request, 'core/auth/register.html', {
        'form': form,
        'page_title': 'Register - engg.pk'
    })


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
    else:
        form = UserLoginForm()

    return render(request, 'core/auth/login.html', {
        'form': form,
        'page_title': 'Login - engg.pk'
    })


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:home')


class UserProfileView(DetailView):
    """View user profile"""
    model = User
    template_name = 'core/profile/view.html'
    context_object_name = 'profile_user'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['page_title'] = f'{user.get_full_name() or user.username} - Profile'
        context['profile'] = user.profile
        # Get user's contributions with optimized queries
        context['forum_posts'] = user.forum_posts.select_related('author', 'author__profile').all()[:5]
        context['insights'] = user.insights.select_related('author', 'author__profile').all()[:5]
        context['program_reviews'] = user.program_reviews.select_related('author', 'author__profile').all()[:5]
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'core/profile/edit.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Profile updated successfully!')
        return reverse_lazy('core:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Profile - engg.pk'
        return context
