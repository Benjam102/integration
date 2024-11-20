from django.db import models

class Airport(models.Model):
    airport_name = models.CharField(max_length=255)
    airport_id = models.CharField(max_length=10)  # Correspond au champ "Id"
    iata_code = models.CharField(max_length=10)  # Correspond au champ "Airport_Id"
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.airport_name} ({self.iata_code})"
