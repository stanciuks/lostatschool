from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),          # include app urls
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import handler404, handler500

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),   # or your home view
]
