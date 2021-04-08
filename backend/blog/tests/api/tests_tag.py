
import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Tag


class TagTests(TestCase):
    """ Test module for Tag model """

    fixtures = [
        'tag',
    ]

    def test_tag_list(self):
        """ test_tag_list - Tag List """

        client = APIClient()
        response = client.get('/api/tag/list/')
        result = json.loads(response.content)

        objects_count = 23
        first_uuid = '4a408eff-7f22-44df-aa48-d3947321d6e8'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_tag_list_filtered_by_name(self):
        """ test_tag_list_filtered_by_name - Tag List filtered by name """

        first_obj = Tag.objects.get(pk=2)

        data = {
            'name': first_obj.name[:-1],
        }

        client = APIClient()
        response = client.get('/api/tag/list/', data)
        result = json.loads(response.content)

        objects_count = 1
        first_uuid = '3a613c48-dcb0-4b76-8362-af3cfce85141'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_tag_ordered_list(self):
        """ test_tag_ordered_list - Tag ordered List """

        data = {
            'ordering': '-name',
        }

        client = APIClient()
        response = client.get('/api/tag/list/', data)
        result = json.loads(response.content)

        objects_count = 23
        first_uuid = '40bed8ac-9b0b-4ad3-bc18-afa4b793cb5f'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)
