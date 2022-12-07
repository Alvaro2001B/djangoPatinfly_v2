from django.shortcuts import render
from rest_framework.response import Response

import core.models


def index(request):
    context = {'project_name': 'Patinfly', 'scooters': core.models.Scooter.objects.all()}
    return render(request, 'index.html', context)



