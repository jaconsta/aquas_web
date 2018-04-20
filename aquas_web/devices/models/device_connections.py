from django.db import models

from .device import Device

class DeviceConnections(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    connection_time = models.DateTimeField(auto_now_add=True)

    SPRINKLE_OK = 'spr_ok'  # Last sprinkle activity was ok
    SPRINKLE_ERROR = 'spr_err'  # Error during last sprinkle activity
    HEARTB = 'hb'   # Device heartbeat
    connection_status_choices = (
        (SPRINKLE_OK, 'sprinkle_ok'),
        (SPRINKLE_ERROR, 'sprinkle_error'),
        (HEARTB, 'ping')
    )
    connection_status = models.CharField(max_length=15, choices=connection_status_choices, default=HEARTB)
