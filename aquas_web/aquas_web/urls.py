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
from django.contrib import admin
from django.urls import path

from users import views as userViews
from dashboard import views as dashboardViews
from devices import views as deviceViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard', dashboardViews.IndexView.as_view()),
    path('dashboard/devices', deviceViews.devices_index),
    path('users/login', userViews.login),
    path('users/logout', userViews.logout),
    path('users/register', userViews.register),
    path('users/forgot_password', userViews.forgot_password)
]
