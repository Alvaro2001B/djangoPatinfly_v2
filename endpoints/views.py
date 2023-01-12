from rest_framework import serializers, request
from rest_framework.authtoken.admin import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import obtain_auth_token
from core.models import Scooter, UserLogin, Rent
from rest_framework.authtoken.models import Token


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class ScooterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scooter
        fields = ['uuid', 'name', 'longitude', 'latitude', 'meters', 'battry_level', 'last_maintenace', 'vacant',
                  'on_maintenance', 'create_date', 'update_date', 'notification_uptadete']


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserLogin
        fields = ['name', 'secondname', 'password', 'token', 'create_date', 'update_date', 'notification_uptadete']
        read_only_fields = ['create_date', 'update_date', 'notification_uptadete', ]


class RentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rent
        fields = ['uuid', 'name', 'token', 'vacant', 'create_date', 'update_date', 'notification_uptadete']
        read_only_fields = ['create_date', 'update_date', 'notification_uptadete', ]
