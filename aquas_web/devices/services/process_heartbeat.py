from devices.models.device import Device
from devices.models.device_heartbeat import DeviceHeartbeat


def process_heartbeats(mqtt_body):
    device_code = mqtt_body['device']
    device = Device.objects.get(unique_id=device_code)

    beat_options = [
        DeviceHeartbeat.SPRINKLE_OK,
        DeviceHeartbeat.SPRINKLE_ERROR,
        DeviceHeartbeat.HEARTBEAT
    ]

    connection_status = mqtt_body.get('type')
    if connection_status not in beat_options:
        print('Invalid heartbeat option.')
        return
    print('Heartbeat type={} received for device {}'.format(connection_status, device.id))

    heartbeat_code = mqtt_body.get('code')
    heartbeat = DeviceHeartbeat(device=device, connection_status=connection_status, heartbeat_code=heartbeat_code)
    heartbeat.save()

