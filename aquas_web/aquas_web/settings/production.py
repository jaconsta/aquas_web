from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aquas_db',
        'USER': 'django_aquas',
        'PASSWORD': 'mypassword',
        'HOST': 'db',
        'PORT': '3306',
    }
}
