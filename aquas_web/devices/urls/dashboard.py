from django.urls import path

from devices.views.dashboard.device import index


urlpatterns = [
    path('', index)
]
