from rest_framework.serializers import ModelSerializer

from ..models import DeviceHeartbeat


class DeviceHeartbeatSerializer(ModelSerializer):
    class Meta:
        model = DeviceHeartbeat
        fields = '__all__'
