from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


def register_get(request):
    return render(request, 'templates/login/page-register.html')


def register_post(request):
    if (request.POST.get('agree_terms') != 'on'):
        print('Terms not accepted')
        return register_get(request)
    form_fields = ('first_name', 'last_name', 'email', 'password')
    user_fields = dict([(field, request.POST[field]) for field in form_fields])
    try:
        User.objects.create_user(user_fields['email'], **user_fields)
    except Exception:  # Detected ones: IntegrityError
        return register_get(request)
    return HttpResponseRedirect('/users/login')


def login_get(request):
    return render(request, 'templates/login/page-login.html')


def login_post(request):
    form_fields = ['username', 'password']
    user_fields = dict([(field, request.POST[field]) for field in form_fields])
    user = authenticate(**user_fields)
    print(user_fields)
    print(user)
    if user is not None:
        user_login(request, user)
        return HttpResponseRedirect('/dashboard')
    return login_get(request)


def forgot_password_get(request):
    return render(request, 'templates/login/pages-forget.html')


def forgot_password_post(request):
    return register_get(request)


def login(request):
    if request.method == 'POST':
        return login_post(request)
    return login_get(request)


def logout(request):
    user_logout(request)
    return login_get(request)


def register(request):
    if request.method == 'POST':
        return register_post(request)
    return register_get(request)


def forgot_password(request):
        if request.method == 'POST':
            return forgot_password_post(request)
        return forgot_password_get(request)
