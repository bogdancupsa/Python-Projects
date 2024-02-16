from django.db import models

# Create your models here.

class Device(models.Model):
    device_id = models.IntegerField(unique=True)
    max_hourly_energy_consumption = models.FloatField()

class SensorData(models.Model):
    timestamp = models.DateTimeField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    measurement_value = models.FloatField()