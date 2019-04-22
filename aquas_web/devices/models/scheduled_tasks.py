from django.db import models


class ScheduledTasks(models.Model):
    device_id = models.ForeignKey('Device')
    task_type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
