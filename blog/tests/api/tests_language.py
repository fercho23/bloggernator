
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer


# list_languages

class LanguageTests(TestCase):
    """ Test module for Language model """

    fixtures = [
        'language',
    ]


    def test_list_languages(self):
        """ Get Languages List """

        client = APIClient()
        response = client.get('/api/language/list/')
        result = json.loads(response.content)

        objects = Language.objects.all()
        serialization = LanguageModelSerializer(objects, many=True).data

        expected_value = {
            'result': True,
            'objects': serialization
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('result', None), expected_value['result'])
        self.assertEqual(result.get('objects', None), expected_value['objects'])