from django.contrib.auth import authenticate
from django.http import JsonResponse
import jwt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from aquas_web.settings.default_variables import jwt_key
from .serializers import UserLoginSerializer


class UserAuthViewSet(GenericViewSet):
    serializer_class = UserLoginSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            return JsonResponse(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(**serialized_data.data)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'},
                                status=status.HTTP_400_BAD_REQUEST)
        user_token = jwt.encode({'email': user.email}, jwt_key, algorithm='HS256')
        return JsonResponse({'login': 'OK', 'token': user_token.decode('utf-8')})
