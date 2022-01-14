from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    carMake = models.CharField(max_length=40, null=True)
    carModel = models.CharField(max_length=200, null=True)
    carCapacity = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.carMake} {self.carModel}'


class CustomUser(models.Model):
    date_of_birth = models.DateField(max_length=40, null=True)
    gender = models.CharField(max_length=1, null=True)
    phone_number = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)

    class Meta:
        abstract = True


class Client(CustomUser):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='client')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



class Driver(CustomUser):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    commission = models.FloatField(null=True)
    scheduled_rides = models.IntegerField(null=True)
    unscheduled_rides = models.IntegerField(null=True)
    documentation = models.FileField(upload_to='files', null=True)
    license_issue_date = models.DateField(null=True)
    license_expiry_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Location(models.Model):
    locationName = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.locationName


class Order(models.Model):
    STATUS = (
        ('CD', 'CREATED'),
        ('CD', 'CANCELLED'),
        ('AD', 'ACCEPTED'),
        ('FSH', 'FINISH'),
    )
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    start_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, related_name='start_location')
    end_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, related_name='end_location')
    price = models.FloatField(null=True)
    time = models.TimeField(null=True)
    numPassengers = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f'{self.start_location}-{self.end_location} {self.time}'


class UserManager(models.Manager):
    def create(self, username, gender):
        user = User(username=username, gender=gender)
        user.save()
        client = Client(user=user, gender=gender)
        client.save()
        return user
