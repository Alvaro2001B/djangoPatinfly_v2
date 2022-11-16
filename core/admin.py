from django.contrib import admin

from core.models import Scooter


class ScooterAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid', 'latitude', 'longitude', 'vacant', 'on_maintenance']
    list_filter = ['vacant', 'on_maintenance']

admin.site.register(Scooter, ScooterAdmin)
