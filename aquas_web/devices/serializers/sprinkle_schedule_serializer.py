from rest_framework.serializers import ModelSerializer

from ..models import SprinkleSchedule


class SprinkleScheduleSerializer(ModelSerializer):
    class Meta:
        model = SprinkleSchedule
        fields = '__all__'
