from django.db import models
from apps.City.models import City

# Create your models here.

class CostOfLivingData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    

    class Meta:
        unique_together = ('city', 'item', 'date')

    def __str__(self):
        return f"{self.item} in {self.city}"