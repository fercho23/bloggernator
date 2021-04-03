
import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models.Language import Language
from blog.models.Post import Post
from blog.models.Tag import Tag

from blog.serializers.PostSerializer import PostModelSerializer

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

    def test_post_list_filtered_by_tag(self):
        """ test_post_list_filtered_by_tag - Post List filtered by tag """
        tag = Tag.objects.filter(slug='wellness').first()

        data = {
            'tags': tag.slug,
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)

        result = json.loads(response.content)

        objects_query = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_query = objects_query.filter(tags__slug=data['tags'])
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_language(self):
        """ test_post_list_filtered_by_language - Post List filtered by language """
        language = Language.objects.filter(slug='english').first()

        data = {
            'language': language.slug,
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)

        result = json.loads(response.content)

        objects_query = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_query = objects_query.filter(language__slug=data['language'])
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_title(self):
        """ test_post_list_filtered_by_title - Post List filtered by title """

        first_obj = Post.objects.first()

        data = {
            'title': first_obj.title[:-1],
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)

        result = json.loads(response.content)

        objects_query = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_query = objects_query.filter(title__icontains=data['title'])
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_ordered_list(self):
        """ test_post_ordered_list - Post ordered List """

        first_obj = Post.objects.first()

        data = {
            'ordering': '-title',
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)

        result = json.loads(response.content)

        objects_query = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_query = objects_query.order_by(data['ordering'])
        objects_count = objects_query.count()
        objects = objects_query.all()[:10]
        serialization = PostModelSerializer(objects, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None), serialization)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_get(self):
        """ test_post_get -Post Get """

        post = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors').first()
        serialization = PostModelSerializer(post).data

        client = APIClient()

        response = client.get('/api/post/{}/'.format(post.uuid))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serialization, result)