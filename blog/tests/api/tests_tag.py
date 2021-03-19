
import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Tag

from blog.serializers.TagSerializer import TagModelSerializer


# list_tags (filters)

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

        objects_query = Tag.objects
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = TagModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)