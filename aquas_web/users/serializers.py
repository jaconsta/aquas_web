from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import jwt
from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.utils.authentication import generate_user_token
from aquas_web.settings.default_variables import jwt_key


class AuthSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    firstName = serializers.CharField(max_length=200, source='first_name', required=False)
    lastName = serializers.CharField(max_length=200, source='last_name', required=False)

    def create(self, validated_data):
        username = validated_data['email']
        try:
            return User.objects.create_user(username, **validated_data)
        except IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: auth_user.username':
                message = 'email {} already exists'.format(username)
            else:
                message = 'Could not create user {}'.format(username)
            raise ValueError(message)

    def authenticate(self):
        credentials = {
            'username': self.validated_data['email'],
            'password': self.validated_data['password']
        }
        user = authenticate(**credentials)
        if user is None:
            raise Exception('Invalid user')
        return generate_user_token(user)# jwt.encode({'email': user.email}, jwt_key, algorithm='HS256')

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

