from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from devices.views.api.device import DeviceViewSet
from devices.views.api.schedule import ScheduleViewSet
from devices.views.api.heartbeat import DeviceHeartbeatViewSet


def register_device_urls(router):
    """
    Add the user managed / related device endpoints
    """
    devices_path = r'devices'

    router.register(devices_path, DeviceViewSet)

    # If it works, delete this
    router.register(r'devices_heartbeat', DeviceHeartbeatViewSet)

    devices_router = routers.NestedSimpleRouter(router, devices_path, lookup='device')
    devices_router.register(r'heartbeats', DeviceHeartbeatViewSet, base_name='device-heartbeat')
    devices_router.register(r'sprinkles', ScheduleViewSet, base_name='device-sprinkle')

    return [
        url(r'^api/', include(devices_router.urls))
    ]
