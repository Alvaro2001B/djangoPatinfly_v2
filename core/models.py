from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


class Scooter(models.Model):
    uuid = models.CharField(max_length=64)
    name = models.CharField(max_length=40)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    meters = models.IntegerField(default=0)
    battry_level = models.IntegerField(100)
    last_maintenace = models.DateField(default=timezone.now)
    vacant = models.BooleanField(default=True)
    on_maintenance = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True)
    notification_uptadete = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class UserLogin(models.Model):
    name = models.CharField('name', max_length=70)
    secondname = models.CharField(max_length=70, blank=True, null=True)
    token = models.CharField(max_length=70)
    password = models.CharField(max_length=70, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True)
    notification_uptadete = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Rent(models.Model):
    uuid = models.CharField(max_length=64)
    name = models.CharField(max_length=40)
    token = models.CharField(max_length=60)
    vacant = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True)
    notification_uptadete = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
