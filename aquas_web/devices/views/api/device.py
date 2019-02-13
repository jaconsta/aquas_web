from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from devices.serializers import DeviceSerializer
from devices.models import Device


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def create(self, request):
        if not request.data.get('name'):
            return JsonResponse({'detail': 'Missing name'}, status=status.HTTP_400_BAD_REQUEST)
        device = Device.createDevice(request.user, request.data.get('name'))
        return JsonResponse({'status': 'device created'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def device_count(self, request):
        """ This one is an effort to overWrite ListDevices """
        return JsonResponse({'total_devices': self.get_queryset().count()})


class ListDevices(ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def device_count(self, request, pk=None):
        return JsonResponse({'total_devices': self.get_queryset().count()})
