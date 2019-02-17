from datetime import datetime

from django.contrib.auth.models import User
from freezegun import freeze_time
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.utils.authentication import generate_user_token
from .models import Device, SprinkleSchedule
from .utils import id_generator


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


class TestUtils(APITestCase):
    def test_unique_device_code(self):
        first_code = id_generator()
        second_code = id_generator()

        self.assertNotEqual(first_code, second_code)

    def test_device_code_len(self):
        first_code = id_generator(100)
        second_code = id_generator(1)

        self.assertEqual(len(first_code), 100)
        self.assertEqual(len(second_code), 1)


class TestSprinkleScheduleOperations(APITestCase):

    @freeze_time("2018-01-01")  # Monday, ex with timezone: , tz_offset=-4)
    def test_initial_schedule(self):
        user = User.objects.create_user('any_user', password='randomString')
        device = Device(name='one_device', owner=user)
        schedule_parameters = {
            'device': device,
            'hour': 10,
            'minute': 12,
            'am_pm': 'am',
            'on_monday': True,
            'on_tuesday': True,
            'on_wednesday': True,
            'on_thursday': True,
            'on_friday': True,
            'on_saturday': True,
            'on_sunday': True,
        }
        hello = SprinkleSchedule(**schedule_parameters)
        next_schedule = hello.when_should_sprinkle_next()
        expected_schedule = datetime(2018, 1, 1, 10, 12, 0)
        # Though it should be the same day hours later datetime(2018, 1, 2, 10, 12, 0)
        self.assertEqual(next_schedule, expected_schedule)

    def test_no_weekday_scheduled(self):
        user = User.objects.create_user('any_user', password='randomString')
        device = Device(name='one_device', owner=user)
        schedule_parameters = {
            'device': device,
            'hour': 10,
            'minute': 12,
            'am_pm': 'am',
            'on_monday': False,
            'on_tuesday': False,
            'on_wednesday': False,
            'on_thursday': False,
            'on_friday': False,
            'on_saturday': False,
            'on_sunday': False,
        }
        new_schedule = SprinkleSchedule(**schedule_parameters)
        next_schedule = new_schedule.when_should_sprinkle_next()

        self.assertIsNone(next_schedule)

    @freeze_time("2019-02-03 12:00:01")
    def test_initial_scheduled_on_sunday(self):
        user = User.objects.create_user('any_user', password='randomString')
        device = Device(name='one_device', owner=user)
        schedule_parameters = {
            'device': device,
            'hour': 10,
            'minute': 12,
            'am_pm': 'am',
            'on_monday': True,
            'on_tuesday': True,
            'on_wednesday': True,
            'on_thursday': True,
            'on_friday': True,
            'on_saturday': True,
            'on_sunday': False,
        }
        hello = SprinkleSchedule(**schedule_parameters)
        next_schedule = hello.when_should_sprinkle_next()
        expected_schedule = datetime(2019, 2, 4, 10, 12, 0)
        self.assertEqual(next_schedule, expected_schedule)



