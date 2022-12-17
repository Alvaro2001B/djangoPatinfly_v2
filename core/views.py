from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from core.models import UserLogin, Scooter, Rent
from rest_framework import status


# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def login(request):
    print(request.data)
    if request.method == 'GET':
        username = request.data['username']
        password = request.data['password']
        try:
            print(str(username) + "-" + str(password))
            print(UserLogin.objects.all())
            user = UserLogin.objects.get(name=username)
        except User.DoesNotExist:
            content = {
                'msg': 'non-existent user',
                'code': status.HTTP_400_BAD_REQUEST
            }
            return Response(content)

        # pwd_valid = check_password(password, user.password)
        # if not pwd_valid:
        #    return Response("Contraseña invalida")
        content = {
            "Token": user.token.split(':')[1].split(">")[0],
            "Code": status.HTTP_200_OK
        }
        return Response(content)
    elif request.method == 'POST':
        username = request.data['username']
        secondname = request.data['secondname']
        password = request.data['password']

        try:
            UserLogin.objects.get(name=username)
            content = {
                "msg": "existing user",
                "code": status.HTTP_400_BAD_REQUEST
            }
            return Response(content)
        except:
            user = authenticate(username=username, password=password)
            print(user)
            token = Token.objects.get_or_create(user=user)
            UserLogin.objects.create(
                name=username,
                secondname=secondname,
                password=password,
                token=""
            )
            user = UserLogin.objects.get(name=username)
            user.token = token
            user.save()
            content = {
                "msg": "User añadido",
                "token": str(token[0]),
                'code': status.HTTP_201_CREATED
            }
            return Response(content)
    elif request.method == 'DELETE':
        UserLogin.objects.all().delete()
        content = {
            'msg': 'Deleted users',
            'code': status.HTTP_200_OK
        }
        return Response(content)

    # UserLogin.objects.create(name=username,secondname= secondname,token=token, password=password )


@api_view(['GET'])
@permission_classes((AllowAny,))
def validate(request):
    if request.method == 'GET':
        username = request.data['username']
        token = request.data['token']

        print('Request:' + str(username) + '-' + str(token))
        try:
            user = UserLogin.objects.get(name=username)
            userT = authenticate(username=username, password=user.password)
            tokenUser = Token.objects.get_or_create(user=userT)
            print('User:' + str(user.name) + '-' + str(tokenUser[0]))
            if user.token == "":
                content = {
                    'msg': 'User not validated',
                    'code': status.HTTP_400_BAD_REQUEST
                }
                return Response(content)
            elif str(tokenUser[0]) == token:
                timeNow = datetime.now()
                print(timeNow)
                print(user.create_date)
                print(timeNow.date() - user.create_date.date())
                days = (timeNow.date() - user.create_date.date()).days
                print(days)
                if int(days) < int(3):
                    content = {
                        'msg': 'User validated',
                        'code': status.HTTP_200_OK
                    }
                    return Response(content)
                else:
                    print(user)
                    user.token = ""
                    user.save()
                    Token.objects.filter(user=userT).delete()
                    token = Token.objects.get_or_create(user=userT)
                    print(token)
                    user.token = token
                    user.save()
                    content = {
                        'msg': 'Create a new token. User validated',
                        'token': str(user.token[0]),
                        'code': status.HTTP_200_OK
                    }
                    return Response(content)
            else:
                content = {
                    'msg':'Invalida token',
                    'code':status.HTTP_401_UNAUTHORIZED
                }
                return Response(content)
        except:
            content = {
                'msg': 'non-existent user',
                'code': status.HTTP_400_BAD_REQUEST
            }
            return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def startRent(request, scooter_uuid):
    print("scooter uuid", scooter_uuid)
    if request.method == 'GET':
        rent = Rent.objects.all
        # scooter = Scooter.objects.get(uuid=scooter_uuid)
        print(str(rent))
        content = {
            'code': status.HTTP_200_OK
        }
    return Response(content)
