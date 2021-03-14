
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models.Community import Community

from blog.serializers.CommunitySerializer import CommunityModelSerializer

# list_community (paginations)
# list_community (filters)

class CommunityTests(TestCase):
    """ Test module for Community model """

    fixtures = [
        'group',
        'community',
    ]

    def test_Community_list(self):
        """ Get Community List """

        client = APIClient()
        response = client.get('/api/community/list/')
        result = json.loads(response.content)

        objects_count = Community.objects.count()
        objects = Community.objects.all()
        serialization = CommunityModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)