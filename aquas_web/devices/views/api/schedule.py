from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action

from devices.services.sprinkle import water_now
from devices.models import Device, SprinkleSchedule
from devices.serializers import SprinkleScheduleSerializer


class ScheduleViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = SprinkleSchedule.objects.all()
    serializer_class = SprinkleScheduleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SprinkleSchedule.objects.update_or_create(device=serializer.validated_data['device'], defaults=serializer.validated_data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            schedule = SprinkleSchedule.objects.get(device=pk)
        except:
            return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        schedule_serialized = self.get_serializer(schedule)
        return JsonResponse(schedule_serialized.data)

    @action(detail=True, methods=['post'])
    def now(self, request, pk=None):
        try:
            device = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            water_now(device)
        except Exception:
            # MQTT exception
            return JsonResponse({'error': 'Could not send the message'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'status': 'Message sent'})
