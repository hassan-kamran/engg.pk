"""
URL configuration for engg.pk project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('forum/', include('forum.urls')),
    path('universities/', include('universities.urls')),
    path('careers/', include('careers.urls')),
    path('jobs/', include('jobs.urls')),
    path('scholarships/', include('scholarships.urls')),
    path('insights/', include('insights.urls')),
    path('startups/', include('startups.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = "engg.pk Administration"
admin.site.site_title = "engg.pk Admin"
admin.site.index_title = "Welcome to engg.pk Admin Portal"
