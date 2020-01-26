from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action

from devices.services.sprinkle import water_now
from devices.models import Device, SprinkleSchedule
from devices.serializers import SprinkleScheduleSerializer


class ScheduleViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Scheduled Sprinkles of a device.
    <b>Note</b>: This endpoint is particularly non-RESTfull specific.
    """
    queryset = SprinkleSchedule.objects.all()
    serializer_class = SprinkleScheduleSerializer

    def create(self, request, *args, **kwargs):
        """
        Set the sprinkle schedule for one device
        <br />
        This is an <i>upsert</i> operation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SprinkleSchedule.objects.update_or_create(device=serializer.validated_data['device'], defaults=serializer.validated_data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, device_pk=None, *args, **kwargs):
        """
        Get the current scheduled sprinkle configuration.
        <br />
        If the device does not have any configuration yet, you will receive a <b>404</b>.
        <br />
        This is a <i>detail view</i>; instead of a list / array you will receive a single object.
        """
        try:
            schedule = SprinkleSchedule.objects.get(device=device_pk)
        except:
            return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        schedule_serialized = self.get_serializer(schedule)
        return JsonResponse(schedule_serialized.data)

    @action(detail=False, methods=['post'])
    def now(self, request, device_pk=None):
        """
        Request my device to start de default sprinkle inmediately.
        """
        try:
            device = Device.objects.get(pk=device_pk)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            water_now(device)
        except Exception:
            # MQTT exception
            return JsonResponse({'error': 'Could not send the message'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'status': 'Message sent'})
