from django.db import transaction

from ..models import Device, DeviceHeartbeat


def save_scheduled_tasks(tasks):
    with transaction.atomic():
        for task in tasks:
            device = Device.objects.get(pk=task['device'])
            scheduled = DeviceHeartbeat(device=device, heartbeat_code=task['code'], task_type=DeviceHeartbeat.SPRINKLE_OK)
            scheduled.save()
