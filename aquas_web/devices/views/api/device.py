from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.decorators import action


from devices.serializers import DeviceSerializer
from devices.models import Device


def get_device(request, device_id):
    device = Device.get_by_id(device_id)
    device_json = serialize('json', [device], cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ListDevices(ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=False, methods=['get'])
    def device_count(self, request, pk=None):
        return JsonResponse({'total_devices': self.queryset.count()})
