from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SprinkleSchedule(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='sprinkle_scheduled')

    # Time is expected to be on Timezone GMT0
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

    next_schedule = models.DateTimeField(null=True)
    last_run = models.DateTimeField(null=True)

    def __str__(self):
        return "#{id}. Device: {device_id}/{device_uuid}".format(
            id=self.id,
            device_id=self.device.id,
            device_uuid=self.device.unique_id
        )

    def sorted_weekdays(self):
        return [
            self.on_monday, self.on_tuesday, self.on_wednesday,
            self.on_thursday, self.on_friday, self.on_saturday, self.on_sunday
        ]

    def get_schedule_days(self, today):
        week_days = self.sorted_weekdays()
        last_day = self.last_run.weekday() if self.last_run else today.weekday()
        try:
            next_day = week_days.index(True, last_day + 1)
        except ValueError:
            next_day = week_days.index(True) + 1
            last_day = 0
            return last_day, next_day

        if today.hour < self.hour:
            next_day -= 1
        return last_day, next_day

    def when_should_sprinkle_next(self):
        # There is not any scheduled day.
        week_days = self.sorted_weekdays()
        if True not in week_days:
            return None

        today = datetime.today()
        last_day, next_day = self.get_schedule_days(today)

        # Calculate next schedule time
        hour = self.hour + (12 if self.am_pm == self.PM else 0)  # 24 hr format
        week_days_delta = next_day - last_day
        days_delta = timedelta(days=week_days_delta)

        next_schedule = datetime(today.year, today.month, today.day, hour, self.minute) + days_delta
        return next_schedule

    def set_last_run(self, last_run: datetime = None) -> datetime:
        if not last_run:
            last_run = datetime.now()

        self.last_run = last_run
        self.save()

    def save(self, *args, **kwargs):
        self.next_schedule = self.when_should_sprinkle_next()
        super().save(*args, **kwargs)
