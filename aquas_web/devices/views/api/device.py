from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from devices.serializers import DeviceSerializer
from devices.models import Device


def get_device(request, device_id):
    device = Device.get_by_id(device_id)
    device_json = serialize('json', [device], cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
