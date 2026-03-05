"""
URL configuration for school_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('students/', include('apps.students.urls', namespace='students')),
    path('academics/', include('apps.academics.urls', namespace='academics')),
    path('ui/notes/', TemplateView.as_view(template_name='ui/notes.html'), name='ui_notes'),
    path('ui/bulletins/', TemplateView.as_view(template_name='ui/bulletins.html'), name='ui_bulletins'),
    path('ui/finance/', TemplateView.as_view(template_name='ui/finance.html'), name='ui_finance'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
