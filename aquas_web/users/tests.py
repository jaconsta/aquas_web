from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserAuthenticationTests(APITestCase):
    def test_register_user(self):
        """
            Successfully registers an user
        """
        url = '/api/auth/register/'
        user_body = {
            'email': 'test@mail.com',
            'password': 'randomString'
        }

        response = self.client.post(url, user_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'register': 'OK'})
        user = User.objects.all()[0]
        self.assertEqual(user.username, user_body['email'])
        self.assertNotEqual(user.password, user_body['password'])

    def test_cannot_register_user(self):
        """
            User sends a wrong email
        """
        url = '/api/auth/register/'
        user_body = {
            'email': '',
            'password': 'randomString'
        }

        response = self.client.post(url, user_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['This field may not be blank.']})

    def test_cannot_register_twice(self):
        """
            User tries to register twice
        """
        url = '/api/auth/register/'
        user_body = {
            'email': 'test@mail.com',
            'password': 'randomString'
        }
        response = self.client.post(url, user_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        duplicate_response = self.client.post(url, user_body, format='json')

        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(duplicate_response.json(), {'error': 'email test@mail.com already exists'})

    def test_login_user(self):
        """
            Successfully login an user
        """
        url = '/api/auth/login/'
        user_body = {
            'email': 'test@mail.com',
            'password': 'randomString'
        }
        self.create_user(*user_body.values())

        response = self.client.post(url, user_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body['login'], 'OK')
        jwt_regex = r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$'
        self.assertRegex(body['token'], jwt_regex)

    def test_fail_mail_login_user(self):
        """
            Cant login an user
        """
        url = '/api/auth/login/'
        user_body = {
            'email': 'test@mail.com',
            'password': 'randomString'
        }
        self.create_user(*user_body.values())

        bad_credentials = {
            'email': 'tesat@mail.com',
            'password': 'randomString'
        }
        response = self.client.post(url, bad_credentials, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    def test_fail_password_login_user(self):
        """
            Cant login an user
        """
        url = '/api/auth/login/'
        user_body = {
            'email': 'test@mail.com',
            'password': 'randomString'
        }
        self.create_user(*user_body.values())

        bad_credentials = {
            'email': 'test@mail.com',
            'password': 'badPassword'
        }
        response = self.client.post(url, bad_credentials, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    @staticmethod
    def create_user(username, password):
        return User.objects.create_user(username, password=password)
