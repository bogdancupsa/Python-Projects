from django.db import models

# Create your models here.

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    max_hourly_energy_consumption = models.FloatField()

    def __str__(self):
        return self.description
