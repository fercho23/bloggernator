
import json

from django.test import TestCase

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.test import APIClient

from blog.models.Post import Post

from blog.serializers.PostSerializer import PostModelSerializer

# list_posts
# list_posts (pagination)
# list_posts (filters)
# list_posts_by_tag
# list_posts_by_language
# list_posts_by_category
# list_posts_by_blogger (authors, contributors)

# detail_post
# get_post
# set_post
# update_post
# delete_post

class PostTests(TestCase):
    """ Test module for Post model """

    # fixtures = [
    #     'post',
    # ]

    def test_post_list(self):
        """ Get Post List """

        client = APIClient()
        response = client.get('/api/post/list/')
        result = json.loads(response.content)

        objects = Post.objects.all()
        serialization = PostModelSerializer(objects, many=True).data

        expected_value = {
            'result': True,
            'objects': serialization
        }

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(result.get('result', None), expected_value['result'])
        self.assertEqual(result.get('objects', None), expected_value['objects'])