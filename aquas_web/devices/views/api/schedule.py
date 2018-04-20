from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from devices.models import Device, SprinkleSchedule


def get(request, device):
    schedule = SprinkleSchedule.objects.get(device=device)
    device_json = serialize('json', [schedule], cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


def post(request, device):
    def get(val, default=None):
        return request.POST.get(val, default)
    minute = get('minute')
    hour = get('hour')
    am_pm = get('AM_PM')

    active = 'on'

    on_monday = request.POST.get('on_monday')
    on_tuesday = request.POST.get('on_tuesday')
    on_wednesday = request.POST.get('on_wednesday')
    on_thursday = request.POST.get('on_thursday')
    on_friday = request.POST.get('on_friday')
    on_saturday = request.POST.get('on_saturday')
    on_sunday = request.POST.get('on_sunday')

    defaults = {
        'minute': minute,
        'hour': hour,
        'am_pm': am_pm,
        'on_monday': on_monday == active,
        'on_tuesday': on_tuesday == active,
        'on_wednesday': on_wednesday == active,
        'on_thursday': on_thursday == active,
        'on_friday': on_friday == active,
        'on_saturday': on_saturday == active,
        'on_sunday': on_sunday == active
    }
    SprinkleSchedule.objects.update_or_create(device=device, defaults=defaults)


def device_schedule(request, device_id):
    device = Device.get_by_id(device_id)
    # Missing catch Device.DoesNotExist
    if request.method == 'POST':
        post(request, device)
    return get(request, device)
