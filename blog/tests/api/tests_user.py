
from PIL import Image
import tempfile
import json
import uuid

from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models.User import User

# from blog.serializers.UserSerializer import UserModelSerializer


# delete_user

# list_bloggers (authors, contributors)
# detail_blogger (authors, contributors)

# list_bloggers_by_language (authors, contributors)


class UserTests(TestCase):
    """ Test module for User model """

    fixtures = [
    #     'language',
    #     'tag',
        'user',
    #     'post',
    ]

    def test_get_user(self):
        """ test_get_user - Get User """

        user = User.objects.get(pk=3)

        client = APIClient()
        response = client.get('/api/user/{}/'.format(user.uuid))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('uuid', result)
        self.assertIn('email', result)
        self.assertIn('username', result)
        self.assertIn('photo', result)

    def test_get_user_that_not_exist(self):
        """ Get User that not exist """

        client = APIClient()
        response = client.get('/api/user/{}/'.format(uuid.uuid4))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        """ test_update_user - Update user """

        user = User.objects.get(pk=3)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            'username': user.username + '.real',
            'photo': tmp_file,
        }

        client = APIClient()
        # client.login(username='lauren', password='secret')
        client.force_authenticate(user)

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
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # client.login(username='lauren', password='secret')
        # client.force_authenticate(user)

        response = client.put('/api/user/{}/update/'.format(user2.uuid), data, format='multipart')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)
