"""djangoPatinflyv2 URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import User

from django.urls import path, include, re_path
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import permission_classes

import frontend.views
from core.models import Scooter, UserLogin, Rent
from djangoPatinflyv2 import settings
from endpoints.views import UserSerializer, ScooterSerializer, LoginSerializer, RentSerializer
from frontend import views as frontend_views
from core import views as core_views
from rest_framework.permissions import AllowAny


# ViewSets define the view behavior.

@permission_classes((AllowAny,))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((AllowAny,))
class ScooterViewSet(viewsets.ModelViewSet):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer


@permission_classes((AllowAny,))
class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserLogin.objects.all()
    serializer_class = LoginSerializer


@permission_classes((AllowAny,))
class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register('scooter', ScooterViewSet)
router.register('endpoints/loginList', LoginViewSet)
router.register('endpoints/rent', RentViewSet)

urlpatterns = [
                  path('', include('frontend.urls')),
                  path('admin_patinfly/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('', include(router.urls)),
                  path('index', frontend_views.index),
                  path('endpoints/login', core_views.login),
                  path('endpoints/rent/start/<str:scooter_uuid>', core_views.startRent),
                  path('endpoints/validate', core_views.validate),
                  path('endpoints/rent/stop/<str:scooter_uuid>', core_views.stopRent),
                  path('endpoints/rent', core_views.rentList),
                  path('endpoints/scooter/<str:scooter_uuid>', core_views.infoScooter),
                  path('endpoints/scooter', core_views.ScooterList),
                  path('status', core_views.serverStatus),
                  path('signIn', core_views.loginWithGoogle),
                  path('login_redirect', frontend_views.loginWithGoogle),
                  path('signOut', core_views.signOut)

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
