from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .serializers import AuthSerializer


class UserAuthViewSet(GenericViewSet):
    serializer_class = AuthSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            return JsonResponse(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_token = serialized_data.authenticate()
        except Exception:
            return JsonResponse({'error': 'Invalid credentials'},
                                status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'login': 'OK', 'token': user_token.decode('utf-8')})

    @action(methods=['post'], detail=False)
    def register(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            return JsonResponse(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serialized_data.save()
        except Exception as e:
            return JsonResponse({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'register': 'OK'}, status=status.HTTP_201_CREATED)
