from rest_framework.viewsets import ModelViewSet

from devices.serializers import DeviceHeartbeatSerializer
from devices.models import DeviceHeartbeat


class DeviceHeartbeatViewSet(ModelViewSet):
    queryset = DeviceHeartbeat.objects.all()
    serializer_class = DeviceHeartbeatSerializer
