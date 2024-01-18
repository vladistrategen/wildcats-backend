from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)  # ISO 3166-1 alpha-3 country code
    timezone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
