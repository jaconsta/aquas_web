from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from devices.serializers import DeviceHeartbeatSerializer
from devices.models import DeviceHeartbeat


class DeviceHeartbeatViewSet(GenericViewSet):
    queryset = DeviceHeartbeat.objects.all()
    serializer_class = DeviceHeartbeatSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        beats_query = self.get_queryset().filter(device__owner=request.user).order_by('device', '-connection_time', 'connection_status')  # .distinct('connection_time', 'heartbeat_code'))
        # replacement of the distinct or first of each group
        beats = {}
        for beat in beats_query:
            key = '{}_{}'.format(beat.device.id, beat.connection_status)
            if key not in beats:
                beats[key] = beat
        beats_json = self.get_serializer(beats.values(), many=True)
        return JsonResponse(beats_json.data, safe=False)
