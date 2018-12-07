from django.contrib.auth.models import User
from django.http import JsonResponse
import jwt
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from aquas_web.settings.default_variables import jwt_key
from devices.serializers import DeviceSerializer
from devices.models import Device


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request):
        bearerToken = request.META.get('HTTP_AUTHORIZATION')[7:]
        email = jwt.decode(bearerToken, key=jwt_key).get('email')
        user = User.objects.get(email=email)
        device = Device.createDevice(user, request.data.get('name'))
        return JsonResponse({'status': 'device created'}, status='201')


class ListDevices(ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=False, methods=['get'])
    def device_count(self, request, pk=None):
        return JsonResponse({'total_devices': self.queryset.count()})
