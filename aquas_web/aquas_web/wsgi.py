"""
WSGI config for aquas_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get('ENVIRONMENT', 'development')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aquas_web.settings.{}".format(environment))

application = get_wsgi_application()
