from rest_framework import serializers, request
from rest_framework.authtoken.admin import User
from rest_framework.response import Response
from rest_framework.decorators import  api_view
from core.models import Scooter, UserLogin


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
        fields = ['name', 'token']
        read_only_fileds = ['token']



