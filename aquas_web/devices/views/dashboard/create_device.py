from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from devices.models import Device


def create_device(request):
    user = request.user
    
    device_name = request.POST['deviceName']
    device = Device.createDevice(user, device_name)

    device_json = serialize('json', Device.objects.filter(pk=device.id), cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)
