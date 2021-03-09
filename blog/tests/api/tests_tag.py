
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models import Tag

from blog.serializers.TagSerializer import TagModelSerializer

# list_tags

class TagTests(TestCase):
    """ Test module for Tag model """

    fixtures = [
        'tag',
    ]

    def test_list_tags(self):
        """ Get Tag List """

        client = APIClient()
        response = client.get('/api/tag/list/')
        result = json.loads(response.content)

        objects = Tag.objects.all()
        serialization = TagModelSerializer(objects, many=True).data

        expected_value = {
            'result': True,
            'objects': serialization
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('result', None), expected_value['result'])
        self.assertEqual(result.get('objects', None), expected_value['objects'])