
from PIL import Image
import tempfile
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models.User import User

from blog.serializers.UserSerializer import UserModelSerializer


# delete_user

# list_bloggers (authors, contributors)
# detail_blogger (authors, contributors)

# list_bloggers_by_language (authors, contributors)


class UserTests(TestCase):
    """ Test module for User model """

    fixtures = [
    #     'language',
    #     'category',
    #     'tag',
        'user',
    #     'post',
    ]

    # def setUp(self):
    #     User.objects.create_user(email='jason.reinhart@bloggernator.com', password='12345', username='jason.reinhart')
    #     User.objects.create_user(email='karen.lowman@bloggernator.com', password='12345', username='karen.lowman')
    #     User.objects.create_superuser(email='barbara.taylor@bloggernator.com', password='12345', username='barbara.taylor')



    def test_get_user(self):
        """ Get user """

        obj = User.objects.get(pk=2)

        client = APIClient()
        response = client.get('/api/user/{}/'.format(obj.uuid))
        result = json.loads(response.content)

        obj_serialized = UserModelSerializer(obj).data

        expected_value = {
            'result': True,
            'object': obj_serialized
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('result', None), expected_value['result'])
        self.assertEqual(result.get('object', None), expected_value['object'])


    def test_update_user(self):
        """ Update user """

        obj = User.objects.get(pk=2)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            'username': 'jason.reinhar.real',
            'photo': tmp_file,
        }

        client = APIClient()
        # client.login(username='lauren', password='secret')
        client.force_authenticate(obj)

        response = client.put('/api/user/{}/update/'.format(obj.uuid), data, format='multipart')
        result = json.loads(response.content)

        obj = User.objects.get(pk=2)
        obj_serialized = UserModelSerializer(obj).data

        expected_value = {
            'result': True,
            'object': obj_serialized
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('result', None), expected_value['result'])
        self.assertEqual(result.get('object', None), expected_value['object'])


    def test_update_another_user_get_validation_error(self):
        """ Update another user get Validation Error """

        obj = User.objects.get(pk=1)
        obj2 = User.objects.get(pk=2)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            'username': 'jason.reinhar.real',
            'photo': tmp_file,
        }

        client = APIClient()
        # client.login(username='lauren', password='secret')
        client.force_authenticate(obj)

        response = client.put('/api/user/{}/update/'.format(obj2.uuid), data, format='multipart')
        result = json.loads(response.content)

        expected_value = {
            'error': True,
        }

        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(result.get('error', None), expected_value['error'])
        self.assertIn('validation_errors', result)
