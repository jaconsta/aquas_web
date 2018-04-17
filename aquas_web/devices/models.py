from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from .utils import id_generator


class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=50, unique=True)

    # Friendly name
    name = models.CharField(max_length=150)

    ACTIVE = 'act'
    DISABLED = 'dis'
    status_choices = (
        (ACTIVE, 'active'),
        (DISABLED, 'disabled')
    )
    status = models.CharField(max_length=5, choices=status_choices, default=ACTIVE)

    register_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def createDevice(cls, user, name):
        unique_id = id_generator()
        print(unique_id)
        device = cls(owner=user, unique_id=unique_id, name=name)
        device.save()
        print('device')
        print(device.name)
        return device


class DeviceConnections(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    connection_time = models.DateTimeField(auto_now_add=True)

    SPRINKLE_OK = 'spr_ok'  # Last sprinkle activity was ok
    SPRINKLE_ERROR = 'spr_err'  # Error during last sprinkle activity
    PING = 'ping'   # Device heartbeat
    connection_status_choices = (
        (SPRINKLE_OK, 'sprinkle_ok'),
        (SPRINKLE_ERROR, 'sprinkle_error'),
        (PING, 'ping')
    )
    connection_status = models.CharField(max_length=15, choices=connection_status_choices, default=PING)


class SprinkleSchedule(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE)

    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    AM = 'am'
    PM = 'pm'
    am_pm_choices = (
        (AM, AM),
        (PM, PM)
    )
    am_pm = models.CharField(max_length=15, choices=am_pm_choices, default=AM)

    on_monday = models.BooleanField(default=False)
    on_tuesday = models.BooleanField(default=False)
    on_wednesday = models.BooleanField(default=False)
    on_thursday = models.BooleanField(default=False)
    on_friday = models.BooleanField(default=False)
    on_saturday = models.BooleanField(default=False)
    on_sunday = models.BooleanField(default=False)
    """
    FIFTEEN_DAYS = 'fifteen_days'
    WEEKLY = 'weekly'
    DAYLY = 'dayly'
    OTHER = 'other'
    sprinkle_frequency_choices = (
        (FIFTEEN_DAYS, 'fifteen_days'),
        (WEEKLY, 'weekly'),
        (DAYLY, 'dayly'),
        (OTHER, 'other')
    )
    sprinkle_frequency = models.CharField(max_length=15, choices=sprinkle_frequency_choices, default=DAYLY)
    """

    # time = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
