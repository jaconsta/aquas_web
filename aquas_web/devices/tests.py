from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.utils.authentication import generate_user_token
from .models import Device


class CreateDevicesTests(APITestCase):
    def test_device_creation(self):
        """
            Simply create the device
        """
        user = User.objects.create_user('any_user', password='randomString')
        token = generate_user_token(user)
        url = '/api/devices/'
        create_body = {
            'name': 'A device'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.decode('utf-8')))
        response = client.post(url, create_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'status': 'device created'})
        device = Device.objects.all()[0]
        self.assertEqual(device.name, create_body['name'])
        self.assertNotEqual(device.unique_id, None)

    def test_cannot_create_device_with_no_name(self):
        """
            Cannot create a device without name
        """
        user = User.objects.create_user('any_user', password='randomString')
        token = generate_user_token(user)

        url = '/api/devices/'
        create_body = {
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.decode('utf-8')))

        response = client.post(url, create_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detail': 'Missing name'})


class TestScheduleDevice(APITestCase):
    def test_set_device_schedule(self):
        """
        Does a simply scheduling
        """
        user = User.objects.create_user('any_user', password='randomString')
        token = generate_user_token(user)
        device = Device(name='one_device', owner=user)
        device.save()

        # Need to make work devices/id/sprinkle
        url = '/api/devices_sprinkle/'.format(device.id)
        sprinkle_body = {
            'monday': True,
            'tuesday': True,
            'wednesday': True,
            'thursday': True,
            'friday': True,
            'saturday': True,
            'sunday': True,
            'am_pm': 'am',
            'minute': 30,
            'hour': 6,
            'device': device.id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.decode('utf-8')))

        response = client.post(url, sprinkle_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), sprinkle_body)

    def test_fails_any_missing_parameter(self):
        """
        Will not schedule if any parameter is missing
        """
        user = User.objects.create_user('any_user', password='randomString')
        token = generate_user_token(user)
        device = Device(name='one_device', owner=user)
        device.save()

        # Need to make work devices/id/sprinkle
        url = '/api/devices_sprinkle/'.format(device.id)
        sprinkle_body = {
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.decode('utf-8')))

        response = client.post(url, sprinkle_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_json = response.json()
        attributes = [
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
            'device',
            'hour',
            'minute'
        ]
        for attribute in attributes:
            self.assertEqual(response_json[attribute][0], 'This field is required.')
