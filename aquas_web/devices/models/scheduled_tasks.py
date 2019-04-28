from django.db import models


class ScheduledTasks(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='scheduled_device_code')
    task_type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    resolved = models.BooleanField(default=False)

    # Track of event sent and response time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_resolved(self):
        self.resolved = True
        self.save()

