from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from devices.serializers import DeviceSerializer
from devices.models import Device


class DeviceViewSet(ModelViewSet):
    """
    General information regarding to the user devices.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not request.data.get('name'):
            return JsonResponse({'detail': 'Missing name'}, status=status.HTTP_400_BAD_REQUEST)
        Device.createDevice(request.user, request.data.get('name'))
        return JsonResponse({'status': 'device created'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def count(self, request):
        """
        Get the count of all the user owned devices.
        <br />
        This one is an effort to overWrite ListDevices
        <br />
        <b>Response structure</b><br />
        { total_devices: <i>&lt;integer&gt;</i> }
        """
        return JsonResponse({'total_devices': self.get_queryset().count()})


# class ListDevices(ReadOnlyModelViewSet):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer
#
#     def get_queryset(self):
#         return Device.objects.filter(owner=self.request.user)
#
#     @action(detail=False, methods=['get'])
#     def device_count(self, request, pk=None):
#         return JsonResponse({'total_devices': self.get_queryset().count()})
