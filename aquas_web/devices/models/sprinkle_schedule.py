from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SprinkleSchedule(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='sprinkle_scheduled')

    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    AM = 'am'
    PM = 'pm'
    am_pm_choices = (
        (AM, AM),
        (PM, PM)
    )
    am_pm = models.CharField(max_length=5, choices=am_pm_choices, default=AM)

    on_monday = models.BooleanField(default=False)
    on_tuesday = models.BooleanField(default=False)
    on_wednesday = models.BooleanField(default=False)
    on_thursday = models.BooleanField(default=False)
    on_friday = models.BooleanField(default=False)
    on_saturday = models.BooleanField(default=False)
    on_sunday = models.BooleanField(default=False)

    def __str__(self):
        return "#{id}. Device: {device_id}/{device_uuid}".format(
            id=self.id,
            device_id=self.device.id,
            device_uuid=self.device.unique_id
        )
