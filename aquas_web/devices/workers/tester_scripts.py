import json

from paho.mqtt import publish

from aquas_web.aquas_web.settings.default_variables import mqtt_host, mqtt_port, mqtt_heartbeat_topic

"""
docker run --name=local-mqt -dt -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
"""


def publish_heartbeat():
    message = {
        'device': 'MBBSBG',
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
        'device': 'MBBSBG',
        'type': 'sprinkle',
        'code': 'Uniq_123'
    }
    payload = json.dumps(message)
    publish.single(
        topic=mqtt_heartbeat_topic,
        payload=payload,
        hostname=mqtt_host,
        port=mqtt_port
    )


if __name__ == '__main__':
    publish_heartbeat()
    publish_sprinkled()

