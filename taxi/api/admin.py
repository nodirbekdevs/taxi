from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Location)
