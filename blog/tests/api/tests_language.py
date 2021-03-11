
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer

# list_language (paginations)
# list_language (filters)

class LanguageTests(TestCase):
    """ Test module for Language model """

    fixtures = [
        'language',
    ]

    def test_language_list(self):
        """ Get Language List """

        client = APIClient()
        response = client.get('/api/language/list/')
        result = json.loads(response.content)

        objects_count = Language.objects.count()
        objects = Language.objects.all()
        serialization = LanguageModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)