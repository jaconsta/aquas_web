from django.db import models

from .device import Device


class DeviceHeartbeat(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    connection_time = models.DateTimeField(auto_now_add=True)

    SPRINKLE_OK = 'sprinkle'  # Last sprinkle activity was ok
    SPRINKLE_ERROR = 'error'  # Error during last sprinkle activity
    HEARTBEAT = 'heartbeat'   # Device heartbeat
    connection_status_choices = (
        (SPRINKLE_OK, 'sprinkle_ok'),
        (SPRINKLE_ERROR, 'sprinkle_error'),
        (HEARTBEAT, 'ping')
    )

    heartbeat_code = models.CharField(max_length=20, blank=True, null=True)
    # Could be named like beat_type
    connection_status = models.CharField(max_length=15, choices=connection_status_choices, default=HEARTBEAT)
