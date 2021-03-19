
import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer

# list_language (filters)

class LanguageTests(TestCase):
    """ Test module for Language model """

    fixtures = [
        'language',
    ]

    def test_language_list(self):
        """ test_language_list - Language List """

        client = APIClient()
        response = client.get('/api/language/list/')
        result = json.loads(response.content)

        objects_query = Language.objects
        objects_count = objects_query.count()
        objects = objects_query.all()
        serialization = LanguageModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, serialization)