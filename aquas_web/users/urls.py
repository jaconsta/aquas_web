from django.urls import include, path

from .views import login, logout, register, forgot_password


urlpatterns = [
    path('login', login),
    path('logout', logout),
    path('register', register),
    path('forgot_password', forgot_password)
]
