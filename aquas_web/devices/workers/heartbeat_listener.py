import atexit
import datetime
import os
import sqlite3
import json

from paho.mqtt import client as mqtt_client

from aquas_web.aquas_web.settings.default_variables import mqtt_heartbeat_topic, mqtt_host


def process_heartbeat(mqtt_body):
    heartbeat_table = 'devices_deviceheartbeat'
    device_table = 'devices_device'
    sqlite_route = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../aquasDb.sqlite3'))

    sqlite_connection = sqlite3.connect(sqlite_route)

    cursor = sqlite_connection.cursor()

    device_code = mqtt_body['device']
    device_query_args = (device_code,)
    device_query = 'SELECT id FROM {table} WHERE unique_id=?'.format(table=device_table)
    cursor.execute(device_query, device_query_args)

    device = cursor.fetchone()
    if not device:
        print('Heartbeat listener: device_code={} not found'.format(device_code))
        return

    SPRINKLE_OK = 'sprinkle'  # Last sprinkle activity was ok
    SPRINKLE_ERROR = 'error'  # Error during last sprinkle activity
    HEARTBEAT = 'heartbeat'  # Device heartbeat
    beat_options = [SPRINKLE_OK, SPRINKLE_ERROR, HEARTBEAT]

    device_id = device[0]
    connection_status = mqtt_body.get('type')
    if connection_status not in beat_options:
        print('Invalid heartbeat option.')
        return
    print('Heartbeat type={} received for device {}'.format(connection_status, device_id))

    # Best sqlite format yyyy-MM-dd HH:mm:ss or '%Y-%m-%d %H:%M:%S'
    connection_time = datetime.datetime.now().isoformat()   # Should come from device
    heartbeat_code = mqtt_body.get('code')

    heartbeat_data = (device_id, connection_time, heartbeat_code, connection_status)
    table_fields = 'device_id,connection_time,heartbeat_code,connection_status'
    heartbeat_insert_query = 'INSERT INTO {table}({fields}) VALUES (?,?,?,?)'.format(table=heartbeat_table, fields=table_fields)
    cursor.execute(heartbeat_insert_query, heartbeat_data)

    sqlite_connection.commit()

    cursor.close()

# from django.conf import settings
# from aquas_web.aquas_web.settings import development
# def django_setup():
#     module = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
#
#     import django
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aquas_web.aquas_web.settings.development".format(module))
#     django.setup()


def mqtt_on_connect(client, userdata, flags, rc):
    # rc code expected => 0
    print("Connected with result code " + str(rc))
    client.subscribe(topic=mqtt_heartbeat_topic)
    print('Subscribed to {0}'.format(mqtt_heartbeat_topic))


def mqtt_on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print('------------------')
    print('Message: topic {0} | qos {1}'.format(message.topic, message.qos))

    # Decode message
    body = json.loads(payload)  # I need to identify the possible exceptions.
    process_heartbeat(body)


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
        print('Process exiting.')
        client.loop_stop()


if __name__ == '__main__':
    try:
        listen_heartbeats()
    except KeyboardInterrupt:
        pass
    finally:
        print('Shutdown')


