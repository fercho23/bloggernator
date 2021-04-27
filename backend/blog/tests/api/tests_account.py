
from PIL import Image
import tempfile
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class AccountTests(TestCase):
    """ Test module for Account actions """

    fixtures = [
        'user',
    ]

    def test_signup_user(self):
        """ test_signup_user - Create an user """

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            'email': '894e1f419dd7422486d571fff98aaac5@bloggernator.com',
            'username': 'user1',
            'password': 'Blog12345',
            'password_confirmation': 'Blog12345',
            'photo': tmp_file,
        }

        client = APIClient()
        response = client.post('/api/account/signup/', data, format='multipart')
        result = json.loads(response.content)

        obj = User.objects.filter(email=data['email']).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', result)
        self.assertIn('user', result)
        self.assertIsNotNone(obj)

    def test_login_user(self):
        """ test_login_user - Login """

        obj = User.objects.get(pk=2)
        data = {
            'email': obj.email,
            'password': 'Blog12345',
        }

        client = APIClient()
        response = client.post('/api/account/login/', data, format='json')
        result = json.loads(response.content)

        first_uuid = obj.uuid

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('user', None)['uuid'], first_uuid)
        self.assertIn('token', result)

    def test_login_user_get_validation_error(self):
        """ test_login_user_get_validation_error - Login with an incorrect password get Validation Error """

        obj = User.objects.get(pk=2)
        data = {
            'email': '9b38b896-3996-4716-baae-276bd8edae73@bloggernator.com',
            'password': '9b38b896-3996-4716-baae-276bd8edae73',
        }

        client = APIClient()
        response = client.post('/api/account/login/', data, format='json')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', result)

    def test_logout_user(self):
        """ test_logout_user - Logout """

        obj = User.objects.get(pk=2)
        token = Token.objects.create(user=obj)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/api/account/logout/')

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', result)