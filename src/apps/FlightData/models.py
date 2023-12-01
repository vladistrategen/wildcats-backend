from django.db import models
from apps.City.models import City

# Create your models here.

class FlightData(models.Model):
    airline = models.CharField(max_length=100)
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name="origin")
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name="destination")
    flight_number = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.airline