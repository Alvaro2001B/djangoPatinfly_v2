from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import core.models


def index(request):
    context = {'project_name': 'Patinfly', 'scooters': core.models.Scooter.objects.all()}
    return render(request, 'index.html', context)


def loginWithGoogle(request):
    return render(request, "frontendLogin/login_redirect.html")
