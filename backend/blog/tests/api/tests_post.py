
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models.Language import Language
from blog.models.Post import Post
from blog.models.Tag import Tag

User = get_user_model()


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

        objects_count = 6
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
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

        objects_count = 3
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
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

        objects_count = 5
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_authors(self):
        """ test_post_list_filtered_by_authors - Post List filtered by authors """

        post = Post.objects.select_related('author').get(pk=1)

        data = {
            'authors': post.author.username,
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)
        result = json.loads(response.content)

        objects_count = 3
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_many_authors(self):
        """ test_post_list_filtered_by_many_authors - Post List filtered by many authors """

        post = Post.objects.prefetch_related('contributors').get(pk=1)

        data = {
            'authors': [contributor.username for contributor in post.contributors.all()],
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)
        result = json.loads(response.content)

        objects_count = 3
        first_uuid = 'ffa0c48a-1d30-41ba-90d6-91412bdaf04c'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_contributors(self):
        """ test_post_list_filtered_by_contributors - Post List filtered by contributors """

        post = Post.objects.prefetch_related('contributors').get(pk=1)

        data = {
            'contributors': post.contributors.first().username,
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)
        result = json.loads(response.content)

        objects_count = 2
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_many_contributors(self):
        """ test_post_list_filtered_by_many_contributors - Post List filtered by many contributors """

        post = Post.objects.prefetch_related('contributors').get(pk=1)

        data = {
            'contributors': [contributor.username for contributor in post.contributors.all()],
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)
        result = json.loads(response.content)

        objects_count = 3
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_list_filtered_by_title(self):
        """ test_post_list_filtered_by_title - Post List filtered by title """

        first_obj = Post.objects.get(pk=1)

        data = {
            'title': first_obj.title[:-1],
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)
        result = json.loads(response.content)

        objects_count = 1
        first_uuid = '5fc757ba-e7ab-4ed0-8b6f-10e8eb2232e6'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_ordered_list(self):
        """ test_post_ordered_list - Post ordered List """

        first_obj = Post.objects.get(pk=1)

        data = {
            'ordering': '-title',
        }

        client = APIClient()
        response = client.get('/api/post/list/', data)
        result = json.loads(response.content)

        objects_count = 6
        first_uuid = 'ffa0c48a-1d30-41ba-90d6-91412bdaf04c'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count', None), objects_count)
        self.assertEqual(result.get('results', None)[0]['uuid'], first_uuid)
        self.assertIn('next', result)
        self.assertIn('previous', result)

    def test_post_get(self):
        """ test_post_get -Post Get """

        post = Post.objects.get(pk=1)

        client = APIClient()
        response = client.get('/api/post/{}/'.format(post.slug))
        result = json.loads(response.content)

        first_uuid = post.uuid

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['uuid'], first_uuid)

    def test_post_create(self):
        """ test_post_create - Post Create """

        user = User.objects.get(pk=3)
        token = Token.objects.create(user=user)
        community = user.community_set.first()
        language = Language.objects.filter(slug='english').first()

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
            'language': language.slug,
            'community': community.slug,
            # 'community': '41834ea0-e06d-4ae2-8aa6-445736edf823',
            # 'community': '7cd3ce2b-a32e-4562-a2e6-28bbdf88bd89',
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
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
        token = Token.objects.create(user=user)

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
            # 'community': '7cd3ce2b-a32e-4562-a2e6-28bbdf88bd89',
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.patch('/api/post/{}/update/'.format(post.slug), data)
        result = json.loads(response.content)

        post = Post.objects.get(pk=post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.body, data['body'])
        self.assertEqual(post.abstract, data['abstract'])

    def test_post_update_contributors(self):
        """ test_post_update_contributors - Post Update Contributors """

        post = Post.objects.get(pk=1)
        user = post.author
        token = Token.objects.create(user=user)

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
            # 'community': '7cd3ce2b-a32e-4562-a2e6-28bbdf88bd89',
            'contributors': [
                User.objects.get(pk=4).username,
                User.objects.get(pk=5).username,
                User.objects.get(pk=6).username,
            ],
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.patch('/api/post/{}/update/'.format(post.slug), data)
        result = json.loads(response.content)

        post = Post.objects.get(pk=post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.body, data['body'])
        self.assertEqual(post.abstract, data['abstract'])
        self.assertEqual(post.contributors.count(), len(data['contributors']))

    def test_post_update_only_author_or_contributors(self):
        """ test_post_update_only_author_or_contributors - Post Update only by author or contributors """

        post = Post.objects.get(pk=1)
        user = User.objects.get(pk=6)
        token = Token.objects.create(user=user)

        data = {
            'title': 'Testing Post Creation',
            'body': 'Detail Testing Post Creation',
            'abstract': 'Abstract Testing Post Creation',
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.patch('/api/post/{}/update/'.format(post.slug), data)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)

    def test_post_delete(self):
        """ test_post_delete - Post Delete """

        post = Post.objects.get(pk=3)
        user = post.author
        token = Token.objects.create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/api/post/{}/delete/'.format(post.slug))

        post = Post.objects.filter(id=post.id).first()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(post)

    def test_post_delete_only_author(self):
        """ test_post_delete_only_author - Post Delete only by author"""

        post = Post.objects.get(pk=2)
        user = User.objects.get(pk=4)
        token = Token.objects.create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/api/post/{}/delete/'.format(post.slug))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)

    def test_post_can_not_be_deleted_if_has_contributors(self):
        """ test_post_can_not_be_deleted_if_has_contributors - Post can not be deleted if it has contributors """

        post = Post.objects.get(pk=1)
        user = post.author
        token = Token.objects.create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/api/post/{}/delete/'.format(post.slug))
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', result)
