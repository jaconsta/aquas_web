from rest_framework.serializers import ModelSerializer

from ..models import Device


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'status', 'unique_id')