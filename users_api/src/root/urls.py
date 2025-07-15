"""root URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from root.health_check import health_check

admin_urls = [
    path('ad6o69ms7in/', admin.site.urls),
]


api_schema_urls = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='index'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


api_urls = [
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/users/', include('users.urls')),
]

non_prefixed_urls = admin_urls + api_schema_urls + api_urls


urlpatterns = [
    path(f'{settings.GATEWAY_PREFIX}', include(non_prefixed_urls)),
    path('ht/', health_check, name='health-check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
