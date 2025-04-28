from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from properties.views import PropertyViewSet
from rest_framework.authtoken.views import obtain_auth_token

# router = DefaultRouter()
# router.register(r'api/properties', PropertyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',obtain_auth_token,name='api_token'),

    path('', include('home.urls')),

    path('properties/', include('properties.urls')),
    path('api/properties/', include('properties.api_urls')),

    path('accounts/', include('accounts.urls')),
    path('api/accounts/', include('accounts.api_urls')),

    path('chat/', include('chat.urls')),
    path('notifications/', include('notifications.urls')),
    # path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
