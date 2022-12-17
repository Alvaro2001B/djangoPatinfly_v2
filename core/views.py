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
                'code': status.HTTP_400_BAD_REQUEST,
                'timestanp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)

        # pwd_valid = check_password(password, user.password)
        # if not pwd_valid:
        #    return Response("Contraseña invalida")
        content = {
            "Token": user.token,
            # .split(':')[1].split(">")[0],
            "Code": status.HTTP_200_OK,
            'timestanp': datetime.now(),
            'version': '1.0'
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
                "code": status.HTTP_400_BAD_REQUEST,
                'timestanp': datetime.now(),
                'version': '1.0'
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
            user.token = str(token).split(':')[1].split(">")[0].split(" ")[1]
            user.save()
            content = {
                "msg": "User añadido",
                "token": str(user.token),
                'code': status.HTTP_201_CREATED,
                'timestanp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
    elif request.method == 'DELETE':
        UserLogin.objects.all().delete()
        #Rent.objects.all().delete()
        content = {
            'msg': 'Deleted users',
            'code': status.HTTP_200_OK,
            'timestanp': datetime.now(),
            'version': '1.0'
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
                    'code': status.HTTP_400_BAD_REQUEST,
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
            elif str(tokenUser) == token:
                timeNow = datetime.now()
                print(timeNow)
                print(user.create_date)
                print(timeNow.date() - user.create_date.date())
                days = (timeNow.date() - user.create_date.date()).days
                print(days)
                if int(days) < int(3):
                    content = {
                        'msg': 'User validated',
                        'code': status.HTTP_200_OK,
                        'timestamp': datetime.now(),
                        'version': '1.0'
                    }
                    return Response(content)
                else:
                    print(user)
                    user.token = ""
                    user.save()
                    Token.objects.filter(user=userT).delete()
                    token = Token.objects.get_or_create(user=userT)
                    print(token)
                    user.token = str(token).split(':')[1].split(">")[0].split(" ")[1]
                    user.save()
                    content = {
                        'msg': 'Create a new token. User validated',
                        'token': str(user.token),
                        'code': status.HTTP_200_OK,
                        'timestamp': datetime.now(),
                        'version': '1.0'
                    }
                    return Response(content)
            else:
                content = {
                    'msg': 'Invalid token',
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
        except:
            content = {
                'msg': 'non-existent user',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def startRent(request, scooter_uuid):
    if request.method == 'GET':
        print("scooter uuid", scooter_uuid)
        token = request.data['token']
        try:
            user = UserLogin.objects.get(token=token)
            scooter = Scooter.objects.get(uuid=scooter_uuid)
        except:
            content = {
                'msg': 'Invalid parameters',
                'code': status.HTTP_400_BAD_REQUEST
            }
            return Response(content)
        try:
            rent = Rent.objects.get(uuid=scooter_uuid)
            if rent.vacant == 1:
                content = {
                    'code': status.HTTP_200_OK,
                    'msg': 'Scooter is alredy rented',
                    'rent': {
                        'uuid': rent.uuid,
                        'date_start': rent.update_date
                    },
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
            else:
                if not scooter.vacant:
                    Rent.objects.create(
                        uuid=scooter_uuid,
                        name=user.name,
                        token=token,
                        vacant=True,
                        update_date=datetime.now()
                    )
                    scooter.vacant = True
                    scooter.save()
                    rent = Rent.objects.get(uuid=scooter_uuid)
                    content = {
                        'code': status.HTTP_200_OK,
                        'msg': 'Scooter rented',
                        'rent': {
                            'uuid': rent.uuid,
                            'date_start': rent.update_date
                        },
                        'timestamp': datetime.now(),
                        'version': '1.0'
                    }
                    return Response(content)
                else:
                    content = {
                        'code': status.HTTP_405_METHOD_NOT_ALLOWED,
                        'msg': 'Scooter is vacant',
                        'rent': '{}',
                        'timestamp': datetime.now(),
                        'version': '1.0'
                    }
                    return Response(content)
        except:
            if not scooter.vacant:
                Rent.objects.create(
                    uuid=scooter_uuid,
                    name=user.name,
                    token=token,
                    update_date=datetime.now()
                )
                scooter.vacant = True
                scooter.save()
                rent = Rent.objects.get(uuid=scooter_uuid)
                content = {
                    'code': status.HTTP_200_OK,
                    'msg': 'Scooter rented',
                    'rent': {
                        'uuid': rent.uuid,
                        'date_start': rent.update_date
                    },
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
            else:
                content = {
                    'code': status.HTTP_405_METHOD_NOT_ALLOWED,
                    'msg': 'Scooter is vacant',
                    'rent': '{}',
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def stopRent(request, scooter_uuid):
    if request.method == 'GET':
        print("scooter uuid", scooter_uuid)
        token = request.data['token']
        try:
            user = UserLogin.objects.get(token=token)
            scooter = Scooter.objects.get(uuid=scooter_uuid)
        except:
            content = {
                'msg': 'Invalid parameters',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        try:
            rent = Rent.objects.get(uuid=scooter_uuid)
            if rent.vacant:
                rent.vacant = False
                rent.save()
            else:
                content = {
                    'msg': 'Scooter not vacant ',
                    'code': status.HTTP_405_METHOD_NOT_ALLOWED,
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
        except:
            content = {
                'msg': 'Scootet not rented',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)

        # if scooter.vacant == 1:
