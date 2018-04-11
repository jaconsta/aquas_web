from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import FormView

from .models import Device


def create_device(request):
    user = request.user
    print(user)
    print(request.POST)
    device_name = request.POST['deviceName']
    device = Device.createDevice(user, device_name)
    print(device)
    device_json = serialize('json', Device.objects.filter(pk=device.id), cls=DjangoJSONEncoder)
    return JsonResponse(device_json, safe=False)


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
