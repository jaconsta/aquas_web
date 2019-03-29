import atexit
import json

from paho.mqtt import client as mqtt_client
from devices.workers.django_setup import django_setup
if __name__ == '__main__':
    django_setup()

from aquas_web.settings.default_variables import mqtt_heartbeat_topic, mqtt_host
from devices.services.process_heartbeat import process_heartbeats
from devices.services.logger import get_console_logger

logger = get_console_logger(__name__)


def mqtt_on_connect(client, userdata, flags, rc):
    # rc code expected => 0
    logger.info("Connected with result code " + str(rc))
    client.subscribe(topic=mqtt_heartbeat_topic)
    logger.info('Subscribed to {0}'.format(mqtt_heartbeat_topic))


def mqtt_on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    logger.info('------------------')
    logger.info('Message: topic {0} | qos {1}'.format(message.topic, message.qos))

    # Decode message
    body = json.loads(payload)  # I need to identify the possible exceptions.
    process_heartbeats(body)


def listen_heartbeats():
    # Client id must be unique.
    client = mqtt_client.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    client.connect(mqtt_host)

    atexit.register(client.loop_stop)
    try:
        client.loop_forever()
    finally:
        logger.info('Process exiting.')
        client.loop_stop()


if __name__ == '__main__':
    try:
        listen_heartbeats()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('Shutdown')


