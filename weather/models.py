# Create your models here.
from django.db import models

# Create your models here.

class WeatherRecord(models.Model):
    date = models.DateField()
    hour = models.IntegerField(default=12)  # 0–23
    temperature = models.FloatField()
    cuaca = models.CharField(max_length=50) 
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.location}"
