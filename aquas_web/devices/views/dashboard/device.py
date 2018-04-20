from django.shortcuts import render

from devices.models import Device
from .create_device import create_device


def get(request):
    devices = Device.objects.filter(owner=request.user)
    context = {'devices': devices}
    return render(request, 'templates/dashboard/devices.html', context)


def index(request):
    if request.method == 'POST':
        return create_device(request)
    return get(request)
