from django.db import transaction

from ..models import ScheduledTasks


def save_scheduled_tasks(tasks):
    with transaction.atomic():
        for task in tasks:
            scheduled = ScheduledTasks(device_id=task['device'], code=task['code'], task_type='sprinkle')
            scheduled.save()
