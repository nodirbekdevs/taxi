from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from . import signals

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['price', 'time', 'numPassengers', 'date_created', 'ride_type', 'start_location', 'end_location', 'client', 'driver', 'vehicle']


class ClientSerializer(serializers.ModelSerializer):
    ride_set = OrderSerializer(many=True)
    user = serializers.StringRelatedField()


    class Meta:
        model = Client
        fields = ['user', 'date_of_birth', 'gender', 'phone_number', 'address', 'ride_set']


class UserSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'client']


class DriverSerializer(serializers.ModelSerializer):
    vehicle = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Driver
        fields = '__all__'


class ClientRegSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = ['user', 'gender', 'date_of_birth', 'phone_number', 'address']


class OrderUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['price', 'time', 'numPassengers', 'date_created', 'ride_type', 'start_location', 'end_location', 'client', 'driver', 'vehicle']


class UserClientRegSerializer(serializers.ModelSerializer):
    client = ClientRegSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username',  'email', 'first_name', 'last_name', 'password', 'client']
        extra_kwargs = {"password": {'write_only': True}}

        def create(self, validated_data):
            validated_data.pop('client')
            user = User.objects.create_user(**validated_data)
            return user


class DriverRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        extra_kwargs = {"password": {'write_only': True}}

        def create(self, validated_data):
            # Creates and returns a new user

            user = Driver(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                is_client=validated_data['is_client']
            )
            user.save()