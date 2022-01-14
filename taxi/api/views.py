from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None and password is None:
        return Response({'error': 'Please provide username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'},
                        status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'id':user.id, 'token':token.key},
                    status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def register(request):

    is_client = request.data.get("is_client")
    username = request.data.get("username")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    password = request.data.get("password")
    client = request.data.get("client")

    if username is None and password is None and first_name is None and last_name is None and is_client is None:
        return Response({'error': 'Please provide email, name, user type and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = UserClientRegSerializer(data=request.data)
    client_details = request.data.pop('client')
    gender = client_details['gender']
    date_of_birth = client_details['date_of_birth']
    address = client_details['address']
    phone_number = client_details['phone_number']

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(id=serializer.data['id'])
        group = Group.objects.get(name='Client')
        user.groups.add(group)
        Client.objects.create(user=user, gender=gender, date_of_birth=date_of_birth, address=address,
                              phone_number=phone_number)
        return Response([serializer.data, serializer.errors], status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def update(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DriverSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Driver.objects.all()
        driver = get_object_or_404(queryset, pk=pk)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def update(self, request, pk=None):
        driver = Driver.objects.get(pk=pk)
        serializer = DriverSerializer(driver, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        driver = Driver.objects.get(pk=pk)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(instance=user)
        if user == request.user:
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class OrderViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response([serializer.data, serializer.errors], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        orders = get_object_or_404(queryset, pk=pk)
        serializer = OrderUserSerializer(orders)
        return Response(serializer.data)

    def update(self, request, pk=None):
        orders = Order.objects.get(pk=pk)
        serializer = OrderSerializer(orders, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        orders = Order.objects.get(pk=pk)
        orders.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationViewSet(viewsets.ViewSet):
    def list(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response({'locations':serializer.data})

    def retrieve(self, request, pk=None):
        queryset = Location.objects.all()
        locations = get_object_or_404(queryset, pk=pk)
        serializer = LocationSerializer(locations)
        return Response({'location':serializer.data})


class VehicleViewSet(viewsets.ViewSet):
    def list(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response({'vehicle':serializer.data})

    def retrieve(self, request, pk=None):
        queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        serializer = LocationSerializer(vehicle)
        return Response({'vehicle':serializer.data})


class ClientRegViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        user_validator(serializer)


class DriverRegViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = DriverSerializer(data=request.data)
        user_validator(serializer)


def user_validator(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Fields not found'}, status=status.HTTP_400_BAD_REQUEST)
