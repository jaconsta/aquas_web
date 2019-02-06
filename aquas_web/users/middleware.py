from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject
from django.http import JsonResponse
import jwt
from rest_framework import status

from aquas_web.settings.default_variables import jwt_key


def bearer_token_authentication(get_response):
    unprotected_paths = [
        '/',
        '/swagger/',
        '/api/auth'
    ]

    def path_start(path, limit=3):
        return '/'.join(path.split('?')[0].split('/')[:limit])

    def is_protected_source(request):
        return path_start(request.path) not in unprotected_paths

    def middleware(request):
        if not is_protected_source(request):
            return get_response(request)

        if 'HTTP_AUTHORIZATION' not in request.META:
            return JsonResponse(
                {"error": 'Missing Authorization header'}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            bearer_token = request.META.get('HTTP_AUTHORIZATION')[7:]
        except jwt.DecodeError:
            return JsonResponse(
                {"error": 'Invalid Access Token'}, status=status.HTTP_401_UNAUTHORIZED
            )
        email = jwt.decode(bearer_token, key=jwt_key).get('email')
        request.user = SimpleLazyObject(lambda: User.objects.get(email=email))

        return get_response(request)

    return middleware
