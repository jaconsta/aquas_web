import json
import time

from paho.mqtt import publish, client as mqtt_client

from aquas_web.settings.default_variables import mqtt_host, mqtt_port, mqtt_heartbeat_topic, mqtt_sprinkle_topic, mqtt_sprinkle_response_topic

from devices.services.logger import get_console_logger
logger = get_console_logger(__name__)


"""
docker run --name=local-mqt -dt -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
"""

DEVICE_UUID = 'TVSZSD'


def publish_heartbeat():
    message = {
        'device': DEVICE_UUID,
        'type': 'heartbeat',
    }
    payload = json.dumps(message)
    publish.single(
        topic=mqtt_heartbeat_topic,
        payload=payload,
        hostname=mqtt_host,
        port=mqtt_port
    )


def publish_sprinkled():
    message = {
        'device': DEVICE_UUID,
        'type': 'sprinkle',
        'code': 'Star Wars'
    }
    payload = json.dumps(message)
    publish.single(
        topic=mqtt_heartbeat_topic,
        payload=payload,
        hostname=mqtt_host,
        port=mqtt_port
    )


def receive_sprinkle_schedule():
    def mqtt_on_connect(client, *args):
        client.subscribe(topic=mqtt_sprinkle_topic.format(DEVICE_UUID))
        print('subscribed to {}'.format(mqtt_sprinkle_topic.format(DEVICE_UUID)))
        
    def mqtt_on_message(client, userdata, message):
        payload = message.payload.decode('utf-8')
        body = json.loads(payload)
        time.sleep(3)
        actions = body['actions'][0]
        response_payload = {
            'device': body['device'],
            'code': actions.get('code'),
            'action': actions['action']
        }
        print('response')
        print(json.dumps(response_payload))
        publish.single(
            topic=mqtt_sprinkle_response_topic,
            payload=json.dumps(response_payload),
            hostname=mqtt_host,
            port=mqtt_port
        )

    client = mqtt_client.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    client.connect(mqtt_host, mqtt_port)

    try:
        client.loop_forever()
    finally:
        logger.info('Process exiting.')
        client.loop_stop()


if __name__ == '__main__':
    # publish_heartbeat()
    # publish_sprinkled()
    receive_sprinkle_schedule()

