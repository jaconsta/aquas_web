import json

from paho.mqtt import publish as mqtt_publish

from aquas_web.settings.default_variables import mqtt_host, mqtt_port


def water_now(device):
    message = json.dumps({
        "device": device.unique_id,
        "actions": [
            {
                "actuator": "sprinkle",
                "action": "now"
            }
        ]})

    mqtt_publish.single(
        topic=f'/pomelo/water/{device.unique_id}',
        payload=message,
        hostname=mqtt_host,
        port=mqtt_port,
        client_id='foo3'
    )

