
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer

User = get_user_model()


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

    def test_language_list_filtered_by_name(self):
        """ test_language_list_filtered_by_name - Language List filtered by name """

        first_obj = Language.objects.first()

        data = {
            'name': first_obj.name[:-1],
        }

        client = APIClient()
        response = client.get('/api/language/list/', data)
        result = json.loads(response.content)

        objects_query = Language.objects
        objects_query = objects_query.filter(name__icontains=data['name'])
        objects_count = objects_query.count()
        objects = objects_query.all()
        serialization = LanguageModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, serialization)

    def test_language_ordered_list(self):
        """ test_language_ordered_list - Language ordered List """

        data = {
            'ordering': '-name',
        }

        client = APIClient()
        response = client.get('/api/language/list/', data)
        result = json.loads(response.content)

        objects_query = Language.objects
        objects_query = objects_query.order_by(data['ordering'])
        objects_count = objects_query.count()
        objects = objects_query.all()
        serialization = LanguageModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, serialization)