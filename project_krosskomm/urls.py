"""project_krosskomm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from announce.views import (
    AnnounceViewSet,
    AnnounceListAPI,
    RegisteredAnnounceListAPI,
)
from core.views import (
    UserViewSet,
    UserListAPI
)

router = routers.DefaultRouter()

# Route POST RETRIEVE DELETE Announce
router.register(r'announces', AnnounceViewSet, basename='announce')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include(router.urls)),
                  path('api/v1/announces/list/', AnnounceListAPI.as_view(), name='api_announce_list'),
                  path('api/v1/registered/announces/list/', RegisteredAnnounceListAPI.as_view(),
                       name='api_registered_announce_list'),
                  path('api/v1/list/users/', UserListAPI.as_view(), name='api_v1_user_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
