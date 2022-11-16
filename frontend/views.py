from django.shortcuts import render

import core.models


def index(request):
    context = {'project_name': 'Patinfly', 'scooters': core.models.Scooter.objects.all()}
    return render(request, 'index.html', context)

