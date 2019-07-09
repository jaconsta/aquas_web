from devices.models import SprinkleSchedule, DeviceHeartbeat, Device

from .logger import get_console_logger

logger = get_console_logger(__name__)


def sprinkle_now_action_finished(device_uuid):
    device = Device.objects.get(unique_id=device_uuid)
    task = DeviceHeartbeat(device=device, connection_status=DeviceHeartbeat.SPRINKLE_NOW)
    task.resolve_sprinkle()
    logger.info('Sprinkle now action - device: {device}'.format(device=device.unique_id))


def process_task_finished(device, code, action):
    if action == 'now':
        return sprinkle_now_action_finished(device)
    if action != 'scheduled':
        return

    scheduled = DeviceHeartbeat.objects.get(device__unique_id=device, heartbeat_code=code)
    sprinkle_schedule = SprinkleSchedule.objects.get(device=scheduled.device)
    sprinkle_schedule.set_last_run()
    scheduled.resolve_sprinkle()
    logger.info('New schedule - device: ${device} on ${next_schedule)'.format(device=device, next_schedule=sprinkle_schedule.next_schedule))
