from django.contrib import admin

# Register your models here.

from .models import FlightData

admin.site.register(FlightData)