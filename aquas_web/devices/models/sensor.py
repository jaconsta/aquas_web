from django.db import models

from .device import Device


class Sensor(models.Model):
    """
        Defines what sensors are attached to the device.
        Currently is a basic characterization on the sensor type:
          * humidity, temperature, etc
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    SOIL_HUMIDITY = 'soil_humidity'
    TEMPERATUE = 'temperature'
    RADAR = 'radar'
    sensor_type_choices = (
        (SOIL_HUMIDITY, SOIL_HUMIDITY),
        (TEMPERATUE, TEMPERATUE),
        (RADAR, RADAR)
    )
    sensor_type = models.CharField(max_length=25, choices=sensor_type_choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
