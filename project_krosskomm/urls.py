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
    UserListAPI, GoogleLogin,
    SignUpView, InfluenceurView,
    EnterpriseView, InfluenceurViewSet,
    EnterpriseViewSet, MyTokenObtainPairView
)
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

# Route POST RETRIEVE DELETE Announce
router.register('announces', AnnounceViewSet, basename='announce')
router.register('users', UserViewSet, basename='user')
router.register('influenceurs', InfluenceurViewSet, basename='influenceur')
router.register('entreprises', EnterpriseViewSet, basename='entreprise')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include(router.urls)),
                  path('dj-rest-auth/', include('dj_rest_auth.urls')),
                  path('api/v1/signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
                  path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
                  path('api/v1/signup/', SignUpView.as_view(), name='signup'),
                  path('api/v1/profile/influenceur/', InfluenceurView.as_view(), name='influenceur_profile'),
                  path('api/v1/profile/entreprise/', EnterpriseView.as_view(), name='entreprise_profile'),
                  path('api/v1/announces/list/', AnnounceListAPI.as_view(), name='api_announce_list'),
                  path('api/v1/registered/announces/list/', RegisteredAnnounceListAPI.as_view(),
                       name='api_registered_announce_list'),
                  path('api/v1/list/users/', UserListAPI.as_view(), name='api_v1_user_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
