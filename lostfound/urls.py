from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Allauth MUST be loaded first
    path("accounts/", include("allauth.urls")),

    # Your app
    path("", include("core.urls")),

    # Admin
    path("admin/", admin.site.urls),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
