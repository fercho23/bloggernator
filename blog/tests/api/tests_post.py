
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blog.models.Language import Language
from blog.models.Post import Post
from blog.models.Tag import Tag

from blog.serializers.PostSerializer import PostModelSerializer

User = get_user_model()

# post_list_by_blogger (authors, contributors)

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

    def test_post_list_filtered_by_author(self):
        """ test_post_list_filtered_by_author - Post List filtered by author """
        post = Post.objects.select_related('author').first()

        data = {
            'author': post.author.uuid,
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)

        result = json.loads(response.content)

        objects_query = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
        objects_query = objects_query.filter(author__uuid=data['author'])
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

    def test_post_create(self):
        """ test_post_create - Post Create """

        user = User.objects.get(pk=3)
        community = user.community_set.first()
        language = Language.objects.filter(slug='english').first()

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
            'language': language.uuid,
            'community': community.uuid,
            # 'community': '41834ea0-e06d-4ae2-8aa6-445736edf823',
            # 'community': '7cd3ce2b-a32e-4562-a2e6-28bbdf88bd89',
        }

        client = APIClient()
        client.force_authenticate(user)

        response = client.post('/api/post/create/', data)
        result = json.loads(response.content)

        post = Post.objects.filter(title=data['title']).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(post)
        self.assertEqual(post.author, user)
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.body, data['body'])
        self.assertEqual(post.abstract, data['abstract'])
        self.assertEqual(post.language, language)
        self.assertEqual(post.community, community)

    def test_post_update(self):
        """ test_post_update - Post Update """

        post = Post.objects.get(pk=1)
        user = post.author

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
            # 'community': '7cd3ce2b-a32e-4562-a2e6-28bbdf88bd89',
        }

        client = APIClient()
        client.force_authenticate(user)

        response = client.patch('/api/post/{}/update/'.format(post.uuid), data)
        result = json.loads(response.content)

        post = Post.objects.get(pk=post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.body, data['body'])
        self.assertEqual(post.abstract, data['abstract'])

    def test_post_update_only_author_or_contributors(self):
        """ test_post_update_only_author_or_contributors - Post Update only by author or contributors """

        post = Post.objects.get(pk=1)
        user = User.objects.get(pk=5)

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
        }

        client = APIClient()
        client.force_authenticate(user)

        response = client.patch('/api/post/{}/update/'.format(post.uuid), data)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)

    def test_post_delete(self):
        """ test_post_delete - Post Delete """

        post = Post.objects.get(pk=2)
        user = post.author

        client = APIClient()
        client.force_authenticate(user)

        response = client.delete('/api/post/{}/delete/'.format(post.uuid))

        post = Post.objects.filter(id=post.id).first()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(post)

    def test_post_delete_only_author(self):
        """ test_post_delete_only_author - Post Delete only by author"""

        post = Post.objects.get(pk=2)
        user = User.objects.get(pk=4)

        client = APIClient()
        client.force_authenticate(user)

        response = client.delete('/api/post/{}/delete/'.format(post.uuid))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)

    def test_post_can_not_be_deleted_if_has_contributors(self):
        """ test_post_can_not_be_deleted_if_has_contributors - Post can not be deleted if it has contributors """

        post = Post.objects.get(pk=1)
        user = post.author

        client = APIClient()
        client.force_authenticate(user)

        response = client.delete('/api/post/{}/delete/'.format(post.uuid))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)
