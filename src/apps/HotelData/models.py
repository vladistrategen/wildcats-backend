from django.db import models
from apps.City.models import City

# Create your models here.

class HotelData(models.Model):
    hotel_name = models.CharField(max_length=100)
    hotel_address = models.CharField(max_length=100)
    hotel_city = models.ForeignKey(City, on_delete=models.CASCADE) 
    hotel_state = models.CharField(max_length=100)
    hotel_zipcode = models.CharField(max_length=100)
    hotel_phone = models.CharField(max_length=100)
    hotel_website = models.CharField(max_length=100)
    hotel_rating = models.CharField(max_length=100)
    hotel_price = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_currency = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.hotel_name