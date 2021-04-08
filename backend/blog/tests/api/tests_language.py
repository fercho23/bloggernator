
import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models.Language import Language


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

        objects_count = 6
        first_uuid = '65b70eae-313b-47c0-8839-756659d4fc18'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), objects_count)
        self.assertEqual(result[0]['uuid'], first_uuid)

    def test_language_list_filtered_by_name(self):
        """ test_language_list_filtered_by_name - Language List filtered by name """

        first_obj = Language.objects.get(pk=2)

        data = {
            'name': first_obj.name[:-1],
        }

        client = APIClient()
        response = client.get('/api/language/list/', data)
        result = json.loads(response.content)

        objects_count = 1
        first_uuid = 'c42baaf7-8b0c-4c2a-842f-0d84b6283c39'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), objects_count)
        self.assertEqual(result[0]['uuid'], first_uuid)

    def test_language_ordered_list(self):
        """ test_language_ordered_list - Language ordered List """

        data = {
            'ordering': '-name',
        }

        client = APIClient()
        response = client.get('/api/language/list/', data)
        result = json.loads(response.content)

        objects_count = 6
        first_uuid = 'ef0568cd-5e32-4d8a-a6fa-7dbfc761dbe6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), objects_count)
        self.assertEqual(result[0]['uuid'], first_uuid)