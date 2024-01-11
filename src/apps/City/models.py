from django.db import models
from apps.Country.models import Country

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    main_iata_code = models.CharField(max_length=3, default="")
    

    def __str__(self):
        return f"{self.name}, {self.country.name}"
