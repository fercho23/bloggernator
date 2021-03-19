
import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models.Language import Language
from blog.models.Post import Post
from blog.models.Tag import Tag

from blog.serializers.PostSerializer import PostModelSerializer

# post_list
# post_list (pagination)
# post_list (filters)
# post_list_by_blogger (authors, contributors)

# detail_post
# get_post
# set_post
# update_post
# delete_post

class PostTests(TestCase):
    """ Test module for Post model """

    fixtures = [
        'user',
        'group',
        'community',
        'language',
        'tag',
        'post',
    ]

    def test_post_list(self):
        """ test_post_list - Post List """

        client = APIClient()
        response = client.get('/api/post/list/')
        result = json.loads(response.content)

        objects_query = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_by_tag(self):
        """ test_post_list_by_tag - Post List By Tag"""
        tag = Tag.objects.filter(slug='wellness').first()

        client = APIClient()
        response = client.get('/api/post/list/by_tag/{}/'.format(tag.slug))

        result = json.loads(response.content)

        filters = {
            'tags__slug': tag.slug
        }

        objects_query = Post.objects.filter(**filters).select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_by_language(self):
        """ test_post_list_by_language - Post List By Language"""
        language = Language.objects.filter(slug='english').first()

        client = APIClient()
        response = client.get('/api/post/list/by_language/{}/'.format(language.slug))

        result = json.loads(response.content)

        filters = {
            'language__slug': language.slug
        }

        objects_query = Post.objects.filter(**filters).select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)
