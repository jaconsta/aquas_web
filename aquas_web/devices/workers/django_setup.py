import os
import django


def django_setup():
    module = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aquas_web.settings.development".format(module))
    django.setup()
