from django.db import transaction

from ..models import ScheduledTasks, Device


def save_scheduled_tasks(tasks):
    with transaction.atomic():
        for task in tasks:
            device = Device.objects.get(pk=task['device'])
            scheduled = ScheduledTasks(device=device, code=task['code'], task_type='sprinkle')
            scheduled.save()
