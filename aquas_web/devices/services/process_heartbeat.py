from devices.models.device import Device
from devices.models.sprinkle_schedule import SprinkleSchedule
from devices.models.device_heartbeat import DeviceHeartbeat

from devices.services.logger import get_console_logger
logger = get_console_logger(__name__)


def process_heartbeats(mqtt_body):
    device_code = mqtt_body['device']
    device = Device.objects.get(unique_id=device_code)

    beat_options = [
        DeviceHeartbeat.HEARTBEAT,
        DeviceHeartbeat.DEVICE_ON,
    ]

    connection_status = mqtt_body.get('type')
    if connection_status not in beat_options:
        logger.error('Invalid heartbeat option.')
        return
    logger.info('Heartbeat type={} received for device {}'.format(connection_status, device.id))

    heartbeat_code = mqtt_body.get('code')
    heartbeat = DeviceHeartbeat(device=device, connection_status=connection_status, heartbeat_code=heartbeat_code)
    heartbeat.save()

    if connection_status == DeviceHeartbeat.SPRINKLE_OK:
        sprinkle = SprinkleSchedule.objects.get(device=device)
        sprinkle.next_schedule = sprinkle.when_should_sprinkle_next()
        sprinkle.save()
