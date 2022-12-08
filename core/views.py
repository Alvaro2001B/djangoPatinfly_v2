from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response


# Create your views here.


@api_view(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        print(str(username)+"-"+str(password))
        print(User.objects.all())
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response('Usuario invalido')

    pwd_valid = check_password(password, user.password)
    if not pwd_valid:
        return Response("Contraseña invalida")

    token = Token.objects.create(user=user)
    print(token.py)
    return Response(token.py)
