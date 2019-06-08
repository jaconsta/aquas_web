import json

from paho.mqtt import publish as mqtt_publish
from paho.mqtt import client as mqtt_client

from aquas_web.settings.default_variables import mqtt_host, mqtt_port, mqtt_sprinkle_topic
from devices.services.logger import get_console_logger
from devices.utils import id_generator

logger = get_console_logger(__name__)


def water_now(device):
    message = json.dumps({
        "device": device.unique_id,
        "actions": [
            {
                "actuator": "sprinkle",
                "action": "now"
            }
        ]})

    try:
        mqtt_publish.single(
            topic='/pomelo/water/{}'.format(device.unique_id),
            payload=message,
            hostname=mqtt_host,
            port=mqtt_port,
            client_id='foo3'
        )
    except ConnectionRefusedError as e:
        logger.error('Could not connect to the MQTT server')
        raise Exception('mqtt_connection')


def scheduled_sprinkle(scheduled):
    client = mqtt_client.Client()
    client.connect(mqtt_host, mqtt_port)
    scheduled_sent = []
    for schedule in scheduled:
        device = schedule.device
        unique_code = id_generator()
        message = json.dumps({
            "device": device.unique_id,
            "actions": [
                {
                    "actuator": "sprinkle",
                    "action": "scheduled",
                    "code": unique_code
                }
            ]})

        try:
            client.publish(mqtt_sprinkle_topic.format(device.unique_id), message).wait_for_publish()
            scheduled_sent.append({"device": device.id, "code": unique_code})
        except ValueError:
            logger.error('Could not send message to ${}.'.format(device.unique_id))
    client.disconnect()
    return scheduled_sent
