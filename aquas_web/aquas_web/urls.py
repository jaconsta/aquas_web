"""aquas_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from aquas_web.swagger import schema_view

from users.views import UserAuthViewSet
from devices.views.api.device import DeviceViewSet, ListDevices
from devices.views.api.schedule import ScheduleViewSet
from devices.views.api.heartbeat import DeviceHeartbeatViewSet

router = routers.DefaultRouter()
router.register(r'auth', UserAuthViewSet, base_name='auth')
router.register(r'devices', DeviceViewSet)
router.register(r'devices_heartbeat', DeviceHeartbeatViewSet)
router.register(r'my_devices', ListDevices)
router.register(r'devices_sprinkle', ScheduleViewSet)

urlpatterns = [
    # API
    url(r'^api/', include(router.urls)),
    # Swagger / OpenAPI docs
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
