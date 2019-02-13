from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Device


class DeviceSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    unique_id = serializers.CharField(read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'name', 'status', 'unique_id')
