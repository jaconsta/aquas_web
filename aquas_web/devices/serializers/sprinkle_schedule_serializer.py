from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import SprinkleSchedule


class SprinkleScheduleSerializer(ModelSerializer):
    monday = serializers.BooleanField(source='on_monday')
    tuesday = serializers.BooleanField(source='on_tuesday')
    wednesday = serializers.BooleanField(source='on_wednesday')
    thursday = serializers.BooleanField(source='on_thursday')
    friday = serializers.BooleanField(source='on_friday')
    saturday = serializers.BooleanField(source='on_saturday')
    sunday = serializers.BooleanField(source='on_sunday')

    class Meta:
        model = SprinkleSchedule
        fields = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday', 'minute', 'hour', 'am_pm', 'device')
