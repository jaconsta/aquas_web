import os
# JWT

jwt_key = os.environ.get('JWT_KEY', '5296558680')
mqtt_host = os.environ.get('MQTT_HOST', 'localhost')
mqtt_port = int(os.environ.get('MQTT_PORT', 1883))
mqtt_sprinkle_topic = os.environ.get('MQTT_SPRINKLE_TOPIC', '/pomelo/water/{}')
mqtt_server_wildcard = os.environ.get('MQTT_SERVER_WILDCARD', '/pomelo/server/#')
mqtt_heartbeat_topic = os.environ.get('MQTT_HEARTBEAT_TOPIC', '/pomelo/server/heartbeat')
mqtt_sprinkle_response_topic = os.environ.get('MQTT_SPRINKRESP_TOPIC', '/pomelo/server/sprinkle/response')
