from rest_framework.serializers import Serializer
from rest_framework import serializers


class UserLoginSerializer(Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(max_length=200)
