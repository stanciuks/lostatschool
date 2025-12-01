"""URL configuration for the lostfound Django project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Authentication (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Core app URLs
    path('', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
