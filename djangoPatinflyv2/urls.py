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

from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from core.models import Scooter, UserLogin
from djangoPatinflyv2 import settings
from endpoints.views import UserSerializer, ScooterSerializer, LoginSerializer
from frontend import views as frontend_views


# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ScooterViewSet(viewsets.ModelViewSet):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer

class LoginViewSet(viewsets.ModelViewSet):
   queryset = UserLogin.objects.all()
   serializer_class = LoginSerializer




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'scooter', ScooterViewSet)
router.register('endpoints/login',LoginViewSet)

urlpatterns = [
    path('admin_patinfly/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('index', frontend_views.index)
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
