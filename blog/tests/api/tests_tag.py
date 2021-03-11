
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models import Tag

from blog.serializers.TagSerializer import TagModelSerializer

# list_tags (paginations)
# list_tags (filters)

class TagTests(TestCase):
    """ Test module for Tag model """

    fixtures = [
        'tag',
    ]

    def test_tag_list(self):
        """ Get Tag List """

        client = APIClient()
        response = client.get('/api/tag/list/')
        result = json.loads(response.content)

        objects_count = Tag.objects.count()
        objects = Tag.objects.all()[:10]
        serialization = TagModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)