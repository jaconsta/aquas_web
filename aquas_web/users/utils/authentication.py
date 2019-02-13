from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject
from django.utils.translation import ugettext_lazy as _
import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from aquas_web.settings.default_variables import jwt_key


def generate_user_token(user):
    return jwt.encode({'email': user.email}, jwt_key, algorithm='HS256')


class BearerAuthentication(BaseAuthentication):
    unprotected_paths = [
        '/',
        '/swagger/',
        '/api/auth'
    ]

    def authenticate(self, request):

        if not self.is_protected_source(request):
            return None, None

        if 'HTTP_AUTHORIZATION' not in request.META:
            raise exceptions.AuthenticationFailed(_('Missing Authorization header'))

        try:
            bearer_token = request.META.get('HTTP_AUTHORIZATION')[7:]
        except jwt.DecodeError:
            return exceptions.AuthenticationFailed(
                _('Invalid Access Token')
            )
        email = jwt.decode(bearer_token, key=jwt_key).get('email')
        user = SimpleLazyObject(lambda: User.objects.get(email=email))

        return user, None

    def authenticate_header(self, request):
        return ''

    @staticmethod
    def path_start(path, limit=3):
        return '/'.join(path.split('?')[0].split('/')[:limit])

    def is_protected_source(self, request):
        return self.path_start(request.path) not in self.unprotected_paths
