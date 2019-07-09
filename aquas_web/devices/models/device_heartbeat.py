from django.db import models

from .device import Device
from django.utils import timezone


class DeviceHeartbeat(models.Model):
    """
    It stores the events sent and received from the devices.

    Events detected now.
    - Heartbeat. Device is alive
    - Sprinkle. A sprinkle job sent and executed.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    connection_time = models.DateTimeField(auto_now_add=True)

    SPRINKLE_OK = 'sprinkle'  # Last sprinkle activity was ok
    SPRINKLE_NOW = 'now'  # Last water_now activity was ok
    SPRINKLE_ERROR = 'error'  # Error during last sprinkle activity
    HEARTBEAT = 'heartbeat'   # Device heartbeat
    DEVICE_ON = 'device_on'   # Device turned on
    connection_status_choices = (
        (SPRINKLE_OK, 'sprinkle_ok'),
        (SPRINKLE_ERROR, 'sprinkle_error'),
        (HEARTBEAT, 'ping'),
        (SPRINKLE_NOW, 'water_now'),
        (DEVICE_ON, 'device_on')
    )

    heartbeat_code = models.CharField(max_length=20, blank=True, null=True)
    resolved = models.BooleanField(default=False)
    # Could be named like beat_type
    connection_status = models.CharField(max_length=15, choices=connection_status_choices, default=HEARTBEAT)

    def resolve_sprinkle(self):
        self.connection_time = timezone.now()
        self.resolve()

    def resolve(self):
        self.resolved = True
        self.save()
