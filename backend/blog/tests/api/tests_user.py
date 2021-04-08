
from PIL import Image
import tempfile
import json
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()

# list_bloggers (authors, contributors)
# detail_blogger (authors, contributors)

# list_bloggers_by_language (authors, contributors)


class UserTests(TestCase):
    """ Test module for User model """

    fixtures = [
        'user',
        'group',
        'community',
        'language',
        'tag',
        'post',
    ]

    def test_get_user(self):
        """ test_get_user - Get User """

        user = User.objects.get(pk=3)

        client = APIClient()
        response = client.get('/api/user/{}/'.format(user.uuid))
        result = json.loads(response.content)

        first_uuid = user.uuid

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['uuid'], first_uuid)

    def test_get_user_that_not_exist(self):
        """ Get User that not exist """

        client = APIClient()
        response = client.get('/api/user/{}/'.format(uuid.uuid4))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        """ test_update_user - Update user """

        user = User.objects.get(pk=3)
        token = Token.objects.create(user=user)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            'username': user.username + '.real',
            'photo': tmp_file,
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.put('/api/user/{}/update/'.format(user.uuid), data, format='multipart')
        result = json.loads(response.content)

        user = User.objects.get(pk=user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])
        self.assertIn('photo', result)

    def test_update_another_user_get_validation_error(self):
        """ test_update_another_user_get_validation_error - Update another user get Validation Error """

        user = User.objects.get(pk=3)
        token = Token.objects.create(user=user)

        user2 = User.objects.get(pk=4)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            'username': 'jason.reinhar.real',
            'photo': tmp_file,
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.put('/api/user/{}/update/'.format(user2.uuid), data, format='multipart')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)

    def test_delete_user(self):
        """ test_delete_user - Delete user """

        data = {
            'email': 'email@email.com',
            'username': 'UniqueUsername',
            'password': 'Blog12345',
        }

        user = User.objects.create_user(**data)
        token = Token.objects.create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/api/user/{}/delete/'.format(user.uuid))

        user = User.objects.filter(id=user.id).first()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(user)

    def test_delete_another_user_get_validation_error(self):
        """ test_delete_another_user_get_validation_error - Delete another user get Validation Error """

        data = {
            'email': 'email@email.com',
            'username': 'UniqueUsername',
            'password': 'Blog12345',
        }

        user = User.objects.create_user(**data)
        token = Token.objects.create(user=user)

        user2 = User.objects.get(pk=4)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/api/user/{}/delete/'.format(user2.uuid))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)