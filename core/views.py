import django
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from core.models import UserLogin, Scooter, Rent
from rest_framework import status


@api_view(['POST'])
@permission_classes((AllowAny,))
def loginWithGoogle(request):
    print(request.data)
    username = request.data['username']
    password = request.data['password']
    token = request.data['token']
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username.split(" ")[0])
            userS = UserLogin.objects.get(name=username.split(" ")[0])
            if userS.token == "":
                newToken = Token.objects.get_or_create(user=user)
                userS.token = str(newToken[0])
                userS.update_date = datetime.now()
                userS.save()
                content = {
                    "msg": "User validated",
                    "code": status.HTTP_200_OK,
                    'timestanp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)

            content = {
                "msg": "existing user",
                "code": status.HTTP_400_BAD_REQUEST,
                'timestanp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        except:
            userSuper = User.objects.get_or_create(username=username.split(" ")[0], password=password)
            tokenS = Token.objects.get_or_create(user=User.objects.get(username=username.split(" ")[0]))
            strSplit = username.split(" ")
            try:
                user = UserLogin.objects.get(name=strSplit[0])
            except:
                UserLogin.objects.create(
                    name=strSplit[0],
                    secondname=strSplit[1] + " " + strSplit[2],
                    password=password,
                    token=tokenS[0],
                    update_date=datetime.now()
                )
            user = UserLogin.objects.get(name=strSplit[0])
            content = {
                "msg": "User añadido",
                "token": str(user.token),
                'code': status.HTTP_200_OK,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def signOut(request):
    if request.method == 'PUT':
        username = request.data['username']
        password = request.data['password']
        try:
            user = UserLogin.objects.get(name=username.split(" ")[0], password=password)
            user.token = ""
            user.update_date = datetime.now()
            user.save()
            content = {
                'msg': 'User validated',
                'code': status.HTTP_200_OK,
                'timestanp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        except:
            content = {
                'msg': 'non-existent user',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestanp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def login(request):
    print(request.data)
    if request.method == 'GET':
        username = request.data['username']
        password = request.data['password']
        try:
            user = UserLogin.objects.get(name=username, password=password)
        except:
            content = {
                'msg': 'non-existent user',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestanp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        content = {
            "Token": user.token,
            "Code": status.HTTP_200_OK,
            'timestanp': datetime.now(),
            'version': '1.0'
        }
        return Response(content)
    elif request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        secondname = request.data['secondname']

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
                token="",
                update_date=datetime.now()
            )
            user = UserLogin.objects.get(name=username)
            user.token = str(token).split(':')[1].split(">")[0].split(" ")[1]
            user.save()
            content = {
                "msg": "User añadido",
                "token": str(user.token),
                'code': status.HTTP_201_CREATED,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
    elif request.method == 'DELETE':
        UserLogin.objects.all().delete()
        # Rent.objects.all().delete()
        content = {
            'msg': 'Deleted users',
            'code': status.HTTP_200_OK,
            'timestamp': datetime.now(),
            'version': '1.0'
        }
        return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def validate(request):
    if request.method == 'GET':
        username = request.data['username']
        token = request.data['token']

        print('Request:' + str(username) + '-' + str(token))
        try:
            user = UserLogin.objects.get(name=username)
            print(user.password)
            userT = User.objects.get(username=username)
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
            elif str(tokenUser[0]) == token:
                timeNow = datetime.now()
                print(timeNow)
                print(user.create_date)
                print(timeNow.date() - user.update_date.date())
                days = (timeNow.date() - user.update_date.date()).days
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
                    # user.token = ""
                    # user.save()
                    Token.objects.filter(user=userT).delete()
                    token = Token.objects.get_or_create(user=userT)
                    print(token)
                    user.token = str(token).split(':')[1].split(">")[0].split(" ")[1]
                    user.update_date = datetime.now()
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
                'msg': 'Invalid data',
                'code': status.HTTP_401_UNAUTHORIZED,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        try:
            rent = Rent.objects.get(uuid=scooter_uuid, vacant=False)
            if not rent.vacant:
                content = {
                    'code': status.HTTP_200_OK,
                    'msg': 'Scooter is already rented',
                    'rent': {
                        'uuid': rent.uuid,
                        'date_start': rent.update_date
                    },
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
        except:
            if scooter.vacant:
                Rent.objects.create(
                    uuid=scooter_uuid,
                    name=user.name,
                    token=token,
                    vacant=False,
                    update_date=datetime.now()
                )
                scooter.vacant = False
                scooter.save()
                rent = Rent.objects.get(uuid=scooter_uuid, vacant=False)
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
                'msg': 'Invalid token',
                'code': status.HTTP_401_UNAUTHORIZED,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        try:
            rent = Rent.objects.get(uuid=scooter_uuid, vacant=False)
            if not rent.vacant:
                rent.vacant = True
                rent.save()
                scooter.vacant = True
                scooter.update_date = datetime.now()
                scooter.save()
                content = {
                    'msg': 'End of rental',
                    'code': status.HTTP_200_OK,
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
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


@api_view(['GET'])
@permission_classes((AllowAny,))
def rentList(request):
    if request.method == 'GET':
        token = request.data['token']
        try:
            user = UserLogin.objects.get(token=token)
        except:
            content = {
                'msg': 'Invalid token',
                'code': status.HTTP_401_UNAUTHORIZED,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)

        content = {
            'msg': 'list of rent ',
            'code': status.HTTP_200_OK,
            'UserRents': Rent.objects.filter(token=token, vacant=True).values(),
            'timestamp': datetime.now(),
            'version': '1.0'
        }
        return Response(content)
    else:
        content = {
            'msg': 'Error',
            'code': status.HTTP_400_BAD_REQUEST,
            'timestamp': datetime.now,
            'version': '1.0'
        }
        return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def ScooterList(request):
    if request.method == 'GET':
        token = request.data['token']
        try:
            try:
                user = UserLogin.objects.get(token=token)
            except:
                content = {
                    'msg': 'Invalid token',
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
            content = {
                'msg': 'scooter list',
                'code': status.HTTP_200_OK,
                'ScooterList': Scooter.objects.all().values(),
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        except:
            content = {
                'msg': 'Error',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestamp': datetime.now,
                'version': '1.0'
            }
            return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def infoScooter(request, scooter_uuid):
    if request.method == 'GET':
        token = request.data['token']
        try:
            try:
                user = UserLogin.objects.get(token=token)
            except:
                content = {
                    'msg': 'Invalid token',
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'timestamp': datetime.now(),
                    'version': '1.0'
                }
                return Response(content)
            scooter = Scooter.objects.get(uuid=scooter_uuid)
            content = {
                'code': status.HTTP_200_OK,
                'msg': 'Info scooter',
                'scooter': {
                    'uuid': scooter.uuid,
                    'name': scooter.name,
                    'longitude': scooter.longitude,
                    'latitude': scooter.latitude,
                    'battery level': scooter.battry_level,
                    'on_mantinace': scooter.on_maintenance,
                    'last_mantinance': scooter.last_maintenace,
                    'vacant': scooter.vacant,
                    'create_date': scooter.create_date
                },
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)
        except:
            content = {
                'msg': 'Scooter does not exists',
                'code': status.HTTP_400_BAD_REQUEST,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))
def serverStatus(request):
    try:
        content = {
            'msg': 'Server status',
            'code': status.HTTP_200_OK,
            'Django version': django.VERSION,
            'timestamp': datetime.now(),
            'version': '1.0'
        }
        return Response(content)
    except:
        content = {
            'msg': 'Server status failed',
            'code': status.HTTP_400_BAD_REQUEST,
            'timestamp': datetime.now(),
            'version': '1.0'
        }
        return Response(content)
