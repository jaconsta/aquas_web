from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import FormView

from .models import Device, SprinkleSchedule


def get_device_by_id(device_id):
    return Device.objects.get(device_id)


def get_device(request, device_id):
    device = get_device_by_id(device_id)
    device_json = serialize('json', device, cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


def create_device(request):
    user = request.user
    print(user)
    print(request.POST)
    device_name = request.POST['deviceName']
    device = Device.createDevice(user, device_name)
    print(device)
    device_json = serialize('json', Device.objects.filter(pk=device.id), cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


def device_schedule_get(request, device):
    schedule = SprinkleSchedule.objects.get(device=device)
    device_json = serialize('json', schedule, cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


def device_schedule_post(request, device):
    def get(val, default=None):
        return request['POST'].get(val, default)
    minute = get('minute')
    hour = get('hour')
    am_pm = get('am_pm')

    on_monday = request['POST'].get('mon')
    on_tuesday = request['POST'].get('tue')
    on_wednesday = request['POST'].get('wed')
    on_thursday = request['POST'].get('thu')
    on_friday = request['POST'].get('fri')
    on_saturday = request['POST'].get('sat')
    on_sunday = request['POST'].get('sun')

    defaults = {
        'minute': minute,
        'hour': hour,
        'am_pm': am_pm,
        'on_monday': on_monday,
        'on_tuesday': on_tuesday,
        'on_wednesday': on_wednesday,
        'on_thursday': on_thursday,
        'on_friday': on_friday,
        'on_saturday': on_saturday,
        'on_sunday': on_sunday
    }
    SprinkleSchedule.objects.update_or_create(device=device, defaults=defaults)


def device_schedule(request, device_id):
    device = get_device_by_id(device_id)
    # Missing catch Device.DoesNotExist
    if request.method == 'POST':
        device_schedule_post(request, device)
    return device_schedule_get(request, device)


def devices_index_get(request):
    devices = Device.objects.filter(owner=request.user)
    context = {'devices': devices}
    return render(request, 'templates/dashboard/devices.html', context)


def devices_index(request):
    if request.method == 'POST':
        return create_device(request)
    return devices_index_get(request)


class DevicesIndex(FormView):
    login_url = '/users/login'
    template_name = 'templates/dashboard/devices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.email)
        context['user'] = self.request.user
        return context
