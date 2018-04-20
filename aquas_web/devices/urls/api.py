from django.urls import path

from devices.views.api.device import get_device
from devices.views.api.schedule import device_schedule


urlpatterns = [
    path('<device_id>', get_device),
    path('<device_id>/schedule', device_schedule)
]
