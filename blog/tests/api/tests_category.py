
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models.Category import Category

from blog.serializers.CategorySerializer import CategoryModelSerializer

# list_category (paginations)
# list_category (filters)

class CategoryTests(TestCase):
    """ Test module for Category model """

    fixtures = [
        'category',
    ]

    def test_category_list(self):
        """ Get Category List """

        client = APIClient()
        response = client.get('/api/category/list/')
        result = json.loads(response.content)

        objects = Category.objects.all()
        serialization = CategoryModelSerializer(objects, many=True).data

        expected_value = {
            'result': True,
            'objects': serialization
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('result', None), expected_value['result'])
        self.assertEqual(result.get('objects', None), expected_value['objects'])