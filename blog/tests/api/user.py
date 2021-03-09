
from PIL import Image
import tempfile
import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from blog.models.User import User


# get_user
# set_user
# update_user
# delete_user

# list_bloggers (authors, contributors)
# detail_blogger (authors, contributors)
# list_posts_by_blogger (authors, contributors)


class UserTests(TestCase):
    """ Test module for User model """

    # fixtures = [
    #     'language',
    #     'category',
    #     'tag',
    #     'user',
    #     'post',
    # ]

    # def setUp(self):
    #     User.objects.create_user(email='jason.reinhart@bloggernator.com', password='12345', username='jason.reinhart')
    #     User.objects.create_user(email='karen.lowman@bloggernator.com', password='12345', username='karen.lowman')
    #     User.objects.create_superuser(email='barbara.taylor@bloggernator.com', password='12345', username='barbara.taylor')


    def test_signup_user(self):
        """Create an user"""

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        client = APIClient()

        data = {
            'email': 'user1@bloggernator.com',
            'username': 'user1',
            'password': '12345',
            'password_confirmation': '12345',
            'photo': tmp_file,
        }

        response = client.post('/api/signup/', data, format='multipart')

        data_to_compare = {
            'email': data['email'],
            'username': data['username'],
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), data_to_compare)
